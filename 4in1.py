import pytweening as pt
import keyboard as k
import pygame as pg
import time
import math
import os

#4-in-1 version

pg.init()

assets_path = "/Users/pj/Downloads/Wolf-Proj/my_multicade"
mame_path = "/Applications/mame0258-arm64/mame"

#ORIENTATION:
#0 = normal, use this for desktop
#1 = 180 degrees
#2 = 90 degrees CCW
#3 = 90 degrees CW
#NOTICE! This version of the program is meant for --->>>VERTICAL DISPLAYS!!!<<<---
orientation = 0
menuw = 224 #generally, you want to set these to the resolution of your monitor, integer scaled down to roughly 224x288 or something
menuh = 288 #fun fact! more games use 224x256, Namco woke up feeling different and decided to use 224x288 for a ton of games
anim_length = 2 #this one is for the names
anim_lengthb = 0.5 #this one is for the selection
counter = 0 #time to count, 0 = infinite
bgm_looped = True #if false, use bgm.wav. if true, use intro.wav and loop.wav
music_intro = True #only used when bgm_looped is true
vsync = True
frame = True
fullscreen = False

#MAME SETUP
machine1 = "pacman" #top left
machine2 = "ncv1" #top right
machine3 = "ncv2" #bottom left
machine4 = "mspacman" #bottom right

bg1 = pg.image.load(os.path.join(assets_path, "bg1.png"))
bg2 = pg.image.load(os.path.join(assets_path, "bg2.png"))
bg3 = pg.image.load(os.path.join(assets_path, "bg3.png"))
bg4 = pg.image.load(os.path.join(assets_path, "bg4.png"))
timerdir = os.path.join(assets_path, "timer/")
logo = pg.image.load(os.path.join(assets_path, "logo.png"))
name1 = pg.image.load(os.path.join(assets_path, "name1.png"))
name2 = pg.image.load(os.path.join(assets_path, "name2.png"))
name3 = pg.image.load(os.path.join(assets_path, "name3.png"))
name4 = pg.image.load(os.path.join(assets_path, "name4.png"))
music = os.path.join(assets_path, "bgm.wav") #same here
credit = pg.mixer.Sound(os.path.join(assets_path, "credit.wav")) #here too (insert coin sound)
choose = pg.mixer.Sound(os.path.join(assets_path, "choose.wav")) #don't forget here (choose game sound)
launch = pg.mixer.Sound(os.path.join(assets_path, "launch.wav")) #and here (game launch sound)

if bgm_looped:
    intro = pg.mixer.Sound(os.path.join(assets_path, "intro.wav")) #here...
    loop = pg.mixer.Sound(os.path.join(assets_path, "loop.wav")) #right here...

global playing
playing = None

timernums = []
for i in range(10):
    timernums.append(pg.image.load(os.path.join(timerdir, f"timer{i}.png")))

def wait_for_start(window: pg.surface.Surface, eee):
    while not k.is_pressed(36): #put in your condition for getting the start key or button or something
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            blend1 = pg.surface.Surface((menuw, menuh))
            blend2 = pg.surface.Surface((menuw, menuh))
            blend3 = pg.surface.Surface((menuw, menuh))
            blend4 = pg.surface.Surface((menuw, menuh))
            blend5 = pg.surface.Surface((menuw, menuh))
            
            blend1.blit(pg.transform.scale(bg1, (menuw/2, menuh/2)), (0, 0))
            blend1.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend1, (0, 0), None, pg.BLEND_RGBA_ADD)
            
            blend2.blit(pg.transform.scale(bg2, (menuw/2, menuh/2)), (0, 0))
            blend2.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend2, (menuw/2, 0), None, pg.BLEND_RGBA_ADD)
            
            blend3.blit(pg.transform.scale(bg3, (menuw/2, menuh/2)), (0, 0))
            blend3.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend3, (0, menuh/2), None, pg.BLEND_RGBA_ADD)
            
            blend4.blit(pg.transform.scale(bg4, (menuw/2, menuh/2)), (0, 0))
            blend4.blit(generate_shadow(menuw, menuh, 127), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend4, (menuw/2, menuh/2), None, pg.BLEND_RGBA_ADD)
            
            window.blit(blend5, (0, 0))
            pg.draw.line(window, (20, 20, 20), (0, menuh/2), (menuw, menuh/2), width = 6)
            pg.draw.line(window, (20, 20, 20), (menuw/2, 0), (menuw/2, menuh), width = 6)
            pg.draw.line(window, (127, 127, 127), (0, menuh/2), (menuw, menuh/2), width = 4)
            pg.draw.line(window, (127, 127, 127), (menuw/2, 0), (menuw/2, menuh), width = 4)
            pg.draw.line(window, (180, 180, 180), (0, menuh/2), (menuw, menuh/2), width = 2)
            pg.draw.line(window, (180, 180, 180), (menuw/2, 0), (menuw/2, menuh), width = 2)
            
            window.blit(logo, (0, menuh - logo.get_height()))
            
            if orientation == 0:
                eee.blit(window, (0, 0))
            elif orientation == 1:
                eee.blit(pg.transform.rotate(window, 180), (0, 0))
            elif orientation == 2:
                eee.blit(pg.transform.rotate(window, 90), (0, 0))
            elif orientation == 3:
                eee.blit(pg.transform.rotate(window, 270), (0, 0))
            
            pg.display.flip()
    credit.play()
    return True

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
    def __init__(self, game1: GameItem, game2: GameItem, game3: GameItem, game4: GameItem):
        self.g1 = game1
        self.g2 = game2
        self.g3 = game3
        self.g4 = game4
        self.window = pg.surface.Surface((menuw, menuh))
        self.windowr = pg.display.set_mode((menuw, menuh) if orientation <= 1 else (menuh, menuw), (pg.NOFRAME * (not frame)) | pg.SCALED | (pg.FULLSCREEN * fullscreen), vsync=vsync)
        pg.display.set_caption("My Multicade (4-in-1)")
        self.window.fill((0, 0, 0))
    
    def menu(self):
        if not wait_for_start(self.window, self.windowr):
            return
        playing = None
        if not bgm_looped:
            pg.mixer.music.load(music)
            pg.mixer.music.play()
        startt = time.time()
        sel = 1
        spaghet = False
        playing1 = 0
        
        name1xs = -name1.get_width()
        name2xs = menuw
        first = True
        
        def pl():
                launch.play()
                if sel == 1:
                    os.system(f"{mame_path} {self.g1.machine} -skip_gameinfo -ui simple")
                elif sel == 2:
                    os.system(f"{mame_path} {self.g2.machine} -skip_gameinfo -ui simple")
                elif sel == 3:
                    os.system(f"{mame_path} {self.g3.machine} -skip_gameinfo -ui simple")
                elif sel == 4:
                    os.system(f"{mame_path} {self.g4.machine} -skip_gameinfo -ui simple")
                return True
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                #change the keys and such to work with your code
                elif event.type == pg.KEYDOWN and not first:
                    if event.key == pg.K_LEFT and sel in [2, 4]:
                        sel -= 1
                        choose.play()
                    elif event.key == pg.K_RIGHT and sel in [1, 3]:
                        sel += 1
                        choose.play()
                    elif event.key == pg.K_DOWN and sel in [1, 2]:
                        sel += 2
                        choose.play()
                    elif event.key == pg.K_UP and sel in [3, 4]:
                        sel -= 2
                        choose.play()
                    elif event.key == pg.K_RETURN and sel != 0 and counter == 0:
                        spaghet = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and first:
                        first = False
            current = time.time()
            timer = counter-abs(math.ceil(startt-current))
            
            blend1 = pg.surface.Surface((menuw, menuh))
            blend2 = pg.surface.Surface((menuw, menuh))
            blend3 = pg.surface.Surface((menuw, menuh))
            blend4 = pg.surface.Surface((menuw, menuh))
            blend5 = pg.surface.Surface((menuw, menuh))
            
            blend1.blit(pg.transform.scale(bg1, (menuw/2, menuh/2)), (0, 0))
            blend1.blit(generate_shadow(menuw, menuh, 127 if sel != 1 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend1, (0, 0), None, pg.BLEND_RGBA_ADD)
            
            blend2.blit(pg.transform.scale(bg2, (menuw/2, menuh/2)), (0, 0))
            blend2.blit(generate_shadow(menuw, menuh, 127 if sel != 2 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend2, (menuw/2, 0), None, pg.BLEND_RGBA_ADD)
            
            blend3.blit(pg.transform.scale(bg3, (menuw/2, menuh/2)), (0, 0))
            blend3.blit(generate_shadow(menuw, menuh, 127 if sel != 3 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend3, (0, menuh/2), None, pg.BLEND_RGBA_ADD)
            
            blend4.blit(pg.transform.scale(bg4, (menuw/2, menuh/2)), (0, 0))
            blend4.blit(generate_shadow(menuw, menuh, 127 if sel != 4 else 32), (0, 0), None, pg.BLEND_RGBA_SUB)
            blend5.blit(blend4, (menuw/2, menuh/2), None, pg.BLEND_RGBA_ADD)
            
            self.window.blit(blend5, (0, 0))
            pg.draw.line(self.window, (20, 20, 20), (0, menuh/2), (menuw, menuh/2), width = 6)
            pg.draw.line(self.window, (20, 20, 20), (menuw/2, 0), (menuw/2, menuh), width = 6)
            pg.draw.line(self.window, (127, 127, 127), (0, menuh/2), (menuw, menuh/2), width = 4)
            pg.draw.line(self.window, (127, 127, 127), (menuw/2, 0), (menuw/2, menuh), width = 4)
            pg.draw.line(self.window, (180, 180, 180), (0, menuh/2), (menuw, menuh/2), width = 2)
            pg.draw.line(self.window, (180, 180, 180), (menuw/2, 0), (menuw/2, menuh), width = 2)
            self.window.blit(name1, (get_between(name1xs, 10, pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), 26))
            self.window.blit(name3, (get_between(name1xs, 10, pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), menuh - name3.get_height() - 60))
            self.window.blit(name2, (get_between(name2xs, menuw - 10 - name2.get_width(), pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), 60))
            self.window.blit(name4, (get_between(name2xs, menuw - 10 - name4.get_width(), pt.easeInQuint(clamp(current-startt, 0, anim_length)/anim_length)), menuh - 25 - name2.get_height()))
        
            if counter != 0:
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
            
            self.window.blit(logo, (0, menuh - logo.get_height()))
            
            if orientation == 0:
                self.windowr.blit(self.window, (0, 0))
            elif orientation == 1:
                self.windowr.blit(pg.transform.rotate(self.window, 180), (0, 0))
            elif orientation == 2:
                self.windowr.blit(pg.transform.rotate(self.window, 90), (0, 0))
            elif orientation == 3:
                self.windowr.blit(pg.transform.rotate(self.window, 270), (0, 0))
            
            pg.display.flip()
            if bgm_looped:
                if playing1 == 0:
                    playing = intro.play()
                    playing1 = 1
                if playing1 == 1:
                    if playing.get_busy():
                        pass
                    else:
                        playing = loop.play(-1)
                        playing1 = 2
            if timer <= -0.5 and counter != 0:
                return pl()
            elif counter == 0:
                if spaghet:
                    if bgm_looped:
                        playing.stop()
                    else:
                        pg.mixer.music.stop()
                    return pl()

game1 = GameItem(bg1, machine1)
game2 = GameItem(bg2, machine2)
game3 = GameItem(bg3, machine3)
game4 = GameItem(bg4, machine4)

menu = Menu(game1, game2, game3, game4)
while True:
    if not menu.menu():
        break