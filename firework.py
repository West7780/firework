#set mode
#mode = 'fire'
mode = input('rain or fire? ')
print('Loading',end="")
import time,random,pygame,math

def genNeon():
    nums = [random.randint(0,85),random.randint(85,170),random.randint(170,255)]
    nums2 = []
    while len(nums)>0:
        i = nums[random.randint(0,len(nums)-1)]
        nums2 += [i]
        nums.remove(i)
    return nums2

def genVector(length):
    num1 = random.uniform(0,abs(length))
    num2 = length-num1
    num3 = random.randint(0,1)
    if num3 == 0: num3 = -1
    num4 = random.randint(0,1)
    if num4 == 0: num4 = -1
    return num1*num3,num2*num4

class particle():
    def __init__(self,x,y,color = (255,255,255),size = 2,lifespan=0):
        self.pos = [x,y]
        self.vel = [0,0]
        self.size = size
        self.color = color
        self.timealive = 0
        self.lifespan = lifespan
        
    def applyForce(self,force):
        self.vel[0] += force[0]
        self.vel[1] += force[1]
    
    def update(self):
        if self.lifespan>0: self.timealive+= 1
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
pygame.mouse.set_visible(0)
mouseColor = genNeon()

raindrops = []
bursting = []
stars = []

while True:
    start = time.time()
    pygame.display.set_caption(mode+"    Particles:"+str(len(raindrops+bursting+stars)))
    pygame.display.get_surface().fill((5,5,5),special_flags = pygame.BLEND_RGB_SUB)

    for part in bursting:
        
        part.show()
        part.applyForce(Gravity)
        part.update()
        
        if part.vel[1] >= random.random()*-1 or int(part.pos[0]) not in range(0,width) or int(part.pos[1]) not in range(0,height):
            for x in range(0,25):
                force = genVector(random.uniform(0.1,0.5))
                stars+= [particle(int(part.pos[0]),int(part.pos[1]),part.color,0.79,150)]
                stars[len(stars)-1].applyForce((force[0]+part.vel[0],force[1]+part.vel[1]))
            bursting.remove(part)

    for part in stars:

        part.show()
        part.applyForce(Gravity)
        part.update()
        
        if part.timealive>=part.lifespan or int(part.pos[0]) not in range(0,width) or int(part.pos[1]) not in range(0,height):
            stars.remove(part)

    for part in raindrops:

        part.show()
        part.applyForce(Gravity)
        part.update()
        
        if int(part.pos[0]) not in range(0,width) or int(part.pos[1]) not in range(0,height):
            raindrops.remove(part)

    pygame.draw.circle(pygame.display.get_surface(), mouseColor, pygame.mouse.get_pos(), 5)

    if mode == 'fire':
        #create burst bursting
        if random.randint(0,10) == 1:
            bursting+= [particle(random.randint(0,width),height,genNeon())]
            bursting[len(bursting)-1].applyForce((random.uniform(-.2,.2),random.uniform(-3,-1.375)))
    elif mode == 'rain':
        #create rain
        if random.randint(0,7) == 1:
            raindrops+= [particle(random.randint(0,width),0,genNeon())]
    else:
        #create burst bursting
        if random.randint(0,10) == 1:
            bursting+= [particle(random.randint(0,width),height,genNeon())]
            bursting[len(bursting)-1].applyForce((random.uniform(-.2,.2),random.uniform(-3,-1.375)))
       #create rain
        if random.randint(0,7) == 1:
            raindrops+= [particle(random.randint(0,width),0,genNeon())]
            
    pygame.display.flip()

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.VIDEORESIZE:
            width,height = event.w,event.h
            pygame.display.set_mode((width,height),pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONUP:
            if 1:
                for x in range(0,150):
                    stars+= [particle(event.pos[0],event.pos[1],mouseColor,1)]
                    stars[len(stars)-1].applyForce(genVector(random.uniform(0,1.25)))
            else:
                raindrops+= [particle(event.pos[0],event.pos[1],mouseColor,4)]
            mouseColor = genNeon()

    end = time.time()
    elapsed = end - start
    if elapsed < 0.02:
        time.sleep(0.02-elapsed)
