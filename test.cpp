#include <opencv2/opencv.hpp>

int main() {
    // Create a simple black image (a 500x500 matrix)
    cv::Mat image = cv::Mat::zeros(500, 500, CV_8UC3);

    // Display the image
    cv::imshow("OpenCV Window", image);

    // Wait for a key press to close the window
    cv::waitKey(0);

    return 0;
}

