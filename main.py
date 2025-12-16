import pygame
import random
import sys
import os

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 5
BASKET_SPEED = 30
FRUIT_SPAWN_RATE = 60  # setiap 30 frame, ada buah baru

def load_image(filename):
    """Memuat gambar dari folder assets."""
    path = os.path.join("assets", filename)
    return pygame.image.load(path).convert_alpha()

class Basket:
    def __init__(self):
        self.image = load_image("basket.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
        self.speed = BASKET_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fruit:
    FRUIT_TYPES = ["apple.png", "banana.png", "orange.png"]

    def __init__(self):
        fruit_image = random.choice(self.FRUIT_TYPES)
        self.image = load_image(fruit_image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += GRAVITY

    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    # Setup layar
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catching Falling Fruits")
    clock = pygame.time.Clock()

    # Objek game
    basket = Basket()
    fruits = []
    score = 0
    lives = 3
    fruit_timer = 0

    # Font untuk teks
    font = pygame.font.SysFont(None, 36)

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input pemain
        keys = pygame.key.get_pressed()

        # Update basket
        basket.update(keys)

        # Spawn buah secara berkala
        fruit_timer += 1
        if fruit_timer >= FRUIT_SPAWN_RATE:
            fruits.append(Fruit())
            fruit_timer = 0

        # Update buah
        for fruit in fruits[:]:
            fruit.update()
            # Tabrakan dengan basket
            if basket.rect.colliderect(fruit.rect):
                fruits.remove(fruit)
                score += 1
            # Buah jatuh ke bawah → kehilangan nyawa
            elif fruit.is_off_screen():
                fruits.remove(fruit)
                lives -= 1
                if lives <= 0:
                    running = False  # Game over

        # Gambar semuanya
        screen.fill((135, 206, 250))  # Warna langit biru

        basket.draw(screen)
        for fruit in fruits:
            fruit.draw(screen)

        # Tampilkan skor dan nyawa
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    # Tampilkan layar game over
    game_over_text = font.render("GAME OVER! Tekan apa saja untuk keluar.", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Tunggu 2 detik

    # Tunggu input sebelum keluar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()