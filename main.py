import pygame
import obj
import random
import pygame_widgets as pw
from pygame_widgets.button import Button

min_num=100
max_num=700
pipe_timer=0
starting=True
game_over=False
score=0

pygame.init()
pygame.mixer.init()

#for screen
width=1200
height=800
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('FlappyBird')

#for sound
jump_sound=pygame.mixer.Sound('assets/sounds/jump.mp3')
die_sound=pygame.mixer.Sound('assets/sounds/die.mp3')
die_sound_played=False

#for text
text_font=pygame.font.SysFont("Ariel",90) #can add mroe flags
def score_text(text,font,col,x,y):
    img=font.render(text,True,col)
    screen.blit(img,(x+10,y+10))
def end_text(text,font,col,x,y):
    img=font.render(text,True,col)
    screen.blit(img,(x-(img.get_width()/2),y+(img.get_height()/2)))

#for start and replay buttons
def restart():
    global pipe_timer, game_over, score, starting, die_sound_played
    #screen.fill((0,0,0))
    player.velocity=0
    pipe_timer=0
    game_over=False
    score=0
    starting=False
    die_sound_played=False
    player.rect.y=height/2
    pipes.empty()
    start.hide()
    replay.hide()
start=Button(screen,screen.get_width()/2.6,screen.get_height()/2,280,50,text="Start Game",textColour=(255, 255, 255),inactiveColour=(76, 175, 80),hoverColour=(56, 142, 60),pressedColour=(46, 125, 50),onClick=restart)
replay=Button(screen,screen.get_width()/2.6,screen.get_height()/1.5,280,50,text="Replay",textColour=(255, 255, 255),inactiveColour=(76, 175, 80),hoverColour=(56, 142, 60),pressedColour=(46, 125, 50),onClick=restart)
start.hide()
replay.hide()

#clock
clock=pygame.time.Clock()

running=True

#background image
bg=pygame.image.load('assets/images/bg.png').convert()
scroll=0

#pipes sprite group
pipes=pygame.sprite.Group()

#bird/player sprite group
birds=pygame.sprite.Group()
player=obj.player(100,screen.get_height()/2) #object creation
birds.add(player)

#gameloop
while running:
    events=pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            running=False
        #bird jump logic (with spacebar)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and not game_over and not starting:
                player.jump()
                jump_sound.play()
    
   #background
    for i in range(2):
        screen.blit(bg,(i*bg.get_width()+scroll,0))
    scroll-=5
    #scroll reset
    if abs(scroll)>bg.get_width():
        scroll=0

    if not game_over and not starting:
        #collision logic
        if pygame.sprite.spritecollide(player,pipes,False) or player.rect.bottom>=screen.get_height() or player.rect.top<=0:
            game_over=True
        #pipe sprites
        pipe_timer+=1
        if pipe_timer>120:
            center=random.randint(min_num,max_num)
            gap=random.randint(80,150)
            tp=obj.pipe(screen.get_width(),center-gap,True)
            bp=obj.pipe(screen.get_width(),center+gap,False)
            pipes.add(tp,bp)
            pipe_timer=0          
        pipes.draw(screen)
        pipes.update()
        #bird sprites
        birds.update()
        birds.draw(screen)
    elif starting:
        start.listen(events)
        start.show()
    else:
        end_text("Game Over",text_font,(0,0,0),width/2,height/2)
        replay.listen(events)
        replay.show()
        if not die_sound_played:
            die_sound.play()
            die_sound_played=True

    #whole window update
    for p in pipes:
        if p.rect.right<=player.rect.left and not p.passed and not p.flipped:
            p.passed=True
            score+=1
    if not starting:
        st="Score: "+str(score)
        score_text(st,text_font,(0,0,0),0,0)
    pw.update(events)
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()