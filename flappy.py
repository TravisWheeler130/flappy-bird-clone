import arcade

screenWidth = 600
screenHeight = 400
screenTitle = "Flappy Bird"

birdSize = 30
gravity = 0.5
jumpStrength = 8

class FlappyGame(arcade.Window):
    pipeList = []
    pipeSpeed = 2
    pipeGap = 150
    pipeWidth = 50
    pipeSpace = 250
    numPipes = 3
    score = 0
    bestScore = 0
    isStarted = False

    def __init__(self):
        super().__init__(screenWidth, screenHeight, screenTitle)
        self.birdY = screenHeight // 2
        self.birdVelocity = 0
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_update_rate(1/60)
        self.score = 0
        self.isStarted = False

        # Sprite
        self.bird = arcade.Sprite("assets/bird.png", scale=0.125)
        self.bird.center_x = 100
        self.bird.center_y = self.birdY

        self.pipe = arcade.Sprite("assets/pipe.png", scale=.5)

        self.spriteList = arcade.SpriteList()
        self.spriteList.append(self.bird)
        #self.bird = None

        self.background = arcade.load_texture("assets/background.png")
        self.backgroundX = 0
        self.backgroundSpeed = self.pipeSpeed * 0.3

    def setup(self):
        self.bird.center_x = 100
        self.bird.center_y = self.birdY
        self.birdY = screenHeight // 2
        self.birdVelocity = 0
        self.generatePipes()
        self.isStarted = False

    def on_draw(self):
        self.clear()
        #arcade.draw(self.backgroundX + screenWidth / 2, screenHeight / 2, screenWidth, screenHeight, self.background)
        #arcade.draw_sprite_rect(self.backgroundX + screenWidth + screenWidth / 2, screenHeight / 2, screenWidth, screenHeight, self.background)
        self.spriteList.draw()
        # self.spriteList.draw_hit_boxes()
        for pipe in self.pipeList:
            x = pipe["x"]
            gapY = pipe["gapY"]
            gapHalf = self.pipeGap / 2
            left = x - self.pipeWidth / 2
            right = x + self.pipeWidth / 2

            # top pipe
            arcade.draw_lrbt_rectangle_filled(left, right, gapY + gapHalf, screenHeight, arcade.color.BLACK)
            # bottom pipe
            arcade.draw_lrbt_rectangle_filled(left, right, 0, gapY - gapHalf, arcade.color.BLACK)
            arcade.draw_text(f"Score: {self.score}    Best: {self.bestScore}", 10, screenHeight - 30, arcade.color.RED, 20)
            if not self.isStarted:
                arcade.draw_text("Press SPACE to start", screenWidth / 2, screenHeight / 2, arcade.color.DARK_GREEN, font_size = 20, anchor_x="center")

    def update(self, deltaTime):
        if not self.isStarted:
            return
        print(f"Bird Y: {self.birdY}, Velocity: {self.birdVelocity}")  # DEBUG
        self.birdVelocity -= gravity
        self.birdY += self.birdVelocity
        self.bird.center_y = self.birdY

        if self.birdY < birdSize / 2:
            self.birdY = birdSize / 2
            self.birdVelocity = 0
        elif self.birdY > screenHeight - birdSize / 2:
            self.birdY = screenHeight - birdSize / 2
            self.birdVelocity = 0
        
        for pipe in self.pipeList:
            pipe["x"] -= self.pipeSpeed

            # Scoring
            if not pipe["scored"] and pipe["x"] + self.pipeWidth < 100:
                self.score += 1
                pipe["scored"] = True
                if self.score > self.bestScore:
                    self.bestScore = self.score

            # Pipe reset
            if pipe["x"] < -self.pipeWidth:
                # Find the rightmost pipe
                furthestX = max(p["x"] for p in self.pipeList)
                pipe["x"] = furthestX + self.pipeSpace
                import random
                pipe["gapY"] = random.randint(100, screenHeight - 100)
                pipe["scored"] = False

            # background scroll
            self.backgroundX -= self.backgroundSpeed
            if self.backgroundX <= -screenWidth:
                self.backgroundX = 0

            # Pipe collision
            pipeLeft = pipe["x"]
            pipeRight = pipe["x"] + self.pipeWidth
            gapY = pipe["gapY"]
            gapHalf = self.pipeGap / 2
            pipeBottom = gapY + gapHalf
            pipeTop = gapY - gapHalf
            
            # Bird collision
            birdLeft = 100 - birdSize / 2
            birdRight = 100 + birdSize / 2
            birdBottom = self.birdY - birdSize / 2
            birdTop = self.birdY + birdSize / 2
            floorY = birdSize / 2
            ceilingY = screenHeight - birdSize / 2

            if birdTop > ceilingY or birdBottom < floorY:
                print("Game Over!")
                self.setup()
                self.score = 0
                break

            if pipeLeft < birdRight and pipeRight > birdLeft:
                if birdTop > pipeBottom or birdBottom < pipeTop:
                    print("Game Over!")
                    self.setup()
                    self.score = 0
                    break


    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if not self.isStarted:
                self.isStarted = True
            print("Jump!")  # DEBUG
            self.birdVelocity = jumpStrength

    def generatePipes(self):
        import random
        self.pipeList.clear()
        for i in range(self.numPipes):
            x = screenWidth + i * self.pipeSpace
            gapY = random.randint(100, screenHeight - 100)
            self.pipeList.append({"x": x, "gapY": gapY, "scored": False})

if __name__ == "__main__":
    window = FlappyGame()
    window.setup()
    arcade.schedule(window.update, 1/60)
    arcade.run()
