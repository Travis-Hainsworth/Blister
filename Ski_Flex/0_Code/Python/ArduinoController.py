import time
import serial

class ArduinoController:
    MOVE_X = 4
    MOVE_FORCE_GAUGES = 24
    MOVE_TO_START = 2
    SET_ACCELERATION = 10
    SET_MAX_SPEED = 8
    RESET_ARDUINO = 16
    SET_CURRENT_POS = 6
    KILL_SWITCH_SIGNAL = 86
    GET_CURRENT_POSITION = 14

    def __init__(self, arduino_port, baud_rate=9600):
        self.arduino_serial = serial.Serial(arduino_port, baud_rate)
        self.kill_switch_pressed = False

    def move_x_mm(self, dis_mm, dir):
        if not self.kill_switch_pressed:
            serial_string = f"{self.MOVE_X},{dis_mm},{dir}"
            ret_signal = self.serial_communication(serial_string)
            if int(ret_signal) == self.KILL_SWITCH_SIGNAL:
                self.kill_switch_pressed = True
            self.arduino_serial.flush()
        else:
            ret_signal = 86
        return ret_signal

    def move_force_gauges(self, left_mm, right_mm):
        if not self.kill_switch_pressed:
            serial_string = f"{self.MOVE_FORCE_GAUGES},{left_mm},{right_mm}"
            ret_signal = self.serial_communication(serial_string)
            if int(ret_signal) == self.KILL_SWITCH_SIGNAL:
                self.kill_switch_pressed = True
            self.arduino_serial.flush()
        return ret_signal

    def return_to_start(self):
        if not self.kill_switch_pressed:
            serial_string = f"{self.MOVE_TO_START},0,1"
            ret_signal = self.serial_communication(serial_string)
            if int(ret_signal) == self.KILL_SWITCH_SIGNAL:
                self.kill_switch_pressed = True
            self.arduino_serial.flush()
        else:
            ret_signal = 86
        return ret_signal

    def get_distance_from_start(self):
        
        serial_string = f"{self.GET_CURRENT_POSITION},0,1"
        self.custom_write(serial_string)
        ret_mm = self.custom_read()
        ret_mm = float(ret_mm)
        self.arduino_serial.flush()
        return ret_mm

    def set_acceleration(self, acceleration):
        serial_string = f"{self.SET_ACCELERATION},{acceleration},0"
        self.custom_write(serial_string)
        ret_signal = self.custom_read()
        self.arduino_serial.flush()
        return ret_signal

    def set_max_speed(self, max_speed):
        serial_string = f"{self.SET_MAX_SPEED},{max_speed},0"
        self.custom_write(serial_string)
        ret_signal = self.custom_read()
        self.arduino_serial.flush()
        return ret_signal

    def reset_arduino(self):
        serial_string = f"{self.RESET_ARDUINO},0,0"
        self.custom_write(serial_string)
        ret_signal = self.custom_read()
        self.arduino_serial.flush()
        return ret_signal

    def set_current_position(self, pos):
        serial_string = f"{self.SET_CURRENT_POS},{pos},0"
        self.custom_write(serial_string)
        ret_signal = self.custom_read()
        self.arduino_serial.flush()
        return ret_signal

    def serial_communication(self, message):
        self.custom_write(message)
        time.sleep(1)
        print("wait")
        while self.arduino_serial.in_waiting == 0:
            pass
        sig = self.custom_read()
        if int(sig) == self.KILL_SWITCH_SIGNAL:
            self.kill_switch_pressed = True
        return sig

    def custom_write(self, message):
        self.arduino_serial.reset_input_buffer()
        self.arduino_serial.write(message.encode())

    def custom_read(self):
        out = self.arduino_serial.readline().decode().strip()
        self.arduino_serial.reset_input_buffer()
        return out

# Usage example:
if __name__ == "__main__":
    arduino_port = "COMX"  # Replace with the actual port your Arduino is connected to
    arduino_controller = ArduinoController(arduino_port)

    # Now you can call the methods on the `ski_rig_controller` object
    arduino_controller.move_x_mm(100, 1)
    distance = arduino_controller.get_distance_from_start()
    print(f"Distance from start: {distance} mm")