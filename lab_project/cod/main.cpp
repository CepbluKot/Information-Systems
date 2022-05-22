#include "opencv4/opencv2/opencv.hpp"
#include "camera.h"
using namespace cv;


int main(int, char **)
{
  Camera* cam1 = new Camera;
  cameraInterpretation cameraClient(cam1);
  
  cameraClient.openCamera();

  Mat edges;
  namedWindow("edges", 1);
  while (1)
  {
    Mat frame = cameraClient.getFrame();
                                         // get a new frame from camera
    cvtColor(frame, edges, COLOR_BGR2GRAY);           // Перевод в градации серого
    GaussianBlur(edges, edges, Size(7, 7), 1.5, 1.5); // Размытие
    Canny(edges, edges, 0, 30, 3);                    // Выделение границ
    imshow("edges", edges);
    if (waitKey(30) >= 0)
      break;
  }
  return 0;
}
