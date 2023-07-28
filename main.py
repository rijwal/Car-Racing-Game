#importing the neccasary modules for this project, the time function allows us to handle various operations 
import pygame
import math
pygame.font.init()

#the scale image which allows for the game to change the size of the pngs in  order to fit with the game screen/window size
def scaleimage(assets, factor):
    sz = round(assets.get_width() * factor), round(assets.get_height() * factor)
    return pygame.transform.scale(assets, sz)

#this code was used from stack overflow.  this code is that if we were to rotate the image, there would be distortions. the code below fixes this
def blit_rotate_center(window, image, top_left, angle): 
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center) #rotating the image but not altering the x and y posititons on the screen, only roating from the center of the image rather than the top left
    window.blit(rotated_image, new_rect.topleft) #blitting the image on the window

#defining and importing the images/assets used in this project, scaling the image to fit the window perfectly
grass = scaleimage(pygame.image.load("assets/grass.png"), 40)
purplecar = scaleimage(pygame.image.load("assets/car2.png"), 1.5)
finishline = pygame.image.load("assets/finish.png")
finish_mask = pygame.mask.from_surface(finishline)
finishline_position = (30,300)
trackborder = scaleimage(pygame.image.load("assets/track-borderz.png"), 0.9)
trackborder_mask = pygame.mask.from_surface(trackborder)
track = scaleimage(pygame.image.load("assets/track.png"),0.9)
Lscreen = scaleimage(pygame.image.load("assets/loading screen.png"), 15)
text = pygame.image.load("assets/text_loadingscreen.png")
font = pygame.font.SysFont("comicsans", 40)
end = scaleimage(pygame.image.load("assets/backgroundend.png"), 0.9)

#setting up a display surface/screen 
w, h = track.get_width(), track.get_height() #using information from the track in order to make the screen size proportionate
window = pygame.display.set_mode((w, h)) #setting the window size as the tracks width and height
pygame.display.set_caption("Car Racing Game! by: Rijwal Sangey") #setting a caption

#setting up frames per second so that it is similar for every single player and it doesn't depend on processor speed
fps = 45

class Scar: #defining a class which will allow for me to inherit from this class into another class (easy method to reduce lines of code)
    IMG = purplecar #using purple car in my image
    def __init__(me, max_velocity, rotation_velocity): #defining the velocity section
        me.img = me.IMG
        me.acceleration = 0.1 #every time the "w" key is pressed, the acceleration increases by 0.1
        me.max_velocity = max_velocity
        me.velocity = 0 #this is because the car should not be moving when the game runs
        me.rotation_velocity = rotation_velocity
        me.angle = 0 #there is no angle set because we only need angles when we are starting up the game, the car should be facing upwards and be 180 degrees
        me.x, me.y = me.START_POS #the x and y will corresprond to the starting position indicating the starting position

    def rotate(me, right=False, left=False): #allows to rotate the car depending on direction turned
            if left: 
                me.angle += me.rotation_velocity #angle increases when turning left
            elif right: 
                me.angle -= me.rotation_velocity #angle decreases turning right
                #note: used guess and check to figure out whether the angle increases or decreases going left and right, at first my turn was inversed.
    def draw(me, win):  
        blit_rotate_center(win, me.img, (me.x, me.y), me.angle)

    def move(me): #trig used in order to move the car (code idea used from stackoverflow)
        r = math.radians(me.angle) #changing to radians because radian is used in computer math
        horizontal = math.sin(r) * me.velocity 
        vertical = math.cos(r) * me.velocity
        me.y -= vertical
        me.x -= horizontal

    def collision(me, mask, x = 0, y = 0): #defining the collison in order to makw sure that the 
       car_mask = pygame.mask.from_surface(me.img)
       offset = (int(me.x - x), int(me.y - y)) #take the x and y values at which we are at and subtract the other masks x and y value from it
       point_of_intersection = mask.overlap(car_mask, offset) #
       return point_of_intersection

    def forwardmove(me): #allowing for the car to move forward
        me.velocity = min(me.velocity + me.acceleration, me.max_velocity)
        me.move()

#allows for keys to be used in order to move the car
    def moveplayer(me): 
        keys = pygame.key.get_pressed() #sees what happens if each key is clicked (turning left and right)
        if keys[pygame.K_RIGHT]: # turns right using arrow key
            me.rotate(right = True)

        if keys[pygame.K_LEFT]: # turns left using arrow key
            me.rotate(left = True)

        if keys[pygame.K_UP]: # goes forward using arrow key
            me.forwardmove()

class PLAYERcar(Scar): #inheriting the class "Scar"
    IMG = purplecar
    START_POS = (30, 240) #decides coordinates of the car in order for it to start

    def bounce(me):
        me.velocity = -me.velocity * 0.8 #makes the bounce which is used when the car hits an obstacle the same amount * 0.8 as the velocity exerted on the wall or tire
        me.move()

#defining the draw function and allowing for the images/assets (background and track) to print on the window at certain positions which are based on coordinates
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
 
    player_car.draw(win) #draws car in window
   
clock = pygame.time.Clock()
images = [(grass,(0,0)), (track, (0,0)), (finishline, (25,300)), (trackborder, (0,0))] #instructing the position of the image
player_car = PLAYERcar(4, 4) #referring to the speed of car

def player_loop(offset): #offset is used to track amount of time in the 
    run = True
    while run:
        clock.tick(fps) #sets the fps while running
        draw(window, images, player_car) #draws the two basic assets (background and the track)

#allowing for the window to stay open unless closed by user which ultimately quits the application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player_car.moveplayer()
       
        if player_car.collision(trackborder_mask) !=None: #allows for the car to bounce off after colliding with the tire or the border 
           player_car.bounce() #makes the car bounce back

        finishline_poi_collision = player_car.collision(finish_mask, *finishline_position) #the asterick is the coordinates
        if finishline_poi_collision != None:
            if finishline_poi_collision[1] == 0:
                player_car.bounce() #bounces back if the player goes in the wrong direction (turns around and passes finish line)
            else:
                finishtime = round(pygame.time.get_ticks()/1000) - offset
                end_loop(finishtime) 

        current_time = round((pygame.time.get_ticks()/1000) - offset, 3) #timer which states time taken rounded 
        time_text = font.render(f"{current_time}", False, (255, 255, 255)) #color of background
        window.blit(time_text, (30, 700)) #where the timer is placed

#updates the screen to display the assets added in the previous code
        pygame.display.update()


#this loop  is used for when the user passes the finishline and their time is taken and printed on the screen alongside a background. The game is offcially over after this. 
def end_loop(current_time):
    run = True
    while run:
        clock.tick(fps) #sets the fps while running
        window.fill((200,200,200))
        window.blit(end, (0,0)) #background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 
        time_text = font.render(f"You finished a lap, your time was: {round(current_time)} seconds!", False, (0, 0, 255)) #final text on screen
        window.blit(time_text, (100, 400)) #positioning


    #updates the screen to display the assets added in the previous code
        pygame.display.update()

def start_loop(): #this loop is used in for the loading screen, it sets the background and text (game title) and for event in the user clicking, the screen closes and opens the game
    run = True
    while run:
        clock.tick(fps) #sets the fps while running
        window.blit(Lscreen, (0,0)) #prints the background
        window.blit(text, (0,0)) #prints the text
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() #quits start screen and goes to main game
        if pygame.mouse.get_pressed()[0]== 1: #allows for anywhere on the mouse to be clicked
            click_time = pygame.time.get_ticks()/1000 #clock on screen
            player_loop(click_time) 
    #updates the screen to display the assets added in the previous code
        pygame.display.update()

start_loop()





