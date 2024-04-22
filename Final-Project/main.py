from settings import *
from tetris import Tetris, Text
import sys
import pathlib
import pygame, sys
from button import Button
from pygame import mixer

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/bgg.jpg")
mixer.music.load("assets/sound.mp3")
mixer.music.play(-1)

def get_font(size): 
    return pygame.font.Font("assets/font/font.ttf", size)

def play():
    while True:
        mixer.music.load("assets/background.mp3")
        mixer.music.play(-1)

        class App:
            def __init__(self):
                pg.init()
                pg.display.set_caption('Tetris')
                self.screen = pg.display.set_mode(WIN_RES)
                self.clock = pg.time.Clock()
                self.set_timer()
                self.images = self.load_images()
                self.tetris = Tetris(self)
                self.text = Text(self)

            def load_images(self):
                files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
                images = [pg.image.load(file).convert_alpha() for file in files]
                images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
                return images

            def set_timer(self):
                self.user_event = pg.USEREVENT + 0
                self.fast_user_event = pg.USEREVENT + 1
                self.anim_trigger = False
                self.fast_anim_trigger = False
                pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
                pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

            def update(self):
                self.tetris.update()
                self.clock.tick(FPS)

            def draw(self):
                self.screen.fill(color=BG_COLOR)
                self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
                self.tetris.draw()
                self.text.draw()
                pg.display.flip()

            def check_events(self):
                self.anim_trigger = False
                self.fast_anim_trigger = False
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.KEYDOWN:
                        self.tetris.control(pressed_key=event.key)
                    elif event.type == self.user_event:
                        self.anim_trigger = True
                    elif event.type == self.fast_user_event:
                        self.fast_anim_trigger = True


            def run(self):
                while True:
                    self.check_events()
                    self.update()
                    self.draw()


        if __name__ == '__main__':
            app = App()
            app.run()

       
    


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Tetris Game Instructions", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

       
        instructions = [
            "1. Objective: The main goal of Tetris is to manipulate the Tetriminos (geometric shapes composed of four square blocks ",
            "   each) by moving them sideways and rotating them, with the aim of creating a horizontal line of ten blocks without gaps.",
            "2. Starting the Game: When you start the game, Tetriminos will begin to fall from the top of the playing field, which is",
            "   called the Matrix."
            "3. Controlling Tetriminos:",
            "   - Move Left/Right: Use the left and right arrow keys to move the Tetriminos sideways.",
            "   - Rotate: Press the up arrow key to rotate the Tetriminos clockwise. Some versions of the game also allow you to ",
            "     rotate counterclockwise by pressing a different key (often 'Z' or 'Ctrl').",
            "   - Soft Drop: Pressing the down arrow key will make the Tetrimino fall faster, this is called a soft drop.",
            "   - Hard Drop: Some versions of Tetris allow for a hard drop, which instantly places the Tetrimino at the bottom",
            "     of the Matrix. This is usually done by pressing the space bar.",
            "4. Clearing Lines: When you create a full horizontal line without gaps, it clears from the Matrix and you earn points.",
            "   The more lines you clear at once, the more points you score. Clearing four lines simultaneously is known as a Tetris.",
            "5. Levels and Speed: As you clear lines, you'll progress through levels. Each level increases the speed at which ",
            "   Tetriminos fall, making the game progressively more challenging.",
            "6. Game Over: The game ends when the Tetriminos stack up to the top of the Matrix and prevent any new Tetriminos",
            "   from entering."
        ]

        for i, instruction in enumerate(instructions):
            instruction_text = get_font(14).render(instruction, True, "Black")
            instruction_rect = instruction_text.get_rect(topleft=(50, 100 + 30 * i))
            SCREEN.blit(instruction_text, instruction_rect)

        OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "orange")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="pink", hovering_color="purple")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="GUIDANCE", font=get_font(75), base_color="#3EB489", hovering_color="purple")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="red", hovering_color="purple")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()




