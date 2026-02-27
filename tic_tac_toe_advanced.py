import tkinter as tk
from tkinter import messagebox
import random
import math

# ---------------------------- Game Logic ----------------------------
def check_winner(board):
    """Return 'X' or 'O' if someone wins, else None. Also return winning pattern."""
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != ' ':
            return board[pattern[0]], pattern
    return None, None

def is_full(board):
    return ' ' not in board

# Bot moves
def bot_move_easy(board, player):
    available = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(available) if available else None

def bot_move_medium(board, player):
    opponent = 'X' if player == 'O' else 'O'
    # Win
    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            if check_winner(board)[0] == player:
                board[i] = ' '
                return i
            board[i] = ' '
    # Block
    for i in range(9):
        if board[i] == ' ':
            board[i] = opponent
            if check_winner(board)[0] == opponent:
                board[i] = ' '
                return i
            board[i] = ' '
    # Random
    available = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(available)

def minimax(board, depth, is_maximizing, ai_player, human_player):
    winner, _ = check_winner(board)
    if winner == ai_player:
        return 10 - depth
    elif winner == human_player:
        return depth - 10
    elif is_full(board):
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = ai_player
                score = minimax(board, depth+1, False, ai_player, human_player)
                board[i] = ' '
                best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = human_player
                score = minimax(board, depth+1, True, ai_player, human_player)
                board[i] = ' '
                best = min(score, best)
        return best

def bot_move_hard(board, player):
    ai_player = player
    human_player = 'X' if player == 'O' else 'O'
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_player
            score = minimax(board, 0, False, ai_player, human_player)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# ---------------------------- GUI Class ----------------------------
class AdvancedTicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Tic-Tac-Toe")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")  # dark blue-gray background

        # Variables
        self.mode = None          # '2player' or 'bot'
        self.difficulty = None     # 'easy', 'medium', 'hard'
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.score_x = 0
        self.score_o = 0
        self.bot_delay = 500       # ms

        # Colors
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.grid_color = "#34495E"
        self.x_color = "#E74C3C"   # red
        self.o_color = "#3498DB"   # blue
        self.win_color = "#F1C40F" # yellow

        # Create main menu
        self.create_menu()

        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------------------- Menus ----------------------------
    def create_menu(self):
        self.clear_window()
        self.root.configure(bg=self.bg_color)

        # Title
        title = tk.Label(self.root, text="Tic-Tac-Toe", font=("Helvetica", 28, "bold"),
                         bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=30)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        # Two Player button
        self.create_beautiful_button(btn_frame, "Two Players", self.start_2player, width=200).pack(pady=10)
        # Vs Computer button
        self.create_beautiful_button(btn_frame, "Vs Computer", self.show_difficulty_menu, width=200).pack(pady=10)
        # Exit button
        self.create_beautiful_button(btn_frame, "Exit", self.root.quit, width=200).pack(pady=10)

    def show_difficulty_menu(self):
        self.clear_window()
        self.root.configure(bg=self.bg_color)

        tk.Label(self.root, text="Select Difficulty", font=("Helvetica", 22, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=30)

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        self.create_beautiful_button(btn_frame, "Easy", lambda: self.start_bot('easy'), width=200).pack(pady=10)
        self.create_beautiful_button(btn_frame, "Medium", lambda: self.start_bot('medium'), width=200).pack(pady=10)
        self.create_beautiful_button(btn_frame, "Hard", lambda: self.start_bot('hard'), width=200).pack(pady=10)
        self.create_beautiful_button(btn_frame, "Back", self.create_menu, width=200).pack(pady=10)

    def create_beautiful_button(self, parent, text, command, width=150):
        btn = tk.Button(parent, text=text, font=("Helvetica", 14, "bold"),
                        bg="#3498DB", fg="white", activebackground="#2980B9",
                        activeforeground="white", bd=0, padx=20, pady=10,
                        width=20, command=command)
        return btn

    # ---------------------------- Game Initialization ----------------------------
    def start_2player(self):
        self.mode = '2player'
        self.reset_game()
        self.create_game_board()

    def start_bot(self, difficulty):
        self.mode = 'bot'
        self.difficulty = difficulty
        self.reset_game()
        self.create_game_board()

    def reset_game(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        # Scores not reset automatically, could add a reset score button

    # ---------------------------- Game Board UI ----------------------------
    def create_game_board(self):
        self.clear_window()
        self.root.configure(bg=self.bg_color)

        # Top bar with scores and mode
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Score X
        score_x_label = tk.Label(top_frame, text=f"X : {self.score_x}", font=("Helvetica", 14, "bold"),
                                 bg=self.bg_color, fg=self.x_color)
        score_x_label.pack(side=tk.LEFT, padx=20)

        # Mode display
        mode_text = "Two Players" if self.mode == '2player' else f"Vs Computer ({self.difficulty.capitalize()})"
        mode_label = tk.Label(top_frame, text=mode_text, font=("Helvetica", 14, "bold"),
                              bg=self.bg_color, fg=self.fg_color)
        mode_label.pack(side=tk.LEFT, expand=True)

        # Score O
        score_o_label = tk.Label(top_frame, text=f"O : {self.score_o}", font=("Helvetica", 14, "bold"),
                                 bg=self.bg_color, fg=self.o_color)
        score_o_label.pack(side=tk.RIGHT, padx=20)

        # Turn indicator
        self.turn_label = tk.Label(self.root, text="Player X's turn", font=("Helvetica", 16, "bold"),
                                   bg=self.bg_color, fg=self.fg_color)
        self.turn_label.pack(pady=5)

        # Canvas for board
        self.canvas_size = 400
        self.cell_size = self.canvas_size // 3
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size,
                                bg="#ECF0F1", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Draw grid lines
        self.draw_grid()

        # Bind click
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=10)

        self.create_beautiful_button(control_frame, "Restart", self.restart_game, width=15).pack(side=tk.LEFT, padx=5)
        self.create_beautiful_button(control_frame, "Menu", self.create_menu, width=15).pack(side=tk.LEFT, padx=5)

        # Store labels for later update
        self.score_x_label = score_x_label
        self.score_o_label = score_o_label

        # If bot mode and current player is O? But we always start with X, so no.
        # However if human wants to be O, we could swap but default X first.

    def draw_grid(self):
        """Draw the 3x3 grid lines."""
        self.canvas.delete("grid")
        for i in range(1, 3):
            # vertical lines
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_size, fill=self.grid_color, width=3, tags="grid")
            # horizontal lines
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_size, y, fill=self.grid_color, width=3, tags="grid")

    def draw_move(self, idx, player):
        """Draw X or O on canvas at given cell index."""
        row, col = divmod(idx, 3)
        x0 = col * self.cell_size + 15
        y0 = row * self.cell_size + 15
        x1 = (col + 1) * self.cell_size - 15
        y1 = (row + 1) * self.cell_size - 15

        if player == 'X':
            self.canvas.create_line(x0, y0, x1, y1, fill=self.x_color, width=5, tags="move")
            self.canvas.create_line(x0, y1, x1, y0, fill=self.x_color, width=5, tags="move")
        else:  # O
            self.canvas.create_oval(x0, y0, x1, y1, outline=self.o_color, width=5, tags="move")

    def highlight_winning_line(self, pattern):
        """Draw a thick line over the winning pattern."""
        if not pattern:
            return
        # Get center coordinates of the three cells
        start_idx = pattern[0]
        end_idx = pattern[2]
        start_row, start_col = divmod(start_idx, 3)
        end_row, end_col = divmod(end_idx, 3)
        # Center points
        x0 = start_col * self.cell_size + self.cell_size // 2
        y0 = start_row * self.cell_size + self.cell_size // 2
        x1 = end_col * self.cell_size + self.cell_size // 2
        y1 = end_row * self.cell_size + self.cell_size // 2
        self.canvas.create_line(x0, y0, x1, y1, fill=self.win_color, width=8, tags="win_line")

    # ---------------------------- Game Logic ----------------------------
    def on_canvas_click(self, event):
        if self.game_over:
            return
        # Determine cell
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if col >= 3 or row >= 3:
            return
        idx = row * 3 + col

        if self.board[idx] != ' ':
            return  # already occupied

        # Human move
        self.make_move(idx, self.current_player)

    def make_move(self, idx, player):
        """Place a mark, update board and canvas, check game status."""
        if self.game_over or self.board[idx] != ' ':
            return False

        self.board[idx] = player
        self.draw_move(idx, player)

        # Check win/draw
        winner, pattern = check_winner(self.board)
        if winner:
            self.game_over = True
            self.highlight_winning_line(pattern)
            self.turn_label.config(text=f"Player {winner} wins!")
            # Update score
            if winner == 'X':
                self.score_x += 1
                self.score_x_label.config(text=f"X : {self.score_x}")
            else:
                self.score_o += 1
                self.score_o_label.config(text=f"O : {self.score_o}")
            # Disable further clicks? We'll just ignore due to game_over flag.
            return True
        elif is_full(self.board):
            self.game_over = True
            self.turn_label.config(text="It's a draw!")
            return True

        # Switch player
        self.current_player = 'O' if player == 'X' else 'X'
        self.turn_label.config(text=f"Player {self.current_player}'s turn")

        # If bot mode and now bot's turn (O), schedule bot move
        if self.mode == 'bot' and self.current_player == 'O' and not self.game_over:
            self.root.after(self.bot_delay, self.bot_move)

        return True

    def bot_move(self):
        if self.game_over or self.current_player != 'O':
            return

        # Choose move based on difficulty
        if self.difficulty == 'easy':
            move = bot_move_easy(self.board, 'O')
        elif self.difficulty == 'medium':
            move = bot_move_medium(self.board, 'O')
        else:  # hard
            move = bot_move_hard(self.board, 'O')

        if move is not None:
            self.make_move(move, 'O')

    def restart_game(self):
        """Reset board for a new game."""
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.canvas.delete("move")
        self.canvas.delete("win_line")
        self.turn_label.config(text="Player X's turn")

# ---------------------------- Main ----------------------------
if __name__ == "__main__":
    game = AdvancedTicTacToe()