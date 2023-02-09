# Magic Carpet

## Installation

Clone this repo, cd magic-carpet

```
sudo apt-get install libboost-all-dev libgtest-dev cmake
git clone https://github.com/Achllle/libroboclaw.git
git clone https://github.com/drewnoakes/joystick.git
cp magic-carpet/joystick_cml.txt joystick/CMakeLists.txt
mkdir build && cd build
cmake ..
cmake --build .
```

## Run

```
./bin/carpetfly
```
will attempt to connect to the joystick at `/dev/input/js0` and roboclaw at
`/dev/serial0` with baud rate 115200 and address 128.

Move the joystick axes to send duty commands to the motors.
