from pid import PID
from lowpass import LowPassFilter
from yaw_controller import YawController

GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle, vehicle_mass,decel_limit):
        self.vehicle_mass = vehicle_mass
        self.wheel_radius = wheel_base
        self.decel_limit=decel_limit

        self.yawcontroller = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)
        self.set_controllers()
        pass

    def control(self, linear_velocity, angular_velocity, current_velocity, dbw_enabled, time_elapsed):
        # Return throttle, brake, steer

        if not dbw_enabled:
            self.set_controllers()
            return 0.0, 0.0, 0.0

        # throttle and brake controllers
        current_velocity=self.lowpass_flt.filt(current_velocity)
        linear_velocity_error = linear_velocity - current_velocity
        throttle = self.pid_throttle.step(linear_velocity_error, time_elapsed)
        brake = 0.0

        if linear_velocity == 0. and current_velocity < 0.1:
            throttle = 0.0
            brake=400

        elif throttle < 0.1 and linear_velocity_error < 0:
             throttle = 0.0
             decel = max(linear_velocity_error,self.decel_limit)
             brake=abs(decel)*self.vehicle_mass*self.wheel_radius

        # steering controller
        steer = self.yawcontroller.get_steering(linear_velocity, angular_velocity, current_velocity)
        #steer = self.lowpass_flt.filt(steer)

        return throttle, brake, steer

    def set_controllers(self):
        self.pid_throttle = PID(0.3, 0.1, 0.0, 0.0, 0.6)
        self.lowpass_flt = LowPassFilter(0.5, 0.2)
