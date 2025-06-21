import arcade

screenWidth = 600
screenHeight = 400
screenTitle = "Flappy Bird"

birdSize = 30
gravity = 0.5
jumpStrength = 10

class FlappyGame(arcade.Window):
    def __init__(self):
        super().__init__(screenWidth, screenHeight, screenTitle)
        self.birdY = screenHeight // 2
        self.birdVelocity = 0
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_update_rate(1/60)

    def setup(self):
        self.birdY = screenHeight // 2
        self.birdVelocity = 0

    def on_draw(self):
        self.clear()
        arcade.draw_triangle_filled(
            100, self.birdY + birdSize / 2,
            100 - birdSize / 2, self.birdY - birdSize / 2,
            100 + birdSize / 2, self.birdY - birdSize / 2,
            arcade.color.YELLOW
        )

    def update(self, deltaTime):
        print(f"Bird Y: {self.birdY}, Velocity: {self.birdVelocity}")  # DEBUG
        self.birdVelocity -= gravity
        self.birdY += self.birdVelocity

        if self.birdY < birdSize / 2:
            self.birdY = birdSize / 2
            self.birdVelocity = 0
        elif self.birdY > screenHeight - birdSize / 2:
            self.birdY = screenHeight - birdSize / 2
            self.birdVelocity = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            print("Jump!")  # DEBUG
            self.birdVelocity = jumpStrength

if __name__ == "__main__":
    window = FlappyGame()
    window.setup()
    arcade.schedule(window.update, 1/60)
    arcade.run()
