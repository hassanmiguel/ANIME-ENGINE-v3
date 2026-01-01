import pygame, math, random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anime Film Engine v3")

clock = pygame.time.Clock()
FPS = 60

# Music
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    pass

# Fonts
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 46)
credit_font = pygame.font.SysFont("arial", 26)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHAR = (40, 40, 60)
GLOW = (200, 220, 255)

particles = []
rain = []

def add_aura(x, y):
    for _ in range(4):
        particles.append([x, y, random.uniform(-1,1), random.uniform(-2,0), 50])

def add_rain():
    rain.append([random.randint(0, WIDTH), random.randint(-50, 0)])

frame = 0
TOTAL = 60

running = True
while running:
    dt = clock.tick(FPS) / 1000
    frame += 1
    t = frame / FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Scene timeline
    if t < 15:
        scene = 1
    elif t < 30:
        scene = 2
    elif t < 45:
        scene = 3
    else:
        scene = 4

    # Day cycle
    if scene == 1:
        sky = (120, 190, 255)
    elif scene == 2:
        sky = (255, 170, 120)
    elif scene == 3:
        sky = (40, 60, 120)
    else:
        sky = (10, 10, 20)

    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(sky)

    # Ground
    pygame.draw.rect(surface, (60, 80, 110), (0, HEIGHT - 130, WIDTH, 130))

    # Camera pan
    cam_x = int(math.sin(t * 0.3) * 30)

    # Character motion
    base_x = WIDTH // 2 + cam_x
    base_y = HEIGHT // 2
    float_y = math.sin(t * 2) * 10
    fly = -abs(math.sin(t * 3)) * 60 if scene == 3 else 0
    y = base_y + float_y + fly

    # Shadow
    pygame.draw.ellipse(surface, (0,0,0,50), (base_x - 30, HEIGHT - 140, 60, 15))

    # Character
    pygame.draw.circle(surface, CHAR, (base_x, int(y)), 28)
    pygame.draw.rect(surface, CHAR, (base_x - 16, y + 28, 32, 70))

    # Aura
    if scene >= 2:
        pygame.draw.circle(surface, GLOW, (base_x, int(y)), 55, 2)
        add_aura(base_x, y)

    # Aura particles
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        pygame.draw.circle(surface, GLOW, (int(p[0]), int(p[1])), 2)
        if p[4] <= 0:
            particles.remove(p)

    # Rain (scene 3)
    if scene == 3:
        for _ in range(3):
            add_rain()
        for drop in rain[:]:
            drop[1] += 15
            pygame.draw.line(surface, (180, 200, 255), (drop[0], drop[1]), (drop[0], drop[1]+10))
            if drop[1] > HEIGHT:
                rain.remove(drop)

    # Subtitles
    if 18 < t < 24:
        surface.blit(font.render("The sky remembers everything.", True, WHITE),
                     (WIDTH//2 - 160, HEIGHT - 90))
    if 33 < t < 38:
        surface.blit(font.render("Then I will answer it.", True, WHITE),
                     (WIDTH//2 - 120, HEIGHT - 90))

    # Ending + credits
    if scene == 4:
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.set_alpha(min(255, int((t - 45) * 12)))
        fade.fill(BLACK)
        surface.blit(fade, (0, 0))

        title = big_font.render("ECHOES OF THE SILENT SKY", True, WHITE)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))

        credits_y = HEIGHT + 100 - int((t - 45) * 40)
        credits = [
            "Director: You",
            "Animation: Code Engine",
            "Music: Your Choice",
            "Studio: Independent",
            "© 2026"
        ]
        for i, line in enumerate(credits):
            txt = credit_font.render(line, True, WHITE)
            surface.blit(txt, (WIDTH//2 - txt.get_width()//2, credits_y + i*35))

    # Letterbox
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, 40))
    pygame.draw.rect(surface, BLACK, (0, HEIGHT - 40, WIDTH, 40))

    # Film grain
    grain = pygame.Surface((WIDTH, HEIGHT))
    grain.set_alpha(20)
    for _ in range(400):
        grain.set_at((random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)), (255,255,255))
    surface.blit(grain, (0,0))

    screen.blit(surface, (0,0))
    pygame.display.flip()

    if t >= TOTAL:
        running = False

pygame.quit()
