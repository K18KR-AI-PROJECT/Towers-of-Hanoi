import pygame, sys, time

pygame.init()  # to initialize all the imported pygame modules 
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))  
clock = pygame.time.Clock()  #updating speed is fixed in case of any changes occur in the program

game_done = False
framerate = 60  # clock argument

# game vars:
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0
x=0
# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196) 
grey = (170, 170, 170)
green = (77, 206, 145)

def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)     # already loaded and needs to be reused many times
    font_surface = font.render(text, aa, color)         
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop #midtop is for positiom
    screen.blit(font_surface, font_rect)                #blitting is like copying of one set of pixels
    									                #to increase the reusability


def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():                 # user inputs
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:            #if q is pressed
                    menu_done = True
                    game_done = True                   #end the game execution
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6                    # maximum no. of disks=6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:       # Quitting from game
                menu_done = True
                game_done = True
        pygame.display.flip()                  # any updte to be visible
        clock.tick(60)                         # updation rate i.e, 60 is frames per seconds 

def game_over(): # game over screen
    global screen, steps
    screen.fill(white)
    min_steps = 2**n_disks-1                 #steps required in optimal solution
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=gold)       # providing the shadow effect in the above line
    blit_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        blit_text(screen, 'You finished in minumum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()           # updates a particular part of screen 
    						        # where as display.update() updates the screen
    time.sleep(2)                   # wait for 2 secs 
    pygame.quit()                   # pygame exit
    sys.exit()                      # console exit

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
        disk['rect'].midtop = (120, ypos)                   #midtop is used for poisitoning the element
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23


def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])                # make the disks
    return

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)] #coordinates are specified here
    pygame.draw.polygon(screen, red, ptr_points)           #make the arrow pointer to indicate the current selected tower
    return

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:  
            over = False
    if over:
        time.sleep(0.2)                   #wait for 0.2seconds
        game_over()

def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()


menu_screen()
make_disks()
# main game loop:
while not game_done:                     # executes unless the game is over
    for event in pygame.event.get():     # event indicates user input via mouse click or keyboard click
        if event.type == pygame.QUIT:            # closing pygame modules
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:     # when in between the game escape is pressed
                reset()
            if event.key == pygame.K_q:          # when Q button on keyboard is pressed
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1)%3   # arrow pointer pointing to which tower
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
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']>disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
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
    pygame.display.flip() #update
    if not floating:
    	check_won()
    clock.tick(framerate)
