import pygame
from random import randint
import os
from typing import Union
import sys
pygame.init()

# Global Constants (Can be altered to change game difficulty/ adaptability)

#* GENERAL CONSTANTS
WIDTH, HEIGHT = 576, 1024 # Screen Width and height
FPS = 60 # Frames Per Second (Used to set clock tick)

#* BIRD CONSTANTS
GRAVITY = 0.3 # Gravity of the free falling bird
FLAP_POWER = 6 # Y-axis velocity of the bird (Negative implying the bird will move upwards)
ROTATION_SPEED = 0.05 # Rotation angle of the bird 
#* PIPE CONSTANTS
PIPE_GAP = 250 # Space between pipes (altered depending on difficulty)
PIPE_THICKNESS = 104 # Thickness of pipe
PIPE_SPEED = 4 # horizontal speed of pipe

#* FLOOR CONSTANTS  
FLOOR_SPEED = 4 # Horizontal speed of the floor

#* FONT AND AUDIO
FONT = pygame.font.Font('font/arcade.TTF',70)
POINT_SOUND = pygame.mixer.Sound(os.path.join('audio', 'point.wav'))
FLAP_SOUND = pygame.mixer.Sound(os.path.join('audio','wing.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('audio','hit.wav'))


class Sprite:
    """
    A class to represent a Sprite (Game object). 
    In this instance, used as a Parent Base Class for all Sprites to be made (bird,pipe and floor).
    ...
    
    Class Attributes
    ----------------
        None
        
    Instance Attributes
    -------------------
        x : int
            - x-axis position of the sprite
        y : int
            - y-axis position of the sprite
        image : str or list
            - path of the image to be rendered on-screen
                str -> single image to be rendered
                list -> animation to be rendered (list of images)
        height : int
            - height of the sprite
        width : int
            - width of the sprite

    Methods
    -------
    
        motion(self):
            Deals with constant movement of the sprite on-screen.
        
        render(self):
            Deals with rendering (displaying) the sprite on-screen
    """
    
    # Initialization
    def __init__(self,x: float,y: float,image: Union[str,list]) -> None:
        """
        Constructs all the necessary attributes for the sprite object.

        Parameters
        ----------
            x : int
                - x-axis position of the sprite
            y : int
                - y-axis position of the sprite
            image : str or list
                - path of the image to be rendered on-screen
                    str -> single image to be rendered
                    list -> animation to be rendered (list of images)
        """
        self.x = x
        self.y = y
        # Here when the image passed is a list, every image in the list is converted to a pygame surface and maintained as a list,
        # If only a single image is passed, it is stored as a single Pygame Surface.
        if type(image) == list:
            self.image = [pygame.transform.scale2x(pygame.image.load(animation).convert_alpha()) for animation in image]
            self.height = self.image[0].get_height()
            self.width = self.image[0].get_width()
        else:
            self.image = pygame.transform.scale2x(pygame.image.load(image).convert_alpha())
            self.height = self.image.get_height()
            self.width = self.image.get_width()
       
    # Methods
     
    def motion(self) -> None:
        """
        Handles constant movement of Sprite on-screen.

        Parameters
        ----------
            None
            
        Returns
        -------
            None
            
        """
        pass
    
    def render(self,screen) -> None:
        """
        Displays Sprite on-screen

        Parameters
        ----------
            screen: pygame screen
            
        Returns
        -------
            None
        """
        pass

class Bird(Sprite):
    """
    A class to represent the sprite Bird. 
    Uses Sprite as a Parent class and inherits it's instance attributes as well as adds some of its own.
    ...
    
    Class Attributes
    ----------------
        last_update: int
            - stores the tick value of pygame for when the bird was intialized. This is used later for animating the bird.
        frame: int
            - represents the frame of the animation to be displayed (here takes values (0,1 or 2) that represent index of the animation list)
            
    Instance Attributes
    -------------------
        Inherits x, y and image (height,width) from the Sprite Class (Parent)
            
            vely : int
                - The y-axis velocity (speed) of the bird
                
            started: bool
                - If the bird has started moving or not (used to check whether the bird is stationary)
            
            degree: float
                - the increasing angle as the bird falls
                
            rotation : float
                - the angle of rotation of the bird sprite
    Methods
    -------
    
        motion(self):
            Deals with constant movement of the bird on-screen.

        render(self):
            Deals with rendering (displaying) the bird on-screen
        
        flap(self):
            Handles flapping of the bird (up movement of the bird when a key is pressed by user)
            
        collision(self,floor,pipe):
            Handles collision detection of the bird with the floor/pipes.
    """
    # Class Attributes
    last_update = pygame.time.get_ticks()
    frame = 0
    
    # Initialization
    def __init__(self,x: float,y: float,image: Union[str,list]) -> None:
        """
        Constructs all the necessary attributes for the bird object.

        Parameters
        ----------
            Inherits x, y and image (height,width) from the Sprite Class (Parent)
            
        """
        Sprite.__init__(self,x,y,image)
        self.vely = 0
        self.started = False
        self.degree = 0
        self.rotation = 0
   
    # Methods
    
    def motion(self) -> None:
        """
        Handles constant motion of the bird, i.e. constant increase in y-axis position (downwards) due to gravity

        Parameters
        ----------
            None
            
        Returns
        -------
            None
        """
        
        # Increase in y velocity and y position of the bird
        self.vely += GRAVITY
        self.y += self.vely
        
        # Increase in angle of rotation of the bird, until 90 (animation effect)
        self.degree += ROTATION_SPEED   
        if self.rotation >= -90:
            self.rotation -= self.degree
        
    def render(self,screen) -> None:
        """
        Displays the bird on-screen.

        Parameters
        ----------
            - screen : pygame screen 
            
        Returns
        -------
            None
        """
        
        # Accessing current tick and checking if 100 ticks has passed since the last update of the bird. 
        # If true, the next frame (animation) of the bird is displayed
        current_time = pygame.time.get_ticks()
        
        if current_time - Bird.last_update >= 100:
            Bird.frame += 1
            Bird.last_update = current_time
            
            # Frame set back to 0 when end of the list is reached
            if Bird.frame >= len(self.image):
                Bird.frame = 0
                
        # Bird is rendered on-screen
        screen.blit(pygame.transform.rotate(self.image[Bird.frame],self.rotation),(self.x,self.y))
        
    def flap(self) -> None:
        """
        Handles flapping of the bird.

        Parameters
        ----------
            None
            
        Returns
        -------
            None
        """
        
        # Reduces the y-velocity of the bird, pushing it upwards on-screen by a factort of FLAP_POWER
        self.vely = -FLAP_POWER
        self.rotation = 20
        self.degree = 0
        
    def collision(self,floor : object,pipe : object) -> bool:
        """
        Checks for collision of the bird with the floor or pipes

        Parameters
        ----------
            - floor: Floor() object
            
            - pipe: Pipe() object
            
        Returns
        -------
            Bool
        """
        # Checks:
            # - if the bird is touching the floor or gone above the ceiling of the game
            # - if the bird is in the x range of the pipe when it is not in the gap (space b/w the top pipe and bottom pipe)
        return (self.y < 0 or self.y > HEIGHT - floor.height - self.height) or \
                (pipe.x < self.x + self.width < pipe.x + pipe.width and \
                (self.y < pipe.gap_start or self.y + self.height > pipe.gap_start + PIPE_GAP))
                
class Floor(Sprite):
    """
    A class to represent the sprite Floor. 
    Uses Sprite as a Parent class and inherits it's instance attributes.
    ...
    
    Class Attributes
    ----------------
        None
        
    Instance Attributes
    -------------------
        Inherits x, y and image (height,width) from the Sprite Class

    Methods
    -------
    
        motion(self):
            Deals with constant movement of the floor on-screen.

        render(self):
            Deals with rendering (displaying) the floor on-screen
    """
    
    # Intialization
    
    def __init__(self,x: float,y: float,image: Union[str,list]) -> None:
        """
        Constructs all the necessary attributes for the floor object.

        Parameters
        ----------
            Inherits x, y and image (height,width) from the Sprite Class
            
        """
        Sprite.__init__(self,x,y,image)
    
    # Methods
    
    def motion(self) -> None:
        """
        Handles constant motion of the floor (right to left), i.e. constant decrease in x-axis position by a factor of FLOOR_SPEED

        Parameters
        ----------
            None
            
        Returns
        -------
            None
        """
        self.x -= FLOOR_SPEED 
        
    def render(self,screen) -> None:
        """
        Displays the floor on-screen
        
        Parameters
        ----------
            screen: pygame screen
            
        Returns
        -------
            None
        """
        # Renders 2 back to back images of the floor to allow for seamless motion.
        screen.blit(self.image,(self.x,self.y))
        screen.blit(self.image,(self.x + WIDTH,self.y)) 
        # If the first image is fully off-screen, the x-position is reset to the original position.
    
    def offscreen(self) -> bool:
        """
        Checks if the floor sprite is off-screen
        
        Parameters
        ----------
            None
            
        Returns
        -------
            Bool
        """
        return self.x < -WIDTH
        
class Pipe(Sprite):
    """
    A class that acts as a Flyweight Factory for the Pipe Class
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        _flyweights : dict
            - A dictionary of existing pipe flyweights (key: state, value: Pipe object)
    Methods
    -------
    
        get_flyweight(self):
            This method updates the dictionary of existing flyweights and returns a Pipe object of the particular shared state
            
    """
    # Intialization
    
    def __init__(self,x: float,image: Union[str,list],shared_state: str) -> None:
        """
        Constructs all the necessary attributes for the pipe object.

        Parameters
        ----------
            Inherits x and image (height,width) from the Sprite Class
            
            gap_start : int
                - y-position of the gap in the pipe (space between top pipe and bottom pipe)
                
            _shared_state : str
                - a state to access pipe object from the flyweight factory (PipeFactory)
            
        """
        Sprite.__init__(self,x,None,image)
        self.gap_start = randint(50, HEIGHT - PIPE_GAP - 224 - 50)
        self._shared_state = shared_state
    
    # Methods
    
    def motion(self) -> None:
        """
        Handles constant motion of the pipe sprite (right to left), i.e. constant decrease in x-axis position by a factor of PIPE_SPEED
        
        Parameters
        ----------
            None
            
        Returns
        -------
            None
        """
        self.x -= PIPE_SPEED
        
    def render(self,screen) -> None:
        """
        Displays the pipe on-screen
        
        Parameters
        ----------
            screen: pygame screen
            
        Returns
        -------
            None
        """
        screen.blit(self.image[0],(self.x,self.gap_start - 640))
        screen.blit(self.image[1],(self.x,self.gap_start + PIPE_GAP))
        
    def offscreen(self) -> bool:
        """
        Checks if the pipe sprite is off-screen
        
        Parameters
        ----------
            None
            
        Returns
        -------
            Bool
        """
        return self.x + PIPE_THICKNESS < 0
        
class PipeFactory:
    """
    A class that acts as a Flyweight Factory for the Pipe Class
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        _flyweights : dict
            - A dictionary of existing pipe flyweights (key: state, value: Pipe object)
    Methods
    -------
    
        get_flyweight(self):
            This method updates the dictionary of existing flyweights and returns a Pipe object of the particular shared state
            
    """
    
    # Intialization
    
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the pipe flyweight object.

        Parameters
        ----------
            None
            
        """
        self._flyweights = {}
        
    # Methods
    
    def get_flyweight(self,x: float,image: Union[str,list],shared_state: str) -> object:
        """
        Updates dictionary of existing flyweights with Pipe object

        Parameters
        ----------
            Inherits x, y and image (height,width) from the Sprite Class
            
        Return
        ------
            Pipe object
            
        """
        self._flyweights[shared_state] = Pipe(x,image,shared_state)
        return self._flyweights[shared_state]
    
class GameMemento:
    """
    A class that acts as a Game Saver (Memento) and keeps a log of Game instance attributes.
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        score : int
            - stores the score of the player (number of pipes passed)
            
        game_over : bool
            - stores whether the player has died and the game is over
            
        bird_state : tuple
            - stores the x and y position of the bird
            
        pipe_state : list
            - stores the x of the pipes
            
        floor_state : int
            - stores the x position of the floor   
            
    Methods
    -------
        None
            
    """
    
    # Intialization
    
    def __init__(self, score: int, game_over: bool, bird_state: tuple, pipe_states: list, floor_state: int):
        """
        Constructs all the necessary attributes for the memento object, to save a particular state of the Game class

        Parameters
        ----------
            score : int
                - stores the score of the player (number of pipes passed)
            
            game_over : bool
                - stores whether the player has died and the game is over
            
            bird_state : tuple
                - stores the x and y position of the bird
            
            pipe_state : list
                - stores the x of the pipes
            
            floor_state : int
                - stores the x position of the floor   
            
        """
        self.score = score
        self.game_over = game_over
        self.bird_state = bird_state
        self.pipe_states = pipe_states
        self.floor_state = floor_state

class GameOriginator:
    """
    A class that acts as a Game Originator (Memento) and allows for creation and restoring of mementos.
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        None
            
    Methods
    -------
        create_memento(self,game):
            - creates a snapshot of the current state of the game
            
        restore_from_memento(self,memento,game):
            - restores a previous snapshot of the game from a GameMemento object

            
    """
    def create_memento(self) -> object:
        """
        Create a snapshot of the current state of the game.
        
        Parameters
        ----------
            None
            
        Return
        ------
            GameMemento object
            
        """
        
        # Storing the fixed coordinates of the sprites during start of the game
        game = Game.get_instance()
        bird_state = (game.bird.x, game.bird.y)
        pipe_states = [pipe.x for pipe in game.pipes]
        floor_state = game.floor.x

        return GameMemento(game.score, game.game_over, bird_state, pipe_states, floor_state)
    
    def restore_from_memento(self, memento: object) -> None:
        """
        Restore the game to the state it was in when the memento was created.
        
        Parameters
        ----------
            memento : object
                - a GameMemento object storing the previous state of the Game.
            
        Return
        ------
            None
            
        """
        game = Game.get_instance()
        # Restoring old save from memento
        game.score = memento.score
        game.game_over = memento.game_over
        bird_state = memento.bird_state
        pipe_states = memento.pipe_states
        floor_state = memento.floor_state

        # Re-initializing Bird, Pipe and Floor objects to original state
        game.bird = Bird(*bird_state, ['sprites/yellowbird-upflap.png', 'sprites/yellowbird-midflap.png', 'sprites/yellowbird-downflap.png'])
        game.pipes = [Game.pipefactory.get_flyweight(x,['sprites/pipe-top.png','sprites/pipe-bottom.png'],'pipe') for x in pipe_states]
        game.floor = Floor(floor_state, HEIGHT - 224, 'sprites/base.png')
    
class Game:
    """
    The main class that manages the overall game state, i.e. handles the scoring, game over conditions and rendering.
    ...
    
    Class Attributes
    ----------------
        __instance : object
            - stores the instance created of the Game object (default set to None)
            
        highscore : int
            - stores the highest score acheived by the user for a game instance
            
        PipeFactory : object
            -  an instance of the PipeFactory class

    Instance Attributes
    -------------------
        score : int
            - the score of the player (number of pipes passed)
            
        game_over : bool
            - if the player has died and the game is over
            
        bird : object
            - an instance of the Bird class, default set to the left-middle of the screen.
            
        pipe : list
            - a list of 2 instances of the Pipe class, default set to outside the screen limits.
            
        floor : object
            - an instance of the Floor class, default set to the bottom of the screen.
            
        observer : object
            - an instance of the Observer class, used to update the score.
            
        controls : dict
            - a dictionary of commands with: key -> key pressed by user, 
                                             value -> function to perform on key press 
            
        difficulty : str
            - a variable that stores the difficulty of the game (difference in PIPE_GAP), determined by command line arguments and default set to 'Easy'
            
    Methods
    -------
        get_instance(): (static method)
            - checks whether an instance of the Game class exists and returns only a single instance of the class (Singleton)
            
        update(self):
            - checks for game over conditions, whether pipe/floor sprite goes offscreen and the constant motion of the sprites
            
        handle_input(self):
            - checks for user input and performs functions for certains key presses.
            
        render(self,screen):
            - creates surfaces and renders(displays) them on-screen
        
        endgame(self):
            - deals with endgame rendering and highscore updation(if applicable)
        
            
    """
    
    # Class Attributes
    __instance = None
    highscore = 0
    pipefactory = PipeFactory()

    
    @staticmethod
    def get_instance() -> object:
        """
        Checks whether an instance of the Game class exists and returns only a single instance of the class.
        
        Parameters
        ----------
            None
            
        Return
        ------
            Game object
            
        """
        if Game.__instance is None:
            Game()
        return Game.__instance
    
    # Intialization
    
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the Game object, and maintains only a single instance

        Parameters
        ----------
            None  
            
        """
        if Game.__instance is not None:
            raise 'Class can have only one instance'
        else:
            Game.__instance = self
        self.score = 0
        self.game_over = False
        # Bird Sprite set to left-mid of the screen
        self.bird = Bird(WIDTH//20,HEIGHT // 2,['sprites/yellowbird-upflap.png','sprites/yellowbird-midflap.png','sprites/yellowbird-downflap.png'])
        
        # Pipe Sprite set to right of the screen (off-screen)
        self.pipes = [Game.pipefactory.get_flyweight(WIDTH + WIDTH//2,['sprites/pipe-top.png','sprites/pipe-bottom.png'],'pipe'),Game.pipefactory.get_flyweight(  WIDTH + WIDTH//2+ 340,['sprites/pipe-top.png','sprites/pipe-bottom.png'],'pipe')]
        
        # Floor Sprite set to bottom of the screen
        self.floor = Floor(0,HEIGHT - 224,'sprites/base.png')
        
        # Observer initialized
        self.observer = Observer()
        
        # Controls mapped
        self.controls = {pygame.K_SPACE : FlapCommand(),pygame.K_UP : FlapCommand(), pygame.K_ESCAPE: ExitCommand()}

        
        # Difficulty of the game (determined by command line arguments)
        self.difficulty = 'Easy'
        global PIPE_GAP
        if len(sys.argv) >= 2:
            if sys.argv[1] == 'h' or sys.argv[1] == 'hard':
                PIPE_GAP = 150
                self.difficulty = 'Hard'
            elif sys.argv[1] == 'm' or sys.argv[1] == 'med':
                PIPE_GAP = 200
                self.difficulty = 'Medium'
        
        
    # Methods

    def update(self) -> None:
        """
        Checks for game over conditions, if the floor/pipes are offscreen and handles constant motion of all sprites.
        
        Parameters
        ----------
            None
            
        Return
        ------
            None
            
        """
        # If player has died, game update does nothing (returns)
        if self.game_over:
            return
        
        # If the floor is offscreen, floor x-position set back to 0
        if self.floor.offscreen():
            self.floor.x = 0

        # Maintaining a list of pipes to remove
        pipes_to_remove = []
        
        # Iterating through existing pipes
        for pipe in self.pipes:
            
            # Pipes are constantly moved to the left
            pipe.motion()
            
            # If collision b/w bird and floor/pipe, game is over and break
            if self.bird.collision(self.floor,pipe):
                self.game_over = True
                HIT_SOUND.play()
                break
            
            # If pipe is offscreen, we add it to pipes to be removed
            if pipe.offscreen():
                pipes_to_remove.append(pipe)
                
            # If the bird passes half the pipe, we notify the observer and it increments score
            if pipe.x  + PIPE_THICKNESS // 2 == (self.bird.x):
                self.observer.update()
        
        # Iterating through pipes to remove
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            # adding a new pipe for every pipe removed
            self.pipes.append(Game.pipefactory.get_flyweight(WIDTH,['sprites/pipe-top.png','sprites/pipe-bottom.png'],'pipe'))
            
        # constant motion of the bird (gravity) and floor (right to left)
        self.bird.motion()
        self.floor.motion()
        
        
    def handle_input(self) -> None:
        """
        Checks for user input and performs functions for certains key presses.
        
        Parameters
        ----------
            None
            
        Return
        ------
            None
            
        """
        # Checking events
        for event in pygame.event.get():
            # If the close button is clicked, window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # If a key press is in our mapped controls, execute that command
            elif event.type == pygame.KEYDOWN:
                command = self.controls.get(event.key)
                if command is not None:
                    command.execute()
                    
    
    
    def render(self,screen,background,logo,press_space,difficulty) -> None:
        """
        Checks for user input and performs functions for certains key presses.
        
        Parameters
        ----------
            screen : pygame screen
            
            background : pygame surface
                - background to be displayed
                
            logo : pygame surface
                - flappy bird logo to be rendered on welcome screen
                
            press_space : pygame surface
                - 'press to start' message on welcome screen
                
            difficulty : pygame surface
                - Mode the game is set to (Easy, Medium or Hard)
            
        Return
        ------
            None
            
        """
        # Creating a surface with updated score
        score = FONT.render(str(self.score),1,(255,255,255))
        
        # Rendering background
        screen.blit(background,(0,0))
        
        # Rendering pipe
        for pipe in self.pipes:
            pipe.render(screen)
            
        # Rendering floor and bird
        self.floor.render(screen)
        self.bird.render(screen)
        
        # Rendering score
        screen.blit(score,((WIDTH-score.get_width())//2,50))

        # If bird is stationary (welcome screen), display logo and press space message
        if not self.bird.started:
            screen.blit(logo,(0,0))
            screen.blit(difficulty,((WIDTH - difficulty.get_width())//2,200))
            screen.blit(press_space,((WIDTH - press_space.get_width())//2,HEIGHT-self.floor.height - press_space.get_height()))
            
        pygame.display.update()
            
    def endgame(self,screen) -> None:
        """
        Performs rendering after the game is over and updates high score (if applicable)
        
        Parameters
        ----------
            screen : pygame screen
            
        Return
        ------
            None
            
        """
        # Set game over argument to True
        self.game_over = True
        
        # Check if the score is greater than previous high score
        if Game.highscore < self.score:
            Game.highscore = self.score
        
        # Creating Game Over, Score and Highscore surfaces
        over = pygame.transform.scale2x(pygame.image.load('sprites/gameover.png').convert_alpha())
        score = FONT.render(f'Score  {str(self.score)}',1,(255,255,255))
        high = FONT.render(f'High Score  {str(Game.highscore)}',1,(255,255,255))
        
        # Rendering the above surfaces on-screen
        screen.blit(over,((WIDTH - over.get_width())//2,HEIGHT//2 - 100)) 
        screen.blit(score,((WIDTH - score.get_width())//2,HEIGHT//2))
        screen.blit(high,((WIDTH - high.get_width())//2,HEIGHT//2 + 50))
        
        pygame.display.update()
        
        
class Command:
    """
    A base Command interface that is used by other concrete command classes.
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        None
    Methods
    -------
    
        execute(self):
            - command to be executed
            
    """
    # Methods
    
    def execute(self) -> None:
        pass
    
class FlapCommand(Command):
    """
    A subclass of the Command Class that defines the command of a bird flap.
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        None
        
    Methods
    -------
    
        execute(self,bird):
            - executes a bird flap
            
    """
    # Methods
    
    def execute(self) -> None:
        """
        Executes the bird flap and plays audio for every flap.
        
        Parameters
        ----------
            None
            
        Return
        ------
            None
            
        """
        game = Game.get_instance()
        # Set started argument of bird to True
        game.bird.started = True
        
        # Execute bird.flap() function (increase in y-position)
        game.bird.flap()
        
        # Play audio chime
        FLAP_SOUND.play()
        
class ExitCommand(Command):
    """
    A subclass of the Command Class that defines the command of closing the game
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        None
        
    Methods
    -------
    
        execute(self,bird):
            - Closes game
            
    """
    # Methods
    def execute(self):
        """
        Executes the pygame.quit() function to exit the game.
    
        Parameters
        ----------
            None
        
        Return
        ------
            None
        
        """
        pygame.quit()
        exit()
        
        
def main():
    """
    Initializes the pygame window and runs the main loop to display the game
    """
    # Creates the pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird for Antoine")
    checkpoint_handler = GameOriginator()
    # Creates the game instance
    game = Game.get_instance()
    
    # Set the welcome screen surfaces
    background=pygame.transform.scale2x(pygame.image.load('sprites/background-night.png'))
    logo = pygame.transform.scale(pygame.image.load('sprites/flappy_logo.png').convert_alpha(),(WIDTH,224))
    press_space = FONT.render('Press SPACE',1,(255,255,255))
    difficulty = FONT.render(f'Mode  {game.difficulty}',1,(255,255,255))
    
    # Creates a memento of the initial state of the game
    start_state = checkpoint_handler.create_memento()
    
    # Sets the clock
    clock = pygame.time.Clock()

    # Main loop
    while True:
        game.render(screen,background,logo,press_space,difficulty)              # Renders all sprites on-screen
        game.handle_input()              # Checks for any input
        if game.bird.started:            # Starts the checks and updation of the sprites if the bird has started moving
            game.update()
        clock.tick(FPS)
        if game.game_over:               # If the game is over, 
            game.endgame(screen)          # endgame method is called, a delay of 3 seconds is set and the game is restored back to its intial state
            pygame.time.delay(3000)
            checkpoint_handler.restore_from_memento(start_state)
            break
    main()                               # The main loop is started again, allowing the game to start again on its own
    
    
class Observer:
    """
    Observer class to notify observers of the game state
    ...
    
    Class Attributes
    ----------------
        None

    Instance Attributes
    -------------------
        None
        
    Methods
    -------
    
        update(self):
            - increases the game score by 1 and plays an audio chime
            
    """
    # Methods
    
    def update(self) -> None:
        game = Game.get_instance()
        
        # Increment game score by 1
        game.score += 1
        
        # Play audio chime
        POINT_SOUND.play()
         
if __name__ == '__main__':
    main()