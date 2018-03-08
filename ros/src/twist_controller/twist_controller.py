from pid import PID
from yaw_controller import YawController

#Import Needed MessageTypes



GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
         
        #self.wheel_base = wheel_base
        #self.steer_ratio = steer_ratio
        #self.min_speed = min_speed
        #self.max_lat_accel = max_lat_accel
        #self.max_steer_angle = max_steer_angle

        #speed_controller = PID(kp, ki, kd, decel_limit, accel_limit)#SOME ARGS NEEDED
        self.steer_controller = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)#SOME ARGS NEEDED

        pass

    def control(self, linear_velocity, angular_velocity, current_velocity):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer

        steer = self.steer_controller.get_steering(linear_velocity, angular_velocity, current_velocity)

        return .1, 0., steer

    def gas_or_brake(*args): 

    	#if desired accel is greater than 0
    		#translate desired accel into pedal %

    	#if desired accel is less than 0
    		#calculate the required braking force

    	#return both 

    	return 0.0, 0.0
