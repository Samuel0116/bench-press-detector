class RepCounter:
    def __init__(self, down_angle=35, up_angle=130):
        self.reps = 0
        self.stage = None
        self.down_angle = down_angle
        self.up_angle = up_angle

    def counter(self, angle):
        if self.stage == "down" and angle <= self.down_angle:
            self.reps += 1
            self.stage = "up"
        elif angle >= self.up_angle:
            self.stage = "down"

        return self.reps
