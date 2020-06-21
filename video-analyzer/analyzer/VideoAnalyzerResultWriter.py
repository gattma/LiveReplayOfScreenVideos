import os
import zipfile
import cv2
from io import BytesIO


def write_replay_file(target_dir, workflow_xml, workflow):
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for img_name, img in workflow:
            is_success, im_buf_arr = cv2.imencode(".png", img)
            zf.writestr(img_name, im_buf_arr.tobytes())

        zf.writestr("workflow.xml", workflow_xml)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(f'{target_dir}/workflow.replay', 'wb') as f:
        f.write(mem_zip.getvalue())


def write_html(target_dir, workflow_html, workflow):
    target_dir_html = f"{target_dir}/html/"
    if not os.path.exists(target_dir_html):
        os.makedirs(target_dir_html)

    workflow_file = open(f"{target_dir_html}workflow.html", "w")
    workflow_file.write(workflow_html)
    workflow_file.close()

    for img_name, img in workflow:
        cv2.imwrite(target_dir_html + img_name, img)


def write_full_frames(target_dir, workflow_full_frames):
    target_dir_frames = f"{target_dir}/fullFrames/"
    if not os.path.exists(target_dir_frames):
        os.makedirs(target_dir_frames)

    i = 0
    for (before, after) in workflow_full_frames:
        cv2.imwrite(f"{target_dir_frames}ACTION{i}.before.png", before)
        cv2.imwrite(f"{target_dir_frames}ACTION{i}.after.png", after)
        i = i + 1