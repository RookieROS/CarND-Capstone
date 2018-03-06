from pid import PID
from yaw_controller import YawController

#Import Needed MessageTypes



GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, *args, **kwargs):
         
        speed_controller = PID(kp, ki, kd, decel_limit, accel_limit)#SOME ARGS NEEDED
        steer_controller = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)#SOME ARGS NEEDED



        pass

    def control(self, *args, **kwargs):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        return 1., 0., 0.

    def gas_or_brake(*args): 

    	#if desired accel is greater than 0
    		#translate desired accel into pedal %

    	#if desired accel is less than 0
    		#calculate the required braking force

    	#return both 

    	return 0.0, 0.0
