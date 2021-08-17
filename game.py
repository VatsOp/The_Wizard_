import pygame
import random
#import exp
pygame.init()
#GAME WINDOW

clock =pygame.time.Clock()
fps=60

bottom_panel=150
screen_width= 800 
screen_height=400 + bottom_panel

screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Kirtan's Playing Ground")




#pygame variables
current_fighter= 1
total_fighters = 3
action_cooldown= 0
action_wait_time =90
attack =False
potion=False
clicked =False




#defne fonts
font = pygame.font.SysFont("Times New Roman",26)

#define colors
red=(255,0,0)
green = (0,255,0)

#LOAD IMAGES

#background image
background_img = pygame.image.load(r'C:\Users\User\Desktop\game\Game_items\img\Background\background.png').convert_alpha()

#panel image
panel_img = pygame.image.load(r'C:\Users\User\Desktop\game\Game_items\img\Icons\panel.png').convert_alpha()

#wand image
wand_img = pygame.image.load(r'C:\Users\User\Desktop\game\Game_items\img\Icons\wand.png').convert_alpha()

#button img
potion_img = pygame.image.load(r'C:\Users\User\Desktop\game\Game_items\img\Icons\potion.png').convert_alpha()

#create funtion for drawing text
def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(img,(x,y))



#function for drawing background
def draw_bg(): 
    screen.blit(background_img,(0,0))


#function for drawing panel
def draw_panel():
    screen.blit(panel_img,(0,screen_height - bottom_panel))
    #show knights stats
    draw_text(f'{Wizard.name} HP: {Wizard.hp}' , font , red, 100 , screen_height - bottom_panel + 10)

    for count,i in enumerate(Bandits_list):
        #show me the health
        draw_text(f'{i.name} HP: {i.hp}' , font , red, 550 , (screen_height - bottom_panel + 10)+ count * 60)
    




#fighter class
class Fighter():
    
    def __init__(self,x,y,name,max_hp,strength,potions):
        
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_portions = potions
        self.potions = potions
        self.alive = True
        self.animation_list=[]  #Animation
        self.frame_index = 0
        self.action=0 #0-Idle , 1-attack , 2-Hurt, 3 - dead
        self.update_time=pygame.time.get_ticks()

        #load idle images
        temp_list=[]
        for i in range(8): #range =0,1,2,3,4,5,6,7
            img = pygame.image.load(f'C:/Users/User/Downloads/Battle-main/Battle-main/img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3)) #scaling 
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load attack images
        temp_list=[]
        for i in range(8): #range =0,1,2,3,4,5,6,7
            img = pygame.image.load(f'C:/Users/User/Downloads/Battle-main/Battle-main/img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3)) #scaling 
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image= self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        
        self.rect.center = (x, 200)


    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image=self.animation_list[self.action][self.frame_index]

        #check if enough time is passed after the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1   

        #if animation has run out then reset
        if self.frame_index >=len(self.animation_list[self.action]):
           
            self.idle()


    def idle(self):
        #set varianbles to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()





    #define attack (attack happens here)
    def attack(self,target):
        #deal damage to enemy
        rand = random.randint(-5,5)
        damage= self.strength + rand
        target.hp -= damage
        #check if target is died
        if target.hp < 1:
            target.hp =0
            target.alive = False
        #damage text
        damage_text=DamageText(target.rect.centerx, target.rect.y,str(damage),red)
        damage_text_group.add(damage_text)

        #set varianbles to attack animation
        self.action =1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()





    def draw(self):
        screen.blit(self.image,self.rect)


#Healthbar class
class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp=max_hp



    def draw(self,hp):
        #update new health
        self.hp=hp
        #calculate health ratio
        ratio = self.hp/self.max_hp
        pygame.draw.rect(screen,red,(self.x,self.y,150,20))
        pygame.draw.rect(screen,green,(self.x,self.y,150 * ratio,20))
    
#class damage to show how much damage the character has taken

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,colour):
        pygame.sprite.Sprite.__init__(self) #precoded
        self.image=font.render(damage,True,colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter=0


    def update(self):
        #move up
        self.rect.y-=1
        #delete the text after few sec
        self.counter+=1
        if self.counter >30:
            self.kill()





#sprite group
damage_text_group = pygame.sprite.Group()





#Hero
Wizard = Fighter(200, 360, 'Wizard', 300, 20, 3)

#Bandit
Bandit1= Fighter(400,270,'Bandit',200,6,1)
Bandit2=Fighter(600,270,'Bandit',200,6,1)
Bandits_list=[Bandit1,Bandit2]

#healthbar
Knight_health_bar = HealthBar(100,screen_height - bottom_panel + 40,Wizard.hp,Wizard.max_hp)
Bandit1_health_bar = HealthBar(550,screen_height - bottom_panel + 40,Bandit1.hp,Bandit1.max_hp)
Bandit2_health_bar = HealthBar(550,screen_height - bottom_panel + 100,Bandit2.hp,Bandit2.max_hp)        






run = True

while run:

    clock.tick(fps)
    #draw background

    draw_bg()


    #draw panel
    draw_panel()
    Knight_health_bar.draw(Wizard.hp)
    Bandit1_health_bar.draw(Bandit1.hp)
    Bandit2_health_bar.draw(Bandit2.hp)

    #draw figther
    Wizard.update()
    Wizard.draw()
   
    #DRAW BANDIT
    for Bandits in Bandits_list:
        Bandits.update()
        Bandits.draw()

    #draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)



    
    #reset action variables
        
    #control player action

    attack =False
    potion = False
    target = None

    #make sure mouse is visible

    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, Bandit in enumerate(Bandits_list):
        if Bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show wand in plaace of mouse
            screen.blit(wand_img , pos)
            if clicked ==True:
                attack = True
                target=Bandits_list[count]



    #player action
    if Wizard.alive == True:
        if current_fighter ==1:
            action_cooldown+=1
            if action_cooldown >= action_wait_time:
                #look for player action
                #attack
                if attack == True and target != None:   
                    Wizard.attack(target)
                    current_fighter +=1
                    action_cooldown =0



    #enemy action
    for count,Bandit in enumerate(Bandits_list): #0:Bandit1, 1:bBandit2
        if current_fighter == 2 + count:
            if Bandit.alive == True:
                    action_cooldown +=1
                    if action_cooldown >=action_wait_time:
                        #attack
                        Bandit.attack(Wizard)
                        current_fighter +=1
                        acion_cooldown = 0

            else:
                    current_fighter += 1

    #if all fighters have had a turn then reset
    if current_fighter > total_fighters:
        current_fighter=1
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            clicked =True
        else:
            clicked = False

        pygame.display.update()


    
pygame.quit()
