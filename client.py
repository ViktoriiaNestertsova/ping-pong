from pygame import *
import socket
from socket import AF_INET,SOCK_STREAM
import json
from threading import Thread
from menu import CtWindow

win= CtWindow()
win.mainloop()
port = win.port
host = win.host
client = socket.socket(AF_INET,SOCK_STREAM)
client.connect((host,port))


# --- НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")
buffer = ""
game_state= {}

try:
    lose_image = image.load("youlose.png")
    lose_image = transform.scale(lose_image, (300, 300))
except:
    lose_image = None

# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            buffer = ""
            game_state = {}
            data = client.recv(24).decode().strip()
            if data.isdigit():
                my_id = int(data)
            else:
                continue
            return my_id, game_state, buffer, client
        except:
            pass

def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)
font_small = font.Font(None, 28)

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()

#функція для малювання сітки
def draw_net():
    segment_height = 20
    gap = 10
    for y in range(0, HEIGHT, segment_height + gap):
        draw.rect(screen, (60, 70, 100), (WIDTH//2 - 2, y, 4, segment_height))

#функція для малювання закруглених прямокутників
def draw_rounded_rect(surface, color, rect, radius=10):
    x, y, width, height = rect
    draw.rect(surface, color, (x + radius, y, width - 2*radius, height))
    draw.rect(surface, color, (x, y + radius, width, height - 2*radius))
    draw.circle(surface, color, (x + radius, y + radius), radius)
    draw.circle(surface, color, (x + width - radius, y + radius), radius)
    draw.circle(surface, color, (x + radius, y + height - radius), radius)
    draw.circle(surface, color, (x + width - radius, y + height - radius), radius)



while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False

        if you_winner:
            text = "Ти переміг!"
            color = (255, 215, 0)

            # Показувати текст перемоги
            win_text = font_win.render(text, True, color)
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(win_text, text_rect)

        else:
            text = "Ти програв"
            color = (200, 100, 100)

            if lose_image:
                image_rect = lose_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
                screen.blit(lose_image, image_rect)

            #Показуємо текст під фото
            win_text = font_win.render(text, True, color)
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            screen.blit(win_text, text_rect)

        restart_text = font_main.render('Натисни R для рестарту', True, (240, 240, 240))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)

        display.update()
        continue  # Блокує гру після перемоги

    if game_state:
        #покращений фон та додано сітку
        screen.fill((20, 25, 45))
        draw_net()

        #покращені платформи з закругленими кутами
        draw_rounded_rect(screen, (0, 255, 150), (20, game_state['paddles']['0'], 20, 100), 15)
        draw_rounded_rect(screen, (255, 50, 255), (WIDTH - 40, game_state['paddles']['1'], 20, 100), 15)

        #покращений м'яч
        draw.circle(screen, (255, 255, 255), (game_state['ball']['x'], game_state['ball']['y']), 10)

        #покращене табло з рахунком
        score_bg = (30, 35, 60)
        draw_rounded_rect(screen, score_bg, (WIDTH // 2 - 80, 15, 160, 60), 15)
        score_text = font_main.render(f"{game_state['scores'][0]}   {game_state['scores'][1]}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))

        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                pass
            if game_state['sound_event'] == 'platform_hit':
                pass

    else:
        #покращений екран очікування
        screen.fill((20, 25, 45))
        wating_text = font_main.render("Очікування гравців...", True, (255, 255, 255))
        screen.blit(wating_text, (WIDTH // 2 - wating_text.get_width() // 2, HEIGHT // 2))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")