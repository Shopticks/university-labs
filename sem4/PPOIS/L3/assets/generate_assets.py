"""Генератор графики для Pac-Man.

Запуск:
    conda activate pygame_env
    python assets/generate_assets.py

Все ассеты создаются в каталоге assets/images/ рядом с этим скриптом.
"""
import math
import os

import pygame

TILE = 24
HALF = TILE // 2

# Палитра в духе оригинальной аркады (синие стены, розовая дверь,
# классические цвета призраков).
COLOR_BG = (0, 0, 0, 0)
COLOR_PACMAN = (255, 221, 0)
COLOR_WALL_FILL = (12, 24, 110)
COLOR_WALL_LINE = (52, 96, 252)
COLOR_DOOR = (255, 184, 222)
COLOR_PELLET = (255, 215, 175)
COLOR_POWER = (255, 215, 175)
COLOR_BLINKY = (255, 0, 0)
COLOR_PINKY = (255, 184, 222)
COLOR_INKY = (0, 255, 222)
COLOR_CLYDE = (255, 184, 71)
COLOR_FRIGHTENED = (33, 33, 222)
COLOR_FRIGHTENED_WHITE = (245, 245, 245)
COLOR_EYE_WHITE = (245, 245, 245)
COLOR_EYE_PUPIL = (33, 33, 222)
COLOR_FRIGHT_FACE = (255, 184, 71)
COLOR_FRIGHT_FACE_WHITE = (220, 0, 0)

OUT_DIR = os.path.join(os.path.dirname(__file__), "images")


# ---------------------------------------------------------------------------
# Утилиты
# ---------------------------------------------------------------------------
def new_surface(size: int = TILE) -> pygame.Surface:
    return pygame.Surface((size, size), pygame.SRCALPHA)


def save(surface: pygame.Surface, name: str) -> None:
    path = os.path.join(OUT_DIR, name)
    pygame.image.save(surface, path)
    print(f"  saved {name}")


# ---------------------------------------------------------------------------
# Pac-Man
# ---------------------------------------------------------------------------
def draw_pacman(direction: str, frame: int) -> pygame.Surface:
    """direction: right/left/up/down; frame: 0 закрыт, 1 средний, 2 открыт."""
    surf = new_surface()
    radius = HALF - 1
    center = (HALF, HALF)
    pygame.draw.circle(surf, COLOR_PACMAN, center, radius)
    if frame == 0:
        return surf  # рот закрыт — просто круг

    # Угол открытия рта: на втором кадре уже, на третьем шире.
    mouth_deg = 30 if frame == 1 else 55
    base_angle = {"right": 0, "up": 90, "left": 180, "down": 270}[direction]
    a1 = math.radians(base_angle - mouth_deg)
    a2 = math.radians(base_angle + mouth_deg)
    p1 = (center[0] + radius * math.cos(a1), center[1] - radius * math.sin(a1))
    p2 = (center[0] + radius * math.cos(a2), center[1] - radius * math.sin(a2))
    # Рисуем "клин" прозрачного цвета поверх круга.
    pygame.draw.polygon(surf, (0, 0, 0, 0), [center, p1, p2])
    # Дополнительно очистим эти пиксели — polygon при SRCALPHA не "вычитает".
    # Используем приём с маской: перерисуем форму на временной поверхности.
    return _mask_out_mouth(surf, center, radius, base_angle, mouth_deg)


def _mask_out_mouth(circle_surf: pygame.Surface, center, radius, base_angle, mouth_deg):
    """Вырезает клин рта из готового круга через побитовую маску."""
    result = new_surface()
    # Маска фигуры pac-man: круг минус клин.
    mask = new_surface()
    pygame.draw.circle(mask, (255, 255, 255, 255), center, radius)
    a1 = math.radians(base_angle - mouth_deg)
    a2 = math.radians(base_angle + mouth_deg)
    far = radius * 2
    p1 = (center[0] + far * math.cos(a1), center[1] - far * math.sin(a1))
    p2 = (center[0] + far * math.cos(a2), center[1] - far * math.sin(a2))
    pygame.draw.polygon(mask, (0, 0, 0, 0), [center, p1, p2])
    # Заливаем pac-man цветом по маске.
    body = new_surface()
    body.fill(COLOR_PACMAN)
    body.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    result.blit(body, (0, 0))
    return result


def draw_pacman_death(frame: int, total: int = 11) -> pygame.Surface:
    """Классическая анимация смерти: рот раскрывается до полного исчезновения."""
    surf = new_surface()
    radius = HALF - 1
    center = (HALF, HALF)
    if frame >= total - 1:
        return surf  # последний кадр — пусто
    mouth_deg = int(8 + (170 * frame) / (total - 2))
    mask = new_surface()
    pygame.draw.circle(mask, (255, 255, 255, 255), center, radius)
    a1 = math.radians(90 - mouth_deg)
    a2 = math.radians(90 + mouth_deg)
    far = radius * 2
    p1 = (center[0] + far * math.cos(a1), center[1] - far * math.sin(a1))
    p2 = (center[0] + far * math.cos(a2), center[1] - far * math.sin(a2))
    pygame.draw.polygon(mask, (0, 0, 0, 0), [center, p1, p2])
    body = new_surface()
    body.fill(COLOR_PACMAN)
    body.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(body, (0, 0))
    return surf


# ---------------------------------------------------------------------------
# Призраки
# ---------------------------------------------------------------------------
def _ghost_body(color, frame: int) -> pygame.Surface:
    """Тело призрака: купол + волнистый низ, два кадра анимации ног."""
    surf = new_surface()
    # Купол: круг + прямоугольник под ним.
    top = 3
    bottom = TILE - 3
    pygame.draw.circle(surf, color, (HALF, HALF), HALF - 3)
    pygame.draw.rect(surf, color, pygame.Rect(3, HALF, TILE - 6, HALF - 3))
    # Срежем низ под "юбку".
    cut = new_surface()
    cut.fill((0, 0, 0, 0))
    pygame.draw.rect(cut, (0, 0, 0, 255), pygame.Rect(0, bottom, TILE, TILE - bottom))
    surf.blit(cut, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # Волны юбки (3 зубца). Frame 0 — пики; frame 1 — впадины смещены.
    skirt_top = bottom - 4
    skirt_bot = bottom + 2
    teeth = 4
    step = (TILE - 6) / teeth
    pts = [(3, skirt_top)]
    for i in range(teeth + 1):
        x = 3 + i * step
        # Чередуем низ/верх; смещение зависит от кадра.
        if (i + frame) % 2 == 0:
            pts.append((x, skirt_bot))
        else:
            pts.append((x, skirt_top))
    pts.append((TILE - 3, skirt_top))
    pts.append((TILE - 3, skirt_top - 2))
    pts.append((3, skirt_top - 2))
    pygame.draw.polygon(surf, color, pts)
    return surf


def _draw_eyes(surf: pygame.Surface, look=(0, 0)) -> None:
    """Рисует пару глаз. look — направление зрачка: (-1,0),(1,0),(0,-1),(0,1) или (0,0)."""
    eye_r = 4
    pupil_r = 2
    lx, ly = HALF - 6, HALF - 2
    rx, ry = HALF + 6, HALF - 2
    pygame.draw.circle(surf, COLOR_EYE_WHITE, (lx, ly), eye_r)
    pygame.draw.circle(surf, COLOR_EYE_WHITE, (rx, ry), eye_r)
    dx, dy = look
    pygame.draw.circle(surf, COLOR_EYE_PUPIL, (lx + dx * 2, ly + dy * 2), pupil_r)
    pygame.draw.circle(surf, COLOR_EYE_PUPIL, (rx + dx * 2, ry + dy * 2), pupil_r)


def draw_ghost(color, frame: int, look=(0, 0)) -> pygame.Surface:
    surf = _ghost_body(color, frame)
    _draw_eyes(surf, look)
    return surf


def draw_ghost_frightened(frame: int, white: bool = False) -> pygame.Surface:
    color = COLOR_FRIGHTENED_WHITE if white else COLOR_FRIGHTENED
    accent = COLOR_FRIGHT_FACE_WHITE if white else COLOR_FRIGHT_FACE
    surf = _ghost_body(color, frame)
    # Лицо "перепуганного" призрака: глаза-точки и зигзаг-рот.
    pygame.draw.circle(surf, accent, (HALF - 6, HALF - 2), 2)
    pygame.draw.circle(surf, accent, (HALF + 6, HALF - 2), 2)
    mouth_y = HALF + 6
    pts = []
    for i in range(7):
        x = HALF - 9 + i * 3
        y = mouth_y + (-2 if i % 2 == 0 else 2)
        pts.append((x, y))
    pygame.draw.lines(surf, accent, False, pts, 2)
    return surf


def draw_eyes_only(look=(0, 0)) -> pygame.Surface:
    """Глаза без тела — призрак возвращается домой."""
    surf = new_surface()
    _draw_eyes(surf, look)
    return surf


# ---------------------------------------------------------------------------
# Стены, дверь, точки, фрукты
# ---------------------------------------------------------------------------
def draw_empty_tile() -> pygame.Surface:
    """Создает полностью прозрачную поверхность размером TILExTILE."""
    return new_surface()

def draw_wall_tile() -> pygame.Surface:
    """Универсальный квадрат стены: заливка + светлая обводка."""
    surf = new_surface()
    pygame.draw.rect(surf, COLOR_WALL_FILL, pygame.Rect(0, 0, TILE, TILE))
    pygame.draw.rect(surf, COLOR_WALL_LINE, pygame.Rect(0, 0, TILE, TILE), width=2)
    return surf


def draw_wall_rounded(corners=("nw", "ne", "se", "sw")) -> pygame.Surface:
    """Стена с возможностью скруглить отдельные углы (для красивой границы)."""
    surf = new_surface()
    r = 8
    pygame.draw.rect(
        surf,
        COLOR_WALL_FILL,
        pygame.Rect(0, 0, TILE, TILE),
        border_top_left_radius=r if "nw" in corners else 0,
        border_top_right_radius=r if "ne" in corners else 0,
        border_bottom_left_radius=r if "sw" in corners else 0,
        border_bottom_right_radius=r if "se" in corners else 0,
    )
    pygame.draw.rect(
        surf,
        COLOR_WALL_LINE,
        pygame.Rect(0, 0, TILE, TILE),
        width=2,
        border_top_left_radius=r if "nw" in corners else 0,
        border_top_right_radius=r if "ne" in corners else 0,
        border_bottom_left_radius=r if "sw" in corners else 0,
        border_bottom_right_radius=r if "se" in corners else 0,
    )
    return surf


def draw_wall_hollow(sides=("n", "s", "e", "w")) -> pygame.Surface:
    """Полая «трубка» в духе оригинальной аркады.

    Контур рисуется только на тех сторонах, которые перечислены в ``sides``:
    это позволяет состыковывать соседние плитки без зазоров. Внутри —
    прозрачность, так что точки и Pac-Man остаются хорошо видны.
    """
    surf = new_surface()
    inset = 6  # отступ от края тайла до внешней линии контура
    gap = 3    # расстояние между внешней и внутренней синими линиями
    thickness = 1

    outer = pygame.Rect(inset, inset, TILE - 2 * inset, TILE - 2 * inset)
    inner = outer.inflate(-2 * gap, -2 * gap)

    def hline(y: int, x0: int, x1: int) -> None:
        pygame.draw.line(surf, COLOR_WALL_LINE, (x0, y), (x1, y), thickness)

    def vline(x: int, y0: int, y1: int) -> None:
        pygame.draw.line(surf, COLOR_WALL_LINE, (x, y0), (x, y1), thickness)

    # Внешняя рамка — только те грани, на которых нет соседа-стены.
    if "n" in sides:
        hline(outer.top, outer.left, outer.right)
    if "s" in sides:
        hline(outer.bottom, outer.left, outer.right)
    if "w" in sides:
        vline(outer.left, outer.top, outer.bottom)
    if "e" in sides:
        vline(outer.right, outer.top, outer.bottom)

    # Внутренняя рамка повторяет геометрию, но смещена внутрь.
    if "n" in sides:
        hline(inner.top, inner.left, inner.right)
    if "s" in sides:
        hline(inner.bottom, inner.left, inner.right)
    if "w" in sides:
        vline(inner.left, inner.top, inner.bottom)
    if "e" in sides:
        vline(inner.right, inner.top, inner.bottom)

    # На «открытых» торцах соединяем внешнюю и внутреннюю линии короткой
    # перемычкой, иначе тайл смотрится недорисованным.
    if "n" not in sides:
        vline(outer.left, outer.top, inner.top)
        vline(outer.right, outer.top, inner.top)
    if "s" not in sides:
        vline(outer.left, inner.bottom, outer.bottom)
        vline(outer.right, inner.bottom, outer.bottom)
    if "w" not in sides:
        hline(outer.top, outer.left, inner.left)
        hline(outer.bottom, outer.left, inner.left)
    if "e" not in sides:
        hline(outer.top, inner.right, outer.right)
        hline(outer.bottom, inner.right, outer.right)
    return surf


def draw_wall_hollow_corner(corner: str) -> pygame.Surface:
    """Скруглённый угол полой «трубки». corner ∈ {nw, ne, sw, se}."""
    surf = new_surface()
    inset = 6
    gap = 3
    thickness = 1
    radius_outer = TILE // 2 - inset
    radius_inner = radius_outer - gap

    # Центр дуги лежит в противоположном углу тайла на расстоянии inset.
    centers = {
        "nw": (TILE - inset, TILE - inset),
        "ne": (inset, TILE - inset),
        "sw": (TILE - inset, inset),
        "se": (inset, inset),
    }
    # Диапазон углов для каждой четверти (pygame.draw.arc измеряет в радианах).
    arcs = {
        "nw": (math.pi / 2, math.pi),
        "ne": (0.0, math.pi / 2),
        "sw": (math.pi, 3 * math.pi / 2),
        "se": (3 * math.pi / 2, 2 * math.pi),
    }
    cx, cy = centers[corner]
    a0, a1 = arcs[corner]

    def arc(radius: int) -> None:
        rect = pygame.Rect(cx - radius, cy - radius, 2 * radius, 2 * radius)
        pygame.draw.arc(surf, COLOR_WALL_LINE, rect, a0, a1, thickness)

    arc(radius_outer)
    arc(radius_inner)

    # Прямые продолжения контура к сторонам тайла, противоположным углу.
    # Для угла nw это правая и нижняя стороны и т.д.
    def hline(y: int, x0: int, x1: int) -> None:
        pygame.draw.line(surf, COLOR_WALL_LINE, (x0, y), (x1, y), thickness)

    def vline(x: int, y0: int, y1: int) -> None:
        pygame.draw.line(surf, COLOR_WALL_LINE, (x, y0), (x, y1), thickness)

    if corner == "nw":
        vline(TILE - inset, cy, TILE)
        vline(TILE - inset - gap, cy, TILE)
        hline(TILE - inset, cx, TILE)
        hline(TILE - inset - gap, cx, TILE)
    elif corner == "ne":
        vline(inset, cy, TILE)
        vline(inset + gap, cy, TILE)
        hline(TILE - inset, 0, cx)
        hline(TILE - inset - gap, 0, cx)
    elif corner == "sw":
        vline(TILE - inset, 0, cy)
        vline(TILE - inset - gap, 0, cy)
        hline(inset, cx, TILE)
        hline(inset + gap, cx, TILE)
    elif corner == "se":
        vline(inset, 0, cy)
        vline(inset + gap, 0, cy)
        hline(inset, 0, cx)
        hline(inset + gap, 0, cx)
    return surf


def draw_ghost_door() -> pygame.Surface:
    surf = new_surface()
    # Сама плитка прозрачная, в центре — розовая горизонтальная полоса.
    bar = pygame.Rect(0, HALF - 2, TILE, 4)
    pygame.draw.rect(surf, COLOR_DOOR, bar)
    return surf


def draw_pellet() -> pygame.Surface:
    surf = new_surface()
    pygame.draw.circle(surf, COLOR_PELLET, (HALF, HALF), 3)
    return surf


def draw_power_pellet() -> pygame.Surface:
    surf = new_surface()
    pygame.draw.circle(surf, COLOR_POWER, (HALF, HALF), 8)
    return surf


def draw_cherry() -> pygame.Surface:
    surf = new_surface()
    pygame.draw.circle(surf, (220, 20, 20), (HALF - 5, HALF + 6), 7)
    pygame.draw.circle(surf, (220, 20, 20), (HALF + 6, HALF + 7), 7)
    pygame.draw.circle(surf, (255, 110, 110), (HALF - 7, HALF + 3), 2)
    pygame.draw.circle(surf, (255, 110, 110), (HALF + 4, HALF + 4), 2)
    # Стебельки.
    pygame.draw.line(surf, (40, 160, 40), (HALF - 5, HALF + 6), (HALF + 2, HALF - 8), 2)
    pygame.draw.line(surf, (40, 160, 40), (HALF + 6, HALF + 7), (HALF + 3, HALF - 8), 2)
    # Листик.
    pygame.draw.polygon(
        surf,
        (40, 200, 60),
        [(HALF + 2, HALF - 8), (HALF + 9, HALF - 11), (HALF + 7, HALF - 5)],
    )
    return surf


def draw_strawberry() -> pygame.Surface:
    surf = new_surface()
    pygame.draw.polygon(
        surf,
        (220, 30, 30),
        [(HALF - 10, HALF - 4), (HALF + 10, HALF - 4), (HALF, HALF + 12)],
    )
    pygame.draw.circle(surf, (220, 30, 30), (HALF - 8, HALF - 4), 5)
    pygame.draw.circle(surf, (220, 30, 30), (HALF + 8, HALF - 4), 5)
    # Семечки.
    for (sx, sy) in [(-4, 0), (4, 0), (0, 4), (-2, -2), (3, -3)]:
        pygame.draw.circle(surf, (255, 230, 120), (HALF + sx, HALF + sy), 1)
    # Зелёный чашелистик.
    pygame.draw.polygon(
        surf,
        (40, 200, 60),
        [
            (HALF - 8, HALF - 6),
            (HALF, HALF - 12),
            (HALF + 8, HALF - 6),
            (HALF + 4, HALF - 4),
            (HALF, HALF - 8),
            (HALF - 4, HALF - 4),
        ],
    )
    return surf


def draw_orange() -> pygame.Surface:
    surf = new_surface()
    pygame.draw.circle(surf, (255, 150, 30), (HALF, HALF + 2), 10)
    pygame.draw.line(surf, (60, 140, 40), (HALF, HALF - 8), (HALF, HALF - 12), 3)
    pygame.draw.polygon(
        surf,
        (40, 200, 60),
        [(HALF, HALF - 12), (HALF + 6, HALF - 10), (HALF + 1, HALF - 8)],
    )
    return surf


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1, 1))
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Pacman:")
    for direction in ("right", "left", "up", "down"):
        for frame in (0, 1, 2):
            save(draw_pacman(direction, frame), f"pacman_{direction}_{frame}.png")

    print("Pacman death:")
    for i in range(11):
        save(draw_pacman_death(i), f"pacman_death_{i}.png")

    print("Ghosts:")
    ghost_palette = {
        "blinky": COLOR_BLINKY,
        "pinky": COLOR_PINKY,
        "inky": COLOR_INKY,
        "clyde": COLOR_CLYDE,
    }
    look_map = {
        "right": (1, 0),
        "left": (-1, 0),
        "up": (0, -1),
        "down": (0, 1),
    }
    for name, color in ghost_palette.items():
        for direction, look in look_map.items():
            for frame in (0, 1):
                save(
                    draw_ghost(color, frame, look),
                    f"ghost_{name}_{direction}_{frame}.png",
                )

    print("Frightened ghost:")
    for frame in (0, 1):
        save(draw_ghost_frightened(frame, white=False), f"ghost_frightened_{frame}.png")
        save(
            draw_ghost_frightened(frame, white=True),
            f"ghost_frightened_white_{frame}.png",
        )

    print("Ghost eyes (eaten state):")
    for direction, look in look_map.items():
        save(draw_eyes_only(look), f"ghost_eyes_{direction}.png")

    print("Maze pieces:")
    save(draw_empty_tile(), "empty_tile.png")
    save(draw_wall_tile(), "wall.png")
    save(draw_wall_rounded(("nw",)), "wall_corner_nw.png")
    save(draw_wall_rounded(("ne",)), "wall_corner_ne.png")
    save(draw_wall_rounded(("sw",)), "wall_corner_sw.png")
    save(draw_wall_rounded(("se",)), "wall_corner_se.png")
    # Полая «трубка» — стиль оригинальной аркадной карты.
    # Базовая плитка со всех четырёх сторон закрыта рамкой; набор «торцов»
    # пригодится, чтобы карта не имела зазоров между соседними стенами.
    save(draw_wall_hollow(("n", "s", "e", "w")), "wall_hollow.png")
    save(draw_wall_hollow(("e", "w")), "wall_hollow_h.png")  # горизонтальный проход
    save(draw_wall_hollow(("n", "s")), "wall_hollow_v.png")  # вертикальный проход
    save(draw_wall_hollow(("s", "e", "w")), "wall_hollow_end_n.png")
    save(draw_wall_hollow(("n", "e", "w")), "wall_hollow_end_s.png")
    save(draw_wall_hollow(("n", "s", "e")), "wall_hollow_end_w.png")
    save(draw_wall_hollow(("n", "s", "w")), "wall_hollow_end_e.png")
    for corner in ("nw", "ne", "sw", "se"):
        save(draw_wall_hollow_corner(corner), f"wall_hollow_corner_{corner}.png")
    save(draw_ghost_door(), "ghost_door.png")

    print("Pickups:")
    save(draw_pellet(), "pellet.png")
    save(draw_power_pellet(), "power_pellet.png")
    save(draw_cherry(), "cherry.png")
    save(draw_strawberry(), "strawberry.png")
    save(draw_orange(), "orange.png")

    pygame.quit()
    print("Done.")


if __name__ == "__main__":
    main()
