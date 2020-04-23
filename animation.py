from geometry import Direction, Vector, Angles


class CreatureAnimator:
    def __init__(self, textures: dict, update_frequency, direction=Direction.DOWN, frame=0):
        """textures must be in <Direction,list> dictionary, where list contains consecutive frames"""
        self.textures = textures
        self.update_frequency = update_frequency
        self.last_update = 0
        self.direction = direction
        self.frame = frame

    def update(self, t, move: Vector):
        if move.zero():
            self.frame = 0
            self.last_update = t
        else:
            dirs = move.get_matching_directions()
            if self.direction in set(dirs):
                if t > self.last_update + self.update_frequency:
                    self.frame = (self.frame + 1) % len(self.textures[self.direction])
                    self.last_update = t
            else:
                self.direction = dirs[0]
                self.frame = 1
                self.last_update = t

    def get_texture(self):
        return self.textures[self.direction][self.frame]

class CyclicAnimator:
    def __init__(self, textures, update_frequency, direction, frame=0):
        self.textures = textures
        self.update_frequency = update_frequency
        self.last_update = 0
        self.direction = direction
        self.frame = frame

    def update(self, t):
        if t > self.last_update + self.update_frequency:
            self.frame = (self.frame + 1) % len(self.textures)
            self.last_update = t

    def get_texture(self):
        return self.textures[self.frame], Angles[self.direction]