class Entity:
    """всё что требует регулярного обновления"""
    CurrId = 0

    def __init__(self):
        self.id = Entity.CurrId
        Entity.CurrId += 1
        self.dead = False

    def update(self, dt, t, world):
        raise NotImplementedError("Пиши код, дядя!")

    def hit(self, damage):
        self.hp = max(self.hp - damage, 0)
        if self.hp == 0:
            self.on_zero_hp()

    def on_zero_hp(self):
        self.dead = True

    def get_sprites(self):
        raise NotImplementedError("Пиши код, дядя!")

    def draw(self, scale, offset):
        raise NotImplementedError("Пиши код, дядя!")
