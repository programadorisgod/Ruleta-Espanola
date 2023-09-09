import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.WINDOWPOS_CENTERED)
background_image = pygame.image.load('background.png')
shadow_image = pygame.image.load('fondo-ruleta.png')
pygame.display.set_caption("Simulación Ruleta Española MYS")


# Colores
BLACK = (28, 28, 20)
RED = (234, 38, 8)
WHITE = (255, 255, 255)
GREEN = (31, 227, 2)


roulette_center_x = screen_width // 3
roulette_center_y = screen_height // 2

# Números en la ruleta española en orden
spanish_roulette_numbers = [
    0,  32, 15, 19,  4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30,  8, 23, 10, 5, 24, 16, 33, 1, 20,
    14, 31,  9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]

spanish_roulette_numbers_order = [
    0,   1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36
]

# Colores correspondientes a cada número (rojo o negro)
number_colors = [
    GREEN, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK,
    RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK,
    RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED, BLACK, RED
]

number_color_map = {
    0:  GREEN, 32: RED, 15: BLACK, 19: RED, 4:  BLACK, 21: RED, 2:  BLACK, 25: RED,
    17: BLACK, 34: RED, 6:  BLACK, 27: RED, 13: BLACK, 36: RED, 11: BLACK, 30: RED,
    8:  BLACK, 23: RED, 10: BLACK, 5:  RED, 24: BLACK, 16: RED, 33: BLACK, 1:  RED, 
    20: BLACK, 14: RED, 31: BLACK, 9:  RED, 22: BLACK, 18: RED, 29: BLACK, 7:  RED,
    28: BLACK, 12: RED, 35: BLACK, 3:  RED, 26: BLACK
}


# Función para dibujar botones para cada número en la ruleta
def draw_number_buttons():
    font = pygame.font.Font(None, 36)
    x, y = screen_width // 1.5, 90  # Posición inicial para los botones
    cell_width, cell_height = 60, 45  # Tamaño de cada casilla
    border_width = 2  # Ancho del borde

    for i, number in enumerate(spanish_roulette_numbers_order):
        if i == 0:
            continue
        color = number_color_map[number]
        text_color = WHITE if color == BLACK else BLACK

        # Dibujar el borde alrededor de la casilla
        border_rect = pygame.Rect(x - border_width, y - border_width, cell_width + 2 * border_width, cell_height + 2 * border_width)
        pygame.draw.rect(screen, (206, 211, 208), border_rect)

        # Dibujar la casilla de apuesta
        pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))

        number_text = font.render(str(number), True, text_color)
        number_rect = number_text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        screen.blit(number_text, number_rect)

        # Mover a la siguiente fila después de cada 3 números
        if (i) % 3 == 0:
            x = screen_width // 1.5
            y += cell_height
        else:
            x += cell_width

    
    # Dibujar el triángulo para el cero
    pygame.draw.line(screen, (206, 211, 208), (851, 75), (942, 30), 3)
    pygame.draw.line(screen, (206, 211, 208), (942, 30), (1032, 75), 3)

    pygame.draw.line(screen, (206, 211, 208), (851, 88), (851, 75), 2)
    pygame.draw.line(screen, (206, 211, 208), (1033, 88), (1033, 75), 2)

    zero_text = font.render('0', True, WHITE)
    zero_rect = zero_text.get_rect(center=(942, 67.5))
    screen.blit(zero_text, zero_rect)

    # Dibujar las casillas de apuesta
    pygame.draw.line(screen, (206, 211, 208), (851, 88), (791, 88), 2)
    pygame.draw.line(screen, (206, 211, 208), (851, 630), (791, 630), 2)
    pygame.draw.line(screen, (206, 211, 208), (791, 88), (791, 630), 2)

    pygame.draw.line(screen, (206, 211, 208), (851, 223), (791, 223), 2)
    pygame.draw.line(screen, (206, 211, 208), (851, 358), (791, 358), 2)
    pygame.draw.line(screen, (206, 211, 208), (851, 493), (791, 493), 2)


    zero_text = font.render('1 a 18', True, WHITE)
    rotated_text = pygame.transform.rotate(zero_text, -90)
    screen.blit(rotated_text, rotated_text.get_rect(center=(820, 157)))

    zero_text = font.render('Rojo', True, WHITE)
    rotated_text = pygame.transform.rotate(zero_text, -90)
    screen.blit(rotated_text, rotated_text.get_rect(center=(820, 292)))

    zero_text = font.render('Negro', True, WHITE)
    rotated_text = pygame.transform.rotate(zero_text, -90)
    screen.blit(rotated_text, rotated_text.get_rect(center=(820, 427)))

    zero_text = font.render('19 a 36', True, WHITE)
    rotated_text = pygame.transform.rotate(zero_text, -90)
    screen.blit(rotated_text, rotated_text.get_rect(center=(820, 562)))
    



# Función para dibujar la ruleta y hacerla girar en sentido contrario a la bola
def draw_roulette(roulette_rotation):
    circle_radius = 250
    number_size = 30
    offset = 25  # Distancia desde el borde exterior hasta el número (ajustar según sea necesario)
    line_length = 1  # Longitud de las líneas negras (ajustar según sea necesario)
    angle_offset = 10  # Ajusta este valor para controlar el espacio entre los números
    roulette_rotation += 5  # Rota la ruleta en 5 grados en sentido contrario a las manecillas del reloj

    # Dibujar el fondo
    screen.blit(background_image, (0, 0))
    # Dibujar la sombra
    screen.blit(shadow_image, (0, 0))
    # Dibujar borde ruleta
    pygame.draw.circle(screen, (255, 175, 38), (roulette_center_x, roulette_center_y), 265)
    pygame.draw.circle(screen, (255, 210, 89), (roulette_center_x, roulette_center_y), 262)
    pygame.draw.circle(screen, (255, 175, 38), (roulette_center_x, roulette_center_y), 253)

    # Dibuja las líneas desde el borde exterior hacia adentro
    for i, number in enumerate(spanish_roulette_numbers):
        color = number_colors[i]
        angle = math.radians(i * (360 / len(spanish_roulette_numbers)) - 90 + roulette_rotation)

        # Calcula las coordenadas (x, y) en el borde del círculo exterior
        x = int(roulette_center_x + circle_radius * math.cos(angle))
        y = int(roulette_center_y + circle_radius * math.sin(angle))

        # Calcula las coordenadas para los vértices de los triángulos
        x1 = roulette_center_x
        y1 = roulette_center_y
        x2 = int(roulette_center_x + (circle_radius - line_length) * math.cos(angle))
        y2 = int(roulette_center_y + (circle_radius - line_length) * math.sin(angle))
        x3 = int(roulette_center_x + (circle_radius - line_length) * math.cos(angle - math.radians(angle_offset)))
        y3 = int(roulette_center_y + (circle_radius - line_length) * math.sin(angle - math.radians(angle_offset)))

        # Dibuja un triángulo desde el borde exterior hacia el centro
        pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3)])
        pygame.draw.line(screen, (105, 62, 40), (x1, y1), (x2, y2), 4)
        pygame.draw.line(screen, (105, 62, 40), (x1, y1), (x3, y3), 4)

    # Dibuja los números en la posición nueva, ligeramente ajustados y rotados hacia el centro
    for i, number in enumerate(spanish_roulette_numbers):
        color = number_colors[i]
        text_color = BLACK
        if color == BLACK:
            text_color = WHITE

        angle = math.radians(i * (360 / len(spanish_roulette_numbers)) - 90 + roulette_rotation)

        # Calcula las coordenadas nuevas para el número, alejado hacia adentro y un poco a la izquierda
        x = int(roulette_center_x + (circle_radius - offset) * math.cos(angle - math.radians(angle_offset)/2))  # Ajuste aquí
        y = int(roulette_center_y + (circle_radius - offset) * math.sin(angle - math.radians(angle_offset)/2))  # Ajuste aquí

        # Dibuja el número en la posición nueva, ligeramente ajustado y rotado hacia el centro
        font = pygame.font.Font(None, number_size)
        text_surface = font.render(str(number), True, text_color)

        # Calcula el ángulo de rotación para que el número mire hacia el centro
        rotation_angle = -math.degrees(angle) - 90  # Girar en sentido contrario (negativo) y hacia arriba (-90 grados)

        # Rota el texto del número
        text_surface = pygame.transform.rotate(text_surface, rotation_angle)

        # Calcula el rectángulo del texto rotado
        text_rect = text_surface.get_rect(center=(x, y))

        # Dibuja el número rotado en la posición nueva
        screen.blit(text_surface, text_rect)

    center_image = pygame.image.load("centro.png")

    # Dibuja el centro de la ruleta (imagen) y rota la imagen
    rotated_center_image = pygame.transform.rotate(center_image, -roulette_rotation + 5)
    center_rect = rotated_center_image.get_rect(center=(roulette_center_x, roulette_center_y))
    screen.blit(rotated_center_image, center_rect)

    # Dibuja el círculo exterior que representa el borde de la ruleta
    pygame.draw.circle(screen, (71, 43, 30), (roulette_center_x, roulette_center_y), circle_radius, 2)


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


# Función principal

def main():
    running = True
    spinning = False
    show_result = False
    
    spin_time = random.randint(7500, 8500)  # Tiempo de giro en milisegundos (5 segundos)
    current_rotation = 0

    ball_radius = 15
    ball_center_x = roulette_center_x
    ball_center_y = roulette_center_y
    ball_angle = 0
    ball_speed = 0  # Inicializamos la velocidad de la bola en 0
    friction_coefficient = 0.98  # Coeficiente de fricción para la bola (ajustable)

    roulette_rotation = 0  # Inicializamos la rotación de la ruleta en 0
    roulette_speed = 8  # Velocidad de rotación de la ruleta (ajustable)
    roulette_friction_coefficient = 0.98  # Coeficiente de fricción para la ruleta (ajustable)
    while running:
        # Dibuja la ruleta girando en sentido contrario a la bola
        draw_roulette( -roulette_rotation)

        # Dibuja los botones de los números después de los otros elementos
        draw_number_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse

                    # Coordenadas del punto de clic
                    click_x, click_y = event.pos

                    # Calcula la distancia desde el punto de clic al centro de la ruleta
                    distance = math.sqrt((click_x - roulette_center_x) ** 2 + (click_y - roulette_center_y) ** 2)


                    # Verifica si el jugador hizo clic en un número
                    for i, number in enumerate(spanish_roulette_numbers_order):
                        x, y = screen_width // 1.5, 50
                        cell_width, cell_height = 60, 60
                        rect = pygame.Rect(x, y, cell_width, cell_height)
                        if rect.collidepoint(event.pos):
                            # Establece la apuesta seleccionada al número
                            apuesta_seleccionada = number

                    if distance >= 200 and distance <= 265 and not spinning:
                        # Comienza a girar la ruleta
                        spinning = True
                        current_rotation = 0
                        ball_speed = 10  # Calcula la velocidad necesaria para girar en 5 segundos
                        roulette_speed = 8  # Restablece la velocidad de la ruleta
                        spin_start_time = pygame.time.get_ticks()  # Registrar el tiempo de inicio del giro
                        show_result = False

 
        # Actualiza la rotación de la ruleta solo cuando está girando
        if spinning:
            roulette_speed *= roulette_friction_coefficient  # Aplicar fricción a la ruleta
            roulette_speed = round(roulette_speed, 12)

            # Asegúrate de que la rotación de la ruleta esté dentro del rango [0, 360]
            if roulette_speed < 0.1:  # Detener laruleta cuando su velocidad es muy baja
                roulette_speed = 0
            else:
                roulette_rotation += roulette_speed
                if roulette_rotation >= 360:
                    roulette_rotation -= 360


        if spinning:
            current_rotation += ball_speed

            if current_rotation >= 360:
                current_rotation -= 360

            if (
                pygame.time.get_ticks() - spin_start_time > spin_time and ball_speed < 0.3
            ):
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
            165 * math.cos(math.radians(ball_angle))
        )  # Aumentamos la separación a 250
        ball_y = ball_center_y + int(
            165 * math.sin(math.radians(ball_angle))
        )  # Aumentamos la separación a 250
        pygame.draw.circle(screen, (215, 215, 210), (ball_x, ball_y), ball_radius)
        pygame.draw.circle(screen, (228, 225, 220), (ball_x, ball_y), ball_radius - 2)
        pygame.draw.circle(screen, (236, 231, 227), (ball_x, ball_y), ball_radius - 6)
        if not spinning and show_result:
                result_color = obtener_color(closest_number)
                font = pygame.font.Font(None, 36)
                text = font.render(f"Resultado: {closest_number} (Color : {result_color}) ", True, (0, 0, 0))
                text_rect = text.get_rect(top= 30, left= 10)
                screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()