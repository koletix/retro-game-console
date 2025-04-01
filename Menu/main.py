import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración de la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Retro Game Console')

# Cargar las miniaturas de los juegos
game_images = [
    pygame.image.load('./frogger/images/sprite_sheets_up.png'),  # Miniatura de Juego 1
    pygame.image.load('./images/game2.png'),  # Miniatura de Juego 2 (cambia según tus imágenes)
    pygame.image.load('./images/game3.png'),  # Miniatura de Juego 3
    pygame.image.load('./images/game4.png')   # Miniatura de Juego 4
]

# Ajustar tamaño de las imágenes de los juegos
game_images = [pygame.transform.scale(img, (200, 200)) for img in game_images]

# Fuente para el texto
font = pygame.font.SysFont('Arial', 50)

# Índice de juego seleccionado
selected_index = 0

# Función para dibujar el menú
def draw_menu():
    screen.fill(BLACK)

    # Título
    title_text = font.render('SELECT GAME', True, GREEN)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    # Mostrar las miniaturas de los juegos
    for i, img in enumerate(game_images):
        x_position = screen_width // 2 - (len(game_images) * 220) // 2 + i * 220
        y_position = 300

        # Dibujar el cuadro alrededor del juego seleccionado
        if i == selected_index:
            pygame.draw.rect(screen, GREEN, (x_position - 10, y_position - 10, 220, 220), 5)

        screen.blit(img, (x_position, y_position))

    # Instrucciones
    instructions_text = font.render('Use Arrow Keys to select', True, BLUE)
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, screen_height - 100))

    pygame.display.update()

# Función para manejar la entrada del usuario
def handle_input():
    global selected_index
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        selected_index = (selected_index - 1) % len(game_images)
    elif keys[pygame.K_RIGHT]:
        selected_index = (selected_index + 1) % len(game_images)
    elif keys[pygame.K_RETURN]:
        print(f"Game {selected_index + 1} selected")
        # Aquí puedes poner el código para iniciar el juego seleccionado

# Ciclo principal
def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar el menú y manejar la entrada
        draw_menu()
        handle_input()

        clock.tick(60)  # Mantener la tasa de fotogramas a 60 FPS

# Iniciar el juego
if __name__ == '__main__':
    main()
