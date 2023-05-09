#Flappy Bird Create Task 2023
#Import modules
from tkinter import *
import random

#Define global variables
GAMECOUNTER = 0
GAMESPEED = 30
GAME = True
path_to_score = "highscore.txt"

height = 700
width = 700

BIRDvelocity = 5
PIPEvelocity = 5
UpForce = 5

BIRD_Y = height/2
PIPE_X = width
PIPESIZE = 120
PIPEDISTANCE = 8 * 60

pipelist = [] #A list to hold pipe rectangles
endcards = [] #A list to hold endgame messages

jumps = 0 #A counter to limit the number of consecutive jumps
SCORE = 0
HighScore = 0

#Set up the game window and canvas
window = Tk()
window.title("Flappy Bird")
canvas = Canvas(height=height, width=width, bg="purple", bd=0)
canvas.pack()

#Create text elements for score and high score display
scoreboard = canvas.create_text(625, 40, text="Score: 0", font=("", 30))
highboard = canvas.create_text(625, 70, text=("High Score: " + str(HighScore)), font=("", 15))
canvas.tag_raise(scoreboard)
canvas.tag_raise(highboard)

#Load bird images
imageBIRD = PhotoImage(file="assets/bird.gif")
imageBIRDUP = PhotoImage(file="assets/bird_up.gif")
imageBIRDDOWN = PhotoImage(file="assets/bird_down.gif")

#Create bird object on canvas
bird = canvas.create_image(120, BIRD_Y, image=imageBIRD)
canvas.tag_lower(bird)


#Function to create a new pair of pipes and add them to the canvas
def pipecreate():
   global PIPE_X

   #Set the gap between the pipes to a random height
   minrand = imageBIRD.height() + (UpForce * 10)
   maxrand = minrand * 1.5
   gap = random.randint(minrand, maxrand)

   #Set the heights of the upper and lower pipes based on the gap
   up_height = random.randint(50, (height - (gap + 50)))
   down_height = up_height + gap

   #Create the pipe rectangles on the canvas
   pipe_up = canvas.create_rectangle(PIPE_X, 0, (PIPE_X + PIPESIZE), up_height, fill="navyblue")
   pipe_down = canvas.create_rectangle(PIPE_X, 700, (PIPE_X + PIPESIZE), down_height, fill="navyblue")

   #Lower the pipes below the bird image
   canvas.tag_lower(pipe_up)
   canvas.tag_lower(pipe_down)

   #Add the new pipe pair to the list of pipes
   pipelist.append([pipe_up, pipe_down, up_height, down_height, PIPE_X])
   print("New Pipe Created...")
   #print(pipelist)


#This function is responsible for applying gravity to the bird
def gravity():

   global BIRD_Y

   #Increase bird's Y coordinate by BIRDvelocity
   BIRD_Y += BIRDvelocity
   #If bird goes below the ground, set its Y coordinate to the ground level and end the game
   if BIRD_Y >= 700-(imageBIRD.height()/3):
       BIRD_Y = 700-(imageBIRD.height()/3)
       gameover()

   #If bird is not jumping, set the bird image to the image of the bird facing down
   if jumps == 0:
       canvas.itemconfigure(bird, image=imageBIRDDOWN)


   #Update bird's coordinates on the canvas
   canvas.coords(bird, 120, BIRD_Y)


   #If game is still on, call this function again after GAMESPEED milliseconds
   if GAME:
       window.after(GAMESPEED, gravity)


#This function is responsible for handling the jump event
def jump(event=None):
   global BIRD_Y
   global jumps

   #If bird is jumping, set the bird image to the image of the bird facing up
   if jumps == 1:
       canvas.itemconfigure(bird, image=imageBIRDUP)

   #If game is still on, move the bird up by UpForce
   if GAME:
       BIRD_Y -= UpForce
       #If bird goes above the top of the screen, set its Y coordinate to the top of the screen
       if BIRD_Y <= 0 + (imageBIRD.height() / 2):
           BIRD_Y = 0 + (imageBIRD.height() / 2)

       #Update bird's coordinates on the canvas
       canvas.coords(bird, 120, BIRD_Y)


   #If bird has not reached its maximum number of jumps, call this function again after 10 milliseconds and increase the number of jumps
   if jumps < 10:
       window.after(10, jump)
       jumps += 1
   #If bird has reached its maximum number of jumps, set the number of jumps to 0
   else:
       jumps = 0


#This function is responsible for moving the pipes and detecting collisions
def pipemotion():
   global SCORE
   global PIPEvelocity
   global GAMESPEED

   #For each pipe in the pipelist
   for pipe in pipelist:
       #Move the pipe to the left by PIPEvelocity
       pipe[4] = pipe[4] - PIPEvelocity
       canvas.coords(pipe[0], pipe[4], 0, (pipe[4] + PIPESIZE), pipe[2])
       canvas.coords(pipe[1], pipe[4], 700, (pipe[4] + PIPESIZE), pipe[3])


       #If the pipe has moved to a position where a new pipe needs to be created, create a new pipe
       if pipe[4] == width - PIPEDISTANCE:
           pipecreate()


       #If the pipe has moved out of the screen, delete it from the canvas and the pipelist, increase the score by 1, and update the scoreboard
       if (pipe[4] + PIPESIZE) < 0:
           canvas.delete(pipe[0])
           canvas.delete(pipe[1])
           pipelist.pop(0)


           SCORE += 1
           canvas.itemconfigure(scoreboard, text=("Score: " + str(SCORE)))


       #If the bird collides with the pipe, end the game
       else:
           #print(BIRD_Y)
           collision(pipe)


   #If game is still on, call this function again after
   if GAME:
       window.after(GAMESPEED, pipemotion)


#Define a function to detect a collision between the bird and the pipes
def collision(pipeL):
   print(str(pipeL) + "\n")
   for i in range(0,len(pipeL)):
        if (i == 0):
            #pipe[2,3,4] = pipe[up_height, down_height, cord_x]
            global SCORE
            #Check if the bird's x-coordinate is within the pipe's x-range
            if pipeL[4] <= 120 + imageBIRD.width()/3 and \
                    (pipeL[4] + PIPESIZE) >= 120 - imageBIRD.width()/3:
                #Check if the bird's y-coordinate is within the pipe's height range
                if BIRD_Y - imageBIRD.height()/3 <= pipeL[2] or \
                        BIRD_Y + imageBIRD.height()/2 >= pipeL[3]:
                    print("loss here")
                    print(BIRD_Y)
                    gameover()


#Define a function to end the game when the bird collides with a pipe
def gameover():
   global GAME
   global HighScore


   GAME = False
   print("GAME OVER")


   #If the current score is greater than the previous high score, display a message indicating a new high score
   if SCORE > HighScore:
       endcard = [canvas.create_text(350, 300, text="GAME OVER", font=("", 50)),
            canvas.create_text(350, 350, text=("-- NEW HIGH SCORE = " + str(SCORE) + " --"), font=("", 30)),
            canvas.create_text(350, 380, text="Press ENTER to restart")]


       #Update the high score and write it to the score file
       HighScore = SCORE
       scorefile = open(path_to_score, "w+")
       scorefile.write(str(HighScore))
   #If the current score is not greater than the previous high score, display a message indicating the current score
   else:
       endcard = [canvas.create_text(350, 300, text="GAME OVER", font=("", 50)),
            canvas.create_text(350, 340, text="Press ENTER to restart")]
   #Add the end card elements to the endcards list and bind the Enter key to the restartgame function
   for item in endcard:
       endcards.append(item)


   window.bind("<Return>", restartgame)
   print("Game over...\n Score: "+ str(SCORE))


#Define a function to restart the game
def restartgame(event=None):
   global SCORE
   global BIRD_Y
   global GAME
   global pipelist
   global endcards
   #Reset the bird's y-coordinate and image, score, and pipe and end card lists
   BIRD_Y = height/2
   canvas.itemconfigure(bird, image=imageBIRD)
   SCORE = 0
   canvas.itemconfigure(scoreboard, text=("Score: " + str(SCORE)))


   for item in pipelist:
       canvas.delete(item[0])
       canvas.delete(item[1])


   for item in endcards:
       canvas.delete(item)


   pipelist = []
   endcards = []
   GAME = True
   main()


#Define the main game loop function
def main():
   global GAMECOUNTER
   global HighScore

   GAMECOUNTER += 1
   #Read the high score from the score file and update the high score display on the canvas
   scorefile = open(path_to_score)
   HighScore = int(scorefile.read())
   scorefile.close()

   canvas.itemconfigure(highboard, text=("High Score: " + str(HighScore)))
   #Print a message indicating the start of the game, and set the window to update the pipe positions, bird gravity, and pipe creation at GAMESPEED intervals
   print()
   print("START", GAMECOUNTER)

   window.after(GAMESPEED, pipecreate)
   window.after(GAMESPEED, pipemotion)
   window.after(GAMESPEED, gravity)


#Bind the space key to the jump
if __name__ == "__main__":
   window.bind("<space>", jump)
   window.bind("<Button-1>", jump)
   window.bind("<Up>", jump)
   main()


window.mainloop()