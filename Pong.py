import pygame
from pyautogui import size
import sys

#paddle class
class Paddle:

    #initial positions, dimensions, speed and color
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        #rect that is used to control the position and collision of the object
        self.playerRect = pygame.Rect(posx, posy, width, height)
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    #displays object on the screen
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)
 
    # Used to update the state of the object
    # yFac represents the direction of the striker movement
    # if yFac == -1 ==> The object is moving upwards
    # if yFac == 1 ==> The object is moving downwards
    # if yFac == 0 ==> The object is not moving
    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac
 
        # Prevent paddle from leaving the top of the screen
        if self.posy <= 0:
            self.posy = 0
        # Prevent paddle from leaving the bottom of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height
 
        # Updating the rect with the new values
        self.playerRect = (self.posx, self.posy, self.width, self.height)
 
    # Used to render the score on to the screen
    # First, create a text object using the font.render() method
    # Then, get the rect of that text using the get_rect() method
    # Finally blit the text on to the screen
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
 
        screen.blit(text, textRect)
 
    def getRect(self):
        return self.playerRect


# Ball class
class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		# If the ball hits the top or bottom surfaces,
		# then the sign of yFac is changed and it
		# results in a reflection
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		# If the ball touches the left wall for the first time,
		# The firstTime is set to 0 and we return 1
		# indicating that Geek2 has scored
		# firstTime is set to 0 so that the condition is
		# met only once and we can avoid giving multiple
		# points to the player
		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	# Used to reset the position of the ball
	# to the center of the screen
	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	# Used to reflect the ball along the X-axis
	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball


def main():
    run = True

    #initialize objects
    player1 = Paddle(WIDTH*.05, HEIGHT//2+75, 20, 150, 10, WHITE)
    player2 = Paddle(WIDTH*.95+20, HEIGHT//2+75, 20, 150, 10, WHITE)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)
	
    Players = [player1, player2]
	
    #initialize player params
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0
	
    while run:
        screen.fill(BLACK)
        
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                if event.key == pygame.K_w:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YFac = 0

        #collision detection
        for player in Players:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        #update objects
        player1.update(player1YFac)
        player2.update(player2YFac)
        point = ball.update()

        #-1 -> player1 has scored
        #+1 -> player2 has scored
        #0 -> None of them scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        #someone has scored a point and the ball is out of bounds.
        #so, we reset it's position
        if point:   
            ball.reset()
            
        #display objects on the screen
        player1.display()
        player2.display()
        ball.display()


        #displaying the scores of the players
        player1.displayScore("player_1 : ", 
                           player1Score, 100, 20, WHITE)
        player2.displayScore("player_2 : ", 
                           player2Score, WIDTH-100, 20, WHITE)
 
        pygame.display.update()
        clock.tick(FPS)     


#initialize pygame and capture display resolution
pygame.init()
resolution = size()
 
# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)
 
# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Basic parameters of the screen
WIDTH, HEIGHT = resolution[0], resolution[1]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
# Used to adjust the frame rate
clock = pygame.time.Clock()
FPS = 60


if __name__ == "__main__":
    main()
    pygame.quit()
