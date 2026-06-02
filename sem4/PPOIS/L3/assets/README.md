# Графика уровня

Все спрайты размером **32×32 px**, формат PNG с альфа-каналом.
Палитра подобрана под классическую аркаду: жёлтый Pac-Man, тёмно-синие
стены, розовая дверь дома призраков, четвёрка призраков с оригинальными
цветами.

## Перегенерация

```bash
conda activate pygame_env
python assets/generate_assets.py        # пересоздаёт images/
python assets/make_contact_sheet.py     # собирает contact_sheet.png
```

`generate_assets.py` — единственный источник правды, никаких внешних
картинок не используется (нет проблем с лицензиями).

## Содержимое `images/`

| Спрайт | Файлы |
|--------|-------|
| Pac-Man | `pacman_{right,left,up,down}_{0,1,2}.png` — направление и фаза рта |
| Смерть Pac-Man | `pacman_death_0.png` … `pacman_death_10.png` |
| Призраки | `ghost_{blinky,pinky,inky,clyde}_{right,left,up,down}_{0,1}.png` |
| Frightened (синий) | `ghost_frightened_{0,1}.png` |
| Frightened (мигание перед концом) | `ghost_frightened_white_{0,1}.png` |
| «Глаза» — съеденный призрак ползёт домой | `ghost_eyes_{right,left,up,down}.png` |
| Стена (заливка) | `wall.png` + `wall_corner_{nw,ne,sw,se}.png` |
| Стена-«трубка» (аркадный стиль) | `wall_hollow.png`, `wall_hollow_{h,v}.png`, `wall_hollow_end_{n,s,e,w}.png`, `wall_hollow_corner_{nw,ne,sw,se}.png` |
| Дверь призраков | `ghost_door.png` |
| Точки | `pellet.png`, `power_pellet.png` |
| Фрукты-бонусы | `cherry.png`, `strawberry.png`, `orange.png` |

`contact_sheet.png` — все спрайты на одной картинке для визуального контроля.
