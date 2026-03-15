import pygame
class player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.birds=[]
        self.r=10
        self.velocity=0
        self.gravity=0.25
        self.jump_strength=-8
        self.temp_im=pygame.image.load('assets/images/b1.png').convert_alpha()
        self.birds.append(pygame.transform.scale(self.temp_im,(self.temp_im.get_width()/self.r,self.temp_im.get_height()/self.r)))
        self.temp_im=pygame.image.load('assets/images/b2.png').convert_alpha()
        self.birds.append(pygame.transform.scale(self.temp_im,(self.temp_im.get_width()/self.r,self.temp_im.get_height()/self.r)))
        self.i=0
        self.image=self.birds[self.i]
        self.rect=self.image.get_rect()
        self.rect.topleft=[x,y]

    def jump(self):
        #jump logic
        self.velocity=self.jump_strength

    def update(self):
        #movement/update logic
        self.i+=0.2
        self.velocity+=self.gravity
        self.rect.y+=self.velocity
        if self.i>=len(self.birds):
            self.i=0
        self.image=self.birds[int(self.i)]

class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,flipped):
        super().__init__()
        self.passed=False
        self.flipped=flipped
        self.r=1
        self.im=pygame.image.load('assets/images/pipe.png').convert_alpha()
        self.im=pygame.transform.scale(self.im,(self.im.get_width()/self.r,self.im.get_height()/self.r))
        if flipped:
            self.im=pygame.transform.flip(self.im,False,True)
        self.image=self.im
        self.rect=self.image.get_rect()
        if flipped:
            self.rect.bottomleft=[x,y] 
        else:
            self.rect.topleft=[x,y]

    def update(self):
        #movement/update logic
        self.rect.x-=5
        if self.rect.x+self.rect.width<=0:
            self.kill()