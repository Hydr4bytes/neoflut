class Ball:
    def __init__(self) -> None:
        self.x = 10
        self.y = 10

        self.dx = 1
        self.dy = 1

    def update(self, screensize):
        self.x += self.dx
        self.y += self.dy

        if(self.x > screensize[0] or self.x < 0):
            self.dx *= -1

        if(self.y > screensize[1] or self.y < 0):
            self.dx *= -1
