import serial
import time
from ArduinoController import ArduinoController
from SkiRigSensorController import ForceGaugeReader, InclinometerReader
from SkiProfileCalculator import SkiProfileCalculator

class SkiRigAutomationController:
    def __init__(self, ski_inclinometer_port, level_inclinometer_port, arduino_port, force_gauge_left_port, force_gauge_right_port):
        self.ski_inclinometer_reader = InclinometerReader(ski_inclinometer_port)
        self.level_inclinometer_reader = InclinometerReader(level_inclinometer_port)
        self.arduino_controller = ArduinoController(arduino_port)
        self.force_gauge_reader = ForceGaugeReader(force_gauge_left_port, force_gauge_right_port)
        self.ski_profile_calculator = 

    def sensor_automation(self, test_interval_mm, direction):
        data_matrix = []
        stop_num = 0
        self.ski_inclinometer_reader.serial_port.reset_input_buffer()
        pitch, roll = self.ski_inclinometer_reader.get_HWT905TTL_data()
        self.arduino_controller.current_pitch = pitch
        self.arduino_controller.current_roll= roll
        kill_switch_pressed = self.arduino_controller.kill_switch_pressed

        while stop_num != 42 and stop_num != 86 and not kill_switch_pressed:
            time.sleep(0.125)
            self.ski_inclinometer_reader.serial_port.reset_input_buffer()
            pitch, roll = self.ski_inclinometer_reader.get_inclinometer_reading()
            force1, force2 = self.force_gauge_reader.force_average(1)

            row_entry = [pitch, roll, force1, force2]
            data_matrix.append(row_entry)
            print("data_matrix: ", data_matrix)

            sig = self.arduino_controller.move_x_mm(-1 * test_interval_mm, direction)
            print(sig)
            stop_num = int(sig)
            kill_switch_pressed = self.arduino_controller.kill_switch_pressed

        return data_matrix

    def level_force_gauges_2(self, desired_angle, precision, step_size):
        desired_angle += 90
        kill_switch_pressed = self.arduino_controller.kill_switch_pressed
        MOVE_FORCE_GAUGES = 24

        roll, pitch = self.level_inclinometer_reader.get_HWT905TTL_data()
        self.arduino_controller.current_pitch = pitch
        self.arduino_controller.current_roll = roll

        ret_signal = 24
        while not (desired_angle - precision) < roll < (desired_angle + precision) and not int(ret_signal) == 86:
            if abs(pitch - desired_angle) < 10:
                step_size = 7
            if abs(pitch - desired_angle) < 5:
                step_size = 5
            if abs(pitch - desired_angle) < 1:
                step_size = 1

            message = self.make_message(str(MOVE_FORCE_GAUGES), roll, desired_angle, precision, step_size)
            ret_signal = self.arduino_controller.serial_communication(message)
            roll, pitch = self.level_inclinometer_reader.get_inclinometer_reading()
            kill_switch_pressed = self.arduino_controller.kill_switch_pressed

        self.arduino_controller.flush()

    def move_force_gauges_until_desired_force_2(self, desired_force_left, desired_force_right, precision, step_size):
        ret_signal = 24
        force_left, force_right = self.force_gauge_reader.force_average(1)
        kill_switch_pressed = self.arduino_controller.kill_switch_pressed

        while not (desired_force_left - precision) < force_left < (desired_force_left + precision) \
                or not (desired_force_right - precision) < force_right < (desired_force_right + precision) \
                and not int(ret_signal) == 86:
            left_step = self.adjust_step_size(desired_force_left, force_left)
            right_step = self.adjust_step_size(desired_force_right, force_right)

            message = self.make_message(str(self.arduino_controller.MOVE_FORCE_GAUGES), force_left, desired_force_left, precision, left_step)
            message = self.make_message(message, force_right, desired_force_right, precision, right_step)
            ret_signal = self.arduino_controller.serial_communication(message)
            force_left, force_right = self.force_gauge_reader.force_average(1)
            kill_switch_pressed = self.arduino_controller.kill_switch_pressed

        self.arduino_controller.flush()

    @staticmethod
    def adjust_step_size(desired, actual):
        if abs(desired - actual) < 20:
            step_size = 10
        elif abs(desired - actual) < 10:
            step_size = 5
        elif abs(desired - actual) < 5:
            step_size = 2
        else:
            step_size = 15

        if desired < actual:
            step_size *= -1

        return step_size

    @staticmethod
    def make_message(m, actual, desired, precision, step_size):
        if actual <= desired + precision and actual >= desired - precision:
            return m + ',0,0'
        elif actual < desired:
            return m + ',0,' + str(step_size)
        else:
            return m + ',' + str(step_size) + ',0'

# Usage example:
if __name__ == "__main__":
    ski_inclinometer_port = "COMX"  # Replace with the actual port your ski inclinometer is connected to
    level_inclinometer_port = "COMY"  # Replace with the actual port your level inclinometer is connected to
    arduino_port = "COMZ"  # Replace with the actual port your Arduino is connected to
    force_gauge_left_port = "COMA"  # Replace with the actual port your left force gauge is connected to
    force_gauge_right_port = "COMB"  # Replace with the actual port your right force gauge is connected to

    ski_rig_controller = SkiRigAutomationController(ski_inclinometer_port, level_inclinometer_port, arduino_port, force_gauge_left_port, force_gauge_right_port)

    # Example of using the sensor_automation function
    test_interval_mm = 10  # Replace with the desired test interval in millimeters
    direction = 1  # Replace with the desired direction (1 for forward, -1 for backward)
    data_matrix = ski_rig_controller.sensor_automation(test_interval_mm, direction)
    print("Data Matrix:", data_matrix)

    # Example of using the level_force_gauges_2 function
    desired_angle = 5  # Replace with the desired angle for leveling
    precision = 1  # Replace with the desired precision level for leveling
    step_size = 5  # Replace with the desired step size for leveling
   
