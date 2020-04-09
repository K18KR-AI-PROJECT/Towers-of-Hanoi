import pygame, sys, time
import webbrowser
from tkinter import *
from tkinter import font

#from playsound import playsound


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
        
def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop  
        screen.fill(white)
        button('Help',550,20,70,30,blue, grey,action='Help',tcolor=white, size=20)
        blit_text(screen, 'Towers of Hanoi', (323,192), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320,190), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 290), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 330), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 390), font_name='sans_serif', size=30, color=black)
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
                    if n_disks > 6:
                        n_disks = 6 #isko change krke maximum kitne bolock chahiye hum increase kr skte hai
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
    						
    time.sleep(2)    
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def draw_towers():
    global screen
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160 , 20))
        #print(xpos)
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
        #print(xpos)
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    #print(towers_midx[0])
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

       # print(disk['val'])

        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23

        #print(ypos)
        disk_number = str(i+1)
        #print("Cordinate of disk " + disk_number)
        #print(disk['rect'].midtop)
        #print(xpos)

def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect']) #make the duisk
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
                pass
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
                            #playsound('sound.mp3')
                            pygame.mixer.music.load('sound.mp3')
                            pygame.mixer.music.play(0)
                            

                            #print(disks[floater]['rect'].midtop )
                            #print(disk['val'])
                            #print(disks[floater]['val'])
                        break
                else: 
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1

    screen.fill(white) #backgroud color
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    button('Menu',20,550,110,50,grey,gold,action='Menu')
    button('Solution',480,550,140,50,grey,red,action='Solution')
    button('Help',550,20,70,30,blue,grey,action='Help', tcolor=white, size=20)
    #button('Quit',520,20,110,40,grey,red,action='Exit')
    pygame.display.flip()     # update
    if not floating:check_won()
    clock.tick(framerate)
exitgame()


'''
def SolTowerOfHanoi(n , from_rod, to_rod, aux_rod): 
    if n == 1: 
        temp = "Move disk 1 from rod " + from_rod + " to rod " + to_rod + "\n"
        textbox.insert(END, temp) 
        return
    SolTowerOfHanoi(n-1, from_rod, aux_rod, to_rod) 
    temp2 = "Move disk " + str(n) + " from rod " + from_rod + " to rod " + to_rod + '\n'
    textbox.insert(END, temp2) 
    SolTowerOfHanoi(n-1, aux_rod, to_rod, from_rod) 

n = n_disks   
root = Tk()

textbox = Text(root)
textbox.pack()

root.geometry("640x445+80+110")
root.configure(background = 'white')
root.title("Solution")
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Divyanisha - 11810030")
filemenu.add_command(label="Priya - 11810037")
filemenu.add_command(label="Sushil - 11809930")
filemenu.add_command(label="Rishabh - 11811114")

menubar.add_cascade(label="About Us", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

url = 'https://github.com/K18KR-AI-PROJECT/Towers-of-Hanoi'
def OpenUrl():
    webbrowser.open_new(url)

editmenu.add_command(label="Visit GitHub repository", command=OpenUrl )
editmenu.add_separator()
editmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Help", menu=editmenu)
root.config(menu=menubar)

helv36 = font.Font(family='Helvetica', size=15, weight='normal')
button_1 = Button(width = 610,font=helv36,text = "Solution for " + str(n) +" disks" ,command=SolTowerOfHanoi(n, 'A', 'C', 'B'))
button_1.pack()


root.mainloop()'''
