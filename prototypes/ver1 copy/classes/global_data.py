import pygame
class constants_structure:
    def __init__(self):
        self.DEFAULT_SCREEN_SIZE = (1280, 720)
        self.MENU_FPS = 15   
        self.FILE_PATH = "projects/prototypes/ver1/"
        
        pygame.font.init()
        self.TITLE_FONT = pygame.font.Font(self.FILE_PATH + "project_lib/fonts/title.ttf", 80)
        self.NORMAL_FONT = pygame.font.Font(self.FILE_PATH + "project_lib/fonts/normal.ttf", 40)
        self.SMALL_FONT = pygame.font.Font(self.FILE_PATH + "project_lib/fonts/normal.ttf", 15)

def draw_text(text, surface, font, location, colour, h_alignment, v_alignment):
    rendered_text = font.render(text, True, colour)
    # find true location from alignment
    if h_alignment == "centre":
        location = (location[0] - (rendered_text.get_width()//2) ,  location[1])
    # alignment "left" changes nothing
    elif h_alignment == "right":
        location = (location[0] - rendered_text.get_width() ,  location[1])
        
    # vertical alignment
    if v_alignment == "centre":
        location = (location[0] ,  location[1] - (rendered_text.get_height()//2))
    # alignment "below" changes nothing
    elif v_alignment == "above":
        location = (location[0] ,  location[1] - rendered_text.get_height())
    
    surface.blit(rendered_text, location)
    return surface