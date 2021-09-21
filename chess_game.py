import pygame
import sys

def main():
    pygame.init()
    WHITE = (255, 255, 255)
    RED_WOOD = (113, 68, 55)
    BROWN_YELLOW = (195, 155, 119)
    BLACK = (0, 0, 0)
    YELLOW = (240, 223, 0)
    GREEN = (75, 233, 0)
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    fps = 10
    turn_font = pygame.font.SysFont('verdana', 32)
    
    board = ["r", "n", "b", "q","k", "b", "n", "r",
             "p", "p", "p", "p","p", "p", "p", "p",
             " ", " ", " ", " "," ", " ", " ", " ",
             " ", " ", " ", " "," ", " ", " ", " ",
             " ", " ", " ", " "," ", " ", " ", " ",
             " ", " ", " ", " "," ", " ", " ", " ",
             "P", "P", "P", "P","P", "P", "P", "P",
             "R", "N", "B", "Q", "K","B", "N", "R",]

    images = {"R":pygame.image.load("rook.png"),
              "N":pygame.image.load("knight.png"),
              "B":pygame.image.load("bishop.png"),
              "Q":pygame.image.load("queen.png"),
              "K":pygame.image.load("king.png"),
              "P":pygame.image.load("pawn.png"),
              "r":pygame.image.load("rook_black.png"),
              "n":pygame.image.load("knight_black.png"),
              "b":pygame.image.load("bishop_black.png"),
              "q":pygame.image.load("queen_black.png"),
              "k":pygame.image.load("king_black.png"),
              "p":pygame.image.load("pawn_black.png")}


    white_pieces = [i for i in range(64) if board[i].isupper()]
    black_pieces = [i for i in range(64) if board[i].islower()]

    move_score {"pawn move":1, "pawn capture":2, "knight move":3, "bishop move":4,"knight capture":5,
                "bishop capture":6, "rook move":7, "rook capture":8, "queen move":9, "queen capture":10,
                "pawn promotion":11, "king threat":12, "check mate":13}
    
    selected = None
    moves = []
    turn = "white"
    def bishop_moves(piece, friend_pieces, foe_pieces):
        moves = []
        i = 1
        while piece[0]+i <= 8 and piece[1]+i <= 8:
            if (piece[1]-1+i)*8+(piece[0]-1+i) in friend_pieces:
                break
            elif (piece[1]-1+i)*8+(piece[0]-1+i) in foe_pieces:
                moves.append((piece[0]+i, piece[1]+i))
                break
            else:
                moves.append((piece[0]+i, piece[1]+i))
            i += 1
        i = 1
        while 0 < piece[0]-i and 0 < piece[1]-i:
            if (piece[1]-1-i)*8+(piece[0]-1-i) in friend_pieces:
                break
            elif (piece[1]-1-i)*8+(piece[0]-1-i) in foe_pieces:
                moves.append((piece[0]-i, piece[1]-i))
                break
            else:
                moves.append((piece[0]-i, piece[1]-i))
            i += 1
        i = 1
        while 0 < piece[0]-i and piece[1]+i <= 8:
            if (piece[1]-1+i)*8+(piece[0]-1-i) in friend_pieces:
                break
            elif (piece[1]-1+i)*8+(piece[0]-1-i) in foe_pieces:
                moves.append((piece[0]-i, piece[1]+i))
                break
            else:
                moves.append((piece[0]-i, piece[1]+i))
            i += 1
        i = 1
        while piece[0]+i <= 8 and 0 < piece[1]-i:
            if (piece[1]-1-i)*8+(piece[0]-1+i) in friend_pieces:
                break
            elif (piece[1]-1-i)*8+(piece[0]-1+i) in foe_pieces:
                moves.append((piece[0]+i, piece[1]-i))
                break
            else:
                moves.append((piece[0]+i, piece[1]-i))
            i += 1
        return moves
    def rook_moves(piece, friend_pieces, foe_pieces):
        moves = []
        i = piece[0]-1
        while 0 < i:
            if (piece[1]-1)*8+(i-1) in friend_pieces:
                break
            elif (piece[1]-1)*8+(i-1) in foe_pieces:
                moves.append((i, piece[1]))
                break
            else:
                moves.append((i, piece[1]))
            i -= 1
        i = piece[0]+1
        while i <= 8:
            if (piece[1]-1)*8+(i-1) in friend_pieces:
                break
            elif (piece[1]-1)*8+(i-1) in foe_pieces:
                moves.append((i, piece[1]))
                break
            else:
                moves.append((i, piece[1]))
            i += 1
        i = piece[1]-1
        while 0 < i:
            if (i-1)*8+(piece[0]-1) in friend_pieces:
                break
            elif (i-1)*8+(piece[0]-1) in foe_pieces:
                moves.append((piece[0], i))
                break
            else:
                moves.append((piece[0], i))
            i -= 1
        i = piece[1]+1
        while i <= 8:
            if (i-1)*8+(piece[0]-1) in friend_pieces:
                break
            elif (i-1)*8+(piece[0]-1) in foe_pieces:
                moves.append((piece[0], i))
                break
            else:
                moves.append((piece[0], i))
            i += 1
        return moves

    def get_moves(piece, friend_pieces, foe_pieces):
        moves = []
        index = (piece[1]-1)*8+(piece[0]-1)
        if board[index] == "P":
            if piece[1] == 7:
                moves.append((piece[0], piece[1]-1))
                moves.append((piece[0], piece[1]-2))
            else:
                moves.append((piece[0], piece[1]-1))
        elif board[index] == "p":
            if piece[1] == 2:
                moves.append((piece[0], piece[1]+1))
                moves.append((piece[0], piece[1]+2))
            else:
                moves.append((piece[0], piece[1]+1))
        elif board[index].lower() == "n":
            for i in [-1, 1]:
                for j in [-2, 2]:
                    moves.append((piece[0]+i, piece[1]+j))
                    moves.append((piece[0]+j, piece[1]+i))
            
        elif board[index].lower() == "r":
            moves = rook_moves(piece, friend_pieces, foe_pieces)
        elif board[index].lower() == "b":
            moves = bishop_moves(piece, friend_pieces, foe_pieces)
        elif board[index].lower() == "q":
            moves = bishop_moves(piece, friend_pieces, foe_pieces)
            moves.extend(rook_moves(piece, friend_pieces, foe_pieces))
        elif board[index].lower() == "k":
            foe_moves = [get_moves(((i%8)+1, (i//8)+1), foe_pieces, friend_pieces) for i in foe_pieces if board[i].lower() != "k"]
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if not (i == 0 and j == 0):
                        if all([(piece[0]+i, piece[1]+j) not in m for m in foe_moves]) and (piece[1]+j-1)*8+(piece[0]+i-1) not in friend_pieces:
                            moves.append((piece[0]+i, piece[1]+j))
        return list(filter(lambda x:(x[1]-1)*8+(x[0]-1) not in friend_pieces and 0 < x[0] <= 8  and 0 < x[1] <= 8, moves))

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
        screen.fill(WHITE)
        screen.blit(turn_font.render(f"{turn}'s move", False, BLACK), (300,42))
        color1 = RED_WOOD
        color2 = BROWN_YELLOW
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        white_pieces = [i for i in range(64) if board[i].isupper()]
        black_pieces = [i for i in range(64) if board[i].islower()]
        for i in range(1, 9):
            for j in range(1, 9):
                if j % 2 == 0:
                    pygame.draw.rect(screen, color1, (j*83, i*83, 83, 83))
                else:
                    pygame.draw.rect(screen, color2, (j*83, i*83, 83, 83))
                if board[8*(i-1)+(j-1)] != " ":screen.blit(images.get(board[8*(i-1)+(j-1)]), (j*83,i*83))
                if j*83+83 > mouse[0] > j*83 and i*83+83 > mouse[1] > i*83 and click[0]:
                    if turn == "white":
                        if not selected and (mouse[1]//83-1)*8+(mouse[0]//83-1) in white_pieces:
                            selected = (mouse[0]//83, mouse[1]//83)
                            moves = get_moves((mouse[0]//83, mouse[1]//83), white_pieces, black_pieces)
                        else: 
                            if (mouse[0]//83, mouse[1]//83) in moves and click[0]:
                                board[(mouse[1]//83-1)*8+(mouse[0]//83-1)], board[(selected[1]-1)*8+(selected[0]-1)] = board[(selected[1]-1)*8+(selected[0]-1)], " "
                                turn = "black"
                                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("move.mp3"))
                            moves = []
                            selected = None
                    else:
                        if not selected and (mouse[1]//83-1)*8+(mouse[0]//83-1) in black_pieces:
                            selected = (mouse[0]//83, mouse[1]//83)
                            moves = get_moves((mouse[0]//83, mouse[1]//83), black_pieces, white_pieces)
                        else:
                            if (mouse[0]//83, mouse[1]//83) in moves and click[0]:
                                board[(mouse[1]//83-1)*8+(mouse[0]//83-1)], board[(selected[1]-1)*8+(selected[0]-1)] = board[(selected[1]-1)*8+(selected[0]-1)], " "
                                turn = "white"
                                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("move.mp3"))
                            moves = []
                            selected = None
            color1, color2 = color2, color1
        if selected != None:
            pygame.draw.rect(screen, GREEN, (selected[0]*83, selected[1]*83, 83, 83), 5)
            for pos in moves:
                if (pos[1]-1)*8+(pos[0]-1) in white_pieces or (pos[1]-1)*8+(pos[0]-1) in black_pieces:
                    pygame.draw.rect(screen, YELLOW, (pos[0]*83, pos[1]*83, 83, 83), 5)
                else:
                    pygame.draw.circle(screen, GREEN, (pos[0]*83+41, pos[1]*83+41), 5)
        pygame.display.update()


if __name__ == "__main__":
    main()
