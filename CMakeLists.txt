cmake_minimum_required(VERSION 3.10)

# set the project name
project(magiccarpet VERSION 0.1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# directory mgmt
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(libroboclaw)
add_subdirectory(joystick)
add_subdirectory(magiccarpet)

