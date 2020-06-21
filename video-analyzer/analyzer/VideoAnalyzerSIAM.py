from workflowBuilder.WorkflowBuilder import WorkflowBuilder
from analyzer.VideoAnalyzerUtil import *
import cv2
import datetime

CURSOR_TEMPLATE = "resources/cursor-own-transparent.png"
FRAME_IDX = 0
TIME_IDX = 1


class VideoAnalyzer:

    def __init__(self, click_detector, debug=False):
        self.debug = debug
        self.click_detector = click_detector

    def process(self, video_path, process_clb=None, extract_exact=False):
        update_gui_or_log("preprocess video...", 0, process_clb)

        frames = self._preprocess_video_(video_path)
        cursor_template = cv2.imread(CURSOR_TEMPLATE)

        width, height = self.click_detector.input_size
        curr_pos_ms = frames[0][TIME_IDX]
        last_click_pos_ms = curr_pos_ms
        before = frames[0][FRAME_IDX]
        after = frames[1][FRAME_IDX]
        reference_img = frames[0][FRAME_IDX]  # TODO reference_img updaten
        workflow_builder = WorkflowBuilder()
        action_cnt, frame_nr = 0, 0
        i = 2
        workflow = []
        workflow_full_frames = []
        update_gui_or_log("start analyzing video...", 0, process_clb)
        print(self.debug)
        start_analyzing = datetime.datetime.now()
        while i < len(frames):
            start = datetime.datetime.now()
            before_region, after_region = preprocess_frames(before, after, width, height)
            click_detected = self.click_detector.predict(before_region, after_region)
            end = datetime.datetime.now()
            if self.debug is True:
                update_gui_or_log(f"Runtime (Step {frame_nr}): {end - start}", -1, process_clb)

            if click_detected:
                elapsed_time = curr_pos_ms - last_click_pos_ms
                update_gui_or_log(f"CLICK detected at frame {frame_nr}, time between two clicks: {elapsed_time}", -1,
                                  process_clb)

                workflow_builder.append("delay", "{:.2f}".format(elapsed_time))
                last_click_pos_ms = curr_pos_ms

                cursor_x1, cursor_y1, cursor_x2, cursor_y2 = find_cursor(frames[i][FRAME_IDX], cursor_template)
                if extract_exact is True:
                    action_img = extract_button(reference_img, (cursor_x1, cursor_y1))
                else:
                    action_img = extract_action_img(reference_img, cursor_x1, cursor_y1, cursor_x2, cursor_y2)

                action_img_filename = f"ACTION{action_cnt}.png"

                workflow.append((action_img_filename, action_img))
                workflow_full_frames.append((frames[i - 1][FRAME_IDX], frames[i][FRAME_IDX]))
                workflow_builder.append("click", action_img_filename, "{}={:.2f}".format("timestamp", curr_pos_ms))
                action_cnt = action_cnt + 1
                i = i + 5
                if i >= len(frames):
                    break

            curr_pos_ms = frames[i][TIME_IDX]
            before = after
            after = frames[i][FRAME_IDX]
            i = i + 1
            frame_nr = frame_nr + 1

            if frame_nr % 3 == 0:
                update_gui_or_log(None, i * 100 / len(frames), process_clb)

        update_gui_or_log(f"FINISHED, RUNTIME: {datetime.datetime.now() - start_analyzing}", 100, process_clb)
        update_gui_or_log(f"ACTION-CNT: {action_cnt}", 100, process_clb)
        return workflow_builder, workflow, workflow_full_frames, reference_img

    def _preprocess_video_(self, video_path):
        print(f"_preprocess_video_({video_path})")
        vid = cv2.VideoCapture(video_path)
        if vid.isOpened() is False:
            if self.debug:
                print(f"not able to open '{video_path}'")
            raise VideoAnalyzerProcessError(f"not able to open '{video_path}'")

        frames = []
        while vid.isOpened():
            ret, frame = vid.read()
            pos_in_millis = vid.get(cv2.CAP_PROP_POS_MSEC)
            if ret is True:
                frames.append((frame, pos_in_millis))
            else:
                print("FINISHED processing video")
                break
        vid.release()
        cv2.destroyAllWindows()
        return frames
