import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configurar la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Retro Game Console')

# Cargar las miniaturas de los juegos (usa tus propias imágenes)
game_images = [
    pygame.image.load('./menu/images menu/frogger.jpg'),  # Miniatura de Juego 1
    pygame.image.load('./menu/images menu/frogger.jpg'),  # Miniatura de Juego 2 (ajusta las rutas)
    pygame.image.load('./menu/images menu/frogger.jpg'),  # Miniatura de Juego 3
    pygame.image.load('./menu/images menu/frogger.jpg')   # Miniatura de Juego 4
]

# Ajustar tamaño de las imágenes de los juegos
game_images = [pygame.transform.scale(img, (200, 200)) for img in game_images]

# Fuentes para texto
font = pygame.font.SysFont('Arial', 50)

# Índice de juego seleccionado
selected_index = 0
scrolling = False

# Crear la superficie para el blur
def create_blur_surface(image):
    """Aplica un efecto de desenfoque (blur) a la imagen."""
    blurred_image = pygame.Surface(image.get_size())
    blurred_image.fill((0, 0, 0))  # Crea un filtro oscuro
    blurred_image.blit(image, (0, 0))
    return pygame.transform.smoothscale(blurred_image, image.get_size())

# Función para dibujar el menú
def draw_menu():
    global selected_index, scrolling
    screen.fill(BLACK)

    # Título
    title_text = font.render('SELECT GAME', True, GREEN)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    # Dibujar las miniaturas de los juegos
    for i, img in enumerate(game_images):
        x_position = screen_width // 2 - (len(game_images) * 220) // 2 + i * 220
        y_position = screen_height // 2 + 100

        # Efecto de blur para los juegos no seleccionados
        if i != selected_index:
            img = create_blur_surface(img)  # Aplicamos el blur

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
    global selected_index, scrolling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not scrolling:
        selected_index = (selected_index - 1) % len(game_images)
        scrolling = True  # Evitar que se cambie de juego rápidamente

    elif keys[pygame.K_RIGHT] and not scrolling:
        selected_index = (selected_index + 1) % len(game_images)
        scrolling = True  # Evitar que se cambie de juego rápidamente

    elif keys[pygame.K_RETURN]:
        print(f"Game {selected_index + 1} selected")
        # Aquí puedes poner el código para iniciar el juego seleccionado

# Ciclo principal
def main():
    global scrolling
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar el menú y manejar la entrada
        draw_menu()
        handle_input()

        # Animación de desplazamiento a la derecha (scrolling)
        if scrolling:
            pygame.time.wait(200)  # Pausa para la animación
            scrolling = False  # Desactivar el scrolling

        clock.tick(60)  # Mantener la tasa de fotogramas a 60 FPS

# Iniciar el juego
if __name__ == '__main__':
    main()
