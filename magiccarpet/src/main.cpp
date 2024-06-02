#include <iostream>
#include "libroboclaw/roboclaw_driver.h"
#include "joystick.hh"
#include <cstdio>

int max_abs_duty = 32767;
unsigned int max_joystick_pos = 16000;

template <typename T>
T clip(const T& n, const T& lower, const T& upper) {
  std::cout << n << ", " << lower << ", " << upper << std::endl;
  return std::max(lower, std::min(n, upper));
}

int js_pos_to_duty(int value) {
  return clip(int(value * static_cast<float>(max_abs_duty) / max_joystick_pos), -max_abs_duty+1, max_abs_duty);
}

int main(int argc, char *argv[]) {
  printf("Starting...");
  std::string serial_port = "/dev/serial0";
  unsigned int baudrate = 115200;
  unsigned int addr = 128;

  // xbox controller
  // unsigned int left_axis = 1;
  // unsigned int right_axis = 4;
  // unsigned int sync_mode_button = 1;

  // spektrum controller
  unsigned int left_axis = 0;
  unsigned int right_axis = 2;
  unsigned int sync_mode_button = 0;

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
  bool sync_mode = false;

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
        // printf("Axis %u is at position %d\n", event.number, event.value);
        if (event.number == left_axis) {
          printf("Axis %u is at position %d\n", event.number, event.value);
          duty.second = js_pos_to_duty(event.value);
          if (sync_mode)
            duty.first = js_pos_to_duty(event.value);
        }
        if (event.number == right_axis && !sync_mode) {
          printf("Axis %u is at position %d\n", event.number, event.value);
          duty.first = js_pos_to_duty(event.value);
        }
      }
      else if (event.isButton()) {
        printf("Button %u is %s\n", event.number, event.value == 0 ? "up" : "down");
        if (event.number == sync_mode_button && event.value != 0)
        {
          sync_mode = !sync_mode;  // flip value
          printf("Sync mode is %s\n", sync_mode == false ? "off" : "on");
        }
      }
    }
    // write duty cycle to roboclaw
    try {
      roboclaw_conns->set_duty(addr, duty);
      // std::cout << "duty: M1: " << duty.first << ", M2:" << duty.second << std::endl;
      // std::cout << roboclaw_conns->get_error(addr) << std::endl;
    }
    catch (const timeout_exception&) {
      std::cout << "caught disconnect." << std::endl;
    }
  }
  duty.first = 0;
  duty.second = 0;
  roboclaw_conns->set_duty(addr, duty);

  return 0;
}
