#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main() {
    // Create a pipeline and start streaming
    rs2::pipeline p;
    rs2::config cfg;
    
    cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
    cfg.enable_stream(RS2_STREAM_DEPTH, 848, 480, RS2_FORMAT_Z16, 10); 
    p.start(cfg);

    rs2::device dev = p.get_active_profile().get_device();
    auto sensors = dev.query_sensors();

    

    while (true) {
        // Capture a frameset
        rs2::frameset frames = p.wait_for_frames();
        rs2::frame color_frame = frames.get_color_frame();
        rs2::frame depth_frame = frames.get_depth_frame();
        
        // Check if the frame is valid
        if (!color_frame) {
            std::cerr << "Error: No color frame captured!" << std::endl;
            continue;
        }

        if (!depth_frame) {
          std::cerr << "Error: No depth frame" << std::endl;
          continue;
        }

        // Convert RealSense frame to OpenCV format
        int width = color_frame.as<rs2::video_frame>().get_width();
        int height = color_frame.as<rs2::video_frame>().get_height();
        
        cv::Mat image(cv::Size(width, height), CV_8UC3, (void*)color_frame.get_data());
        cv::Mat depth_image(cv::Size(width, height), CV_16UC1, (void*)depth_frame.get_data());
        

        cv::Mat depth_image_normalized;

        cv::normalize(depth_image, depth_image_normalized, 0, 255, cv::NORM_MINMAX);
        depth_image_normalized.convertTo(depth_image_normalized, CV_8UC1);


        // Show the frame in OpenCV window
        cv::imshow("RealSense OpenCV", image);
        cv::imshow("Depth Image", depth_image_normalized);        
      
        cv::waitKey(1);
    }

    return 0;
}


