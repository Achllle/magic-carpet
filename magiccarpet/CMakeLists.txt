cmake_minimum_required(VERSION 3.10)

# set the project name
project(magiccarpet VERSION 0.1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# directory mgmt
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

configure_file(magiccarpetConfig.h.in magiccarpetConfig.h)

find_package(Boost 1.55.0 REQUIRED COMPONENTS system filesystem)
find_package(InfluxDB)

############################################################
# Create an executable
############################################################

# add the executable
add_executable(carpetfly
    src/main.cpp
)

# add binary tree for finding magiccarpetConfig
target_include_directories(carpetfly
    PUBLIC
        "${PROJECT_BINARY_DIR}"
    PRIVATE
        libroboclaw
        joystick
)

target_link_libraries(carpetfly
    PRIVATE
        libroboclaw
        joystick
        InfluxData::InfluxDB
)
