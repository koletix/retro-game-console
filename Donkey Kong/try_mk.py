import os
import game_mk

os.environ['SDL_VIDEO_CENTERED'] = '1' 
game_mk.pygame.init()
game_mk.run_mk()
game_mk.pygame.quit()