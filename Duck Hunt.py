import pygame

pygame.init()

windowwidth = 600
windowheight = 500
displaysurf = pygame.display.set_mode((windowwidth,windowheight))
master_sheet = pygame.image.load('SpriteSheet.png').convert()
master_sheet.set_colorkey((255,0,255))
foreground = pygame.transform.scale(master_sheet.subsurface(0,237,300,250), (windowwidth, windowheight))

duck_wingup = pygame.image.load('Duck.png')
duck_wingdown = pygame.image.load('Duck_Wingdown.png')


BGCol = (0,128,255)

pygame.display.set_caption('Py Hunt')
fps = 60
fpsclock = pygame.time.Clock()
bullet = pygame.image.load('bullet.png')
dog = pygame.image.load('Dog.png')
duck_dead = pygame.image.load('Duck_Dead.png')
duck_shot = pygame.image.load('Duck_Shot.png')
dog_sheet = pygame.image.load('DogSheet.png')





def main():
    running = True
    mousex = 0
    mousey = 0
    #leftmouseclicked = False
    rounds_left = 10
    global duckx
    duckx = 300
    global ducky
    ducky = 300
    duckx_mult = -1
    ducky_mult = -1
    ducks_killed = 0
    level = 1
    licznik = 0
    chances = 3
    gameStartAnim()
    while running:
        if level == 1:
            duck_speed = 2
        else:
            duck_speed = 1 * level + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            #if event.type = pygame.MOUSEMOTION:
            #    mousex, mousey = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousex, mousey = event.pos
                #leftmouseclicked = True
                if rounds_left >= 0:
                    shotsfired(mousex, mousey)
                    rounds_left -= 1
                if rounds_left <= 0:
                    pass

                if shotsfired(mousex, mousey) == True and rounds_left > 0 and (duckx_mult != 0):
                    ducks_killed += 1
                    duckKillAnim(duckx, ducky)
                    duckx = 300
                    ducky = 300
                    duckx_mult = -1
                    ducky_mult = -1
                    licznik = 0
                    if ducks_killed % 10 == 0 and ducks_killed > 0:
                        level += 1




            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                rounds_left = 10

        if duckx <= 0 or duckx >= 568:
            duckx_mult = duckx_mult*(-1)
        if ducky <= 0 or ducky >= 350:
            ducky_mult = ducky_mult*(-1)
        duckx = duckx + (duck_speed*duckx_mult)
        ducky = ducky + (duck_speed*ducky_mult)

        displaysurf.fill(BGCol)
        if licznik%7 == 0:
            duck = duck_wingdown
        if licznik%15 == 0:
            duck = duck_wingup
        if duckx_mult == 1:
            displaysurf.blit(duck, (duckx, ducky))
        if duckx_mult == -1:
            displaysurf.blit(pygame.transform.flip(duck, True, False), (duckx, ducky))
        displaysurf.blit(foreground, (0, 0))
        for rnd in range(rounds_left):
            displaysurf.blit(bullet, (25*rnd + 4, 420))
        pygame.display.update()
        fpsclock.tick(fps)

        licznik += 1
        if licznik >= 600:
            roundlost(duckx, ducky, chances)
            licznik = 0
            duckx = 300
            ducky = 300
            duckx_mult = -1
            ducky_mult = -1
            chances -= 1
        if chances <= 0:
            gameOver()
        print(ducks_killed, rounds_left, level, duck_speed, licznik, duck, chances, fpsclock.get_fps())
    pygame.quit()

def shotsfired(x,y):
        if x in range(duckx, duckx+60) and y in range(ducky, ducky+69):
            return True
        else:
            return False
def duckKillAnim(x, y):
    dog_x = 256
    dog_y = 450

    displaysurf.fill(BGCol)
    displaysurf.blit(duck_shot, (x, y))
    displaysurf.blit(foreground, (0,0))
    pygame.display.update()
    pygame.time.wait(750)
    while y < 400:
        y = y + 0.33
        displaysurf.fill(BGCol)
        displaysurf.blit(duck_dead, (x, y))
        displaysurf.blit(foreground, (0,0))
        pygame.display.update()
    while dog_y > 220:
        dog_y -= 0.25
        displaysurf.fill(BGCol)
        displaysurf.blit(dog, (dog_x, dog_y))
        displaysurf.blit(foreground, (0, 0))
        pygame.display.update()
    pygame.time.wait(250)
    while dog_y < 500:
        dog_y += 0.25
        displaysurf.fill(BGCol)
        displaysurf.blit(dog, (dog_x, dog_y))
        displaysurf.blit(foreground, (0, 0))
        pygame.display.update()
    pygame.time.wait(500)
def roundlost(x, y, lives):
    i = 0
    d = None
    while x < 610:

        displaysurf.fill(BGCol)
        if i%7 == 0:
            d = duck_wingup
        if i%15 == 0:
            d = duck_wingdown
        x += 4
        displaysurf.blit(d, (x,y))
        displaysurf.blit(foreground, (0,0))
        pygame.display.update()
        fpsclock.tick(fps)
        i += 1
    lives -= 1

    return lives

def gameOver():
    pygame.quit()


def spriteSheetCutter(spritesheet, sprite_w, sprite_h, locx, locy, iter_x, iter_y):
    frames = []
    for i in range (0, iter_y):
        for n in range(0, iter_x):
            frames.append(spritesheet.subsurface(locx+(n*sprite_w), locy+(i*sprite_h), sprite_w, sprite_h))
    return frames

def gameStartAnim():
    start_frames = spriteSheetCutter(master_sheet, 110, 79, 0, 0, 5 ,2)
    start_frames = start_frames[:-2]
    frame_iterator = 0

    anim_running = True
    counter = 0
    x, y = 0, 350
    while anim_running:
        current_frame = start_frames[frame_iterator % 5]
        counter += 1
        if counter%30 == 0 and counter != 0:
            frame_iterator += 1
        if frame_iterator == 5:
            jumping = True
            while jumping:
                displaysurf.fill(BGCol)
                displaysurf.blit(foreground, (0, 0))
                displaysurf.blit(start_frames[5], (x, y))
                pygame.display.update()
                fpsclock.tick(fps)
                pygame.time.wait(500)
                jumping = False
            while True:
                x += 2
                y -= 2
                displaysurf.fill(BGCol)
                displaysurf.blit(foreground, (0, 0))
                displaysurf.blit(start_frames[6], (x, y))
                pygame.display.update()
                fpsclock.tick(fps)
                if y <= 220:
                    break
            while True:
                x += 2
                y += 2
                displaysurf.fill(BGCol)
                displaysurf.blit(start_frames[7], (x, y))
                displaysurf.blit(foreground, (0, 0))
                pygame.display.update()
                fpsclock.tick(fps)
                if y >= 360:
                    break
            anim_running = False
        displaysurf.fill(BGCol)
        displaysurf.blit(foreground, (0,0))
        displaysurf.blit(current_frame, (x,y))
        x += 1

        pygame.display.update()
        fpsclock.tick(fps)
        print(frame_iterator)
def sheettest(frames):
    while True:
        displaysurf.fill(BGCol)
        displaysurf.blit(foreground, (0,0))
        for i in range(len(frames)):
            displaysurf.blit(frames[i],(110*i + 5, 0))
        pygame.display.update()
        fpsclock.tick(fps)

#sheettest(spriteSheetCutter(master_sheet, 110, 79, 0, 0, 5, 2))
#sheettest(dogSpriteSheet())

if __name__ == '__main__':
    main()