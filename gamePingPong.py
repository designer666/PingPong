from tkinter import *
import random

# Глобальные переменные
# Настройки окна
WIDTH = 900
HEIGHT = 300

# Настройки ракеток
# Ширина ракетки
PAD_W = 10
# Высота ракетки
PAD_H = 100

# Радиус мяча
BALL_RADIUS = 40

# Скорость мяча
# По горизонтали
BALL_X_CHANGE = 20
# По вертикали
BALL_Y_CHANGE = 0

# Настройки окна
root = Tk()
root.title("Ping-pong")

# Настройки поля
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#009900")
c.pack()

# Элементы игрового поля
# Левая линия
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# Правая линия
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
# Разделитель игрового поля
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

# Создание мяча
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="#ADFF2F")

# Создание ракетки
# Левая ракетка
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="#FF0000")
# Правая ракетка
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="#FF0000")

# Скорость ракеток
PAD_SPEED = 20
# Скорость левой ракетки
LEFT_PAD_SPEED = 0
# Скорость правой ракетки
RIGHT_PAD_SPEED = 0

# Установка скорости с каждым ударом
BALL_SPEED_UP = 1.0
# Установка максимальной скорости мяча
BALL_MAX_SPEED = 30
# Установка начальной скорости мяча по горизониали
BALL_X_SPEED = 20
# Установка начальной скорости мяча по вертикали
BALL_Y_SPEED = 20
# Установка расстояния до правого края
right_line_distance = WIDTH - PAD_W

# Установка очков для игроков
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Просчет скорости
INITIAL_SPEED = 20

# Метод обновления счета
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text = PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

# Метода респауна мяча
def respawn_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    c.coords(BALL, WIDTH/2 - BALL_RADIUS/2, HEIGHT/2 - BALL_RADIUS/2, WIDTH/2 + BALL_RADIUS/2, HEIGHT/2 + BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)
    # BALL_Y_SPEED = -(BALL_Y_SPEED * -INITIAL_SPEED)/abs(BALL_Y_SPEED)

# Метод для движения ракеток
def move_pad():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

# Метод для движения мяча
def move_ball():
    # c.move(BALL, BALL_X_CHANGE, BALL_Y_CHANGE)
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot)/2
    # Вертикальный отскок
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce('punch')
            else:
                # pass
                update_score('left')
                respawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('punch')
            else:
                # pass
                update_score('right')
                respawn_ball()
    else:
        if ball_right > WIDTH/2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)
    if ball_bot + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')

# Метод для управления отскоком от ракеток
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'punch':
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

# Текст очков
p_1_text = c.create_text(WIDTH - WIDTH/6, PAD_H/4, text = PLAYER_1_SCORE, font = 'arial 18', fill = 'aqua')
p_2_text = c.create_text(WIDTH/6, PAD_H/4, text = PLAYER_2_SCORE, font = 'arial 18', fill = 'aqua')


# Метод для запуска методов
def main():
    move_ball()
    move_pad()
    # Выозов самого себя
    root.after(30, main)

# Создание реакций на клавиши
c.focus_set()

# Метод обработки нажатия на клавиши
def moveevent_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

# Привязка к полю
c.bind("<KeyPress>", moveevent_handler)

# Метод для отпускание клавиш
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0

# Привязка к полю
c.bind("<KeyRelease>", stop_pad)

# Запуск мяча
main()

# Запуск окна
root.mainloop()
