"""Собирает контрольный лист со всеми спрайтами в одной PNG."""
import os
import pygame

HERE = os.path.dirname(__file__)
IMG = os.path.join(HERE, "images")
TILE = 24
PAD = 10
COLS = 12

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame.init()
pygame.display.set_mode((1, 1))

files = sorted(f for f in os.listdir(IMG) if f.endswith(".png"))
rows = (len(files) + COLS - 1) // COLS
W = COLS * (TILE + PAD) + PAD
H = rows * (TILE + PAD + 10) + PAD + 20

surf = pygame.Surface((W, H))
surf.fill((20, 20, 20))
font = pygame.font.SysFont("Menlo", 8)

for i, name in enumerate(files):
    col = i % COLS
    row = i // COLS
    x = PAD + col * (TILE + PAD)
    y = PAD + row * (TILE + PAD + 10)
    img = pygame.image.load(os.path.join(IMG, name))
    surf.blit(img, (x, y))
    label = font.render(name.replace(".png", ""), True, (200, 200, 200))
    surf.blit(label, (x, y + TILE + 1))

pygame.image.save(surf, os.path.join(HERE, "contact_sheet.png"))
print("contact_sheet.png saved")
pygame.quit()
