import pygame,sys
from game import Game
from colors import Colors
from button import Button

pygame.init()

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Tetris")

BG = pygame.image.load("assets/background.jpg")

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def easy():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Easy Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,350)

    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0,1)
                if event.key == pygame.K_SPACE and game.game_over == False:
                    game.rotate()
            if event.type == game_update and game.game_over == False:
                game.move_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over == True:
                    game.game_over = False
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()

        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))
            RESTART_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 490), 
                            text_input="Start Over", font=get_font(17), base_color=Colors.white, hovering_color=Colors.orange)
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 565), 
                            text_input="QUIT", font=get_font(17), base_color=Colors.white, hovering_color=Colors.dark_blue)
            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def medium():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Medium Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,250)

    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0,1)
                if event.key == pygame.K_SPACE and game.game_over == False:
                    game.rotate()
            if event.type == game_update and game.game_over == False:
                game.move_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over == True:
                    game.game_over = False
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()

        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))
            RESTART_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 490), 
                            text_input="Start Over", font=get_font(17), base_color=Colors.white, hovering_color=Colors.orange)
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 565), 
                            text_input="QUIT", font=get_font(17), base_color=Colors.white, hovering_color=Colors.dark_blue)
            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def hard():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Hard Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,150)

    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0,1)
                if event.key == pygame.K_SPACE and game.game_over == False:
                    game.rotate()
            if event.type == game_update and game.game_over == False:
                game.move_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over == True:
                    game.game_over = False
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()

        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))
            RESTART_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 490), 
                            text_input="Start Over", font=get_font(17), base_color=Colors.white, hovering_color=Colors.orange)
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Restart Rect.png"), pos=(1039, 565), 
                            text_input="QUIT", font=get_font(17), base_color=Colors.white, hovering_color=Colors.dark_blue)
            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def main_menu():
    while True:
        screen.blit(BG, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        menu_surface = get_font(100).render("TETRIS", True, "#b68f40")
        menu_rect = menu_surface.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 230), 
                            text_input="EASY", font=get_font(40), base_color=Colors.white, hovering_color=Colors.green)
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Medium Rect.png"), pos=(640, 350), 
                            text_input="MEDIUM", font=get_font(40), base_color=Colors.white, hovering_color=Colors.purple)
        HARD_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 470), 
                            text_input="HARD", font=get_font(40), base_color=Colors.white, hovering_color=Colors.red)
        EXIT_BUTTON = Button(image=pygame.image.load("assets/Exit Rect.png"), pos=(640, 590), 
                            text_input="EXIT", font=get_font(40), base_color=Colors.white, hovering_color=Colors.dark_blue)

        screen.blit(menu_surface, menu_rect)

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, EXIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(mouse_pos):
                    easy()
                if MEDIUM_BUTTON.checkForInput(mouse_pos):
                    medium()
                if HARD_BUTTON.checkForInput(mouse_pos):
                    hard()
                if EXIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()