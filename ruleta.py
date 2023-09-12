import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width  = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.WINDOWPOS_CENTERED)
background_image = pygame.image.load('background.png')
shadow_image     = pygame.image.load('fondo-ruleta.png')
pygame.display.set_caption("Simulación Ruleta Española MYS")


# Colores
BLACK = ( 28,  28, 20)
RED   = (234,  38, 8)
WHITE = (255, 255, 255)
WHITED = (206, 211, 208)
GREEN = ( 31, 227, 2)


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

ubicaciones_tabla = []
money_per_ficha = 0

# Crear función para mostrar la capa de inicio
def show_start_layer():
    running = True
    amount = 0

    background = pygame.image.load('fondo_inicio.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en el botón "Modo Estándar"
                if 177 <= event.pos[0] <= 570 and 311 <= event.pos[1] <= 410:
                    amount = 10000
                    running = False
                # Verificar si se hizo clic en el botón "Modo Premium"
                elif 711 <= event.pos[0] <= 1104 and 311 <= event.pos[1] <= 410:
                    amount = 50000
                    running = False

        screen.blit(background, (0, 0))


        pygame.display.flip()
    
    return amount


# Función para dibujar la tabla de dinero por color
def draw_money_table(fichas, amount):
    font = pygame.font.Font(None, 36)
    money_per_ficha = amount

    # Calcula el dinero total para cada tipo de ficha
    dinero_rojo_carmesi = sum(1 for ficha in fichas if ficha.image_name == "ficha rojo carmesi.png") * money_per_ficha
    dinero_azul_oscuro = sum(1 for ficha in fichas if ficha.image_name == "ficha azul oscuro.png") * money_per_ficha
    dinero_purpura = sum(1 for ficha in fichas if ficha.image_name == "ficha purpura.png") * money_per_ficha
    dinero_azul = sum(1 for ficha in fichas if ficha.image_name == "ficha azul.png") * money_per_ficha

    pygame.draw.line(screen, WHITED, (10, 10), (220, 10), 3)  # Línea superior
    pygame.draw.line(screen, WHITED, (10, 10), (10, 143), 3)  # Línea izquierda
    pygame.draw.line(screen, WHITED, (220, 10), (220, 143), 3)  # Línea derecha
    pygame.draw.line(screen, WHITED, (10, 143), (220, 143), 3)  # Línea inferior
    pygame.draw.line(screen, WHITED, (55, 10), (55, 143), 3) # Línea interna

    # Dibuja cuadros de colores para representar los tipos de ficha
    pygame.draw.rect(screen, (152, 30,  55), (20,  20, 25, 25))  # Rojo Carmesí
    pygame.draw.rect(screen, (30,  78, 152), (20,  50, 25, 25))  # Azul Oscuro
    pygame.draw.rect(screen, (99,  29, 151), (20,  80, 25, 25))  # Purpura
    pygame.draw.rect(screen, (0,  186, 237), (20, 110, 25, 25))  # Azul

    text_rojo_carmesi = font.render(f'${dinero_rojo_carmesi}', True, WHITED)
    text_azul_oscuro  = font.render(f'${dinero_azul_oscuro}', True, WHITED)
    text_purpura      = font.render(f'${dinero_purpura}', True, WHITED)
    text_azul         = font.render(f'${dinero_azul}', True, WHITED)

    screen.blit(text_rojo_carmesi, (70,  20))
    screen.blit(text_azul_oscuro,  (70,  50))
    screen.blit(text_purpura,      (70,  80))
    screen.blit(text_azul,         (70, 110))



# Función para dibujar la tabla de apuestas de la ruleta
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
        pygame.draw.rect(screen, WHITED, border_rect)

        # Dibujar la casilla de apuesta
        pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))

        number_text = font.render(str(number), True, text_color)
        number_rect = number_text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        screen.blit(number_text, number_rect)

        ubicaciones_tabla.append({'pos': (x, y + 6),'rect': pygame.Rect(x, y, cell_width, cell_height)})

        # Mover a la siguiente fila después de cada 3 números
        if (i) % 3 == 0:
            x = screen_width // 1.5
            y += cell_height
        else:
            x += cell_width


    
    # Dibujar el triángulo para el cero
    pygame.draw.line(screen, WHITED, (851, 75), (942, 30), 3)
    pygame.draw.line(screen, WHITED, (942, 30), (1032, 75), 3)

    pygame.draw.line(screen, WHITED, (851, 88), (851, 75), 2)
    pygame.draw.line(screen, WHITED, (1033, 88), (1033, 75), 2)

    zero_text = font.render('0', True, WHITE)
    zero_rect = zero_text.get_rect(center=(942, 67.5))
    screen.blit(zero_text, zero_rect)

    ubicaciones_tabla.append({'pos': (912, 51.5), 'rect': pygame.Rect(853, 32, 180, 56)})

    # Dibujar las casillas de apuesta
    pygame.draw.line(screen, WHITED, (851, 88), (791, 88), 2)
    pygame.draw.line(screen, WHITED, (851, 630), (791, 630), 2)
    pygame.draw.line(screen, WHITED, (791, 88), (791, 630), 2)

    pygame.draw.line(screen, WHITED, (851, 223), (791, 223), 2)
    pygame.draw.line(screen, WHITED, (851, 358), (791, 358), 2)
    pygame.draw.line(screen, WHITED, (851, 493), (791, 493), 2)


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

    ubicaciones_tabla.append({'pos': (791, 144), 'rect': pygame.Rect(793,  90,  58, 133)})
    ubicaciones_tabla.append({'pos': (791, 278), 'rect': pygame.Rect(793, 225,  58, 133)})
    ubicaciones_tabla.append({'pos': (791, 412), 'rect': pygame.Rect(793, 360,  58, 133)})
    ubicaciones_tabla.append({'pos': (791, 547), 'rect': pygame.Rect(793, 495,  58, 135)})



    pygame.draw.line(screen, WHITED, (851, 631), (851, 676), 2)
    pygame.draw.line(screen, WHITED, (851, 676), (1034, 676), 2)
    pygame.draw.line(screen, WHITED, (1033, 631), (1033, 676), 2)
    pygame.draw.line(screen, WHITED, (941, 631), (941, 676), 2)

    zero_text = font.render('Par', True, WHITE)
    screen.blit(zero_text, zero_text.get_rect(center=(896, 656)))

    zero_text = font.render('Impar', True, WHITE)
    screen.blit(zero_text, zero_text.get_rect(center=(988, 656)))

    ubicaciones_tabla.append({'pos': (865, 639), 'rect': pygame.Rect(853, 632,  88, 44)})
    ubicaciones_tabla.append({'pos': (955, 639), 'rect': pygame.Rect(943, 632,  90, 44)})


# Clase para representar una ficha
class Ficha():
    def __init__(self, image, x, y):
        self.image_name = image
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.resaltada = False 
        self.apuesta = False
        self.coordenadas = (x, y)

# Funcion para dibujar las fichas de apostar
def cargar_fichas(a, b, c, d):
    fichas = []
    for i in range(1, a + 1):
        fichas.append(Ficha("ficha rojo carmesi.png", 1055, 115.5))
    for i in range(1, b + 1):
        fichas.append(Ficha("ficha azul oscuro.png", 1055, 255.5))
    for i in range(1, c + 1):
        fichas.append(Ficha("ficha purpura.png", 1055, 380.5))
    for i in range(1, d + 1):
        fichas.append(Ficha("ficha azul.png", 1055, 515.5))
    return fichas

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



def verificar_apuestas_y_calcular_ganancias(fichas, closest_number, result_color):
    result_number = closest_number
    result_color = obtener_color(result_number)

    # Crear diccionarios para llevar un registro de las apuestas ganadoras y perdedoras
    apuestas_resultados  = {
        "ficha rojo carmesi.png": 0,
        "ficha azul oscuro.png": 0,
        "ficha purpura.png": 0,
        "ficha azul.png": 0}

    # Iterar a través de las fichas y verificar las apuestas
    for ficha in fichas:
        count = 0
        if ficha.apuesta:
            if result_number != 0 and ficha.rect.colliderect(ubicaciones_tabla[result_number-1]['rect']):
                apuestas_resultados[ficha.image_name] += 35
            elif (result_number == 0 and ficha.rect.colliderect(ubicaciones_tabla[36]['rect'])):
                apuestas_resultados[ficha.image_name] += 35
            else:
                count += 1
            if 0 < result_number < 19 and ficha.rect.colliderect(ubicaciones_tabla[37]['rect']):
                apuestas_resultados[ficha.image_name] += 1
            else:
                count += 1
            if result_color == "Rojo" and ficha.rect.colliderect(ubicaciones_tabla[38]['rect']):
                apuestas_resultados[ficha.image_name] += 1
            else:
                count += 1
            if result_color == "Negro" and ficha.rect.colliderect(ubicaciones_tabla[39]['rect']):
                apuestas_resultados[ficha.image_name] += 1
            else:
                count += 1
            if 18 < result_number < 37 and ficha.rect.colliderect(ubicaciones_tabla[40]['rect']):
                apuestas_resultados[ficha.image_name] += 1
            else:
                count += 1
            if (result_number != 0 and result_number % 2 == 0 and ficha.rect.colliderect(ubicaciones_tabla[41]['rect'])
                or result_number % 2 != 0 and ficha.rect.colliderect(ubicaciones_tabla[42]['rect'])):
                apuestas_resultados[ficha.image_name] += 1
            else:
                count += 1
            if (count > 5):
                apuestas_resultados[ficha.image_name] -= 1

            ficha.apuesta = False

    return apuestas_resultados




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
    show_profits = False
    
    current_rotation = 0

    fichas = cargar_fichas(5, 5, 5, 5)

    ball_center_x = roulette_center_x
    ball_center_y = roulette_center_y
    ball_angle = random.randint(0, 360)
    ball_speed = 0  # Inicializamos la velocidad de la bola en 0
    friction_coefficient = 0.98  # Coeficiente de fricción para la bola (ajustable)

    roulette_rotation = 0  # Inicializamos la rotación de la ruleta en 0
    roulette_speed = random.randint(8, 20)  # Velocidad de rotación de la ruleta (ajustable)
    roulette_friction_coefficient = 0.98  # Coeficiente de fricción para la ruleta (ajustable)

    amount = show_start_layer()

    result_color = ""
    apuestas_resultados = {}
    fichas_count = []

    while running:
        # Dibuja la ruleta girando en sentido contrario a la bola
        draw_roulette( -roulette_rotation)

        # Dibuja la tabla de efectivo actual
        draw_money_table(fichas, amount)

        # Dibuja los botones de los números después de los otros elementos
        draw_number_buttons()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Coordenadas del punto de clic
                click_x, click_y = event.pos

                if event.button == 3: # Boton derecho del mouse
                    if not spinning:
                        count = 0
                        for i, ficha in enumerate(reversed(fichas)):
                            if ficha.rect.collidepoint(event.pos):
                                count += 1
                                if ficha.apuesta == True:
                                    seleccionada = False
                                    for fich in fichas:
                                        if fich.resaltada: seleccionada = True

                                    if not seleccionada and count <= 4: 
                                        ficha.apuesta = False
                                    elif count > 4:
                                        count = 0
                                        break
                                else:
                                    # Cambia el estado de resaltado de la ficha
                                    if count <= 4: 
                                        ficha.resaltada = not ficha.resaltada
                            else:
                                ficha.resaltada = False
                                    

                if event.button == 1:  # Botón izquierdo del mouse
                    # Calcula la distancia desde el punto de clic al centro de la ruleta
                    distance = math.sqrt((click_x - roulette_center_x) ** 2 + (click_y - roulette_center_y) ** 2)

                    if not spinning:
                        for ficha in reversed(fichas):
                            if ficha.rect.collidepoint(event.pos):
                                if ficha.apuesta == True:
                                    seleccionada = False
                                    for fich in fichas:
                                        if fich.resaltada: seleccionada = True

                                    if not seleccionada: 
                                        ficha.apuesta = False
                                    break
                                else:
                                    for fich in fichas:
                                        if ficha != fich: fich.resaltada = False
                                    # Cambia el estado de resaltado de la ficha
                                    ficha.resaltada = not ficha.resaltada
                                    break

                        for i, ficha in enumerate(fichas):    
                            if ficha.resaltada:
                                for ubicacion in ubicaciones_tabla:
                                    if ubicacion['rect'].collidepoint(event.pos):
                                        # Colocar la ficha en la casilla
                                        ficha.resaltada = False
                                        ficha.apuesta = True
                                        if i != 0: ficha.rect.x = ubicacion['pos'][0] + ((30 / (len(fichas))) * i)
                                        else: ficha.rect.x = ubicacion['pos'][0]
                                        ficha.rect.y = ubicacion['pos'][1]
                                        ficha.rect.width = 30
                                        ficha.rect.height = 31
                                        break


                    if distance >= 200 and distance <= 265 and not spinning:
                        # Comienza a girar la ruleta
                        spinning = True
                        current_rotation = 0
                        ball_speed = random.randint(9, 40)  # Calcula la velocidad necesaria para girar en 5 segundos
                        roulette_speed = random.randint(8, 35)  # Restablece la velocidad de la ruleta
                        show_result = False
                        show_profits = False

        for ficha in fichas:
            if ficha.resaltada:
                # Mueve ligeramente la ficha si está resaltada
                ficha.rect.x = 1070
                screen.blit(ficha.image, ficha.rect)
            else:
                if not ficha.apuesta:
                    ficha.rect.width = 90
                    ficha.rect.height = 100
                    ficha.rect.x, ficha.rect.y = ficha.coordenadas
                    screen.blit(ficha.image, ficha.rect)
                else:
                    screen.blit(pygame.transform.scale(ficha.image, (30, 31)), ficha.rect)

        # Contar fichas no apostadas y crear textos
        fichas_rojas_act = sum(1 for ficha in fichas if not ficha.apuesta and ficha.image_name == "ficha rojo carmesi.png")
        fichas_rojas = sum(1 for ficha in fichas if ficha.image_name == "ficha rojo carmesi.png")

        fichas_azules_oscuras_act = sum(1 for ficha in fichas if not ficha.apuesta and ficha.image_name == "ficha azul oscuro.png")
        fichas_azules_oscuras = sum(1 for ficha in fichas if ficha.image_name == "ficha azul oscuro.png")

        fichas_purpuras_act = sum(1 for ficha in fichas if not ficha.apuesta and ficha.image_name == "ficha purpura.png")
        fichas_purpuras = sum(1 for ficha in fichas if ficha.image_name == "ficha purpura.png")

        fichas_azules_act = sum(1 for ficha in fichas if not ficha.apuesta and ficha.image_name == "ficha azul.png")
        fichas_azules = sum(1 for ficha in fichas if ficha.image_name == "ficha azul.png")


        font = pygame.font.Font(None, 36)
        texto_fichas_rojas = font.render(f'{fichas_rojas_act}/{fichas_rojas}', True, WHITED)
        texto_fichas_azules_oscuras = font.render(f'{fichas_azules_oscuras_act}/{fichas_azules_oscuras}', True, WHITED)
        texto_fichas_purpuras = font.render(f'{fichas_purpuras_act}/{fichas_purpuras}', True, WHITED)
        texto_fichas_azules = font.render(f'{fichas_azules_act}/{fichas_azules}', True, WHITED)

        screen.blit(texto_fichas_rojas, texto_fichas_rojas.get_rect(center=(1210, 165)))
        screen.blit(texto_fichas_azules_oscuras, texto_fichas_azules_oscuras.get_rect(center=(1210, 305)))
        screen.blit(texto_fichas_purpuras, texto_fichas_purpuras.get_rect(center=(1210, 430)))
        screen.blit(texto_fichas_azules, texto_fichas_azules.get_rect(center=(1210, 565)))
 
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

            if (ball_speed < 0.3):
                show_result = True
                show_profits = True
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

        pygame.draw.circle(screen, (215, 215, 210), (ball_x, ball_y), 15)
        pygame.draw.circle(screen, (228, 225, 220), (ball_x, ball_y), 13)
        pygame.draw.circle(screen, (236, 231, 227), (ball_x, ball_y), 9)


        if not spinning and show_profits:
            
            if show_result:
                result_color = obtener_color(closest_number)
                apuestas_resultados = verificar_apuestas_y_calcular_ganancias(fichas, closest_number, result_color)
                fichas_count = [0,0,0,0]
                
                for ficha in fichas:
                    if ficha.image_name == "ficha rojo carmesi.png":
                        fichas_count[0] += 1
                    elif ficha.image_name == "ficha azul oscuro.png":
                        fichas_count[1] += 1
                    elif ficha.image_name == "ficha purpura.png":
                        fichas_count[2] += 1
                    else:
                        fichas_count[3] += 1
            
            # Mostrar ganancias y perdidas
            text_rojo_carmesi = font.render(f' {apuestas_resultados["ficha rojo carmesi.png"]}', True, WHITED)
            if apuestas_resultados["ficha rojo carmesi.png"] > -1:
                text_rojo_carmesi = font.render(f'+{apuestas_resultados["ficha rojo carmesi.png"]}', True, WHITED)
            
            text_azul_oscuro = font.render(f' {apuestas_resultados["ficha azul oscuro.png"]}', True, WHITED)
            if apuestas_resultados["ficha azul oscuro.png"] > -1:
                text_azul_oscuro = font.render(f'+{apuestas_resultados["ficha azul oscuro.png"]}', True, WHITED)

            text_purpura = font.render(f' {apuestas_resultados["ficha purpura.png"]}', True, WHITED)
            if apuestas_resultados["ficha purpura.png"] > -1:
                text_purpura = font.render(f'+{apuestas_resultados["ficha purpura.png"]}', True, WHITED)
            
            text_azul = font.render(f' {apuestas_resultados["ficha azul.png"]}', True, WHITED)
            if apuestas_resultados["ficha azul.png"] > -1:
                text_azul = font.render(f'+{apuestas_resultados["ficha azul.png"]}', True, WHITED)
            

            screen.blit(text_rojo_carmesi, (230,  20))
            screen.blit(text_azul_oscuro,  (230,  50))
            screen.blit(text_purpura,      (230,  80))
            screen.blit(text_azul,         (230, 110))

            if show_result:
                fichas_count[0] += apuestas_resultados["ficha rojo carmesi.png"]
                fichas_count[1] += apuestas_resultados["ficha azul oscuro.png"]
                fichas_count[2] += apuestas_resultados["ficha purpura.png"]
                fichas_count[3] += apuestas_resultados["ficha azul.png"]

                # Reflejarlas en las fichas
                fichas = cargar_fichas(fichas_count[0], fichas_count[1], fichas_count[2], fichas_count[3])
                print(closest_number, result_color)
                show_result = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()