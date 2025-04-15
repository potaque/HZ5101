import pygame
from sprites import *
from config import *
import sys
import os
import asyncio

async def main():
    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            pygame.display.set_caption("My Game")
            self.clock = pygame.time.Clock()
            font_path = os.path.join("font", "Quire Sans.ttf")
            self.font = pygame.font.Font(font_path, 32)
            self.running = True
            self.character_spritesheet = Spritesheet("img/character.png")
            self.terrain_spritesheet = Spritesheet("img/terrain.png")
            self.obj_spritesheet = Spritesheet("img/obj.png")
            self.all_sprites = pygame.sprite.Group()
            self.blocks = pygame.sprite.Group()
            self.objects = pygame.sprite.Group()
            self.path = pygame.sprite.Group()
            self.current_interaction = None
            self.current_interaction = None
            self.dialogue_text = ""
            self.text_timer = 0
            # self.intro = type('Intro', (object,), {})()
            # self.intro.background = pygame.image.load("img/introbackground.png").convert()

        def createTilemap(self):
            for i, row in enumerate(tilemap):  # Loop through rows
                for j, column in enumerate(row):  # Loop through columns
                    ground = Ground(self, j, i)
                    if column == 'B':  # If the tile is a block
                        block = Block(self, j, i)  # Create a Block object
                        self.all_sprites.add(block)  # Add it to the all_sprites group
                        self.blocks.add(block)  # Add it to the blocks group
                    if column == 'A':  # If the tile is a block
                        block = Block(self, j, i)  # Create a Block object
                        self.all_sprites.add(block)  # Add it to the all_sprites group
                        self.blocks.add(block)  # Add it to the blocks group
                    if column == 'C':  # If the tile is a block
                        block = Block(self, j, i)  # Create a Block object
                        self.all_sprites.add(block)  # Add it to the all_sprites group
                    if column == 'O': #If the tile is an object
                        object = Object(self, j, i)  # Create an Object object
                        self.all_sprites.add(object)  # Add it to the all_sprites group
                        self.objects.add(object)  # Add it to the objects group
                    if column == 'P':  # If the tile is the player
                        self.player = Player(self, j, i)  # Create the Player object
                        self.all_sprites.add(self.player)  # Add it to the all_sprites group
        
        def new(self):
            self.playing = True
            self.all_sprites = pygame.sprite.LayeredUpdates()
            self.blocks = pygame.sprite.LayeredUpdates()
            self.objects = pygame.sprite.LayeredUpdates()
            self.createTilemap() 

        def events(self):
            # game loop events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self.current_interaction:
                        if event.type == pygame.KEYDOWN:
                            if isinstance(self.current_interaction, Object):
                                self.dialogue_text = "You picked up a milk!"
                                self.text_timer = pygame.time.get_ticks()
                                self.current_interaction.kill()  # Remove the object from the game
                                self.current_interaction = None

        def update (self):
            # game loop update
            self.all_sprites.update()

            hits = pygame.sprite.spritecollide(self.player, self.objects, False)
            self.current_interaction = None
            for obj in hits:
                if isinstance(obj, Object):  # You can add more types here
                    self.current_interaction = obj

        def draw(self):
            # game loop draw
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            # press E to interact prompt
            if self.current_interaction:
                prompt = self.font.render("Press E to interact", True, WHITE)
                prompt_rect = prompt.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 80))
                self.screen.blit(prompt, prompt_rect)

            
            # Show dialogue after interaction
            if self.dialogue_text and pygame.time.get_ticks() - self.text_timer < 2000:
                text_surface = self.font.render(self.dialogue_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
                text_bg = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
                text_bg.fill(BLACK)
                text_bg.set_alpha(200)
                self.screen.blit(text_bg, (text_rect.x - 10, text_rect.y - 5))
                self.screen.blit(text_surface, text_rect)
            else:
                self.dialogue_text = ""


                self.clock.tick(FPS)
            
            pygame.display.update()

        def main(self):
            #game loop
            while self.playing:
                self.events()
                self.update()
                self.draw()
            self.running = False

        def game_over(self):
            pass

        # def intro_screen(self):
        #         intro = True
        #         title = self.font.render('My Game', True, BLACK)
        #         title_rect = title.get_rect(x=10, y=10)
        #         play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)
        #         while intro:
        #             for event in pygame.event.get():
        #                 if event.type == pygame.QUIT:
        #                     intro = False
        #                     self.running = False
        #         mouse_pos = pygame.mouse.get_pos()
        #         mouse_pressed = pygame.mouse.get_pressed()
                
        #         if play_button.is_pressed(mouse_pos, mouse_pressed):
        #             intro = False
                
        #         self.screen.blit(self.intro.background, (0, 0))
        #         self.screen.blit(title, title_rect)
        #         self.screen.blit(play_button.image, play_button.rect)
        #         self.clock.tick(FPS)
        #         pygame.display.update()
    g = Game()
    # g.intro_screen()
    g.new()
    while g.running:
        g.main()
        g.game_over()

    pygame.quit()
    sys.exit()

    await asyncio.sleep(0)

asyncio.run(main())
