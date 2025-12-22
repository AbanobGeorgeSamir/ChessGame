import pygame
import os

WIDTH, HEIGHT = 800, 800       
TILE_SIZE = WIDTH // 8       
FPS = 60                  
IMAGE_FOLDER = "images"    

WHITE_COLOR = (255, 255, 255)
DARK = (118, 150, 86)
LIGHT = (238, 238, 210)
HIGHLIGHT_COLOR = (200, 200, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")
clock = pygame.time.Clock()

def load_piece_images():
    pieces = ["black_bishop", "black_king", "black_knight", "black_pawn", "black_queen", "black_rook",
              "white_bishop", "white_king", "white_knight", "white_pawn", "white_queen", "white_rook"]
    images = {}
    for piece in pieces:
        path = os.path.join(IMAGE_FOLDER, f"{piece}.png")
        if os.path.exists(path):
            images[piece] = pygame.transform.scale(pygame.image.load(path), (TILE_SIZE - 10, TILE_SIZE - 10))
        else:
            print(f"Error: Image not found - {path}")
    return images

piece_images = load_piece_images()

def get_team(piece):
    if piece.startswith("white_"):
        return "white"
    elif piece.startswith("black_"):
        return "black"
    return None

board = [
    ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
    ["black_pawn"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["white_pawn"] * 8,
    ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]
]

selected_piece = None
selected_pos = None
valid_moves = []
turn = "white"  

def get_valid_moves(row, col):
    piece = board[row][col]
    team = get_team(piece)
    moves = []
    
    if "pawn" in piece:
        direction = -1 if team == "white" else 1
        if 0 <= row + direction < 8 and board[row + direction][col] == "":
            moves.append((row + direction, col))
        if team == "white" and row == 6 and board[row + direction][col] == "" and board[row + 2 * direction][col] == "":
            moves.append((row + 2 * direction, col))
        if team == "black" and row == 1 and board[row + direction][col] == "" and board[row + 2 * direction][col] == "":
            moves.append((row + 2 * direction, col))
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] != "" and get_team(board[new_row][new_col]) != team:
                moves.append((new_row, new_col))
                
    elif "knight" in piece:
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                dest = board[new_row][new_col]
                if dest == "" or get_team(dest) != team:
                    moves.append((new_row, new_col))
                    
    elif "bishop" in piece:
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    dest = board[new_row][new_col]
                    if dest == "":
                        moves.append((new_row, new_col))
                    else:
                        if get_team(dest) != team:
                            moves.append((new_row, new_col))
                        break
                else:
                    break
                    
    elif "rook" in piece:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    dest = board[new_row][new_col]
                    if dest == "":
                        moves.append((new_row, new_col))
                    else:
                        if get_team(dest) != team:
                            moves.append((new_row, new_col))
                        break
                else:
                    break
                    
    elif "queen" in piece:
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    dest = board[new_row][new_col]
                    if dest == "":
                        moves.append((new_row, new_col))
                    else:
                        if get_team(dest) != team:
                            moves.append((new_row, new_col))
                        break
                else:
                    break
                    
    elif "king" in piece:
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                dest = board[new_row][new_col]
                if dest == "" or get_team(dest) != team:
                    moves.append((new_row, new_col))
                    
    return moves

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            if (row, col) in valid_moves:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)
            
            piece = board[row][col]
            if piece:
                screen.blit(piece_images[piece], (col * TILE_SIZE + 5, row * TILE_SIZE + 5))
                
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE_COLOR)
    draw_board()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE
            
            if selected_piece:
                if (row, col) in valid_moves:
                    board[row][col] = selected_piece
                    board[selected_pos[0]][selected_pos[1]] = ""
                    turn = "black" if turn == "white" else "white"
                selected_piece = None
                valid_moves = []
            else:
                if board[row][col] != "" and get_team(board[row][col]) == turn:
                    selected_piece = board[row][col]
                    selected_pos = (row, col)
                    valid_moves = get_valid_moves(row, col)
                    
    pygame.display.flip()
    
pygame.quit()
