#include <fstream>
#include <opencv4/opencv2/opencv.hpp>
#include "modules/camera.h"
#include "modules/detection.h"


const std::vector<cv::Scalar> colors = {cv::Scalar(255, 255, 0), cv::Scalar(0, 255, 0), cv::Scalar(0, 255, 255), cv::Scalar(255, 0, 0)};


int main(int argc, char ** argv)
{

    std::vector<std::string> class_list = load_class_list();

    cv::Mat frame;
    cv::dnn::Net net;

    load_net(net);

    auto model = cv::dnn::DetectionModel(net);
    model.setInputParams(1./255, cv::Size(416, 416), cv::Scalar(), true);

    

    // IPCamera* cam2 = new IPCamera("192.168.100.5:8080", "test", "test");
    USBCamera* cam1 = new USBCamera(0);
    cameraAbstraction cameraClient(cam1);
  
    cameraClient.open();


    while(true)
    {

        frame = cameraClient.getFrame();


        if (frame.empty())
        {
            std::cout << "End of stream\n";
            break;
        }

        std::vector<int> classIds;
        std::vector<float> confidences;
        std::vector<cv::Rect> boxes;
        model.detect(frame, classIds, confidences, boxes, .2, .4);

        int detections = classIds.size();

        for (int i = 0; i < detections; ++i) {

            auto box = boxes[i];
            auto classId = classIds[i];
            const auto color = colors[classId % colors.size()];
            cv::rectangle(frame, box, color, 3);

            cv::rectangle(frame, cv::Point(box.x, box.y - 20), cv::Point(box.x + box.width, box.y), color, cv::FILLED);
            cv::putText(frame, class_list[classId].c_str(), cv::Point(box.x, box.y - 5), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0));
        
            std::cout<< class_list[classId].c_str() << " " << box.x << box.y - 5 ;
        }

        
        cv::imshow("output", frame);

        if(cv::waitKey(1) != -1) {
            
            std::cout << "finished by user\n";
            break;
        }
    }

    

    return 0;
}