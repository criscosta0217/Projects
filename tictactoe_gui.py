import tkinter as tk
from tkinter import messagebox

board = [' ' for x in range(10)]  # index 0 unused


def insertLetter(letter, pos):
    board[pos] = letter


def spaceIsFree(pos):
    return board[pos] == ' '


def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # left
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # middle col
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # right
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diag
            (bo[9] == le and bo[5] == le and bo[1] == le))    # diag


def isBoardFull(bo):
    # index 0 is always blank, so > 1 means there are still playable spaces
    return bo.count(' ') <= 1


def selectRandom(li):
    import random
    return random.choice(li)


def compMove():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0

    # winning move or block
    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                return i

    cornersOpen = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if cornersOpen:
        return selectRandom(cornersOpen)

    if 5 in possibleMoves:
        return 5

    edgesOpen = [i for i in possibleMoves if i in [2, 4, 6, 8]]
    if edgesOpen:
        return selectRandom(edgesOpen)

    return move  # 0 means no move possible


# ---------------- GUI PART ----------------

root = tk.Tk()
root.title("Tic Tac Toe")

status_var = tk.StringVar(value="Your turn (X). Click a square.")
buttons = {}


def update_gui():
    """Refresh button text based on board state."""
    for pos in range(1, 10):
        buttons[pos].config(text=board[pos])


def end_game(message):
    status_var.set(message)
    messagebox.showinfo("Game Over", message)
    for pos in range(1, 10):
        buttons[pos].config(state="disabled")


def handle_player_click(pos):
    """Player clicks a button -> place X -> check -> computer plays O -> check."""
    if not spaceIsFree(pos):
        return

    # Player move
    insertLetter('X', pos)
    update_gui()

    if isWinner(board, 'X'):
        end_game("You win! (X)")
        return

    if isBoardFull(board):
        end_game("It's a tie!")
        return

    # Computer move
    status_var.set("Computer thinking...")
    root.update_idletasks()

    move = compMove()
    if move == 0:
        end_game("It's a tie!")
        return

    insertLetter('O', move)
    update_gui()

    if isWinner(board, 'O'):
        end_game("Computer wins! (O)")
        return

    if isBoardFull(board):
        end_game("It's a tie!")
        return

    status_var.set("Your turn (X). Click a square.")


def new_game():
    global board
    board = [' ' for x in range(10)]
    for pos in range(1, 10):
        buttons[pos].config(state="normal")
    update_gui()
    status_var.set("Your turn (X). Click a square.")


# Layout: 3x3 grid, mapping to your positions:
# 7 8 9
# 4 5 6
# 1 2 3
pos_grid = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3]
]

for r in range(3):
    for c in range(3):
        pos = pos_grid[r][c]
        btn = tk.Button(
            root,
            text=" ",
            width=6,
            height=3,
            font=("Arial", 18),
            command=lambda p=pos: handle_player_click(p)
        )
        btn.grid(row=r, column=c, padx=5, pady=5)
        buttons[pos] = btn

status_label = tk.Label(root, textvariable=status_var, font=("Arial", 12))
status_label.grid(row=3, column=0, columnspan=3, pady=(8, 0))

new_btn = tk.Button(root, text="New Game", command=new_game)
new_btn.grid(row=4, column=0, columnspan=3, pady=8)

update_gui()
root.mainloop()
