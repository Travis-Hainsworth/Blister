import time
from SkiRigAutomationController import SkiRigAutomationController
from SkiProfileCalculator import SkiProfileCalculator

class SkiFlexTester:
    def __init__(self, ski_inclinometer_port, level_inclinometer_port, arduino_port, force_gauge_left_port, force_gauge_right_port, test_interval = 50, test_name):
        self.ski_rig_automation_controller = SkiRigAutomationController(ski_inclinometer_port, level_inclinometer_port, arduino_port, force_gauge_left_port, force_gauge_right_port)
        self.ski_profile_calculator = SkiProfileCalculator()
        self.test_interval_mm = test_interval
        self.dir_name = test_name
        self.unloaded = None
        self.loaded = None
        self.torsion = None

        

    def run_unloaded_test(self):
        try:
            KILL_SWITCH_SIGNAL = self.ski_rig_automation_controller.arduino_controller.KILL_SWITCH_SIGNAL
            kill_switch_pressed = self.ski_rig_automation_controller.arduino_controller.kill_switch_pressed
            if not kill_switch_pressed:
                pass_check = self.requirment_check(False)
                if ~pass_check:
                    return
                self.make_sure_at_start()
                self.make_sure_level()   
                self.make_sure_desired_force(0, 0)
                data_matrix_unloaded = self.ski_rig_automation_controller.sensor_automation(self.test_interval_mm, 0)
                kill_switch_pressed = self.ski_rig_automation_controller.arduino_controller.kill_switch_pressed
                pause(2)
        except Exception as e:
            print(e)

    def run_loaded_test(self):
        try:
            KILL_SWITCH_SIGNAL = self.ski_rig_automation_controller.arduino_controller.KILL_SWITCH_SIGNAL
            kill_switch_pressed = self.ski_rig_automation_controller.arduino_controller.kill_switch_pressed
            if not kill_switch_pressed:
                pass
                # Perform other checks and operations
                # ...

        except Exception as e:
            print(e)

    def run_torsion_test(self):
        try:
            KILL_SWITCH_SIGNAL = self.ski_rig_automation_controller.arduino_controller.KILL_SWITCH_SIGNAL
            kill_switch_pressed = self.ski_rig_automation_controller.arduino_controller.kill_switch_pressed
            if not kill_switch_pressed:
                pass
                # Perform other checks and operations
                # ...

        except Exception as e:
            print(e)

    def make_sure_at_start(self):
        distance_from_start = self.ski_rig_automation_controller.arduino_controller.get_distance_from_start()
        print(distance_from_start)
        if distance_from_start != 0:
            ret_sig = self.ski_rig_automation_controller.arduino_controller.return_to_start()

    def make_sure_level(self):
        pitch, roll = self.ski_rig_automation_controller.level_inclinometer_reader.get_HWT905TTL_data()
        self.ski_rig_automation_controller.level_inclinometer_reader.current_pitch = pitch
        self.ski_rig_automation_controller.level_inclinometer_reader.current_roll = roll
        desired_angle = 0
        precision = 0.25
        step_size_level = 15
        if not (pitch < desired_angle + precision and pitch > (desired_angle - precision)):
            ret_sig = self.ski_rig_automation_controller.level_force_gauges_2(desired_angle, precision, step_size_level)

    def make_sure_desired_force(self, left, right):
        force_left, force_right = self.ski_rig_automation_controller.force_gauge_reader.force_average(1)
        desired_force_left = left
        desired_force_right = right
        precision = 0.2
        step_size_force = 10
        if force_left > desired_force_left + precision or force_right > desired_force_left + precision:
            ret_sig = self.ski_rig_automation_controller.move_force_gauges_until_desired_force(desired_force_left, desired_force_right, precision, step_size_force)
    
    def requirement_check(comp, intermediate_test):
        

        message = ""
        pass_check = True

        if not dir_name:
            message = "Please set dir name before running tests"
            pass_check = False
        elif not test_interval_mm:
            message = "Please set the test interval before running unloaded test."
            pass_check = False
        elif intermediate_test and not unloaded:
            message = "Please run unloaded test before a loaded and torsion test."
            pass_check = False

        if not pass_check:
            # Handle the error, e.g., display an alert
            # in Python GUI frameworks like Tkinter or PyQt,
            # or simply print the error message for console applications.
            # For this example, let's just print the message.
            print("Test Error:", message)

        return pass_check

    # Other methods and helper functions can be added as needed
