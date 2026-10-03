import math
import random
import tkinter as tk
from tkinter import messagebox

try:
    from logo_data import LOGO_PNG_BASE64, LOGO_SMALL_PNG_BASE64
except Exception:
    LOGO_PNG_BASE64 = None
    LOGO_SMALL_PNG_BASE64 = None

INITIAL_BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
]

PIECE_SYMBOLS = {
    "wK": "\u2654", "wQ": "\u2655", "wR": "\u2656",
    "wB": "\u2657", "wN": "\u2658", "wP": "\u2659",
    "bK": "\u265A", "bQ": "\u265B", "bR": "\u265C",
    "bB": "\u265D", "bN": "\u265E", "bP": "\u265F",
}

PIECE_VALUES = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000}

LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#F6F66B"
CHECK_COLOR = "#FF6B6B"
HINT_COLOR = "#7CFC9A"
ACCENT_COLOR = "#2E2E2E"
GOLD_COLOR = "#FFD700"
SQUARE_SIZE = 64
BOARD_PIXELS = SQUARE_SIZE * 8


class StartScreen:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("Chess - Start")
        self.root_window.geometry("360x560")
        self.root_window.resizable(False, False)
        self.root_window.configure(bg=ACCENT_COLOR)
        self.start_callback = None

        self.logo_canvas = tk.Canvas(
            self.root_window, width=240, height=240,
            bg=ACCENT_COLOR, highlightthickness=0
        )
        self.logo_canvas.pack(pady=(30, 10))
        self.logo_canvas.bind("<Motion>", self.on_logo_motion)
        self.logo_canvas.bind("<Leave>", self.on_logo_leave)
        self.logo_canvas.bind("<Button-1>", self.on_logo_click)

        self.title_label = tk.Label(
            self.root_window, text="CHESS", font=("Arial", 40, "bold"),
            fg=GOLD_COLOR, bg=ACCENT_COLOR
        )
        self.title_label.pack()

        self.subtitle_label = tk.Label(
            self.root_window, text="3D Animated Edition", font=("Arial", 13),
            fg="#CCCCCC", bg=ACCENT_COLOR
        )
        self.subtitle_label.pack(pady=(5, 20))

        self.start_button = tk.Button(
            self.root_window, text="START GAME", font=("Arial", 16, "bold"),
            width=15, bg=GOLD_COLOR, fg=ACCENT_COLOR, relief="flat",
            activebackground="#FFC000", command=self.go_to_settings
        )
        self.start_button.pack(pady=10)

        self.developer_label = tk.Label(
            self.root_window, text="Developed By Huraira Bin Badar",
            font=("Arial", 10, "italic"), fg="#888888", bg=ACCENT_COLOR
        )
        self.developer_label.pack(side="bottom", pady=(10, 12))

        self.animation_frame = 0
        self.hover_position = (120, 120)
        self.is_clicked = False
        self.animate_logo()

    def go_to_settings(self):
        for widget in self.root_window.winfo_children():
            widget.destroy()
        SettingsScreen(self.root_window, self.start_callback)

    def on_logo_motion(self, event):
        self.hover_position = (event.x, event.y)

    def on_logo_leave(self, event):
        self.hover_position = (120, 120)

    def on_logo_click(self, event):
        self.is_clicked = True
        self.root_window.after(200, self.reset_click)

    def reset_click(self):
        self.is_clicked = False

    def animate_logo(self):
        if not self.logo_canvas.winfo_exists():
            return
        self.logo_canvas.delete("all")
        center_x, center_y = 120, 120

        glow_radius = 70 + 6 * ((self.animation_frame % 40) / 40.0)
        for ring in range(6, 0, -1):
            alpha_color = "#%02X%02X00" % (40 + ring * 8, 30 + ring * 6)
            self.logo_canvas.create_oval(
                center_x - glow_radius - ring * 2, center_y - glow_radius - ring * 2,
                center_x + glow_radius + ring * 2, center_y + glow_radius + ring * 2,
                outline=alpha_color, width=2
            )

        hover_x, hover_y = self.hover_position
        tilt_x = (hover_x - center_x) / 12.0
        tilt_y = (hover_y - center_y) / 12.0
        if self.is_clicked:
            tilt_x *= 0.2
            tilt_y *= 0.2

        crown_base_y = center_y + 35
        self.logo_canvas.create_polygon(
            center_x - 50, crown_base_y, center_x + 50, crown_base_y,
            center_x + 40, crown_base_y + 15, center_x - 40, crown_base_y + 15,
            fill=GOLD_COLOR, outline="#B8860B", width=2
        )

        peak_left = (center_x - 40, center_y - 20)
        peak_center = (center_x, center_y - 45)
        peak_right = (center_x + 40, center_y - 20)
        self.logo_canvas.create_polygon(
            center_x - 50, crown_base_y,
            peak_left[0] + tilt_x, peak_left[1] + tilt_y,
            center_x - 20, center_y - 5,
            peak_center[0] + tilt_x, peak_center[1] + tilt_y,
            center_x + 20, center_y - 5,
            peak_right[0] + tilt_x, peak_right[1] + tilt_y,
            center_x + 50, crown_base_y,
            fill=GOLD_COLOR, outline="#B8860B", width=2
        )

        for peak_point in [peak_left, peak_center, peak_right]:
            px = peak_point[0] + tilt_x
            py = peak_point[1] + tilt_y
            self.logo_canvas.create_oval(
                px - 7, py - 7, px + 7, py + 7,
                fill="#FF4444", outline="#8B0000", width=2
            )

        cross_x = peak_center[0] + tilt_x
        cross_y = peak_center[1] + tilt_y - 18
        self.logo_canvas.create_line(cross_x - 6, cross_y, cross_x + 6, cross_y, fill="white", width=3)
        self.logo_canvas.create_line(cross_x, cross_y - 6, cross_x, cross_y + 6, fill="white", width=3)

        for gem_x in [center_x - 25, center_x, center_x + 25]:
            self.logo_canvas.create_oval(
                gem_x - 5, crown_base_y + 3, gem_x + 5, crown_base_y + 13,
                fill="#33CCFF", outline="#003366", width=1
            )

        for i in range(8):
            angle = (self.animation_frame * 4 + i * 45) * math.pi / 180
            sx = center_x + 100 * math.cos(angle)
            sy = center_y + 100 * math.sin(angle)
            if 0 <= sx <= 240 and 0 <= sy <= 240:
                size = 2 + (i % 3)
                self.logo_canvas.create_oval(
                    sx - size, sy - size, sx + size, sy + size, fill="white", outline=""
                )

        self.animation_frame += 1
        self.root_window.after(50, self.animate_logo)


class SettingsScreen:
    def __init__(self, root_window, start_callback):
        self.root_window = root_window
        self.root_window.title("Chess - Settings")
        self.root_window.geometry("380x620")
        self.root_window.resizable(False, False)
        self.root_window.configure(bg=ACCENT_COLOR)
        self.start_callback = start_callback

        self.game_mode = tk.StringVar(value="computer")
        self.difficulty = tk.StringVar(value="Medium")
        self.suggestions_enabled = tk.BooleanVar(value=True)

        tk.Label(
            self.root_window, text="SETTINGS", font=("Arial", 26, "bold"),
            fg=GOLD_COLOR, bg=ACCENT_COLOR
        ).pack(pady=(25, 20))

        tk.Label(
            self.root_window, text="Game Mode", font=("Arial", 14, "bold"),
            fg="#CCCCCC", bg=ACCENT_COLOR
        ).pack(anchor="w", padx=40)
        tk.Radiobutton(
            self.root_window, text="vs Computer (AI)", font=("Arial", 12),
            variable=self.game_mode, value="computer", bg=ACCENT_COLOR,
            fg="white", selectcolor=ACCENT_COLOR, activebackground=ACCENT_COLOR,
            highlightthickness=0, command=self.update_mode_visibility
        ).pack(anchor="w", padx=50)
        tk.Radiobutton(
            self.root_window, text="2 Players (local)", font=("Arial", 12),
            variable=self.game_mode, value="human", bg=ACCENT_COLOR,
            fg="white", selectcolor=ACCENT_COLOR, activebackground=ACCENT_COLOR,
            highlightthickness=0, command=self.update_mode_visibility
        ).pack(anchor="w", padx=50)

        self.difficulty_frame = tk.Frame(self.root_window, bg=ACCENT_COLOR)
        self.difficulty_frame.pack(pady=(15, 5), fill="x", padx=40)
        tk.Label(
            self.difficulty_frame, text="Difficulty", font=("Arial", 14, "bold"),
            fg="#CCCCCC", bg=ACCENT_COLOR
        ).pack(anchor="w")
        self.difficulty_buttons = {}
        button_row = tk.Frame(self.difficulty_frame, bg=ACCENT_COLOR)
        button_row.pack(anchor="w", pady=5)
        for difficulty in ["Easy", "Medium", "Hard"]:
            button = tk.Button(
                button_row, text=difficulty, font=("Arial", 11, "bold"), width=8,
                bg="#444444", fg="white", relief="flat", activebackground=GOLD_COLOR,
                command=lambda d=difficulty: self.select_difficulty(d)
            )
            button.grid(row=0, column=["Easy", "Medium", "Hard"].index(difficulty), padx=4)
            self.difficulty_buttons[difficulty] = button
        self.select_difficulty("Medium")

        tk.Label(
            self.root_window, text="Suggestions / Hints", font=("Arial", 14, "bold"),
            fg="#CCCCCC", bg=ACCENT_COLOR
        ).pack(anchor="w", padx=40, pady=(20, 5))
        suggestion_frame = tk.Frame(self.root_window, bg=ACCENT_COLOR)
        suggestion_frame.pack(anchor="w", padx=50)
        tk.Radiobutton(
            suggestion_frame, text="On (show best move hints)", font=("Arial", 11),
            variable=self.suggestions_enabled, value=True, bg=ACCENT_COLOR,
            fg="white", selectcolor=ACCENT_COLOR, activebackground=ACCENT_COLOR,
            highlightthickness=0
        ).pack(anchor="w")
        tk.Radiobutton(
            suggestion_frame, text="Off (no hints)", font=("Arial", 11),
            variable=self.suggestions_enabled, value=False, bg=ACCENT_COLOR,
            fg="white", selectcolor=ACCENT_COLOR, activebackground=ACCENT_COLOR,
            highlightthickness=0
        ).pack(anchor="w")

        tk.Button(
            self.root_window, text="BEGIN GAME", font=("Arial", 16, "bold"),
            width=15, bg=GOLD_COLOR, fg=ACCENT_COLOR, relief="flat",
            activebackground="#FFC000", command=self.begin_game
        ).pack(pady=30)

        tk.Label(
            self.root_window, text="Developed By Huraira Bin Badar",
            font=("Arial", 10, "italic"), fg="#888888", bg=ACCENT_COLOR
        ).pack(side="bottom", pady=(0, 12))

        self.update_mode_visibility()

    def update_mode_visibility(self):
        if self.game_mode.get() == "computer":
            for button in self.difficulty_buttons.values():
                button.config(state="normal")
                self.select_difficulty(self.difficulty.get())
        else:
            for button in self.difficulty_buttons.values():
                button.config(state="disabled", bg="#333333", fg="#777777")

    def select_difficulty(self, difficulty):
        self.difficulty.set(difficulty)
        if self.game_mode.get() != "computer":
            return
        for button_name, button in self.difficulty_buttons.items():
            if button_name == difficulty:
                button.config(bg=GOLD_COLOR, fg=ACCENT_COLOR)
            else:
                button.config(bg="#444444", fg="white")

    def begin_game(self):
        config = {
            "game_mode": self.game_mode.get(),
            "difficulty": self.difficulty.get(),
            "suggestions_enabled": self.suggestions_enabled.get(),
        }
        for widget in self.root_window.winfo_children():
            widget.destroy()
        if self.start_callback:
            self.start_callback(config)


class ChessAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.search_depth = {"Easy": 1, "Medium": 2, "Hard": 3}.get(difficulty, 2)

    def choose_move(self, board, color):
        all_legal_moves = self.get_all_legal_moves(board, color)
        if not all_legal_moves:
            return None
        if self.difficulty == "Easy":
            return random.choice(all_legal_moves)

        best_move = None
        best_score = -999999
        for move in all_legal_moves:
            score = self.evaluate_move(board, move, color, self.search_depth, -999999, 999999)
            if score > best_score:
                best_score = score
                best_move = move
            elif score == best_score and random.random() < 0.3:
                best_move = move
        return best_move

    def evaluate_move(self, board, move, color, depth, alpha, beta):
        from_square, to_square = move
        saved_state = self.save_board_state(board, from_square, to_square)
        self.apply_move_to_board(board, from_square, to_square)
        if depth <= 0:
            score = self.evaluate_board(board, color)
        else:
            opponent_color = "b" if color == "w" else "w"
            opponent_moves = self.get_all_legal_moves(board, opponent_color)
            if not opponent_moves:
                score = 99999
            else:
                score = 999999
                for opponent_move in opponent_moves:
                    opp_from, opp_to = opponent_move
                    opp_saved = self.save_board_state(board, opp_from, opp_to)
                    self.apply_move_to_board(board, opp_from, opp_to)
                    opp_score = self.evaluate_board(board, color)
                    self.restore_board_state(board, opp_from, opp_to, opp_saved)
                    if opp_score < score:
                        score = opp_score
                    if score < beta:
                        beta = score
                    if beta <= alpha:
                        break
        self.restore_board_state(board, from_square, to_square, saved_state)
        return score

    def save_board_state(self, board, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        state = {
            "from_piece": board[from_row][from_col],
            "to_piece": board[to_row][to_col],
            "en_passant": None,
        }
        moving_piece = board[from_row][from_col]
        if moving_piece and moving_piece[1] == "P" and to_col != from_col and board[to_row][to_col] == "":
            state["en_passant"] = (from_row, to_col, board[from_row][to_col])
        return state

    def apply_move_to_board(self, board, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        moving_piece = board[from_row][from_col]
        if moving_piece and moving_piece[1] == "P":
            if to_col != from_col and board[to_row][to_col] == "":
                board[from_row][to_col] = ""
            if to_row == 0 or to_row == 7:
                moving_piece = moving_piece[0] + "Q"
        board[to_row][to_col] = moving_piece
        board[from_row][from_col] = ""

    def restore_board_state(self, board, from_square, to_square, state):
        from_row, from_col = from_square
        to_row, to_col = to_square
        board[from_row][from_col] = state["from_piece"]
        board[to_row][to_col] = state["to_piece"]
        if state["en_passant"]:
            ep_row, ep_col, ep_piece = state["en_passant"]
            board[ep_row][ep_col] = ep_piece

    def evaluate_board(self, board, color):
        score = 0
        for row_index in range(8):
            for col_index in range(8):
                piece = board[row_index][col_index]
                if piece:
                    piece_value = PIECE_VALUES.get(piece[1], 0)
                    if piece[0] == color:
                        score += piece_value
                        if piece[1] == "P":
                            score += (6 - abs(3.5 - row_index)) * 0.1
                    else:
                        score -= piece_value
                        if piece[1] == "P":
                            score -= (6 - abs(3.5 - row_index)) * 0.1
        return score

    def get_all_legal_moves(self, board, color):
        all_moves = []
        for row_index in range(8):
            for col_index in range(8):
                piece = board[row_index][col_index]
                if piece and piece[0] == color:
                    for move_target in self.get_legal_moves_for_board(board, row_index, col_index):
                        all_moves.append(((row_index, col_index), move_target))
        return all_moves

    def get_legal_moves_for_board(self, board, row_index, col_index):
        pseudo_moves = self.get_pseudo_legal_moves_for_board(board, row_index, col_index)
        legal_moves = []
        moving_piece = board[row_index][col_index]
        moving_color = moving_piece[0]
        for move_row, move_col in pseudo_moves:
            saved_state = self.save_board_state(board, (row_index, col_index), (move_row, move_col))
            self.apply_move_to_board(board, (row_index, col_index), (move_row, move_col))
            king_position = self.find_king_position_on_board(board, moving_color)
            opponent_color = "b" if moving_color == "w" else "w"
            if king_position and not self.is_square_attacked_on_board(board, king_position, opponent_color):
                legal_moves.append((move_row, move_col))
            self.restore_board_state(board, (row_index, col_index), (move_row, move_col), saved_state)
        return legal_moves

    def get_pseudo_legal_moves_for_board(self, board, row_index, col_index):
        piece = board[row_index][col_index]
        if not piece:
            return []
        piece_color = piece[0]
        piece_type = piece[1]
        moves = []
        if piece_type == "P":
            direction = -1 if piece_color == "w" else 1
            start_row = 6 if piece_color == "w" else 1
            if 0 <= row_index + direction < 8 and board[row_index + direction][col_index] == "":
                moves.append((row_index + direction, col_index))
                if row_index == start_row and board[row_index + 2 * direction][col_index] == "":
                    moves.append((row_index + 2 * direction, col_index))
            for delta_col in [-1, 1]:
                new_col = col_index + delta_col
                new_row = row_index + direction
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece and target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
        elif piece_type == "N":
            knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for delta_row, delta_col in knight_offsets:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if not target_piece or target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
        elif piece_type in ["B", "R", "Q"]:
            sliding_directions = []
            if piece_type in ["B", "Q"]:
                sliding_directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            if piece_type in ["R", "Q"]:
                sliding_directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for delta_row, delta_col in sliding_directions:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                    new_row += delta_row
                    new_col += delta_col
        elif piece_type == "K":
            king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for delta_row, delta_col in king_offsets:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if not target_piece or target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
        return moves

    def find_king_position_on_board(self, board, color):
        for row_index in range(8):
            for col_index in range(8):
                if board[row_index][col_index] == color + "K":
                    return (row_index, col_index)
        return None

    def is_square_attacked_on_board(self, board, square, attacking_color):
        target_row, target_col = square
        for row_index in range(8):
            for col_index in range(8):
                piece = board[row_index][col_index]
                if piece and piece[0] == attacking_color:
                    if (target_row, target_col) in self.get_pseudo_legal_moves_for_board(board, row_index, col_index):
                        return True
        return False


class ChessGame:
    def __init__(self, root_window, config):
        self.root_window = root_window
        self.root_window.title("Chess - 3D")
        self.root_window.geometry(f"{BOARD_PIXELS + 40}x{BOARD_PIXELS + 150}")
        self.root_window.resizable(False, False)
        self.root_window.configure(bg=ACCENT_COLOR)

        self.board = [row[:] for row in INITIAL_BOARD]
        self.current_turn = "w"
        self.selected_square = None
        self.valid_moves_for_selected = []
        self.king_in_check_position = None
        self.hint_move = None
        self.hints_active = False

        self.game_mode = config.get("game_mode", "computer")
        self.difficulty = config.get("difficulty", "Medium")
        self.suggestions_enabled = config.get("suggestions_enabled", True)
        self.player_color = "w"
        self.ai_color = "b"
        self.is_ai_thinking = False
        self.is_animating = False
        self.ai_opponent = ChessAI(self.difficulty) if self.game_mode == "computer" else None
        self.hint_ai = ChessAI("Hard")

        header_frame = tk.Frame(self.root_window, bg=ACCENT_COLOR)
        header_frame.pack(fill="x", pady=(8, 4))

        if LOGO_SMALL_PNG_BASE64:
            self.header_logo_photo = tk.PhotoImage(data=LOGO_SMALL_PNG_BASE64)
            tk.Label(
                header_frame, image=self.header_logo_photo, bg=ACCENT_COLOR
            ).pack(side="left", padx=(12, 4))

        mode_text = "vs Computer" if self.game_mode == "computer" else "2 Players"
        self.status_label = tk.Label(
            header_frame, text="White's turn", font=("Arial", 15, "bold"),
            fg=GOLD_COLOR, bg=ACCENT_COLOR
        )
        self.status_label.pack(side="left", padx=15)

        self.mode_label = tk.Label(
            header_frame, text=f"{mode_text} | {self.difficulty}",
            font=("Arial", 10), fg="#999999", bg=ACCENT_COLOR
        )
        self.mode_label.pack(side="left", padx=10)

        self.hint_button = tk.Button(
            header_frame, text="Hint", font=("Arial", 11, "bold"),
            bg=GOLD_COLOR, fg=ACCENT_COLOR, relief="flat", width=6,
            state="normal" if self.suggestions_enabled else "disabled",
            command=self.show_hint
        )
        self.hint_button.pack(side="right", padx=15)

        self.board_canvas = tk.Canvas(
            self.root_window, width=BOARD_PIXELS, height=BOARD_PIXELS,
            bg=ACCENT_COLOR, highlightthickness=0
        )
        self.board_canvas.pack(padx=20, pady=5)
        self.board_canvas.bind("<Button-1>", self.on_canvas_click)

        tk.Label(
            self.root_window, text="Developed By Huraira Bin Badar",
            font=("Arial", 9, "italic"), fg="#777777", bg=ACCENT_COLOR
        ).pack(side="bottom", pady=(0, 6))

        self.draw_board()

    def square_center_pixels(self, row_index, col_index):
        center_x = col_index * SQUARE_SIZE + SQUARE_SIZE / 2
        center_y = row_index * SQUARE_SIZE + SQUARE_SIZE / 2
        return center_x, center_y

    def pixel_to_square(self, pixel_x, pixel_y):
        col_index = int(pixel_x // SQUARE_SIZE)
        row_index = int(pixel_y // SQUARE_SIZE)
        if 0 <= row_index < 8 and 0 <= col_index < 8:
            return (row_index, col_index)
        return None

    def draw_board(self, animation_state=None):
        self.board_canvas.delete("all")
        for row_index in range(8):
            for col_index in range(8):
                top_x = col_index * SQUARE_SIZE
                top_y = row_index * SQUARE_SIZE
                base_color = LIGHT_COLOR if (row_index + col_index) % 2 == 0 else DARK_COLOR

                if self.king_in_check_position == (row_index, col_index):
                    base_color = CHECK_COLOR
                if self.selected_square == (row_index, col_index):
                    base_color = "#6CA8CD"
                if self.hints_active and (row_index, col_index) in self.valid_moves_for_selected:
                    base_color = HIGHLIGHT_COLOR
                if self.hint_move and (row_index, col_index) in (self.hint_move[0], self.hint_move[1]):
                    base_color = HINT_COLOR

                self.board_canvas.create_rectangle(
                    top_x, top_y, top_x + SQUARE_SIZE, top_y + SQUARE_SIZE,
                    fill=base_color, outline=""
                )

                piece = self.board[row_index][col_index]
                if animation_state and (row_index, col_index) == animation_state["from_square"]:
                    continue
                if piece:
                    center_x, center_y = self.square_center_pixels(row_index, col_index)
                    self.draw_piece(center_x, center_y, piece, font_size=36)

        if animation_state:
            self.draw_floating_piece(animation_state)

    def draw_piece(self, center_x, center_y, piece, font_size=36):
        symbol = PIECE_SYMBOLS.get(piece, "")
        if not symbol:
            return
        text_color = "white" if piece[0] == "w" else "black"
        self.board_canvas.create_text(
            center_x, center_y, text=symbol, font=("Arial", font_size),
            fill=text_color
        )

    def draw_floating_piece(self, animation_state):
        piece = animation_state["piece"]
        current_x = animation_state["current_x"]
        current_y = animation_state["current_y"]
        arc_height = animation_state["arc_height"]
        shadow_scale = animation_state["shadow_scale"]
        piece_scale = animation_state["piece_scale"]

        shadow_radius_x = 18 * shadow_scale
        shadow_radius_y = 7 * shadow_scale
        self.board_canvas.create_oval(
            current_x - shadow_radius_x, current_y + 18 - shadow_radius_y,
            current_x + shadow_radius_x, current_y + 18 + shadow_radius_y,
            fill="#000000", outline="", stipple="gray50"
        )

        lifted_y = current_y - arc_height
        font_size = int(36 * piece_scale)
        self.draw_piece(current_x, lifted_y, piece, font_size=font_size)

    def on_canvas_click(self, event):
        if self.is_animating or self.is_ai_thinking:
            return
        if self.game_mode == "computer" and self.current_turn != self.player_color:
            return

        clicked_square = self.pixel_to_square(event.x, event.y)
        if clicked_square is None:
            return
        row_index, col_index = clicked_square
        clicked_piece = self.board[row_index][col_index]

        if self.selected_square is not None:
            if (row_index, col_index) in self.valid_moves_for_selected:
                self.hint_move = None
                self.hints_active = False
                self.start_move_animation(self.selected_square, (row_index, col_index))
                self.selected_square = None
                self.valid_moves_for_selected = []
                return
            else:
                self.selected_square = None
                self.valid_moves_for_selected = []
                self.hints_active = False

        if clicked_piece and clicked_piece[0] == self.current_turn:
            self.selected_square = (row_index, col_index)
            self.valid_moves_for_selected = self.get_legal_moves(row_index, col_index)
            self.hints_active = False

        self.draw_board()

    def start_move_animation(self, from_square, to_square, callback=None):
        self.is_animating = True
        from_row, from_col = from_square
        moving_piece = self.board[from_row][from_col]
        start_x, start_y = self.square_center_pixels(from_row, from_col)
        end_x, end_y = self.square_center_pixels(*to_square)
        total_frames = 18
        max_arc_height = 30

        def animate_frame(frame_index):
            if not self.board_canvas.winfo_exists():
                return
            if frame_index > total_frames:
                self.is_animating = False
                self.make_move(from_square, to_square)
                self.draw_board()
                if callback:
                    callback()
                else:
                    if not self.check_game_over():
                        self.trigger_ai_move()
                return

            progress = frame_index / total_frames
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            arc_height = max_arc_height * math.sin(math.pi * progress)
            shadow_scale = 1.0 - 0.5 * math.sin(math.pi * progress)
            piece_scale = 1.0 + 0.35 * math.sin(math.pi * progress)

            animation_state = {
                "from_square": from_square,
                "piece": moving_piece,
                "current_x": current_x,
                "current_y": current_y,
                "arc_height": arc_height,
                "shadow_scale": shadow_scale,
                "piece_scale": piece_scale,
            }
            self.draw_board(animation_state=animation_state)
            self.root_window.after(18, animate_frame, frame_index + 1)

        animate_frame(0)

    def trigger_ai_move(self):
        if self.game_mode != "computer":
            return
        if self.current_turn == self.ai_color:
            self.is_ai_thinking = True
            self.status_label.config(text="AI is thinking...")
            self.root_window.after(120, self.execute_ai_move)

    def execute_ai_move(self):
        ai_move = self.ai_opponent.choose_move(self.board, self.ai_color)
        self.is_ai_thinking = False
        if ai_move:
            from_square, to_square = ai_move
            self.start_move_animation(from_square, to_square)
        else:
            self.check_game_over()

    def show_hint(self):
        if not self.suggestions_enabled or self.is_animating or self.is_ai_thinking:
            return
        if self.game_mode == "computer" and self.current_turn != self.player_color:
            return

        suggested_move = self.hint_ai.choose_move(self.board, self.current_turn)
        if suggested_move:
            self.hint_move = suggested_move
            self.hints_active = True
            if self.selected_square is None:
                from_square = suggested_move[0]
                self.selected_square = from_square
                self.valid_moves_for_selected = self.get_legal_moves(*from_square)
            self.draw_board()
            self.status_label.config(text="Hint: yellow = moves, green = best")
            self.root_window.after(3000, self.clear_hint)

    def clear_hint(self):
        self.hint_move = None
        self.hints_active = False
        self.draw_board()
        self.update_status_text()

    def update_status_text(self):
        if self.current_turn == "w":
            self.status_label.config(text="White's turn")
        else:
            self.status_label.config(text="Black's turn")

    def make_move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        moving_piece = self.board[from_row][from_col]

        if moving_piece[1] == "P":
            if to_col != from_col and self.board[to_row][to_col] == "":
                self.board[from_row][to_col] = ""
            if to_row == 0 or to_row == 7:
                moving_piece = moving_piece[0] + "Q"

        self.board[to_row][to_col] = moving_piece
        self.board[from_row][from_col] = ""
        self.current_turn = "b" if self.current_turn == "w" else "w"
        self.update_check_status()
        self.update_status_text()

    def update_check_status(self):
        self.king_in_check_position = None
        opponent_color = "b" if self.current_turn == "w" else "w"
        king_position = self.find_king_position(self.current_turn)
        if king_position and self.is_square_attacked(king_position, opponent_color):
            self.king_in_check_position = king_position

    def find_king_position(self, color):
        for row_index in range(8):
            for col_index in range(8):
                if self.board[row_index][col_index] == color + "K":
                    return (row_index, col_index)
        return None

    def is_square_attacked(self, square, attacking_color):
        target_row, target_col = square
        for row_index in range(8):
            for col_index in range(8):
                piece = self.board[row_index][col_index]
                if piece and piece[0] == attacking_color:
                    if (target_row, target_col) in self.get_pseudo_legal_moves(row_index, col_index):
                        return True
        return False

    def get_legal_moves(self, row_index, col_index):
        pseudo_moves = self.get_pseudo_legal_moves(row_index, col_index)
        legal_moves = []
        moving_piece = self.board[row_index][col_index]
        moving_color = moving_piece[0]
        for move_row, move_col in pseudo_moves:
            saved_from = self.board[row_index][col_index]
            saved_to = self.board[move_row][move_col]
            saved_en_passant_pawn = None
            en_passant_col = None
            if moving_piece[1] == "P" and move_col != col_index and saved_to == "":
                en_passant_col = move_col
                saved_en_passant_pawn = self.board[row_index][move_col]
                self.board[row_index][move_col] = ""
            self.board[move_row][move_col] = saved_from
            self.board[row_index][col_index] = ""
            king_position = self.find_king_position(moving_color)
            opponent_color = "b" if moving_color == "w" else "w"
            if king_position and not self.is_square_attacked(king_position, opponent_color):
                legal_moves.append((move_row, move_col))
            self.board[row_index][col_index] = saved_from
            self.board[move_row][move_col] = saved_to
            if saved_en_passant_pawn is not None:
                self.board[row_index][en_passant_col] = saved_en_passant_pawn
        return legal_moves

    def get_pseudo_legal_moves(self, row_index, col_index):
        piece = self.board[row_index][col_index]
        if not piece:
            return []
        piece_color = piece[0]
        piece_type = piece[1]
        moves = []
        if piece_type == "P":
            direction = -1 if piece_color == "w" else 1
            start_row = 6 if piece_color == "w" else 1
            if 0 <= row_index + direction < 8 and self.board[row_index + direction][col_index] == "":
                moves.append((row_index + direction, col_index))
                if row_index == start_row and self.board[row_index + 2 * direction][col_index] == "":
                    moves.append((row_index + 2 * direction, col_index))
            for delta_col in [-1, 1]:
                new_col = col_index + delta_col
                new_row = row_index + direction
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = self.board[new_row][new_col]
                    if target_piece and target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
                    elif not target_piece:
                        if piece_color == "w" and row_index == 3:
                            if self.board[row_index][new_col] == "bP":
                                moves.append((new_row, new_col))
                        elif piece_color == "b" and row_index == 4:
                            if self.board[row_index][new_col] == "wP":
                                moves.append((new_row, new_col))
        elif piece_type == "N":
            knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for delta_row, delta_col in knight_offsets:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = self.board[new_row][new_col]
                    if not target_piece or target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
        elif piece_type in ["B", "R", "Q"]:
            sliding_directions = []
            if piece_type in ["B", "Q"]:
                sliding_directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            if piece_type in ["R", "Q"]:
                sliding_directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for delta_row, delta_col in sliding_directions:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = self.board[new_row][new_col]
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                    new_row += delta_row
                    new_col += delta_col
        elif piece_type == "K":
            king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for delta_row, delta_col in king_offsets:
                new_row, new_col = row_index + delta_row, col_index + delta_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = self.board[new_row][new_col]
                    if not target_piece or target_piece[0] != piece_color:
                        moves.append((new_row, new_col))
        return moves

    def has_any_legal_moves(self, color):
        for row_index in range(8):
            for col_index in range(8):
                piece = self.board[row_index][col_index]
                if piece and piece[0] == color:
                    if self.get_legal_moves(row_index, col_index):
                        return True
        return False

    def check_game_over(self):
        if not self.has_any_legal_moves(self.current_turn):
            if self.king_in_check_position is not None:
                if self.game_mode == "computer":
                    winner = "You" if self.current_turn == self.ai_color else "AI"
                    win_text = f"{winner} win!"
                else:
                    winner = "Black" if self.current_turn == "w" else "White"
                    win_text = f"{winner} wins!"
                self.status_label.config(text=f"Checkmate! {win_text}")
                messagebox.showinfo("Game Over", f"Checkmate! {win_text}")
            else:
                self.status_label.config(text="Stalemate! Draw!")
                messagebox.showinfo("Game Over", "Stalemate! Draw!")
            return True
        return False


def main():
    root_window = tk.Tk()

    if LOGO_PNG_BASE64:
        root_window.logo_photo = tk.PhotoImage(data=LOGO_PNG_BASE64)
        root_window.iconphoto(True, root_window.logo_photo)

    def start_game_with_config(config):
        ChessGame(root_window, config)

    start_screen = StartScreen(root_window)
    start_screen.start_callback = start_game_with_config
    root_window.mainloop()


if __name__ == "__main__":
    main()
