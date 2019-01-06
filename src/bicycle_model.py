import math

class BicycleModel:
    def __init__(self, wheelbase_length, steer_angle = 0.0):
        self.wheelbase_length = wheelbase_length
        self.steer_angle = 0.0
    
    def set_steer_angle(self, steer_angle):
        self.steer_angle = steer_angle
    
    def set_rear_curvature(self, k_rear):
        self.steer_angle = math.atan(k_rear * self.wheelbase_length)
    
    def get_rear_curvature(self):
        return math.tan(self.steer_angle) / self.wheelbase_length
    
    def set_front_curvature(self, k_front):
        self.steer_angle = math.asin(self.wheelbase_length * k_front)

    def get_front_curvature(self):
        return math.sin(self.steer_angle) / self.wheelbase_length
    
    def get_steer_angle(self):
        return self.steer_angle
    
    def get_offset_bicycle(self, delta_y):
        if self.steer_angle == 0.0:
            return BicycleModel(self.wheelbase_length, 0.0)
        new_bike = BicycleModel(self.wheelbase_length)
        new_bike.set_rear_curvature(1./(1./self.get_rear_curvature() - delta_y))
        return new_bike

class AckermannModel(BicycleModel):
    def __init__(self, wheelbase_length, front_wheelbase_width, steer_angle = 0.0):
        BicycleModel.__init__(self, wheelbase_length, steer_angle)
        self.front_wheelbase_width = front_wheelbase_width

    def get_left_bicycle(self):
        return self.get_offset_bicycle(self.front_wheelbase_width / 2.)
    
    def get_right_bicycle(self):
        return self.get_offset_bicycle(-1 * self.front_wheelbase_width / 2.)


if __name__ == "__main__":
    for wheelbase_length in [1., 2.]:
        for wheelbase_width in [1., 2.]:
           for curvature in [-1, -0.5, 0, 0.5, 1]:
                car = AckermannModel(wheelbase_length, wheelbase_length)
                car.set_rear_curvature(curvature)
                print(
                    'wheelbase_length: ', wheelbase_length, 
                    'wheelbase_width: ', wheelbase_width, 
                    'curvature: ', curvature,
                    'left_steer_angle', car.get_left_bicycle().get_steer_angle(),
                    'center_steer_angle: ', car.get_steer_angle(), 
                    'right_steer_angle', car.get_right_bicycle().get_steer_angle())


