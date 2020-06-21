from workflowBuilder.WorkflowBuilder import WorkflowBuilder
from analyzer.VideoAnalyzerUtil import extract_action_img, update_gui_or_log, extract_button

import cv2
import datetime


def valid_point(x_act, y_act, x_last, y_last):
    if (x_last - 1 <= x_act <= x_last + 1) and (y_last - 1 <= y_act <= y_last + 1):
        return False
    else:
        return True


class VideoAnalyzer:

    def __init__(self, click_detector, debug=False):
        self.debug = debug
        self.click_detector = click_detector

    def process(self, video_path, process_clb=None, extract_exact=False):
        vid = cv2.VideoCapture(video_path)
        if vid.isOpened() is False:
            update_gui_or_log("Error opening video stream or file", 0)
            return ""

        reference_img = None
        ret, frame = vid.read()
        if ret is True:
            reference_img = frame

        workflow_builder = WorkflowBuilder()
        cnt = 0
        delay = 9
        frame_nr = 0

        workflow = []

        last_x1 = last_y1 = last_x2 = last_y2 = -1
        last_pos_ms = curr_pos_ms = vid.get(cv2.CAP_PROP_POS_MSEC)
        start_analyzing = datetime.datetime.now()
        while vid.isOpened():
            ret, frame = vid.read()
            if ret is True:
                if delay >= 9 and frame_nr % 2 == 0:
                    start = datetime.datetime.now()
                    found, x1, y1, x2, y2, score = self.click_detector.detect(frame)
                    end = datetime.datetime.now()
                    if self.debug:
                        update_gui_or_log("RUNTIME (detection): {}".format(end - start), -1, process_clb)

                    if found and score > 0.97 \
                            and valid_point(x1, y1, last_x1, last_y1) \
                            and valid_point(x2, y2, last_x2, last_y2):
                        if self.debug:
                            update_gui_or_log(f"SAVE region of interest, SCORE: {score}", -1, process_clb)

                        workflow_builder.append("delay", "{:.2f}".format(curr_pos_ms - last_pos_ms))
                        last_pos_ms = curr_pos_ms

                        if extract_exact is True:
                            action_img = extract_button(reference_img, (x1, y1))
                        else:
                            action_img = extract_action_img(reference_img, x1, y1, x2, y2)

                        action_img_filename = f"ACTION{cnt}.png"

                        workflow.append((action_img_filename, action_img))
                        workflow_builder.append("click", action_img_filename)
                        workflow_builder.append("click", action_img_filename,
                                                "{}={:.2f}".format("timestamp", curr_pos_ms))
                        cnt = cnt + 1
                        delay = 0

                        last_x1, last_x2, last_y1, last_y2 = x1, x2, y1, y2
                        # TODO reference_img bei Ansichtwechsel updaten

                frame_nr = frame_nr + 1
                delay = delay + 1
                curr_pos_ms = vid.get(cv2.CAP_PROP_POS_MSEC)
            else:
                break

        vid.release()
        cv2.destroyAllWindows()

        update_gui_or_log(f"TOTAL Runtime: {datetime.datetime.now() - start_analyzing}", 100, process_clb)
        update_gui_or_log(f"ACTIONS detected: {cnt}", 100, process_clb)
        return workflow_builder, workflow, None
