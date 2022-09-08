import time, random, pygame


def input_number(prompt="", min1=float("-Infinity"), max1=float("Infinity")):
    while True:
        try:
            if prompt == "": prompt = "Enter a number greater than " + str(min1) + " and less than " + str(max1)
            x = float(input(prompt))
            if x >= min1 and x <= max1:
                return x
            else:
                print("Please enter a number greater than", min1, "and less than", max1)
        except:
            print("Please enter a number greater than", min1, "and less than", max1)


fpsCap = int(input_number("What would you like the fps cap to be? (enter zero for infinity) ", 0))

elapsed = 0.1

Gravity = (0, .01)

pygame.init()


def generate_neon_color():
    nums = [random.randint(0, 85), random.randint(85, 170), random.randint(170, 255)]
    nums2 = []
    while len(nums) > 0:
        i = nums[random.randint(0, len(nums) - 1)]
        nums2 += [i]
        nums.remove(i)
    return nums2


class Particle:
    def __init__(self, x, y, color=(255, 255, 255), size=2):
        self.pos = [x, y]
        self.vel = [0, 0]
        self.size = size
        self.color = color

    def apply_force(self, force):
        self.vel[0] += force[0]
        self.vel[1] += force[1]

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def show(self):
        pygame.draw.circle(pygame.display.get_surface(), self.color, (int(self.pos[0]), int(self.pos[1])),
                           int(self.size))


elapsed = 1

Gravity = (0, .01)

pygame.init()

width, height = 500, 500
pygame.display.init()
pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_icon(pygame.Surface((32, 32)))

fireworks = []
stars = []

while True:
    start = time.time()
    pygame.display.set_caption(
        "Firework    Fireworks: " + str(len(fireworks)) + "    Stars: " + str(len(stars)) + "    FPS: " + str(1 / elapsed))
    pygame.display.get_surface().fill((4, 4, 4), special_flags=pygame.BLEND_RGB_SUB)

    for part in fireworks:

        part.show()
        part.apply_force(Gravity)
        part.update()

        if part.vel[1] >= -1 or int(part.pos[0]) not in range(0, width) or int(part.pos[1]) not in range(0, height):
            for x in range(0, 25):
                stars += [Particle(int(part.pos[0]), int(part.pos[1]), part.color, 2)]
                stars[len(stars) - 1].apply_force(
                    (random.uniform(-0.5, 0.5) + part.vel[0], random.uniform(-0.5, 0.5) + part.vel[1]))
            fireworks.remove(part)

    for part in stars:

        part.show()
        part.apply_force(Gravity)
        part.update()

        if int(part.pos[0]) not in range(0, width) or int(part.pos[1]) not in range(0, height):
            stars.remove(part)
            pass

    # create fireworks
    if random.randint(0, 10) == 1:
        fireworks += [Particle(random.randint(0, width), height, generate_neon_color())]
        fireworks[len(fireworks) - 1].apply_force((random.uniform(-.2, .2), random.uniform(-4, -1.375)))

    pygame.display.flip()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            pygame.display.set_mode((width, height), pygame.RESIZABLE)

    end = time.time()
    elapsed = end - start
    if fpsCap > 0:
        if elapsed < (1 / fpsCap):
            time.sleep((1 / fpsCap) - elapsed)
        elapsed = time.time() - start

input("Press enter to quit...")
