import pygame, math, random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anime Film Engine v7 - Visual Novel")

clock = pygame.time.Clock()
FPS = 60

# Music & sound
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    pass
try:
    thunder_sound = pygame.mixer.Sound("thunder.wav")
except:
    thunder_sound = None

# Fonts
font = pygame.font.SysFont("arial", 22)
name_font = pygame.font.SysFont("arial", 24, bold=True)
big_font = pygame.font.SysFont("arial", 46)
credit_font = pygame.font.SysFont("arial", 26)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHAR = (40, 40, 60)
GLOW = (200, 220, 255)
CLOUD = (220, 220, 220)
DIALOG_BG = (10,10,20,180)

# Particle groups
particles = pygame.sprite.Group()
rain = pygame.sprite.Group()
fireflies = pygame.sprite.Group()

# Film grain
grain_surface = pygame.Surface((WIDTH, HEIGHT))
grain_surface.set_alpha(20)
for _ in range(400):
    grain_surface.set_at((random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)), (255,255,255))

# Vignette
vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for x in range(WIDTH):
    for y in range(HEIGHT):
        dx = (x - WIDTH//2) / (WIDTH//2)
        dy = (y - HEIGHT//2) / (HEIGHT//2)
        distance = math.sqrt(dx*dx + dy*dy)
        alpha = min(180, int(distance * 180))
        vignette.set_at((x, y), (0, 0, 0, alpha))

# Hills
hills = [
    {"y": HEIGHT-100, "color": (50,70,100), "speed": 0.1, "height": 100},
    {"y": HEIGHT-80, "color": (40,60,90), "speed": 0.2, "height": 80},
    {"y": HEIGHT-60, "color": (30,50,80), "speed": 0.4, "height": 60}
]

# Clouds
cloud_layers = [
    [{"x": random.randint(0, WIDTH), "y": random.randint(30,150), "size": random.randint(80,150)} for _ in range(5)],
    [{"x": random.randint(0, WIDTH), "y": random.randint(50,200), "size": random.randint(100,180)} for _ in range(4)]
]

# Stars
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT//2), "alpha": random.randint(100,255), "dir": random.choice([-1,1])} for _ in range(120)]

# Fireflies
class Firefly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(HEIGHT//2, HEIGHT-140)
        self.vx = random.uniform(-0.3,0.3)
        self.vy = random.uniform(-0.3,0.3)
        self.alpha = random.randint(50,180)
        self.image = pygame.Surface((4,4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,100,self.alpha), (2,2), 2)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.life = random.randint(100,300)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.rect.center = (int(self.x), int(self.y))
        self.alpha += random.choice([-2,2])
        self.alpha = max(50,min(180,self.alpha))
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, (255,255,100,self.alpha), (2,2), 2)
        if self.life <= 0: self.kill()

for _ in range(15):
    fireflies.add(Firefly())

# Particle classes
class AuraParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, 0)
        self.life = 50
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GLOW + (150,), (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.rect.center = (int(self.x), int(self.y))
        if self.life <= 0: self.kill()
        else: self.image.set_alpha(int(self.life / 50 * 150))

class RainDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, 0)
        self.speed = random.randint(12, 18)
        self.image = pygame.Surface((2, 10))
        self.image.fill((180, 200, 255))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > HEIGHT: self.kill()

# Helper functions
def add_aura(x, y, amount=4):
    for _ in range(amount):
        particles.add(AuraParticle(x, y))

def add_rain(amount=3):
    for _ in range(amount):
        rain.add(RainDrop())

# Characters
characters = {
    "Hero": {"pos": "left", "color": (100,200,255)},
    "Mysterious Figure": {"pos": "right", "color": (255,100,150)}
}

# Dialogue timeline
scenes = [
    {"time":0, "dialog":("Hero","The sky remembers everything."), "effects":[]},
    {"time":20, "dialog":("Mysterious Figure","Then I will answer it."), "effects":["rain"]},
    {"time":40, "dialog":("Hero","The night is alive with magic."), "effects":["fireflies","lightning"]},
]

frame = 0
TOTAL = 60
running = True
lightning_timer = 0
shake_offset = [0,0]

while running:
    dt = clock.tick(FPS)/1000
    frame +=1
    t = frame/FPS

    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False

    # Day-night
    day_fraction = t/TOTAL
    if day_fraction<0.25: sky=(int(120+(255-120)*(day_fraction/0.25)), int(190+(200-190)*(day_fraction/0.25)), int(255-155*(day_fraction/0.25)))
    elif day_fraction<0.5: sky=(255,200,255-int(155*(0.5-day_fraction)/0.25))
    elif day_fraction<0.75: sky=(255-int(245*(day_fraction-0.5)/0.25),170-int(150*(day_fraction-0.5)/0.25),120-int(120*(day_fraction-0.5)/0.25))
    else: sky=(10,10,20)

    # Sun & moon
    sun_x = int(WIDTH*day_fraction)
    sun_y = int(HEIGHT//2 - math.sin(day_fraction*2*math.pi)*200)
    moon_x = int(WIDTH*((day_fraction+0.5)%1))
    moon_y = int(HEIGHT//2 - math.sin((day_fraction+0.5)*2*math.pi)*200)

    # Scene determination
    if t<15: scene_num=1
    elif t<30: scene_num=2
    elif t<45: scene_num=3
    else: scene_num=4

    cam_x = int(math.sin(t*0.3)*30)
    if lightning_timer>0:
        shake_offset=[random.randint(-8,8),random.randint(-8,8)]
        lightning_timer-=1
    else: shake_offset=[0,0]

    surface=pygame.Surface((WIDTH,HEIGHT))
    surface.fill(sky)

    # Sun/moon
    pygame.draw.circle(surface,(255,255,180),(sun_x,sun_y),40)
    pygame.draw.circle(surface,(200,200,255,100),(moon_x,moon_y),30)

    # Clouds
    for i,layer in enumerate(cloud_layers):
        for c in layer:
            speed=0.2*(i+1)
            c["x"]+=speed
            if c["x"]-c["size"]>WIDTH: c["x"]=-c["size"]; c["y"]=random.randint(30,200)
            pygame.draw.ellipse(surface,CLOUD,(int(c["x"]),int(c["y"]),c["size"],c["size"]//2))

    # Hills
    for h in hills:
        pygame.draw.rect(surface,h["color"],(0,h["y"],WIDTH,h["height"]))

    # Stars
    if day_fraction>=0.75 or day_fraction<0.25:
        for s in stars:
            s["alpha"] += s["dir"]*2
            if s["alpha"]>255: s["alpha"]=255; s["dir"]=-1
            if s["alpha"]<100: s["alpha"]=100; s["dir"]=1
            surface.set_at((s["x"],s["y"]),(s["alpha"],s["alpha"],s["alpha"]))

    # Character motion
    base_x=WIDTH//2+cam_x
    base_y=HEIGHT//2
    float_y=math.sin(t*2)*10
    fly=-abs(math.sin(t*3))*60 if scene_num==3 else 0
    y=base_y+float_y+fly

    pygame.draw.ellipse(surface,(0,0,0,50),(base_x-30,HEIGHT-140,60,15))
    pygame.draw.circle(surface,CHAR,(base_x,int(y)),28)
    pygame.draw.rect(surface,CHAR,(base_x-16,y+28,32,70))

    # Aura
    if scene_num>=2:
        pygame.draw.circle(surface,GLOW,(base_x,int(y)),55,2)
        add_aura(base_x,y,2)

    particles.update()
    particles.draw(surface)

    # Scene events
    current_dialog = None
    for s in scenes:
        if s["time"]<=t<s["time"]+5:
            current_dialog=s
            if "rain" in s["effects"]: add_rain(3)
            if "fireflies" in s["effects"]:
                fireflies.update()
                fireflies.draw(surface)
            if "lightning" in s["effects"] and lightning_timer==0:
                lightning_timer=4
                if thunder_sound: thunder_sound.play()

    # Update rain
    rain.update()
    rain.draw(surface)

    # Fireflies
    fireflies.update()
    fireflies.draw(surface)

    # Dialogue box
    if current_dialog:
        char_name,text=current_dialog["dialog"]
        box=pygame.Surface((WIDTH-100,100),pygame.SRCALPHA)
        box.fill(DIALOG_BG)
        surface.blit(box,(50,HEIGHT-140))
        surface.blit(name_font.render(char_name,True,WHITE),(60,HEIGHT-130))
        surface.blit(font.render(text,True,WHITE),(60,HEIGHT-100))

    # Ending credits
    if scene_num==4:
        fade=pygame.Surface((WIDTH,HEIGHT))
        fade.set_alpha(min(255,int((t-45)*12)))
        fade.fill(BLACK)
        surface.blit(fade,(0,0))
        title=big_font.render("ECHOES OF THE SILENT SKY",True,WHITE)
        glow=big_font.render("ECHOES OF THE SILENT SKY",True,GLOW)
        surface.blit(glow,(WIDTH//2-glow.get_width()//2+2,HEIGHT//2-60+2))
        surface.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT//2-60))
        credits_y=HEIGHT+100-int((t-45)*40)
        credits=["Director: You","Animation: Code Engine","Music: Your Choice","Studio: Independent","© 2026"]
        for i,line in enumerate(credits):
            txt=credit_font.render(line,True,WHITE)
            surface.blit(txt,(WIDTH//2-txt.get_width()//2,credits_y+i*35))

    pygame.draw.rect(surface,BLACK,(0,0,WIDTH,40))
    pygame.draw.rect(surface,BLACK,(0,HEIGHT-40,WIDTH,40))
    surface.blit(grain_surface,(0,0))
    surface.blit(vignette,(0,0))

    screen.blit(surface,shake_offset)
    pygame.display.flip()

    if t>=TOTAL: running=False

pygame.quit()
