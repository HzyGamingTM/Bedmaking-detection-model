import pyrealsense2 as rs
import numpy as np
import cv2


def main():
    # ----------------------------
    # 1. Configure RealSense pipeline
    # ----------------------------
    pipeline = rs.pipeline()
    config = rs.config()

    # Enable color + depth streams  
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 5)

    # Start the pipeline
    profile = pipeline.start(config)

    # Align depth to color stream
    align = rs.align(rs.stream.color)

    try:
        while True:
            # ----------------------------
            # 2. Wait for frames
            # ----------------------------
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)

            color_frame = aligned_frames.get_color_frame()

            if not color_frame:
                continue

            # ----------------------------
            # 3. Convert to numpy arrays
            # ----------------------------
            color_image = np.asanyarray(color_frame.get_data())
             


            # ----------------------------
            # 4. Display windows
            # ----------------------------
 
            cv2.imshow("Image", color_image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC to exit
                break

    finally:
        # ----------------------------
        # 5. Clean up
        # ----------------------------
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
