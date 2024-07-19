import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 480
screen_height = 480
cell_size = 20
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Cargar las imágenes
snake_head_image = pygame.image.load('gus.png')
snake_head_image = pygame.transform.scale(snake_head_image, (cell_size, cell_size))
fruit_image = pygame.image.load('fruit.png')
fruit_image = pygame.transform.scale(fruit_image, (cell_size, cell_size))

# Función para mostrar mensaje de Game Over
def show_game_over_message():
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render('Perdiste el juego!', True, RED)
    screen.blit(game_over_text, (screen_width // 4, screen_height // 2))
    pygame.display.flip()
    pygame.time.wait(6000)  # Espera 6 segundos antes de cerrar

# Función principal del juego
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.change_direction(RIGHT)

        if not game_over:
            if snake.move():
                if snake.collides_with_food(food):
                    snake.eat_food()
                    food.randomize_position()
                
                if snake.check_collision():
                    game_over = True
                    show_game_over_message()
                    # Reiniciar el juego después de mostrar el mensaje
                    snake.reset()
                    game_over = False
            else:
                game_over = True
                show_game_over_message()
                # Reiniciar el juego después de mostrar el mensaje
                snake.reset()
                game_over = False

        # Dibujar todo
        screen.fill(BLACK)
        snake.draw()
        food.draw()
        pygame.display.flip()

        clock.tick(10)  # Velocidad de actualización

class Snake:
    def __init__(self):
        self.body = [(screen_width // 2, screen_height // 2)]
        self.length = 1
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * cell_size) % screen_width, (head_y + dir_y * cell_size) % screen_height)
        if new_head in self.body[1:]:
            return False
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()
        return True

    def change_direction(self, direction):
        self.direction = direction

    def collides_with_food(self, food):
        return self.body[0] == food.position

    def eat_food(self):
        self.length += 1

    def check_collision(self):
        return any(self.body[0] == part for part in self.body[1:])

    def draw(self):
        # Rotar la imagen de la cabeza según la dirección
        if self.direction == UP:
            rotated_head = pygame.transform.rotate(snake_head_image, 90)
        elif self.direction == DOWN:
            rotated_head = pygame.transform.rotate(snake_head_image, 270)
        elif self.direction == LEFT:
            rotated_head = pygame.transform.rotate(snake_head_image, 180)
        elif self.direction == RIGHT:
            rotated_head = snake_head_image

        for i, segment in enumerate(self.body):
            if i == 0:
                screen.blit(rotated_head, segment)
            else:
                pygame.draw.rect(screen, BROWN, (segment[0], segment[1], cell_size, cell_size))

    def reset(self):
        self.body = [(screen_width // 2, screen_height // 2)]
        self.length = 1
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

class Food:
    def __init__(self):
        self.position = (random.randint(0, grid_width - 1) * cell_size, random.randint(0, grid_height - 1) * cell_size)

    def draw(self):
        screen.blit(fruit_image, self.position)

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * cell_size, random.randint(0, grid_height - 1) * cell_size)

if __name__ == "__main__":
    main()

