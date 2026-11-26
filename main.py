import random
import tkinter as tk


WIDTH, HEIGHT = 440, 600
TOP, BOTTOM = 76, 552
TITLE = "青空シューティング"
INK = "#13252b"
PAPER = "#fff1cf"
SKY = "#266a71"
ENEMY = "#ff9b77"
FONT = "Yu Gothic UI"


class Game:
    def __init__(self, root):
        self.root = root
        root.title(TITLE)
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()
        self.keys = set()
        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)
        root.bind("<FocusOut>", lambda event: self.keys.clear())
        self.draw_background()
        self.reset()
        self.tick()

    def key_down(self, event):
        self.keys.add(event.keysym)

    def key_up(self, event):
        self.keys.discard(event.keysym)

    def reset(self):
        self.x, self.y = WIDTH // 2, BOTTOM - 38
        self.bullets, self.enemies = [], []
        self.frame = 0
        self.last_shot = -6
        self.score = 0
        self.running = True

    def tick(self):
        if self.running:
            self.update()
        self.draw()
        self.root.after(33, self.tick)

    def update(self):
        self.frame += 1
        self.x += 7 * (("Right" in self.keys) - ("Left" in self.keys))
        self.y += 7 * (("Down" in self.keys) - ("Up" in self.keys))
        self.x = max(22, min(WIDTH - 22, self.x))
        self.y = max(TOP + 24, min(BOTTOM - 22, self.y))

        if "space" in self.keys and self.frame - self.last_shot >= 6:
            self.bullets.append([self.x, self.y - 17])
            self.last_shot = self.frame
        if self.frame % 23 == 0:
            self.enemies.append([random.randint(24, WIDTH - 24), TOP - 18])

        for bullet in self.bullets:
            bullet[1] -= 11
        for enemy in self.enemies:
            enemy[1] += 4

        # 命中した弾と敵を消す。コピーを使い、ループ中の削除で要素を飛ばさない。
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if abs(bullet[0] - enemy[0]) < 16 and abs(bullet[1] - enemy[1]) < 15:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 100
                    break

        self.bullets = [bullet for bullet in self.bullets if bullet[1] > TOP]
        self.enemies = [enemy for enemy in self.enemies if enemy[1] < BOTTOM + 18]
        for x, y in self.enemies:
            if abs(x - self.x) < 29 and abs(y - self.y) < 25:
                self.running = False
                break

    def text(self, x, y, value, size, color=PAPER, anchor="center", tag="field"):
        self.canvas.create_text(
            x, y, text=value, fill=color, anchor=anchor,
            font=(FONT, size, "bold"), tags=tag,
        )

    def draw_background(self):
        c = self.canvas
        c.configure(bg=SKY)
        for x in range(20, WIDTH, 40):
            c.create_line(x, TOP, x, BOTTOM, fill="#387c80")
        for y in range(TOP, BOTTOM, 40):
            c.create_line(0, y, WIDTH, y, fill="#387c80")
        for x, y in [(18, 122), (328, 118), (64, 216), (366, 296), (18, 429), (290, 482)]:
            c.create_line(x, y, x + 66, y, fill="#79aeaa", width=2)
            c.create_line(x + 21, y + 7, x + 95, y + 7, fill="#538e8e")
        c.create_rectangle(8, TOP + 8, WIDTH - 8, BOTTOM - 8, outline="#79aeaa")

    def plane(self, x, y, enemy=False):
        # 同じ形を上下反転して、敵機の向きを変える。
        direction = -1 if enemy else 1
        shape = [(0, -19), (6, -7), (20, 9), (20, 14),
                 (6, 9), (0, 15), (-6, 9), (-20, 14), (-20, 9), (-6, -7)]
        points = [(x + dx, y + dy * direction) for dx, dy in shape]
        self.canvas.create_polygon(
            points, fill=ENEMY if enemy else PAPER, outline=INK, width=2, tags="field",
        )
        self.canvas.create_rectangle(
            x - 2, y - 3, x + 2, y + 4, fill=INK, outline="", tags="field",
        )

    def draw(self):
        c = self.canvas
        c.delete("field")
        for x, y in self.bullets:
            c.create_line(x, y, x, y + 9, fill="#ffdf82", width=3, tags="field")
        for x, y in self.enemies:
            self.plane(x, y, enemy=True)
        self.plane(self.x, self.y)

        c.create_rectangle(0, 0, WIDTH, TOP, fill=INK, outline="", tags="field")
        c.create_rectangle(0, BOTTOM, WIDTH, HEIGHT, fill=INK, outline="", tags="field")
        self.text(18, 18, TITLE, 11, anchor="w")
        self.text(18, 50, f"得点  {self.score:05d}", 15, anchor="w")
        self.text(WIDTH // 2, 576, "矢印キー  移動    |    スペース  発射", 11)
        if not self.running:
            c.create_rectangle(49, 224, 391, 372, fill=INK, outline=PAPER, width=2, tags="field")
            self.text(WIDTH // 2, 276, "ゲーム終了", 23)
            self.text(WIDTH // 2, 324, f"得点  {self.score:05d}", 16)


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
