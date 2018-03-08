from pid import PID
from yaw_controller import YawController

#Import Needed MessageTypes



GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, vehicle_mass, wheel_radius, kp, ki, kd, decel_limit, accel_limit, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
         
        #self.wheel_base = wheel_base
        #self.steer_ratio = steer_ratio
        #self.min_speed = min_speed
        #self.max_lat_accel = max_lat_accel
        #self.max_steer_angle = max_steer_angle
        self.accel_limit = accel_limit
        self.decel_limit = decel_limit
        self.vehicle_mass = vehicle_mass
        self.wheel_radius = wheel_radius

        self.speed_controller = PID(kp, ki, kd, decel_limit, accel_limit)#SOME ARGS NEEDED
        self.steer_controller = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)#SOME ARGS NEEDED

        pass

    def control(self, sample_time, linear_velocity, angular_velocity, current_velocity):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer

        speed_error = current_velocity - (linear_velocity/ONE_MPH)

        steer = self.steer_controller.get_steering(linear_velocity, angular_velocity, current_velocity)
        accel = self.speed_controller.step(speed_error, sample_time)

        throttle, brake = self.gas_or_brake(accel)

        return throttle, brake, steer

    def gas_or_brake(self, accel): 

    	if accel >= 0: 
    		throttle = min(accel/self.accel_limit, 1.0)
    	else:
    		throttle = 0

    	if accel < 0: 
    		decel = max(accel, self.decel_limit)
    		brake = decel * self.vehicle_mass * self.wheel_radius
    	else: 
    		brake = 0

    	return throttle, brake

    	#if desired accel is less than 0
    		#calculate the required braking force

    	#return both 

    	#return 0.0, 0.0
