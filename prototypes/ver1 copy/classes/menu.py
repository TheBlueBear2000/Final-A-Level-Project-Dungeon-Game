import pygame
from classes.global_data import draw_text
from classes.global_data import constants_structure
constants = constants_structure()

def default_response_function():
    return

class button:
    def __init__(self, location, size, text, response_function=default_response_function, font=constants.NORMAL_FONT):
        self.location = location
        self.size = size
        self.text = text
        self.response_function = response_function
        self.font = font
        
        self.under_pointer = False
        
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/buttons/ratio1-{ratio}.png").convert()
        
    
        
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
        
    def draw(self, screen, tickCount=None):
        # Draw button
        screen.blit(pygame.transform.scale(self.texture, self.size), self.location)
        
        # Shade if hovered over
        if self.under_pointer:
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)               # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            pygame.draw.rect(temp_surface, (0, 0, 0, 128), (0, 0, *self.size))
            screen.blit(temp_surface, self.location)
            
        # Add text
        screen = draw_text(self.text, screen, self.font, 
                            (self.location[0] + ((self.size[0])//2), self.location[1] + ((self.size[1])//2)),
                            (0,0,0),
                            "centre",
                            "centre")
        
        return screen
    
    
class textInputBox:
    def __init__(self, location, size, button_name, protected=False, font = constants.NORMAL_FONT):
        self.location = location
        self.size = size
        self.name = button_name
        self.protected = protected
        self.font = font
        
        self.selected = False
        self.content = ""
        
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/text_input/ratio1-{ratio}.png").convert()
        
    def response_function(self):
        self.selected = not self.selected # toggle selection
    
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
            
            
            
        if self.selected:
            for key in keyspressed:
                if key == '\x08':
                    self.content = self.content[:-1]
                elif key == "\r":
                    self.selected = False
                elif len(self.content) <= 17:
                    self.content += key
        
    
            
    
    def draw(self, screen, tickCount=None):
        # Draw button
        screen.blit(pygame.transform.scale(self.texture, self.size), self.location)
        
        # Shade if hovered over
        if self.under_pointer or self.selected:
            if self.selected and not self.under_pointer:
                intensity = 64
            else:
                intensity = 128
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            pygame.draw.rect(temp_surface, (0, 0, 0, intensity), (0, 0, *self.size))
            screen.blit(temp_surface, self.location)
            
        # Add text
        if self.content != "" or self.selected:
            if self.protected:
                protected_string = "*" * len(self.content)
                content = self.font.render(protected_string, True, (0, 0, 0))
            else:
                content = self.font.render(self.content, True, (0, 0, 0))
        else:
            content = self.font.render(self.name, True, (50, 50, 50))
        screen.blit(content, (self.location[0] + ((self.size[0] - content.get_width())//2), self.location[1] + ((self.size[1] - content.get_height())//2)))
        
        if tickCount % 16 < 8 and self.selected:
            pygame.draw.rect(screen, (0, 0, 0), (self.location[0] + (self.size[0] + content.get_width())//2 + 4, self.location[1] + 30, 7, 40))
        
        
        
        return screen
    
    
class displayedError:
    def __init__(self, error_message, start_tick):
        self.error_message = error_message
        self.start_tick = start_tick 
    
    def draw(self, screen):
        intensity = 128
        font = pygame.font.Font(constants.FILE_PATH + "project_lib/fonts/normal.ttf", 20)
        
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        content = font.render(self.error_message, True, (255, 50, 50, intensity) )
        temp_surface.blit(content, ((constants.DEFAULT_SCREEN_SIZE[0] - content.get_width())//2, 5))
        screen.blit(temp_surface, (0,0))
        
        return screen
    
    
class savegameButton:
    def __init__(self, location, size, savegame_display_details):
        self.location = location
        self.size = size
        self.savegame_display_details = savegame_display_details
        self.middle_font = pygame.font.Font(constants.FILE_PATH + "project_lib/fonts/normal.ttf", 30)
        
        self.under_pointer = False
        
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/text_input/ratio1-{ratio}.png").convert() # Use text input button design
    
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
            
    def response_function(self):
        return
    
    def draw(self, screen, tickCount=None):
        # Draw button
        screen.blit(pygame.transform.scale(self.texture, self.size), self.location)
        
        # Shade if hovered over
        if self.under_pointer:
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)               # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            pygame.draw.rect(temp_surface, (0, 0, 0, 128), (0, 0, *self.size))
            screen.blit(temp_surface, self.location)
            
        # Add text
        info = [self.savegame_display_details["name"],
                "Level: " + str(self.savegame_display_details["level"]),
                "Last Saved: " + str(self.savegame_display_details["last_save"]),
                "Created: " + str(self.savegame_display_details["created"])]
        
        for i, line in enumerate(info):
            if i == 0:
                text = self.middle_font.render(line, True, (0, 0, 0))
                screen.blit(text, (self.location[0] + ((self.size[0] - text.get_width())//2), 
                                self.location[1] + (self.size[1]//2) + (self.size[1]//8 * (i-1)) - 20))
            else:
                text = constants.SMALL_FONT.render(line, True, (0, 0, 0))
                screen.blit(text, (self.location[0] + ((self.size[0] - text.get_width())//2), 
                                    self.location[1] + (self.size[1]//2) + (self.size[1]//8 * (i-1))))
            
        return screen