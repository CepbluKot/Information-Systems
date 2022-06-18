#include <opencv4/opencv2/opencv.hpp>
#include <fstream>


const std::string YOLO_VERSION = "v4-tiny";


std::vector<std::string> load_class_list() {
    std::vector<std::string> class_list;
    std::ifstream ifs("config_files/classes.txt");
    std::string line;
    while (getline(ifs, line))
    {
        class_list.push_back(line);
    } 
    return class_list;
}


std::vector<std::string> class_list = load_class_list();


void load_net(cv::dnn::Net &net) {
    auto result = cv::dnn::readNetFromDarknet("config_files/yolo" + YOLO_VERSION + ".cfg", "config_files/yolo" + YOLO_VERSION + ".weights");
    std::cout << "Running on CPU\n";
    result.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
    result.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
    
    net = result;
}
