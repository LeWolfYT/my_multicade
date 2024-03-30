import pytweening as pt
import pygame as pg
import keyboard as k
import time
import math
import os

pg.init()

assets_path = "/Users/pj/Downloads/Wolf-Proj/multicade"
mame_path = "/Applications/mame0258-arm64/mame"

#ORIENTATION:
#0 = normal, use this for desktop
#1 = flipped
#2 = horizontal 90 degrees
#3 = horizontal 270 degrees
#NOTICE! This version of the program is meant for --->>>VERTICAL DISPLAYS!!!<<<---
orientation = 0
menuw = 224 #generally, you want to set these to the resolution of your monitor, integer scaled down to roughly 224x288 or something
menuh = 288 #fun fact! more games use 224x256, Namco woke up feeling different and decided to use 224x288 for a ton of games
anim_length = 2 #this one is for the names
anim_lengthb = 0.5 #this one is for the selection
vsync = True
frame = True
fullscreen = False

#MAME SETUP
machine1 = "pacman"
machine2 = "ncv1"

bg1 = pg.image.load(os.path.join(assets_path, "bg1.png"))
bg2 = pg.image.load(os.path.join(assets_path, "bg2.png"))
timerdir = os.path.join(assets_path, "timer/")
name1 = pg.image.load(os.path.join(assets_path, "name1.png"))
name2 = pg.image.load(os.path.join(assets_path, "name2.png"))
music = os.path.join(assets_path, "bgm.wav") #same here
credit = pg.mixer.Sound(os.path.join(assets_path, "credit.wav")) #here too (insert coin sound)
choose = pg.mixer.Sound(os.path.join(assets_path, "choose.wav")) #don't forget here (choose game sound)
launch = pg.mixer.Sound(os.path.join(assets_path, "launch.wav")) #and here (game launch sound)

timernums = []
for i in range(10):
    timernums.append(pg.image.load(os.path.join(timerdir, f"timer{i}.png")))

def wait_for_start(window: pg.surface.Surface):
    while not k.is_pressed(36): #put in your condition for getting the start key or button or something
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            mask1, mask2 = generate_masks(menuw/2)
            
            blend1 = pg.surface.Surface((menuw, menuh))
            blend2 = pg.surface.Surface((menuw, menuh))
            blend3 = pg.surface.Surface((menuw, menuh))
                
            blend1.blit(pg.transform.scale(bg1, (menuw, menuh)), (0, 0))
            blend1.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend1.blit(mask1, (0, 0), None, pg.BLEND_RGBA_SUB)
            
            blend2.blit(pg.transform.scale(bg2, (menuw, menuh)), (0, 0))
            blend2.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend2.blit(mask2, (0, 0), None, pg.BLEND_RGBA_SUB)
            blend3.blit(blend1, (0, 0))
            blend3.blit(blend2, (0, 0), None, pg.BLEND_RGB_ADD)
            window.blit(blend3, (0, 0))
            pg.draw.line(window, (20, 20, 20), (menuw/2 - 40, menuh), (menuw/2 + 40, 0), width = 6)
            pg.draw.line(window, (127, 127, 127), (menuw/2 - 40, menuh), (menuw/2 + 40, 0), width = 4)
            pg.draw.line(window, (180, 180, 180), (menuw/2 - 40, menuh), (menuw/2 + 40, 0), width = 2)
            pg.display.flip()
    credit.play()
    return True

def generate_masks(xpos):
    mask1s = pg.surface.Surface((menuw, menuh))
    mask1s.fill((0, 0, 0, 0))
    pg.draw.polygon(mask1s, (255, 255, 255, 255), [(0, 0), (0, menuh), (xpos-40, menuh), (xpos+40, 0)])
    mask2s = pg.surface.Surface((menuw, menuh))
    mask2s.fill((0, 0, 0, 0))
    pg.draw.polygon(mask2s, (255, 255, 255, 255), [(menuw, 0), (menuw, menuh), (xpos-40, menuh), (xpos+40, 0)])
    return mask2s, mask1s

def generate_shadow(w, h, opacity):
    sh = pg.surface.Surface((w, h))
    sh.fill([opacity] * 4)
    return sh

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def get_between(a, b, amount):
    return a*(1-amount)+b*amount

class GameItem():
    def __init__(self, bg, machine):
        self.bg = bg
        self.machine = machine
    def launch(self, command):
        os.system(command)

class Menu():
    def __init__(self, game1: GameItem, game2: GameItem):
        self.g1 = game1
        self.g2 = game2
        self.window = pg.display.set_mode((menuw, menuh), (pg.NOFRAME * (not frame)) | pg.SCALED | (pg.FULLSCREEN * fullscreen), vsync=vsync)
        pg.display.set_caption("My Multicade")
        self.window.fill((0, 0, 0))
    
    def menu(self):
        if not wait_for_start(self.window):
            return
        pg.mixer.music.load(music)
        pg.mixer.music.play()
        pg.mixer.music.set_volume(2.5)
        bar_x = menuw/2
        bar_origin = menuw/2
        target1 = round(menuw/4)
        target2 = round(menuw/4*3)
        startt = time.time()
        sel = 0
        anim_startb = 0
        
        name1xs = -name1.get_width()
        name2xs = menuw
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                #change the keys and such to work with your code
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and sel != 1:
                        sel = 1
                        bar_origin = bar_x
                        choose.play()
                        anim_startb = time.time()
                    elif event.key == pg.K_RIGHT and sel != 2:
                        sel = 2
                        bar_origin = bar_x
                        choose.play()
                        anim_startb = time.time()
            if sel == 1:
                bar_x = get_between(bar_origin, target2, pt.easeInOutQuad(clamp(time.time()-anim_startb, 0, anim_lengthb)/anim_lengthb))
            elif sel == 2:
                bar_x = get_between(bar_origin, target1, pt.easeInOutQuad(clamp(time.time()-anim_startb, 0, anim_lengthb)/anim_lengthb))
            mask1, mask2 = generate_masks(bar_x)
            current = time.time()
            timer = 20-abs(math.ceil(startt-current))
            
            blend1 = pg.surface.Surface((menuw, menuh))
            blend2 = pg.surface.Surface((menuw, menuh))
            blend3 = pg.surface.Surface((menuw, menuh))
            
            blend1.blit(pg.transform.scale(bg1, (menuw, menuh)), (0, 0))
            blend1.blit(generate_shadow(menuw, menuh, 127 if sel != 1 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend1.blit(mask1, (0, 0), None, pg.BLEND_RGBA_SUB)
            
            blend2.blit(pg.transform.scale(bg2, (menuw, menuh)), (0, 0))
            blend2.blit(generate_shadow(menuw, menuh, 127 if sel != 2 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend2.blit(mask2, (0, 0), None, pg.BLEND_RGBA_SUB)
            blend3.blit(blend1, (0, 0))
            blend3.blit(blend2, (0, 0), None, pg.BLEND_RGB_ADD)
            
            self.window.blit(blend3, (0, 0))
            pg.draw.line(self.window, (20, 20, 20), (bar_x - 40, menuh), (bar_x + 40, 0), width = 6)
            pg.draw.line(self.window, (127, 127, 127), (bar_x - 40, menuh), (bar_x + 40, 0), width = 4)
            pg.draw.line(self.window, (180, 180, 180), (bar_x - 40, menuh), (bar_x + 40, 0), width = 2)
            self.window.blit(name1, (get_between(name1xs, 10, pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), 50))
            self.window.blit(name2, (get_between(name2xs, menuw - 10 - name2.get_width(), pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), menuh - 50 - name2.get_height()))
        
            if timer > 0:
                if len(str(timer)) == 2:
                    sur1 = timernums[int(str(timer)[0])]
                    sur2 = timernums[int(str(timer)[1])]
                    self.window.blit(sur1, (menuw/2-sur1.get_width()-1, 8))
                    self.window.blit(sur2, (menuw/2+1, 8))
                elif len(str(timer)) == 1:
                    sur1 = timernums[int(str(timer)[0])]
                    self.window.blit(sur1, (round(menuw/2-sur1.get_width()/2), 8))
            else:
                sur1 = timernums[0]
                self.window.blit(sur1, (round(menuw/2-sur1.get_width()/2), 8))
            
            pg.display.flip()
            if timer <= -0.5:
                launch.play()
                if sel == 1:
                    os.system(f"{mame_path} {self.g1.machine} -skip_gameinfo -ui simple")
                elif sel == 2:
                    os.system(f"{mame_path} {self.g2.machine} -skip_gameinfo -ui simple")
                else:
                    if round(time.time()) % 2 == 0:
                        os.system(f"{mame_path} {self.g1.machine} -skip_gameinfo -ui simple")
                    else:
                        os.system(f"{mame_path} {self.g2.machine} -skip_gameinfo -ui simple")
                return True

game1 = GameItem(bg1, machine1)
game2 = GameItem(bg2, machine2)

menu = Menu(game1, game2)
while True:
    if not menu.menu():
        break