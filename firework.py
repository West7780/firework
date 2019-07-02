import time,random,pygame,math

def genNeon():
    nums = [random.randint(0,85),random.randint(85,170),random.randint(170,255)]
    nums2 = []
    while len(nums)>0:
        i = nums[random.randint(0,len(nums)-1)]
        nums2 += [i]
        nums.remove(i)
    return nums2
    
class particle():
    def __init__(self,x,y,color = (255,255,255),size = 2):
        self.pos = [x,y]
        self.vel = [0,0]
        self.size = size
        self.color = color

    def applyForce(self,force):
        self.vel[0] += force[0]
        self.vel[1] += force[1]
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def show(self):
        pygame.draw.circle(pygame.display.get_surface(), self.color, (int(self.pos[0]),int(self.pos[1])), int(self.size))

Gravity = (0,.01)

pygame.init()

width,height = 500,500
pygame.display.init()
pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_icon(pygame.Surface((32,32)))

fireworks = []
stars = []

while True:
    start = time.time()
    pygame.display.set_caption("Firework    Particles:"+str(len(fireworks+stars)))
    pygame.display.get_surface().fill((5,5,5),special_flags = pygame.BLEND_RGB_SUB)

    for part in fireworks:
        
        part.show()
        part.applyForce(Gravity)
        part.update()
        
        if part.vel[1] >= -1 or int(part.pos[0]) not in range(0,width) or int(part.pos[1]) not in range(0,height):
            for x in range(0,25):
                stars+= [particle(int(part.pos[0]),int(part.pos[1]),part.color,0.79)]
                stars[len(stars)-1].applyForce((random.uniform(-0.5,0.5)+part.vel[0],random.uniform(-0.5,0.5)+part.vel[1]))
            fireworks.remove(part)

    for part in stars:

        part.show()
        part.applyForce(Gravity)
        part.update()
        
        if int(part.pos[0]) not in range(0,width) or int(part.pos[1]) not in range(0,height):
            stars.remove(part)
            pass
        
    #create fireworks
    if random.randint(0,10) == 1:
        fireworks+= [particle(random.randint(0,width),height,genNeon())]
        fireworks[len(fireworks)-1].applyForce((random.uniform(-.2,.2),random.uniform(-3,-1.375)))
        
    pygame.display.flip()

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.VIDEORESIZE:
            width,height = event.w,event.h
            pygame.display.set_mode((width,height),pygame.RESIZABLE)

    end = time.time()
    elapsed = end - start
    if elapsed < 0.015:
        time.sleep(0.015-elapsed)
