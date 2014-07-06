start_image_filename = 'start.png'
back_image_filename = 'bg.jpg'
block_image_filename = 'pipe.png'
import pygame
from pygame.locals import *
from gameobjects.vector2 import *   
import random
import math
SCREEN_SIZE = (378,537)
#SCREEN_SIZE = (600,800)
class Object(object):#实体类
    def __init__(self,name,position):
        self.name = name
        self.position = Vector2(*position)
        self.speed = 0


class Fish(Object):#小球类
    def __init__(self,name,position,r):
        Object.__init__(self,name,position)
        self.r = r
    def render(self,screen):#绘制小球自己
        x,y = self.position
        pygame.draw.circle(screen, (251,162,40), (int(x),int(y)),self.r)
class Block(Object):#方块类
    def __init__(self,name,position,ID,image):
        Object.__init__(self,name,position)
        self.ran = random.randint(0,200)#随机值用于开口位置
        self.ID = ID#用于标记这是第几个方块，方便统计分数
        self.image = image
    def render(self,screen):#绘制上下两个长方形形成障碍物
        x,y = self.position       
        screen.blit(self.image,(x,250+self.ran))
        screen.blit(self.image,(x,self.ran-353))
class Button(object):#按钮类
    def __init__(self , position,image):
 
        self.position = position
        self.image = image
 
    def render(self, screen):
        x, y = self.position
        w, h = self.image.get_size()
        screen.blit(self.image, (x-w/2, y-h/2))
 
    def is_over(self, point):#判断鼠标是否在按钮上
        if (SCREEN_SIZE[0]-self.image.get_size()[0])/2 < point[0]<(SCREEN_SIZE[0]+self.image.get_size()[0])/2:
            if (SCREEN_SIZE[1]-self.image.get_size()[1])/2 < point[1]<(SCREEN_SIZE[1]+self.image.get_size()[1])/2:
                return True
        
def start():#开始界面
    buttons = {}
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#设置窗口
    start_image = pygame.image.load(start_image_filename).convert_alpha()
    bg_image = pygame.image.load(back_image_filename).convert()
    buttons["start"] = Button((189,269),start_image)#开始按钮位置
    while True:
        screen.fill((140,215,251))#填色
        button_pressed = None#初始化按钮
        buttons["start"]
        screen.blit(bg_image, (0,0))
        for button in buttons.values():#绘制所有按钮
            button.render(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:#如果鼠标按下
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        button_pressed = button_name
                        break
            if button_pressed is not None:
                if button_pressed == "start":#如果按得是开始按钮
                    run()#开始

    
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#窗口
    bg_image = pygame.image.load(back_image_filename).convert()
    block_image = pygame.image.load(block_image_filename).convert_alpha()
    r = 20
    font = pygame.font.SysFont("arial",32)#字体
    fish = Fish("flappy fish",(189.,269.),r)#球类
    block1 = Block("Block1",(378.,0.),1,block_image)#方块1
    block2 = Block("Block2",(378.,0.),0,block_image)#方块2
    run1 = 0#运行标志位
    flag1 = 0#计数标志位
    run2 = 0
    flag2 = 0
    clock = pygame.time.Clock()#引入时钟
    point_text = "0"#初始化分数
    ID = 1#初始化方块ID
    bgx,bgy = bg_image.get_size()
    x = bgx/2
    y = bgy/2
    width = 70
    while True:
        screen.blit(bg_image, (0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:#空格就获得向上的速度
                 if event.key == K_SPACE:
                    fish.speed = -3
        time_passed = clock.tick(80)/1000#80fps
        fish.speed += time_passed * 10#小球的加速度
        fish.position += (0,fish.speed)#计算小球位置
        block1.speed = time_passed * 80#方块的速度
        block1.position[0] -= block1.speed#方块的位置
        block2.position[0] -= block2.speed
        block1.render(screen)#绘制
        block2.render(screen)
        fish.render(screen)
        screen.blit(font.render(point_text,True,(0,0,0)),(189,50))#打印分数
        pygame.display.update()#update


        if fish.position[1] - r< 0:#到达顶方的碰撞
            fish.position[1] = r
            fish.speed = 0
        if fish.position[1] +r > 537:#到达最下方判定死亡
            start()
        if block1.position[0] < 189 - width - r and flag1 == 0 :#当一个方块x坐标左移到170时另一个方块准备就绪
            block2.position[0] = bgx
            block2.speed = 0
            block2.ran = random.randint(0,200)
            ID+=1
            block2.ID = ID
            flag1 = 1
            flag2 = 0
        if block2.position[0] < 189 - width - r and flag2 == 0 :
            block1.position[0] = bgx
            block1.speed = 0
            block1.ran = random.randint(0,200)
            ID+=1
            block1.ID = ID
            flag2 = 1
            flag1 = 0
        
        if block1.position[0] < 40 and run1 == 0:#当一个方块左移到100时，另一个方块获得速度
            block2.speed = time_passed * 80
            run1 = 1
            run2 = 0
        if block2.position[0] < 40 and run2 == 0:
            block1.speed = time_passed * 80
            run2 = 1
            run1 = 0
        
        if x - width - r <= block1.position[0] <= x + r :#判定碰撞
            if x < block1.position[0] <= x + r and (math.sqrt(r**2 - (block1.position[0]-x)**2)+100+block1.ran > fish.position[1] or (math.sqrt(r**2 - (block1.position[0]-x)**2))>250+block1.ran - fish.position[1]):
                start()
            if x - width <= block1.position[0] <= x and (fish.position[1] < block1.ran + 100 + r or fish.position[1] > 250 - r + block1.ran):
                start()
            if x - width - r <= block1.position[0] < x - width and (math.sqrt(r**2 - (block1.position[0]-(x-width-r))**2)+100+block1.ran > fish.position[1] or (math.sqrt(r**2 - (block1.position[0]-(x-width-r))**2))>250+block1.ran- fish.position[1]):
                start()
            
        if x - width - r <= block2.position[0] <= x + r :#判定碰撞
            if x < block2.position[0] <= x + r and (math.sqrt(r**2 - (block2.position[0]-x)**2)+100+block2.ran > fish.position[1] or (math.sqrt(r**2 - (block2.position[0]-x)**2))>250+block2.ran - fish.position[1]):
                start()
            if x - width <= block2.position[0] <= x and (fish.position[1] < block2.ran + 100 + r or fish.position[1] > 250 - r + block2.ran):
                start()
            if x - width - r <= block2.position[0] < x - width and (math.sqrt(r**2 - (block2.position[0]-(x-width-r))**2)+100+block2.ran > fish.position[1] or (math.sqrt(r**2 - (block2.position[0]-(x-width-r))**2))>250+block2.ran - fish.position[1]):
                start()
        point_text = str(min (block1.ID,block2.ID))#获得当前分数






if __name__ == "__main__":
    start()
