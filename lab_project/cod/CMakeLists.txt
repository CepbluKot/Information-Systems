cmake_minimum_required(VERSION 3.21)
project(cv)

set(CMAKE_CXX_STANDARD 14)

find_package( OpenCV REQUIRED )
set(SOURCE_FILES main.cpp)
add_executable(cv ${SOURCE_FILES})
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(cv ${OpenCV_LIBS} )