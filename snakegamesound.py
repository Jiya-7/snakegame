"""
SNAKE GAME - PYTHON 3.14 (WINDOWS)

Features:
- Wall wrap (snake does not die on edges)
- Snake dies only when touching itself
- Restart button
- Sound effects (eat + game over)
- Beginner-friendly comments
"""

import tkinter as tk      # GUI library (built-in)
import random             # For random food position
import winsound           # For sound effects (Windows only)

# ---------------------------------
# GAME CONSTANTS
# ---------------------------------

WIDTH = 400          # Width of game window
HEIGHT = 400         # Height of game window
CELL_SIZE = 20       # Size of snake block
SPEED = 120          # Snake speed (milliseconds)

# ---------------------------------
# MAIN GAME CLASS
# ---------------------------------

class SnakeGame:
    def __init__(self, root):
        """
        This runs when the game starts
        """

        self.root = root
        self.root.title("Snake Game - Python 3.14")

        # Create game canvas
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="black"
        )
        self.canvas.pack()

        # Restart button
        self.restart_button = tk.Button(
            root,
            text="Restart Game",
            command=self.restart_game
        )
        self.restart_button.pack(pady=5)

        # Keyboard controls
        root.bind("<Up>", lambda e: self.change_direction("UP"))
        root.bind("<Down>", lambda e: self.change_direction("DOWN"))
        root.bind("<Left>", lambda e: self.change_direction("LEFT"))
        root.bind("<Right>", lambda e: self.change_direction("RIGHT"))

        # Start game
        self.restart_game()

    # ---------------------------------
    # SOUND FUNCTIONS
    # ---------------------------------

    def play_eat_sound(self):
        """Sound when snake eats food"""
        winsound.Beep(800, 100)

    def play_game_over_sound(self):
        """Sound when game ends"""
        winsound.Beep(300, 400)

    # ---------------------------------
    # RESTART GAME
    # ---------------------------------

    def restart_game(self):
        """
        Resets all values and starts a new game
        """

        self.snake = [
            (200, 200),
            (180, 200),
            (160, 200)
        ]

        self.direction = "RIGHT"
        self.score = 0
        self.game_running = True

        self.food = self.create_food()
        self.update_game()

    # ---------------------------------
    # CREATE FOOD
    # ---------------------------------

    def create_food(self):
        """
        Generates food at a random position
        """

        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return (x, y)

    # ---------------------------------
    # CHANGE DIRECTION
    # ---------------------------------

    def change_direction(self, new_direction):
        """
        Changes direction
        Prevents reverse movement
        """

        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    # ---------------------------------
    # GAME LOOP
    # ---------------------------------

    def update_game(self):
        """
        Main game loop
        """

        if not self.game_running:
            return

        # Get current head position
        head_x, head_y = self.snake[0]

        # Move snake
        if self.direction == "UP":
            head_y -= CELL_SIZE
        elif self.direction == "DOWN":
            head_y += CELL_SIZE
        elif self.direction == "LEFT":
            head_x -= CELL_SIZE
        elif self.direction == "RIGHT":
            head_x += CELL_SIZE

        # ---------------------------------
        # WALL WRAP (NO DEATH)
        # ---------------------------------

        if head_x < 0:
            head_x = WIDTH - CELL_SIZE
        elif head_x >= WIDTH:
            head_x = 0

        if head_y < 0:
            head_y = HEIGHT - CELL_SIZE
        elif head_y >= HEIGHT:
            head_y = 0

        new_head = (head_x, head_y)

        # ---------------------------------
        # SELF COLLISION
        # ---------------------------------

        if new_head in self.snake:
            self.game_over()
            return

        # Add new head
        self.snake.insert(0, new_head)

        # ---------------------------------
        # FOOD COLLISION
        # ---------------------------------

        if new_head == self.food:
            self.score += 1
            self.play_eat_sound()
            self.food = self.create_food()
        else:
            self.snake.pop()

        # Redraw game
        self.draw_game()

        # Repeat game loop
        self.root.after(SPEED, self.update_game)

    # ---------------------------------
    # DRAW GAME
    # ---------------------------------

    def draw_game(self):
        """
        Draws snake, food and score
        """

        self.canvas.delete("all")

        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y,
                x + CELL_SIZE,
                y + CELL_SIZE,
                fill="green"
            )

        # Draw food
        fx, fy = self.food
        self.canvas.create_rectangle(
            fx, fy,
            fx + CELL_SIZE,
            fy + CELL_SIZE,
            fill="red"
        )

        # Draw score
        self.canvas.create_text(
            60, 10,
            fill="white",
            text=f"Score: {self.score}"
        )

    # ---------------------------------
    # GAME OVER
    # ---------------------------------

    def game_over(self):
        """
        Stops game and shows Game Over
        """

        self.game_running = False
        self.play_game_over_sound()

        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            fill="white",
            font=("Arial", 20),
            text=f"GAME OVER\nScore: {self.score}"
        )

# ---------------------------------
# START PROGRAM
# ---------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
