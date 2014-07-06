start_image_filename = 'start.png'
back_image_filename = 'bg.jpg'
block_image_filename = 'pipe.png'
bird_image_filename = 'bird.png'
title_image_filename = 'main.png'
ready_image_filename = 'ready.png'
import pygame
from pygame.locals import *
from gameobjects.vector2 import *   
import random
import math
SCREEN_SIZE = (378,537)#屏幕分辨率
run1 = 0#全局变量
run2 = 0
over = 0
def load_image(file, width, number):#用于载入子图
    surface = pygame.image.load(file).convert_alpha()
    height = surface.get_height() 
    return [surface.subsurface(
        Rect((i * width, 0), (width, height))
        ) for i in range(number)]
class Object(object):#实体类
    def __init__(self,name,position):
        self.name = name
        self.position = Vector2(*position)
        self.speed = 0
class Fish(pygame.sprite.Sprite):#精灵类
    images = []
    def __init__(self,r):#初始化
        self.order = 0#图片序列号
        self.rate = 0.2#更新速率0.2秒
        self.height = 60#图片高度
        self.number = 3#图片数量
        self.position = Vector2(189,269)#位置
        self.r = r#碰撞半径
        self.speed = 0#速度
        pygame.sprite.Sprite.__init__(self)
        self.images = load_image(bird_image_filename,80, 3)#载图
        self.image = self.images[self.order]#判断是哪个贴图
        #self.rect = Rect(0, 0, self.width, self.height)
        #self.life = self._life
        self.passed_time = 0#根据时间判断
 
    def update(self, passed_time):#更新图片
        self.passed_time += passed_time
        self.order = ( self.passed_time / self.rate ) % self.number
        if self.order == 0 and self.passed_time > self.rate:
            self.passed_time = 0
        self.image = self.images[int(self.order)]

    def render(self,screen):#其实精灵类有自己的blit方法，这里写的不好
        x,y = self.position
        x -= 40
        y -= 30
        screen.blit(self.image,(int(x),int(y)))

class Block(Object):#管道类，最一开始用方块实现的，所以叫BLOCK
    def __init__(self,name,position,ID,image):
        Object.__init__(self,name,position)
        self.ran = random.randint(0,200)#随机值用于开口位置
        self.ID = ID#用于标记这是第几个管道，方便统计分数
        self.image = image#图片
    def render(self,screen):#绘制
        x,y = self.position       
        screen.blit(self.image,(x,250+self.ran))#画下方管道
        screen.blit(self.image,(x,self.ran-353))#画上方管道
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
    title_image = pygame.image.load(title_image_filename).convert_alpha()
    ready_image = pygame.image.load(ready_image_filename).convert_alpha()
    bg_image = pygame.image.load(back_image_filename).convert()
    buttons["start"] = Button((189,269),start_image)#开始按钮位置
    pygame.event.set_allowed(KEYDOWN)#允许按键
    x,y = title_image.get_size()
    while True:
        button_pressed = None#初始化按钮
        buttons["start"]
        screen.blit(bg_image, (0,0))
        screen.blit(title_image,(SCREEN_SIZE[0]/2-x/2,100+y/2))
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
                    screen.blit(bg_image, (0,0))#准备画面
                    screen.blit(ready_image,(0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)#停2S
                    run()#开始
def dead(block1,block2,fish):#如果dead
    block1.speed = 0#管道静止
    block2.speed = 0
    global run1
    global run2
    global over
    run1 = 1#防止游戏接着跑
    run2 = 1
    over = 1
    pygame.time.wait(1000)#等一秒
    fish.speed = -35#bird向上跳
    pygame.event.set_blocked(KEYDOWN)#阻止键盘操作
    
def run():
    pygame.init()#初始化
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#窗口
    bg_image = pygame.image.load(back_image_filename).convert()
    block_image = pygame.image.load(block_image_filename).convert_alpha()
    r = 15#bird半径
    font = pygame.font.SysFont("arial",32)#字体
    fish = Fish(r)#bird
    block1 = Block("Block1",(378.,0.),1,block_image)#管道1
    block2 = Block("Block2",(378.,0.),0,block_image)#管道2
    flag1 = 0#计数标志位
    flag2 = 0
    global run1
    global run2
    global over
    run1 = 0#运行标志位
    run2 = 0
    over = 0#结束标志位，为1则结束
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
                    fish.speed = -6
        passed_time = clock.tick(80)/1000#80fps
        fish.speed += passed_time * 25#小球的加速度
        fish.position += (0,fish.speed)#计算小球位置
        if over!=1:
            block1.speed = passed_time * 160#方块的速度
        block1.position[0] -= block1.speed#方块的位置
        block2.position[0] -= block2.speed
        block1.render(screen)#绘制
        block2.render(screen)
        if fish.speed < 0:
            fish.update(passed_time)#鸟在上飞过程才扇翅膀
        else:
            fish.image = fish.images[0]#下降过程图片静止
        fish.render(screen)
        screen.blit(font.render(point_text,True,(0,0,0)),(189,50))#打印分数
        pygame.display.update()#update


        if fish.position[1] - r< 0:#到达顶方的碰撞
            fish.position[1] = r
            fish.speed = 0
        if over == 0:
            if fish.position[1] + r > 537:#到达最下方
                    dead(block1,block2,fish)#dead
                    fish.position -= (0,30)#防止直接退出
        elif fish.position[1] > 580:#掉下以后
            pygame.time.wait(1000)#等一秒退出
            start()
        if block1.position[0] < 189 - width - r and flag1 == 0 :#当一个方块x到一定值时另一个方块准备就绪
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
        
        if block1.position[0] < 40 and run1 == 0:#当一个方块左移到40时，另一个方块获得速度
            block2.speed = block1.speed
            run1 = 1
            run2 = 0
        if block2.position[0] < 40 and run2 == 0:
            block1.speed = block2.speed
            run2 = 1
            run1 = 0
        if over!=1:
            
            if x - width - r <= block1.position[0] <= x + r :#判定碰撞
                if x < block1.position[0] <= x + r and (math.sqrt(r**2 - (block1.position[0]-x)**2)+100+block1.ran > fish.position[1] or (math.sqrt(r**2 - (block1.position[0]-x)**2))>250+block1.ran - fish.position[1]):
                    dead(block1,block2,fish)
                    
                if x - width <= block1.position[0] <= x and (fish.position[1] < block1.ran + 100 + r or fish.position[1] > 250 - r + block1.ran):
                    dead(block1,block2,fish)
                if x - width - r <= block1.position[0] < x - width and (math.sqrt(r**2 - (block1.position[0]-(x-width-r))**2)+100+block1.ran > fish.position[1] or (math.sqrt(r**2 - (block1.position[0]-(x-width-r))**2))>250+block1.ran- fish.position[1]):
                    dead(block1,block2,fish)
                
            if x - width - r <= block2.position[0] <= x + r :#判定碰撞
                if x < block2.position[0] <= x + r and (math.sqrt(r**2 - (block2.position[0]-x)**2)+100+block2.ran > fish.position[1] or (math.sqrt(r**2 - (block2.position[0]-x)**2))>250+block2.ran - fish.position[1]):
                    dead(block1,block2,fish)
                if x - width <= block2.position[0] <= x and (fish.position[1] < block2.ran + 100 + r or fish.position[1] > 250 - r + block2.ran):
                    dead(block1,block2,fish)
                if x - width - r <= block2.position[0] < x - width and (math.sqrt(r**2 - (block2.position[0]-(x-width-r))**2)+100+block2.ran > fish.position[1] or (math.sqrt(r**2 - (block2.position[0]-(x-width-r))**2))>250+block2.ran - fish.position[1]):
                    dead(block1,block2,fish)
        point_text = str(min (block1.ID,block2.ID))#获得当前分数






if __name__ == "__main__":
    start()
