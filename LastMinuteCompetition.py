from numpy import *
from numpy.linalg import solve, norm
import numpy as np
import math
import pygame as pg
import os
import time

#Made by Sasho Ivanov (4681657)


def intersect(a,b,p,q):                                         #defining some functions most of them from the bouncing assignment
    a, b, p, q = list(a), list(b), list(p), list(q)             #It may look strange that we put all to list and then to array again, but
                                                                #we were getting a float converted to a int when assigning to an array entry
    a[0] = a[0]*8/xmax
    a[1] = (ymax - a[1])*8/ymax
    
    b[0] = b[0]*8/xmax
    b[1] = (ymax - b[1])*8/ymax
    a, b, p, q = np.array(a), np.array(b), np.array(p), np.array(q)
    
    A = np.matrix([ [ b[0] - a[0] , p[0] - q[0] ] , [ b[1] - a[1] , p[1] - q[1] ] ])
    c = np.matrix([ [p[0] - a[0]] , [ p[1] - a[1]] ])
    sol = (A.I)*c
    
    lam, mu = sol[0,0], sol[1, 0]
    
    s = a + lam * (b - a)

    if 0<= lam <= 1 and 0<= mu <= 1:
        pass
    else:
        s = None
    
    return lam, mu, s


def mirrorv(a, b, p, q, v, s):
    a, b, p, q = list(a), list(b), list(p), list(q)
    
    
    a[0] = a[0]*8/xmax
    a[1] = (ymax - a[1])*8/ymax
    
    b[0] = b[0]*8/xmax
    b[1] = (ymax - b[1])*8/ymax
    a, b, p, q = np.array(a), np.array(b), np.array(p), np.array(q)


    e = b - a
    h = q - p
    n = np.array( [ e[1] , -e[0] ] )
    
    if n.dot(h) >= 0:
        n = np.array( [ -e[1] ,e[0] ] )
    
    n = n / norm(n)
    r = q
    vnew = v
    if s is not None:
        qr = abs(2 * (q - s).dot(n))
        QR = qr*n
        r = q + QR
    
        dv = 2*(norm(v.dot(n)))*n
        vnew = v + dv
    
    return r, vnew
def points(rect):                       # this function gives us the coordinates of all the points in an rect
                                        # and it groups them together to be easy to create vectors to test for bouncing
    points = []

    for i in range(4):
        points.append(2*[0])
    
    points[0][0] = rect.topleft
    points[0][1] = rect.topright
    points[1][0] = rect.topleft
    points[1][1] = rect.bottomleft
    points[2][0] = rect.bottomleft
    points[2][1] = rect.bottomright
    points[3][0] = rect.topright
    points[3][1] = rect.bottomright

    return points
def remove(platforms):                  # this removes entries from the list of platforms when they are out of the screen
                                        # this helps with impoving performance as the program checks for every entry in the 
    platforms = list(set(platforms))    # platforms and obstacles all 4 sides and it slows down the program a lot (can be seen if you place a lot of platforms)
    if len(platforms) > 1:              # sometimes the ball goes inside the obstacles, the problem may be that the for loops are too slow and dont have enough time to go thought all the entries, but that is rare.
        var = list(platforms[0])
        if var[1] > 800:
            del platforms[0]
    return platforms

    
    
black = (0 ,0 ,0)
white = (255,255,255)
orange  = (255,165,0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "350,40"    #puts the screen more to the center when run

pg.init()
xmax = 800
ymax = 750
xbox = 650

scr = pg.display.set_mode((xmax,ymax))

ballpic = pg.image.load("ball1.gif")        #some pygame image loading and getting rects
platform = pg.image.load("platform.png")
backround = pg.image.load("Bckrnd.png")
backround2 = pg.image.load("BckrndFlipped.png")
bblack = pg.image.load("black.gif")
bblack2 = pg.image.load("black2.png")
obstacle = pg.image.load("obstacle.png")
bonus = pg.image.load("bonus.gif")
start = pg.image.load("start.gif")


ballrect = ballpic.get_rect()
prect = platform.get_rect()
backrect = backround.get_rect()
obsrect = obstacle.get_rect()
bonusrect = bonus.get_rect()
backrect2 = backround2.get_rect()
backrect2.left = 650
bblackrect = bblack.get_rect()
startrect = start.get_rect()






num = 0                                         #here some variables and list needed are defined
yb = 800
count = 0
score = 0
startnum = 10
platforms = []
obstacles = []
bonusplat = []
future = time.time()
running = False
startscr = True
obswait = 1
obsgo = 0


while startscr:                         #start screen
    pg.event.pump()
    keys = pg.key.get_pressed()
    scr.blit(start, startrect)

    pg.display.flip()
    
    if keys[pg.K_SPACE]:
        startscr = False
        running = True

        t = pg.time.get_ticks()*0.001


        p, q, = np.array([3, 6]), np.array([1, 2])      #here we define the speed magnitude and convert it to pixels
        v = (q - p)/0.1                                 #we choose to divide the screen into 8x8 coordinate system thats why we divide by 8
        x = p[0]/8*xmax                                 #and convert back and forward
        y = ymax - p[1]/8*ymax
        vx = v[0]/80*xmax
        vy =  - v[1]/80*ymax

while running:

    pg.event.pump()
    
    t0 = t
    t = pg.time.get_ticks()*0.001
    dt = t - t0

    x = x + vx*dt
    y = y + vy*dt

    if x>xbox:                                      #bouncing of the edges and end game
        vx = -vx                                    #playfield is smaller than screen 
        x = xbox - (x - xbox) 
    elif x<150:
        vx = -vx
        x = 151
        
    if y>ymax:
        print("You lost\nYour score is: %s" % score)
        running = False
        
    
    
    scr.fill(black)
    
    bblackrect.left = 150
    scr.blit(bblack, bblackrect)
    
    p = np.array([x/xmax*8 , (ymax-y)*8/ymax])                  #more converting
    q = np.array([(x+vx*10)/xmax*8,(ymax-(y+vy*10))*8/ymax])
    v = np.array([vx*80/xmax, -vy*80/ymax])

    
    if pg.mouse.get_pressed()[0] == 0:                  #this portion builds platforms on mouse click
        flag = True
    if flag:
        
        if pg.mouse.get_pressed()[0] == 1:
            prect.center = pg.mouse.get_pos()
            if prect.collidepoint((x,y)) == False:       #addded this because sometimes ball gets stuck in platform if the ball is in the platform rect
                flag = False
             
                pos = pg.mouse.get_pos()
                posx = list(pos)
                if 150 < posx[0] < 650 and startnum >0:
                
                    platforms.append(pos)
                    startnum = startnum -1


    if obsgo<(obswait-200):                     #this is for the random generation of obstacles and bonus drops
        seed = random.randint(0,50)

        if seed % 50 == 0:
            obsgo = obswait
            seed = random.randint(1,35)
            poso = (seed*10+225,-100)
            obstacles.append(poso)
        seed2 = random.randint(0,400)

        if seed2 % 400 == 0 :
            obsgo = obswait
            seed = random.randint(1,35)
            posb = (seed*10+225,-100)
            bonusplat.append(posb)

            
           

    
    platforms = remove(platforms)
    obstacles = remove(obstacles)
    bonusplat = remove(bonusplat)

    
    
    if y>300:                                           #when the y is above 300 (possitive down) the screen is static   
        for i in platforms:                             #here bouncing is checked for everything
            prect.center = i
            scr.blit(platform, prect)
            
            
            for j in points(prect):
                
                lam, mu, s = intersect(j[0],j[1],p,q)
                r, vnew = mirrorv(j[0],j[1],p,q,v,s)
                
                if s is not None and abs(s[0]/8*xmax - x )< 5 and abs(ymax-s[1]/8*ymax - y) < 5 :

                    vx = vnew[0]/80*xmax
                    vy = - vnew[1]/80*ymax
        for k in obstacles:
            obsrect.center = k
            scr.blit(obstacle, obsrect)

            for j in points(obsrect):
                
                lam, mu, s = intersect(j[0],j[1],p,q)
                r, vnew = mirrorv(j[0],j[1],p,q,v,s)
                
                if s is not None and abs(s[0]/8*xmax - x )< 5 and abs(ymax-s[1]/8*ymax - y) < 5 :

                    vx = vnew[0]/80*xmax
                    vy = - vnew[1]/80*ymax
        for m in range(len(bonusplat)):
            varbon = list(bonusplat[m])
            bonusrect.center = varbon[0], varbon[1]
            scr.blit(bonus, bonusrect)

            if bonusrect.collidepoint((x,y)):
                startnum = startnum + 5
                score = score + 1
                bonusplat[m] = (varbon[0], 900)
                

    if y <= 300:                                        #to create the illusion of going up we need to move stuff down
                                                        #when y is smaller than 300 it feels like the ball is going up and bouncing is checked also
            
        for i in range(len(platforms)):
            var = list(platforms[i])
            platforms[i] = var[0], var[1] + abs(vy)/150


            prect.center = platforms[i]
            scr.blit(platform, prect)
            
            
            
            for j in points(prect):
                
                lam, mu, s = intersect(j[0],j[1],p,q)
                r, vnew = mirrorv(j[0],j[1],p,q,v,s)
                
                if s is not None and abs(s[0]/8*xmax - x )< 5 and abs(ymax-s[1]/8*ymax - y) < 5 :

                    vx = vnew[0]/80*xmax
                    vy = - vnew[1]/80*ymax
        



        for k in range(len(obstacles)):
            varo = list(obstacles[k])
            obstacles[k] = varo[0], varo[1] +abs(vy)/150

            obsrect.center = obstacles[k]
            scr.blit(obstacle, obsrect)

            for j in points(obsrect):
                
                lam, mu, s = intersect(j[0],j[1],p,q)
                r, vnew = mirrorv(j[0],j[1],p,q,v,s)
                
                if s is not None and abs(s[0]/8*xmax - x )< 5 and abs(ymax-s[1]/8*ymax - y) < 5 :

                    vx = vnew[0]/80*xmax
                    vy = - vnew[1]/80*ymax
        for m in range(len(bonusplat)):

            varb = list(bonusplat[m])
            bonusplat[m] = varb[0], varb[1] + abs(vy)/150
            bonusrect.center = bonusplat[m]
            scr.blit(bonus ,bonusrect)

            if bonusrect.collidepoint((x,y)):
                startnum = startnum + 5
                score = score + 1
                bonusplat[m] = (varb[0], 900)           #putting coordinates outside of screen
                                                        #to be deleted by remove fuction we defined
        
        y = 300


    dy = yb % backround.get_height()                        # here the backround is moved down
    scr.blit(backround, (0,dy - backround.get_height()))
    scr.blit(backround2, (650,dy - backround.get_height()))
    if dy < yb :
        scr.blit(backround, (0,dy) )
        scr.blit(backround2, (650,dy))
    if y <= 300 and vy <0:           
        

        yb = yb + abs(vy)/150
        obswait = yb


        
    pg.font.init()                                          #this creates the text on the top right corner for platforms left
    font = pg.font.SysFont("Arial", 22, True)
    textsurface = font.render("Platforms left: %s" % startnum, False, orange)
    scoresurface = font.render("Your score: %s" % score, False, orange)
    scr.blit(textsurface, (653,50))
    scr.blit(scoresurface, (653,100))
    

    ballrect.center = (x,y)
    
    scr.blit(ballpic, ballrect)
    
    
   
    
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
pg.quit()










