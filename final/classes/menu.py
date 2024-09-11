import pygame
from classes.global_data import draw_text
from classes.global_data import constants_structure
constants = constants_structure()

def default_response_function(): # Default response function does nothing
    return

class button:
    def __init__(self, location, size, text, response_function=default_response_function, font=constants.NORMAL_FONT):
        # Set all attributes
        self.location = location
        self.size = size
        self.text = text
        self.response_function = response_function
        self.font = font
        
        self.under_pointer = False
        
        # Get texture based on button shape
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/buttons/ratio1-{ratio}.png").convert()
        
    
        
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If mouse pointer is within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
        
    def draw(self, screen, tickCount=None):
        # Draw button
        screen.blit(pygame.transform.scale(self.texture, self.size), self.location)
        
        # Shade if hovered over
        if self.under_pointer:
            # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
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
        # Set attributes
        self.location = location
        self.size = size
        self.name = button_name
        self.protected = protected
        self.font = font
        
        self.selected = False
        self.content = ""
        
        # Get texture based on button shape
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/text_input/ratio1-{ratio}.png").convert()
        
    def response_function(self):
        self.selected = not self.selected # toggle selection
    
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If mouse pointer is within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
            
        # Check keyboard inputs to add to content
        if self.selected:
            for key in keyspressed:
                if key == '\x08': # Backspace
                    self.content = self.content[:-1]
                elif key == "\r": # Enter
                    self.selected = False
                elif len(self.content) <= 17: # Maximum string length is 17
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
                
            # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) 
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
        
        # Draw text cursor
        if tickCount % 16 < 8 and self.selected:
            pygame.draw.rect(screen, (0, 0, 0), (self.location[0] + (self.size[0] + content.get_width())//2 + 4, self.location[1] + 30, 7, 40))
        
        return screen
    
    
class displayedError:
    def __init__(self, error_message, start_tick):
        # Set attributes
        self.error_message = error_message
        self.start_tick = start_tick 
    
    def draw(self, screen):
        intensity = 128
        font = pygame.font.Font(constants.FILE_PATH + "project_lib/fonts/normal.ttf", 20)
        
        # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        content = font.render(self.error_message, True, (255, 50, 50, intensity) )
        temp_surface.blit(content, ((constants.DEFAULT_SCREEN_SIZE[0] - content.get_width())//2, 5))
        screen.blit(temp_surface, (0,0))
        
        return screen
    
    
class savegameButton:
    def __init__(self, location, size, savegame_display_details, game_data):
        # Set attributes
        self.location = location
        self.size = size
        self.savegame_display_details = savegame_display_details
        self.middle_font = pygame.font.Font(constants.FILE_PATH + "project_lib/fonts/normal.ttf", 30)
        
        self.game_data = game_data
        
        self.under_pointer = False
        
        # Get texture based on button shape
        ratio = (size[0]/size[1])
        self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/text_input/ratio1-{ratio}.png").convert() # Use text input button design
    
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If mouse pointer is within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
    
    def response_function(self, screen):
        # Open screen to edit savegame
        from functions.loops.savegame_options import open_savegame
        open_savegame(*self.game_data, self.savegame_display_details, screen)
        return
    
    def draw(self, screen, tickCount=None):
        # Draw button
        screen.blit(pygame.transform.scale(self.texture, self.size), self.location)
        
        # Shade if hovered over
        if self.under_pointer:
            # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, (0, 0, 0, 128), (0, 0, *self.size))
            screen.blit(temp_surface, self.location)
            
        # Add text
        info = [self.savegame_display_details["name"],
                "Level: " + str(self.savegame_display_details["level"]),
                "Last Saved: " + str(self.savegame_display_details["last_save"]),
                "Created: " + str(self.savegame_display_details["created"])]
        
        for i, line in enumerate(info):
            if i == 0: # Name of savegame
                text = self.middle_font.render(line, True, (0, 0, 0))
                screen.blit(text, (self.location[0] + ((self.size[0] - text.get_width())//2), 
                                self.location[1] + (self.size[1]//2) + (self.size[1]//8 * (i-1)) - 20))
            else: # Savegame details
                text = constants.SMALL_FONT.render(line, True, (0, 0, 0))
                screen.blit(text, (self.location[0] + ((self.size[0] - text.get_width())//2), 
                                    self.location[1] + (self.size[1]//2) + (self.size[1]//8 * (i-1))))
            
        return screen
    
    
    
    
class KeyBindingInput:
    def __init__(self, location, size, name, key, protected=False, font = constants.NORMAL_FONT):
        # Set attributes
        self.location = location
        self.size = size
        self.name = name
        self.key = key
        self.protected = protected
        self.font = font
        
        self.selected = False
        self.content = ""
        
        # Get texture based on button shape
        ratio = (size[0]/size[1])
        
        self.selected_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/text_input/ratio1-{ratio}.png").convert()
        self.default_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/buttons/ratio1-{ratio}.png").convert()
        
    def response_function(self):
        self.selected = not self.selected
        return self.selected
        #self.selected = not self.selected # toggle selection
    
    def update(self, mouse_pos, keyspressed=[]):
        if (mouse_pos[0] > self.location[0] and
            mouse_pos[1] > self.location[1] and
            mouse_pos[0] < self.location[0] + self.size[0] and
            mouse_pos[1] < self.location[1] + self.size[1] ): # If mouse pointer is within button boundary
            self.under_pointer = True
        else:
            self.under_pointer = False
            
    
    def draw(self, screen, tickCount=None):
        # Draw button depending on state
        if self.selected:
            screen.blit(pygame.transform.scale(self.selected_texture, self.size), self.location)
        else:
            screen.blit(pygame.transform.scale(self.default_texture, self.size), self.location)
        
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
        # add key
        screen = draw_text(self.key.upper(), screen, self.font, 
                            (self.location[0] + ((self.size[0])//2), self.location[1] + ((self.size[1])//2)),
                            (0,0,0),
                            "centre",
                            "centre")
        # add binding name
        screen = draw_text(self.name.replace("_", " ").title() + ": ", screen, self.font, 
                            (self.location[0], self.location[1] + ((self.size[1])//2)),
                            (0,0,0),
                            "right",
                            "centre")
        
        return screen
