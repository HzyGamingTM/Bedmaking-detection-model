#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main() {
    // Create a pipeline and start streaming
    rs2::pipeline p;
    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);


    p.start(cfg);

    while (true) {
        // Capture a frameset
        rs2::frameset frames = p.wait_for_frames();
        rs2::frame color_frame = frames.get_color_frame();



        // Check if the frame is valid
        if (!color_frame) {
            std::cerr << "Error: No color frame captured!" << std::endl;
            continue;
        }

        // Convert RealSense frame to OpenCV format
        int width = color_frame.as<rs2::video_frame>().get_width();
        int height = color_frame.as<rs2::video_frame>().get_height();
        cv::Mat image(cv::Size(width, height), CV_8UC3, (void*)color_frame.get_data());

        // Show the frame in OpenCV window
        cv::imshow("RealSense OpenCV", image);

        // Wait for key press to close window
        if (cv::waitKey(1) >= 0) break;  // Short wait to keep window open
    }

    return 0;
}


