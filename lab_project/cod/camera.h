/* 
    create interface for cameras 
    create interpretation for cameras (choose which cam to use, maybe multiple cameras)
    create camera class with details
*/
#include "opencv4/opencv2/opencv.hpp"
using namespace cv;

class cameraInterface // просто интерфейс для всех камер
{
    public:
        virtual VideoCapture openCamera() { } // открытие камеры
        virtual Mat getFrame() { } // получение кадра 
};

class cameraInterpretation : public cameraInterface // через эту интерпретацию взаимодействуем со всеми камерами
{
    public:
        cameraInterpretation(cameraInterface* input_camera)
        {
            selected_camera = input_camera;
        }

        VideoCapture openCamera() 
        { 
            return selected_camera->openCamera();
        }

        Mat getFrame()
        {
            return selected_camera->getFrame();
        }

    private:
        cameraInterface* selected_camera;
};


class Camera : public cameraInterface // детади взаимодейсвия с камерой
{
    public:
        Camera(int input_camera_id = 0)
        {
            selected_camera_id = input_camera_id;
        }
        
        VideoCapture openCamera() 
        {
            cameraObject.open(selected_camera_id);
            if (!cameraObject.isOpened())
                std::cout << "\n\nerror\n\n"; // какие там ошибки в опенсиви есть?
            return cameraObject;
        }

        Mat getFrame()
        {
            if (!cameraObject.isOpened())
                std::cout << "\n\nerror\n\n";
            Mat frame;
            cameraObject >> frame;
            return frame;
        }
        
    private:
        int selected_camera_id;
        VideoCapture cameraObject;
};
