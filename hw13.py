# Part E: Right and left walls loop (wall_loop method) and the Player can't move after game is over (self.game_over bool).

# A
import turtle, random, math

class Game:
    '''
    Purpose: 
        Represents the controls and the logic of the game
    Instance variables: 
        player: a SpaceCraft object representing the player's spacecraft
        ball: a list of Obstacle objects representing the balls that the player needs to avoid
    Methods: 
        init: initializes the Game object
        gameloop: controls the main logic of the game
        obstacle: checks if the player collided with an obstacle
        wall_loop: makes the player going off the left edge of the window teleport to the right edge and vice versa
    '''
    def __init__(self):
        #Bottom left corner of screen is (0, 0)
        #Top right corner is (500, 500)
        turtle.setworldcoordinates(0, 0, 500, 500)
        cv = turtle.getcanvas()
        cv.adjustScrolls()
        #Ensure turtle is running as fast as possible
        turtle.delay(0)

        self.player = SpaceCraft(random.uniform(100,400), random.uniform(250,450), random.uniform(-4,4), random.uniform(-2,0))
        turtle.onkeypress(self.player.thrust, 'Up')
        turtle.onkeypress(self.player.left_turn, 'Left')
        turtle.onkeypress(self.player.right_turn, 'Right') 

        self.ball = []
        for i in range(10):
            self.ball.append(Obstacles(random.uniform(0,500), random.uniform(0,500), 'blue', 0, 3))
        self.gameloop() 
        
        #These two lines must always be at the BOTTOM of __init__
        turtle.listen()
        turtle.mainloop()


    def gameloop(self): 
        self.obstacle()
        self.wall_loop()
        if self.player.ycor() > 10:
            self.player.move()
            turtle.ontimer(self.gameloop, 30)
        else:
            if -3 < self.player.xvel < 3 and -3 < self.player.yvel < 3:
                turtle.penup()
                turtle.goto(250, 250)
                turtle.hideturtle()
                turtle.write('Successful landing!', move=False, align="center", font=("Arial", 15, "normal"))
                self.player.game_over = True
            else:
                turtle.penup()
                turtle.goto(250, 250)
                turtle.hideturtle()
                turtle.write('You crashed!', move=False, align="center", font=("Arial", 15, "normal"))
                turtle.speed(0)
                turtle.penup()
                self.player.game_over = True
    
    def obstacle(self):
        for ball in self.ball:
            if ball.ycor() < 5:
                ball.goto(random.uniform(0,500), random.uniform(0,500))
            distance = math.sqrt(((self.player.xcor() - ball.xcor())**2) + ((self.player.ycor() - ball.ycor())**2))
            if distance < 10:
                turtle.penup()
                turtle.goto(250, 250)
                turtle.hideturtle()
                turtle.write('You crashed!', move=False, align="center", font=("Arial", 15, "normal"))
                self.player.game_over = True

    def wall_loop(self):
        if self.player.xcor() < 0:
            self.player.goto(500, self.player.ycor())
        if self.player.xcor() > 500:
            self.player.goto(0, self.player.ycor())
        

class SpaceCraft(turtle.Turtle):
    '''
    Purpose: 
        Represents the spacecraft object for the game
    Instance variables:
        xpos: the x coords of the spacecraft
        ypos: the y coords of the spacecraft
        xvel: the velocity of the spacecraft in the x direction
        yvel: the velocity of the spacecraft in the y direction
        fuel: the amount of fuel left in the spacecraft
        game_over: a boolean indicating whether the game is over or not
    Methods: 
        move: updates the position of the spacecraft based on its velocity
        thrust: increases the velocity of the spacecraft in the direction it is pointing and decreases the amount of fuel left
        left_turn: turns the spacecraft left by 15 degrees and decreases the amount of fuel left
        right_turn: turns the spacecraft right by 15 degrees and decreases the amount of fuel left
    '''
    def __init__(self, xpos, ypos, xvel, yvel):
        turtle.Turtle.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel 
        self.yvel = yvel
        self.fuel = 40
        self.left(90)
        self.penup()
        self.speed(0)
        self.goto(xpos, ypos)
        self.game_over = False

    def move(self):
        self.yvel -= 0.0486
        xpos = self.xcor() + self.xvel
        ypos = self.ycor() + self.yvel
        self.goto(xpos, ypos)

    def thrust(self):
        if not self.game_over:
            if self.fuel > 0:
                self.fuel -= 1
                angle = math.radians(self.heading())
                self.xvel += math.cos(angle)
                self.yvel += math.sin(angle)
                print(f'Remaining Fuel Units: {self.fuel}')
            else:
                print('Out of fuel')

    def left_turn(self):
        if not self.game_over:
            if self.fuel > 0:
                self.fuel -= 1
                self.left(15)
                print(f'Remaining Fuel Units: {self.fuel}')
            else:
                print('Out of fuel')

    def right_turn(self):
        if not self.game_over:
            if self.fuel > 0:
                self.fuel -= 1
                self.right(15)
                print(f'Remaining Fuel Units: {self.fuel}')
            else:
                print('Out of fuel')


class Obstacles(turtle.Turtle):
    '''
    Purpose: 
        Represents the obstacles for the game
    Instance variables: 
        vx: velocity of the obstacle in the x direction
        vy: velocity of the obstacle in the y direction
    Methods: 
        init: initializes Obstacles with the given parameters
        move: moves the obstacle on the screen every 30 milliseconds
    '''
    def __init__(self, px, py, color, vx, vy):
        turtle.Turtle.__init__(self)
        self.vx = vx
        self.vy = vy
        self.shape('circle')
        self.color(color)
        self.speed(0)
        self.penup()
        self.goto(px, py)
        self.pendown()
        self.move()
        
    def move(self):
        self.px = self.xcor() - self.vx
        self.py = self.ycor() - self.vy
        self.penup()
        self.goto(self.px, self.py)
        turtle.ontimer(self.move, 30)


if __name__ == '__main__':
    Game()

