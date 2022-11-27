import Config
from Rock import Rock

class Rocks_luncher():
    def __init__(self) -> None:
        self.rocks = []
        self.pressed = False

        self.static_rocks = []

    def add_rock(self, pos):
        self.rocks.append(Rock(*pos))

    def update_variables(self, water, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            self.pressed = True
        else:
            if self.pressed:
                if mouse_pos[0] > 0 and mouse_pos[0] < Config.WINDOW_SIZE[0]:
                    self.add_rock(mouse_pos)
                    self.pressed = False

        trash_bin = []
        for rock in self.rocks:
            rock.update_variables(water)
            if rock.pos[1] + rock.radius > Config.WINDOW_SIZE[1]:
                rock.pos[1] = Config.WINDOW_SIZE[1] - rock.radius
                trash_bin.append(rock)
                if len(self.static_rocks) > 20:
                    self.static_rocks.pop(0)
                self.static_rocks.append(rock)

        for rock in trash_bin:
            self.rocks.remove(rock)


    def draw(self, surface):
        for rock in self.rocks:
            rock.draw(surface)
        
        for rock in self.static_rocks:
            rock.draw(surface)