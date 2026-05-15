import pygame
import sys

w = 800
h = 800
columns = 8
rows = 8
block_size = w//columns # to get len of each lise of the boxes
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

# function to create the chess board 
def board(screen):
    colors=[LIGHT_BROWN,DARK_BROWN] 

    #loop to find exact row and colum of the box so we can find which color and position the box should be 
    for row in range(rows): 
        for col in range(columns):
            color_index = (row+col)%2 # it finds the remainder (if 1 then the box color is difftent and for 0 its diffrent)... used to create the alternative box diffrent color 
            color = colors[color_index]
            rect = pygame.Rect(col*block_size,row*block_size,block_size,block_size) # set the dimensions and place of the box 
            pygame.draw.rect(screen, color, rect) # final step to add color to specific box position/area on screen

def main(): 
    pygame.init()
    screen= pygame.display.set_mode((w,h)) #create the sceen with the given dimensions
    pygame.display.set_caption("Master's Chess")
    run=True
    while run: # used to create events and interact with the board 
        for event in pygame.event.get(): # this one is used to create a exit point so we can exit from the infinite loop of events 
            if event.type == pygame.QUIT:
                run=False
        board(screen) # call the board function to create those boxes on screen so it looks like chess board
        pygame.display.flip() # to update the whole screen so the chess board shows up else the the board will not have the boxes without update
    pygame.quit()
    sys.exit()


# used to tell that run main only if main() is called else dont
if __name__ == "__main__": 
    main()