import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.BUTTON_LEFT)
pygame.display.set_caption("Simulación Ruleta Española MYS")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
custom_color =(255,255,245,0.2)



roulette_center_x = screen_width // 3
roulette_center_y = screen_height //2

apuestas = [
    "Pleno", "Semipleno", "Pleno doble", "Caballo",
    "Tercio", "Cuadro", "Docena", "Columna",
    "Par o Impar", "Rojo o Negro", "Falta o Pasa", "Seisena"
]

# Números en la ruleta española en orden
spanish_roulette_numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20,
    14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]

spanish_roulette_numbers_order = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36
]

# Colores correspondientes a cada número (rojo o negro)
number_colors = [
    GREEN, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK,
    RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK,
    RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED
]
number_color_map_table = {
    0: "GREEN", 1: "RED", 2: "BLACK", 3: "RED", 4: "BLACK", 5: "RED", 6: "BLACK",
    7: "RED", 8: "BLACK", 9: "RED", 10: "BLACK", 11: "RED", 12: "RED", 13: "BLACK",
    14: "RED", 15: "BLACK", 16: "RED", 17: "BLACK", 18: "RED", 19: "RED", 20: "BLACK",
    21: "RED", 22: "BLACK", 23: "RED", 24: "BLACK", 25: "RED", 26: "BLACK", 27: "RED",
    28: "BLACK", 29: "BLACK", 30: "RED", 31: "BLACK", 32: "RED", 33: "BLACK", 34: "RED",
    35: "BLACK", 36: "RED"
}
def draw_number_table():
    font = pygame.font.Font(None, 36)
    x, y = screen_width // 1.5, 50  # Posición inicial para la tabla de números
    row = 0
    cell_width, cell_height = 60, 60  # Tamaño de cada cuadro

    for i, number in enumerate(spanish_roulette_numbers_order):
        color = number_color_map[number]
        text_color = WHITE if color == BLACK else BLACK  # Color del texto para mayor visibilidad
        number_text = font.render(str(number), True, text_color)
        number_rect = number_text.get_rect(topleft=(x + 5, y + 5))  # Ajusta el texto dentro del cuadro
        pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))  # Dibuja el cuadro con color
        screen.blit(number_text, number_rect)

        # Mover a la siguiente fila después de cada 3 números
        if (i + 1) % 3 == 0:
            x = screen_width // 1.5
            y += cell_height  # Espaciado vertical entre las filas
        else:
            x += cell_width  # Espaciado horizontal entre los números


# Función para dibujar la ruleta y hacerla girar en sentido contrario a la bola
def draw_roulette(ball_angle, roulette_rotation):
  
    for i, number in enumerate(spanish_roulette_numbers):
        color = number_colors[i]
        text_color = WHITE
        angle = math.radians(
            i * (360 / len(spanish_roulette_numbers)) - 90 + roulette_rotation
        )  # Alinea los números y gira la ruleta
        x = int(
            roulette_center_x + 250 * math.cos(angle)
        )  # Aumentamos la separación a 250
        y = int(
            roulette_center_y + 250 * math.sin(angle)
        )  # Aumentamos la separación a 250
        pygame.draw.circle(screen, color, (x, y), 22, 0)
        pygame.draw.circle(screen, BLACK, (x, y), 22, 2)

        font = pygame.font.Font(None, 36)
        text = font.render(str(number), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    # Dibuja el botón de girar como texto
    start_button = font.render("Girar", True, GREEN)
    screen.blit(start_button, (50, 50))


# Función para girar la ruleta y obtener un número aleatorio
def spin_roulette():
    return random.choice(spanish_roulette_numbers)

number_color_map = {
    0: GREEN, 32: RED, 15: BLACK, 19: RED, 4: BLACK, 21: RED, 2: BLACK, 25: RED,
    17: BLACK, 34: RED, 6: BLACK, 27: RED, 13: BLACK, 36: RED, 11: BLACK, 30: RED,
    8: BLACK, 23: RED, 10: BLACK, 5: RED, 24: BLACK, 16: RED, 33: BLACK, 1: RED, 
    20: BLACK, 14: RED, 31: BLACK, 9: RED, 22: BLACK, 18: RED, 29: BLACK, 7: RED,
    28: BLACK, 12: RED, 35: BLACK, 3: RED, 26: BLACK
}

number_color_map_table = {
    0: "GREEN", 1: "RED", 2: "BLACK", 3: "RED", 4: "BLACK", 5: "RED", 6: "BLACK",
    7: "RED", 8: "BLACK", 9: "RED", 10: "BLACK", 11: "RED", 12: "RED", 13: "BLACK",
    14: "RED", 15: "BLACK", 16: "RED", 17: "BLACK", 18: "RED", 19: "RED", 20: "BLACK",
    21: "RED", 22: "BLACK", 23: "RED", 24: "BLACK", 25: "RED", 26: "BLACK", 27: "RED",
    28: "BLACK", 29: "BLACK", 30: "RED", 31: "BLACK", 32: "RED", 33: "BLACK", 34: "RED",
    35: "BLACK", 36: "RED"
}

# Función para obtener el color de un número
def obtener_color(numero):
    if numero in number_color_map:
        color = number_color_map[numero]
        if color == RED:
            return "Rojo"
        elif color == BLACK:
            return "Negro"
        elif color == GREEN:
            return "Verde"
    return None

def mostrar_apuestas():
    font = pygame.font.Font(None, 24)
    text_color = BLACK
    x, y = 10, screen_height - 380

    for apuesta in apuestas:
        text = font.render(apuesta, True, text_color)
        text_rect = text.get_rect(topleft=(x, y))
        screen.blit(text, text_rect)
        y += 25  # Espaciado entre cada apuesta


#Organizar los números en tres columnas


# Función para dibujar la grilla con los números de la ruleta



# Función principal


def main():
    running = True
    spinning = False
    show_result = False
    
    spin_time = random.randint(
        5000, 10000
    )  # Tiempo de giro en milisegundos (5 segundos)
    current_rotation = 0
    result = None

    ball_radius = 15
    ball_center_x = roulette_center_x
    ball_center_y = roulette_center_y
    ball_angle = 0
    ball_speed = 0  # Inicializamos la velocidad de la bola en 0
    friction_coefficient = 0.99  # Coeficiente de fricción para la bola (ajustable)

    roulette_rotation = 0  # Inicializamos la rotación de la ruleta en 0
    roulette_speed = 2  # Velocidad de rotación de la ruleta (ajustable)
    roulette_friction_coefficient = 0.99  # Coeficiente de fricción para la ruleta (ajustable)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    if (
                        50 <= event.pos[0] <= 150
                        and 50 <= event.pos[1] <= 100
                        and not spinning
                    ):
                        spinning = True
                        result = None
                        current_rotation = 0
                        ball_speed = 5  # Calcular la velocidad necesaria para girar en 5 segundos
                        roulette_speed = 2  # Restablecer la velocidad de la ruleta
                        spin_start_time = pygame.time.get_ticks()  # Registrar el tiempo de inicio del giro
                        show_result = False
        screen.fill(WHITE)
 
        # Dibuja el título "Apuestas" en la parte superior de la lista de apuestas
        font = pygame.font.Font(None, 36)
        title_text = font.render("Apuestas", True, BLACK)
        title_rect = title_text.get_rect(midtop=(screen_width // 20, 450))
        screen.blit(title_text, title_rect)
        # Actualiza la rotación de la ruleta solo cuando está girando
        if spinning:
            roulette_speed *= roulette_friction_coefficient  # Aplicar fricción a la ruleta
            roulette_speed = round(roulette_speed, 12)

            # Asegúrate de que la rotación de la ruleta esté dentro del rango [0, 360]
            if roulette_speed < 0.01:  # Detener laruleta cuando su velocidad es muy baja
                roulette_speed = 0
            else:
                roulette_rotation += roulette_speed

                if roulette_rotation >= 360:
                    roulette_rotation -= 360

        # Dibuja la ruleta girando en sentido contrario a la bola
        draw_roulette(ball_angle, -roulette_rotation)
        mostrar_apuestas()
        draw_number_table()

        if spinning:
            current_rotation += ball_speed

            if current_rotation >= 360:
                current_rotation -= 360

            if (
                pygame.time.get_ticks() - spin_start_time > spin_time
            ):
                result = spin_roulette()
                show_result = True
                spinning = False
                ball_speed = 0  # Detener la esfera al instante al final del giro
            else:
                # Aplicar fricción para reducir la velocidad de la bola gradualmente
                ball_speed *= friction_coefficient
                ball_speed = round(ball_speed, 8)

            ball_x = ball_center_x + int(
                250 * math.cos(math.radians(ball_angle))
            )  # Calcular la posición de la bolita
            ball_y = ball_center_y + int(
                250 * math.sin(math.radians(ball_angle))
            )

            closest_number = None
            min_distance = float("inf")

            for i, number in enumerate(spanish_roulette_numbers):
                angle = math.radians(
                    i * (360 / len(spanish_roulette_numbers)) - 90 - roulette_rotation
                )
                x = int(
                    roulette_center_x + 250 * math.cos(angle)
                )
                y = int(
                   roulette_center_y + 250 * math.sin(angle)
                )

                # Calcular la distancia entre la posición de la bolita y las coordenadas de cada número
                distance = math.sqrt((x - ball_x) ** 2 + (y - ball_y) ** 2)

                if distance < min_distance:
                    min_distance = distance
                    closest_number = number

          
        # Mover la esfera alrededor del centro de la ruleta
        ball_angle += ball_speed
        if ball_angle >= 360:
            ball_angle -= 360

        ball_x = ball_center_x + int(
            250 * math.cos(math.radians(ball_angle))
        )  # Aumentamos la separación a 250
        ball_y = ball_center_y + int(
            250 * math.sin(math.radians(ball_angle))
        )  # Aumentamos la separación a 250
        pygame.draw.circle(screen, custom_color, (ball_x, ball_y), ball_radius)
        if not spinning and show_result:
                result_color = obtener_color(closest_number)
                font = pygame.font.Font(None, 36)
                text = font.render(f"Resultado: {closest_number} (Color : {result_color}) ", True, (0, 0, 0))
                text_rect = text.get_rect(
                top= 130, left= 10)
         
                screen.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()