#include <iostream>
#include "libroboclaw/roboclaw_driver.h"
#include "joystick.hh"

int main(int argc, char *argv[]) {
  std::string serial_port = "/dev/serial0";
  unsigned int baudrate = 115200;
  unsigned int addr = 128;

  // initialize roboclaw
  libroboclaw::driver *roboclaw_conns;
  roboclaw_conns = new libroboclaw::driver(serial_port, baudrate);
  std::pair<int, int> enc_res = roboclaw_conns->get_encoders(addr);
  std::cout << "encoders: M1: " << enc_res.first << ", M2:" << enc_res.second << std::endl;

  // initialize our joystick
  Joystick joystick("/dev/input/js0");
  
  // Ensure that it was found and that we can use it
  if (!joystick.isFound())
  {
    printf("open failed.\n");
    exit(1);
  }

  // initialize vars
  std::pair<int, int> duty(0, 0);

  while (true)
  {
    // Restrict rate
    usleep(1000);

    // Attempt to sample an event from the joystick
    JoystickEvent event;
    if (joystick.sample(&event))
    {
      if (event.isAxis())
      {
        printf("Axis %u is at position %d\n", event.number, event.value);
        if (event.number == 1) {
          duty.first = event.value;
        }
        if (event.number == 4) {
          duty.second = event.value;
        }
      }
    }
    // write duty cycle to roboclaw
    roboclaw_conns->set_duty(addr, duty);
  }


  return 0;
}
