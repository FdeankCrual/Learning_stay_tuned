import pygame
import sys

w = 800
h = 800
columns = 8
rows = 8
block_size = w//columns # to get len of each lise of the boxes
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
IMAGES={} # all images of the peices are stored here

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

class GameState():  
    def __init__(self):
        self.board=[
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.white_to_move=True
        self.move_log=[]
    
    def undo_move(self):
        if len(self.move_log)!=0:
            move=self.move_log.pop()
            self.board[move.start_row][move.start_col]=move.piece_to_move
            self.board[move.end_row][move.end_col]=move.piece_captured

            if move.is_enpassant:
                if move.piece_to_move == 'wP':
                    self.board[move.end_row + 1][move.end_col] = 'bP'
                elif move.piece_to_move == 'bP':
                    self.board[move.end_row - 1][move.end_col] = 'wP'
                    
            self.white_to_move = not self.white_to_move

    def in_check(self):
        y = False
        for i in range(8):
            for j in range(8):
                if self.board[i][j]=='bK' and self.white_to_move == False:
                    king_row = i
                    king_col = j
                elif self.board[i][j]=='wK' and self.white_to_move == True:
                    king_row = i
                    king_col = j
        self.white_to_move = not self.white_to_move
        psudo_moves=self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in psudo_moves:
            if move.end_row == king_row and move.end_col == king_col:
                y = True
                break
        return y
    
    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            move = moves[i]
            self.make_move(move)

            if self.in_check():
                moves.remove(move)

            self.undo_move()
        return moves

    def make_move(self,move):
        self.board[move.start_row][move.start_col]='--'
        self.board[move.end_row][move.end_col]=move.piece_to_move

        if move.is_enpassant:
            if move.piece_to_move == 'wP':
                self.board[move.end_row + 1][move.end_col] = '--' # Clear Black Pawn
            elif move.piece_to_move == 'bP':
                self.board[move.end_row - 1][move.end_col] = '--' # Clear White Pawn
        
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    
    def get_all_possible_moves(self):
        moves=[]
        for r in range(8):
            for c in range(8):
                peice=self.board[r][c]
                if peice!='--':
                    color= peice[0]
                    peice_type=peice[1]

                    if((color=="w" and self.white_to_move) or (color=="b" and not self.white_to_move)):
                        if peice_type=='R':
                            self.get_rook_moves(r,c,moves)
                        if peice_type=='P':
                            self.get_pawn_moves(r,c,moves)
                        if peice_type=='B':
                            self.get_bishop_moves(r,c,moves)
                        if peice_type=='N':
                            self.get_knight_moves(r,c,moves)
                        if peice_type=='K':
                            self.get_king_moves(r,c,moves)
                        if peice_type=='Q':
                            self.get_queen_moves(r,c,moves)
        return moves
    
    def get_king_moves(self,row,col,moves):
        y= self.board[row][col]
        if 7>=row-1>=0 and 7>=col+1>=0:
            x=self.board[row-1][col+1]
            
            if x[0]!= y[0]:
                moves.append(Move((row,col),(row-1,col+1),self.board))

        if 7>=row-1>=0 and 7>=col-1>=0:
            x=self.board[row-1][col-1]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row-1,col-1),self.board))
        
        if 7>=row+1>=0 and 7>=col+1>=0:
            x=self.board[row+1][col+1]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row+1,col+1),self.board))

        if 7>=row+1>=0 and 7>=col-1>=0:
            x=self.board[row+1][col-1]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row+1,col-1),self.board))


        
        if 7>=col+1>=0:
            x=self.board[row][col+1]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row,col+1),self.board))

        if 7>=col-1>=0:
            x=self.board[row][col-1]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row,col-1),self.board))
        
        if 7>=row+1>=0 and 7>=col>=0:
            x=self.board[row+1][col]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row+1,col),self.board))

        if 7>=row-1>=0 and 7>=col>=0:
            x=self.board[row-1][col]

            if x[0]!= y[0]:
                moves.append(Move((row,col),(row-1,col),self.board))

    def get_queen_moves(self,row,col,moves):
        y= self.board[row][col]
        j=row
        for i in range(col+1, 8, 1):
            j=j-1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))

        j=row   
        for i in range(col-1, -1, -1):
            j=j+1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))                   
        
        j=row
        for i in range(col+1, 8, 1):
            j=j+1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))
             
            
        j=row   

        for i in range(col-1, -1, -1):
            j=j-1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))
        
        for i in range(col+1, 8, 1):
            x=self.board[row][i]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(row,i),self.board))
                break
            else:
                moves.append(Move((row,col),(row,i),self.board))

        for i in range(col-1, -1, -1):
            x=self.board[row][i]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(row,i),self.board))
                break
            else:
                moves.append(Move((row,col),(row,i),self.board))

        for i in range(row+1, 8, 1):
            x=self.board[i][col]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(i,col),self.board))
                break
            else:
                moves.append(Move((row,col),(i,col),self.board))
            
            
        for i in range(row-1, -1, -1):

            x=self.board[i][col]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(i,col),self.board))
                break
            else:
                moves.append(Move((row,col),(i,col),self.board))

    def get_knight_moves(self,row,col,moves):
        y= self.board[row][col]
        if 0<=row+2<=7:
            if 0<=col-1<=7:
                checker=self.board[row+2][col-1]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row+2,col-1),self.board))
            if 0<=col+1<=7:
                checker=self.board[row+2][col+1]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row+2,col+1),self.board))
        if 0<=row-2<=7:
            if 0<=col-1<=7:
                checker=self.board[row-2][col-1]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row-2,col-1),self.board))
            if 0<=col+1<=7:
                checker=self.board[row-2][col+1]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row-2,col+1),self.board))
        if 0<=col+2<=7:
            if 0<=row-1<=7:
                checker=self.board[row-1][col+2]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row-1,col+2),self.board))
            if 0<=row+1<=7:
                checker=self.board[row+1][col+2]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row+1,col+2),self.board))
        if 0<=col-2<=7:
            if 0<=row-1<=7:
                checker=self.board[row-1][col-2]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row-1,col-2),self.board))
            if 0<=row+1<=7:
                checker=self.board[row+1][col-2]
                if checker[0]!=y[0]:
                    moves.append(Move((row,col),(row+1,col-2),self.board))
        
    def get_bishop_moves(self,row,col,moves):
        y=self.board[row][col]
        j=row
        for i in range(col+1, 8, 1):
            j=j-1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))

        j=row   
        for i in range(col-1, -1, -1):
            j=j+1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))
                  
            
        
        j=row
        for i in range(col+1, 8, 1):
            j=j+1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))
             
            
        j=row   

        for i in range(col-1, -1, -1):
            j=j-1
            if 7>=j>=0:
                x=self.board[j][i]
                if x[0]== y[0]:
                    break
                elif x[0]!= y[0] and x!='--':
                    moves.append(Move((row,col),(j,i),self.board))
                    break
                else:
                    moves.append(Move((row,col),(j,i),self.board))
                    
    def get_pawn_moves(self, row, col, moves):
        y = self.board[row][col]

        if y[0] == 'b':
            # En passant Logic black (Black pawn must be on Row 4)
            if row == 4 and len(self.move_log) > 0:
                last_move = self.move_log[-1]
                # Enemy pawn must be White ('wP') and have advanced from row 6 to row 4
                if col + 1 <= 7 and self.board[row][col+1] == 'wP':
                    if last_move.end_row == row and last_move.end_col == col+1 and last_move.start_row == 6:
                        moves.append(Move((row, col), (row+1, col+1), self.board, is_enpassant=True))
                if 0 <= col - 1 and self.board[row][col-1] == 'wP':
                    if last_move.end_row == row and last_move.end_col == col-1 and last_move.start_row == 6:
                        moves.append(Move((row, col), (row+1, col-1), self.board, is_enpassant=True))

            if row == 1:
                for i in range(2, 4, 1):
                    if self.board[i][col] != '--':
                        break
                    else: 
                        moves.append(Move((row, col), (i, col), self.board))

            if row != 1 and row + 1 <= 7:  # Guard added to prevent out-of-bounds at back rank
                if self.board[row+1][col] == '--':
                    moves.append(Move((row, col), (row+1, col), self.board))       

            if row + 1 <= 7 and col + 1 <= 7:
                l = self.board[row+1][col+1]
                if l[0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))

            if row + 1 <= 7 and col - 1 >= 0:
                l = self.board[row+1][col-1]
                if l[0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))

        if y[0] == 'w':
            # En passant logic white (White pawn must be on Row 3)
            if row == 3 and len(self.move_log) > 0:
                last_move = self.move_log[-1]
                # Enemy pawn must be Black ('bP') and have advanced from row 1 to row 3
                if col + 1 <= 7 and self.board[row][col+1] == 'bP':
                    if last_move.end_row == row and last_move.end_col == col+1 and last_move.start_row == 1:
                        moves.append(Move((row, col), (row-1, col+1), self.board, is_enpassant=True))
                if 0 <= col - 1 and self.board[row][col-1] == 'bP':
                    if last_move.end_row == row and last_move.end_col == col-1 and last_move.start_row == 1:
                        moves.append(Move((row, col), (row-1, col-1), self.board, is_enpassant=True))

            if row == 6:
                for i in range(5, 3, -1):
                    if self.board[i][col] != '--':
                        break
                    else: 
                        moves.append(Move((row, col), (i, col), self.board))

            if row != 6 and row - 1 >= 0:  # Guard added to prevent out-of-bounds at back rank
                if self.board[row-1][col] == '--':
                    moves.append(Move((row, col), (row-1, col), self.board))

            if row - 1 >= 0 and col + 1 <= 7:
                l = self.board[row-1][col+1]
                if l[0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
            
            if row - 1 >= 0 and col - 1 >= 0:
                l = self.board[row-1][col-1]
                if l[0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))

        return moves
            
    def get_rook_moves(self, row, col, moves):
        
        y=self.board[row][col]
        for i in range(col+1, 8, 1):
            x=self.board[row][i]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(row,i),self.board))
                break
            else:
                moves.append(Move((row,col),(row,i),self.board))

        for i in range(col-1, -1, -1):
            x=self.board[row][i]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(row,i),self.board))
                break
            else:
                moves.append(Move((row,col),(row,i),self.board))

        for i in range(row+1, 8, 1):
            x=self.board[i][col]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(i,col),self.board))
                break
            else:
                moves.append(Move((row,col),(i,col),self.board))
            
            
        for i in range(row-1, -1, -1):

            x=self.board[i][col]
            if x[0]== y[0]:
                break
            elif x[0]!= y[0] and x!='--':
                moves.append(Move((row,col),(i,col),self.board))
                break
            else:
                moves.append(Move((row,col),(i,col),self.board))


class Move():
    def __init__(self, start_sq,end_sq, board,is_enpassant=False):
        self.start_row=start_sq[0]
        self.start_col=start_sq[1]
        self.end_row=end_sq[0]
        self.end_col=end_sq[1]
        self.piece_to_move=board[self.start_row][self.start_col]
        self.piece_captured=board[self.end_row][self.end_col]

        self.is_enpassant = is_enpassant
        if self.is_enpassant:
            self.piece_captured = 'bP' if self.piece_to_move == 'wP' else 'wP'

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.start_row == other.start_row and 
                    self.start_col == other.start_col and 
                    self.end_row == other.end_row and 
                    self.end_col == other.end_col)
        return False
        


def load_images():
    pieces=['bR','bN','bB','bQ','bK','bP','wR','wN','wB','wQ','wK','wP']
    for piece in pieces:
        img= pygame.image.load(f'chess_pieces/{piece}.png')
        scaled_img= pygame.transform.scale(img,(block_size,block_size))
        IMAGES[piece]= scaled_img

def draw_pieces(screen, gs):
    for row in range(8):
        for col in range(8):
            piece= gs[row][col]
            if piece != '--':
                img=IMAGES[piece]
                screen.blit(img,(col*block_size,row*block_size))



def main(): 
    pygame.init()
    screen= pygame.display.set_mode((w,h)) #create the sceen with the given dimensions
    pygame.display.set_caption("Master's Chess")
    run=True
    load_images()
    gs = GameState()

    #temp. data types to move the peice
    sq_selected=() # tuple to keep track of last selected sq
    player_clicked=[] # keep track of 2 co-oordinates where the peice is and where it wants it to go
    while run: # used to create events and interact with the board 
        for event in pygame.event.get(): # this one is used to create a exit point so we can exit from the infinite loop of events 
            if event.type == pygame.QUIT:
                run=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                x= location[1]//block_size
                y= location[0]//block_size

                if sq_selected==(x,y):
                    player_clicked=[]
                    sq_selected=()
                else:
                    sq_selected = (x,y)
                    player_clicked.append(sq_selected)
                    if len(player_clicked)==1:
                        if gs.board[player_clicked[0][0]][player_clicked[0][1]]=='--':
                            player_clicked=[]
                            sq_selected=()
                    elif len(player_clicked)==2:
                        clr_1=gs.board[player_clicked[0][0]][player_clicked[0][1]]
                        clr_2=gs.board[player_clicked[1][0]][player_clicked[1][1]]
                        if clr_1[0]==clr_2[0]:
                            player_clicked=[]
                            sq_selected=()
                        else:
                            move = Move(player_clicked[0], player_clicked[1], gs.board)
                            valid_moves= gs.get_valid_moves()
                            if move in valid_moves:                      
                                match_index = valid_moves.index(move)
                                gs.make_move(valid_moves[match_index])
                            player_clicked=[]
                            sq_selected=()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # Check if user pressed 'z'
                    gs.undo_move() # Roll back the last move
                    # Force-wiping tracking variables ensures selections clear on undo
                    player_clicked = []
                    sq_selected = ()

        board(screen) # call the board function to create those boxes on screen so it looks like chess board
        draw_pieces(screen, gs.board)
        pygame.display.flip() # to update the whole screen so the chess board shows up else the the board will not have the boxes without update
    pygame.quit()
    sys.exit()
    
# used to tell that run main only if main() is called else dont
if __name__ == "__main__": 
    main()