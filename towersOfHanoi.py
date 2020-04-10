import pygame, sys, time
import random
from pygame.locals import *
import webbrowser
from playsound import playsound


pygame.init()  # to initialize all the imported pygame modules 
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((650, 650))  
clock = pygame.time.Clock()  

pygame.mixer.music.load('backsound.mp3')
pygame.mixer.music.play(-1)

game_done = False
framerate = 60  

# game vars:
SPACE_PER_PEG = 200
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196) 
grey = (170, 170, 170)
green = (77, 206, 145)
logo_color = (136, 212, 152)
logo_background = (26, 174, 111)
test_menu_back = (254, 219, 39)


def color_generator():
	r = random.randint(0,255)
	g = random.randint(0,255)
	b = random.randint(0,255)
	rgb = (r,g,b)
	return rgb

rgb = color_generator()


def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    
        font = pygame.font.SysFont(font_name, size)     
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop 
    screen.blit(font_surface, font_rect)     									

def hanoi(pegs, start, target, n):
    if n == 1:
        pegs[target].append(pegs[start].pop())
        yield pegs
    else:
        aux = 3 - start - target  # start + target + aux = 3
        for i in hanoi(pegs, start, aux, n-1): yield i
        for i in hanoi(pegs, start, target, 1): yield i
        for i in hanoi(pegs, aux, target, n-1): yield i
            
def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen):
    """
    Given a pile of pegs, displays them on the screen, nicely inpilated
    like in a piramid, the smaller in lighter color.
    """
    for i, pegwidth in enumerate(pegs): 
        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            (255-pegwidth, 255-pegwidth, 255-pegwidth),
            (
              start_x + (SPACE_PER_PEG - pegwidth)/2 , # Handles alignment putting pegs in the middle, like a piramid
              start_y - peg_height * i,                # Pegs are one on top of the other, height depends on iteration
              pegwidth,
              peg_height
            )
        )
        
def visual_hanoi(number_of_pegs, base_width, peg_height, sleeping_interval, msteps):
    """
    Visually shows the process of optimal solution of an tower of hanoi problem.
    """
    pegs = [[i * base_width for i in reversed(range(1, number_of_pegs+1))], [], []]
    positions = hanoi(pegs, 0, 2, number_of_pegs)

    pygame.init()
    screen = pygame.display.set_mode( (650, 650) )
    pygame.display.set_caption('Towers of Hanoi Solution')
    time.sleep(1)
    for position in positions:
        screen.fill(white) 
        msteps+=1
        blit_text(screen, 'Steps: '+str(msteps), (320, 20), font_name='mono', size=30, color=black)
        for i, pile in enumerate(position):
            display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen)
        
        pygame.display.update()
        time.sleep(sleeping_interval)
   

def exitgame():
    pygame.quit()
    sys.exit()
        
global text1, text2, text3, text4
text1 = ''
text2 = ''
text3 = ''
text4 = ''

def text_fun():
    if menu_done == False:
        text1 = 'Towers of Hanoi'
        text2 = 'Towers of Hanoi'
        text3 = 'Use arrow keys to select difficulty:'
        text4 = 'Press ENTER to continue'
        blit_text(screen, text1, (323,192), font_name='sans serif', size=90, color=grey)
        blit_text(screen, text2, (320,190), font_name='sans serif', size=90, color=logo_color)
        blit_text(screen, text3, (320, 290), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 330), font_name='sans serif', size=40, color=blue)
        blit_text(screen, text4, (320, 390), font_name='sans_serif', size=30, color=black)
    


def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done, menu_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop  
        screen.fill(white)
        button('Manual',500,20,120,40,grey,manual_text_color,action='Help',tcolor=white, size=20)
        text_fun()
        button('Visit GitHub',30,20,200,40, grey, manual_text_color,action='Github',tcolor=white, size=20)
        
        for event in pygame.event.get():  #inputs 
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q: #if q is pressed
                    exitgame()
                    '''menu_done = True
                    game_done = True  #end the game execution'''
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 8:
                        n_disks = 8 #isko change krke maximum kitne bolock chahiye hum increase kr skte hai
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 2:
                        n_disks = 2
            if event.type == pygame.QUIT:  #end kr rhe hai window ko yua end kr rhe hai game ko
                menu_done = True
                game_done = True
        pygame.display.flip() #ye wali call is required in order for any updates that you make to the game screen to become visible.
        clock.tick(60)  #60is frames per seconds ki kiss rate pr update hoga
        
def game_over(): # game over screen
    global screen, steps
    screen.fill(white)
    min_steps = 2**n_disks-1 #optimal solution ke liye
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=gold) #do baar islye kyon ki dusra wala pahe wle ke niche hai to shadow wala effect dega
    blit_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        blit_text(screen, 'You finished in minumum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip() #ye flip only ek particular part of screen ke contents ko update krta hai
    						
    time.sleep(4)    
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def draw_towers():
    global screen
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160 , 20))
       
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
        
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)
    
def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)  #midtop is used for poisitoning the element
        disk['val'] = n_disks-i


        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23

        
        disk_number = str(i+1)
        

def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, manual_text_color, disk['rect']) #make the duisk
    return

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)] #coordinates are specified here
    pygame.draw.polygon(screen, red, ptr_points) #make the arrow below the tower used to indicate the current sselcted tower
    return

def textbutton(msg, color, x, y, width, height, size):
    font = pygame.font.SysFont('mono', size)
    text_surf = font.render(msg, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x+(width/2)), y+(height/2))
    screen.blit(text_surf,text_rect)
    
def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()


def webLinker():
    webbrowser.open_new('https://github.com/K18KR-AI-PROJECT/Towers-of-Hanoi')
    exitgame()


def button(text, x, y, width, height, inactive_color, active_color, action=None, tcolor=black, size=27):
    cur=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    #print(click)
    if (x + width > cur[0] > x and y + height > cur[1] > y):
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0]==1 and action!=None:
            if action=='Solution':          # 'Solution' button pressed
                visual_hanoi(number_of_pegs = n_disks,base_width = 30,peg_height = 40,sleeping_interval = 0.7,msteps=0)
                pygame.display.set_caption('Towers of Hanoi')
                
            if action=='Menu':              # 'Menu' button pressed
                reset()
                
            if action=='Help':
                manual_page()
                pygame.display.set_caption('Towers of Hanoi')
                
            if action == 'Github':
                webLinker()

            if action == 'Mainmenu':
                menu_screen()
                
                
                
            '''if action=='Quit':           # 'Quit' button pressed
                exitgame()'''
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    textbutton(text, tcolor, x, y, width, height, size)          # write text on button
    

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:  
            over = False
    if over:
        time.sleep(0.2)  #wait for 0.2seconds
        game_over()

manual_text_color = (153, 185, 152)
manual_text_color2 = (253, 206, 170)
manual_background_color = (39, 54, 59)

def manual_page():
    pygame.init()
    screen = pygame.display.set_mode((650,650)) 
    screen.fill(manual_background_color)
    pygame.display.set_caption('Manual')
    blit_text(screen, ' INSTRUCTIONS :)', (323,100), font_name='sans serif', size=50, color=manual_text_color)
    blit_text(screen, 'a. Use Up arrow key to increase number of blocks and Down arrow to do opposite', (320, 200), font_name='sans serif', size=23, color=manual_text_color)
    blit_text(screen, 'b. Use Arrows on keyboard to move the disks', (320, 247), font_name='sans serif', size=23, color=manual_text_color)
    blit_text(screen, 'c. Only one disk can be moved at a time', (320, 287), font_name='sans serif', size=23, color=manual_text_color)
    blit_text(screen, 'd. No bigger disk can be placed on top of the smaller disk', (320, 327), font_name='sans serif', size=23, color=manual_text_color)
    blit_text(screen, 'e. Press Q to Quit the game', (320, 367), font_name='sans serif', size=23, color=manual_text_color)
    blit_text(screen, 'f. Press ESC to head to Game Menu', (320, 407), font_name='sans serif', size=23, color=manual_text_color)
    #button('< Go back to menu',27,550,240,40,grey,manual_text_color,action='Mainenu',tcolor=white, size = 20)
    pygame.display.update()
    time.sleep(6)
    
 



#manual_page()
menu_screen()
make_disks()
# main game loop:
while not game_done:   #by default game done is set to false so not gamedone means true
    for event in pygame.event.get():     #event indicates kya perform ho rha hai it can be mouse click or keyboard click
        if event.type == pygame.QUIT:  #pygame ke modules ko jab clode kr rhe hai
            exitgame()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #when in between the game escape is pressed
                reset()
            if event.key == pygame.K_q:  #whrn Q button on keyboard is pressed
                exitgame()
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1)%3  #axis me move krte samay right side is positive and leftside is negative wrt to any point
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at-1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        #playsound('right.mp3')
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']>disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                            #playsound('right.mp3')
                        else:
                            #blit_text(screen, 'Illegal Move!!', (323,192), font_name='sans serif', size=90, color=red)
                            print("Illegal move!!!")
                            
                            playsound('sound.mp3')
                            #pygame.mixer.music.load('sound.mp3')
                            #pygame.mixer.music.play(0)
                            

                            #print(disks[floater]['rect'].midtop )
                            #print(disk['val'])
                            #print(disks[floater]['val'])
                        break
                else: 
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1

    screen.fill(white) #background color
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    button('< Go back to menu',27,550,240,40,grey,manual_text_color,action='Menu',tcolor=white, size = 20)
    button('Solution',465,550,150,40,grey,manual_text_color,action='Solution', size = 20,tcolor=white)
    button('Manual',500,20,120,40,grey,manual_text_color,action='Help', tcolor=white, size=20)
    #button('Visit GitHub',30,20,200,40, grey, manual_text_color,action='Github',tcolor=white, size=20)
    #button('Quit',520,20,110,40,grey,red,action='Exit')
    pygame.display.flip()     # update
    if not floating:check_won()
    clock.tick(framerate)
exitgame()
