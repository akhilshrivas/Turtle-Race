# turtle_race.py
# A simple Turtle Racing game with countdown, lanes, finish line, and restart.
# Run: python turtle_race.py

import random
import turtle as T

# ---------- Config ----------
WIDTH, HEIGHT = 900, 540
LANES = 6
COLORS = ["red", "blue", "green", "orange", "purple", "deeppink"]
NAMES = ["Ruby", "Bolt", "Mint", "Tiger", "Violet", "Candy"]  # labels on shells
MARGIN_X = 80
MARGIN_Y = 60
STEP_MIN, STEP_MAX = 2, 6  # speed range each tick
TICK_MS = 35                # timer tick
FONT = ("Arial", 16, "normal")
BIGFONT = ("Arial", 42, "bold")

# ---------- Game State ----------
state = {
    "screen": None,
    "pen": None,
    "turtles": [],
    "start_x": None,
    "finish_x": None,
    "running": False,
    "winner": None,
    "banner": None,
    "count": 3,
    "bet_color": None,
}

# ---------- Helpers ----------
def center_write(pen, text, font=BIGFONT, y_offset=0):
    pen.clear()
    pen.hideturtle()
    pen.up()
    pen.goto(0, y_offset)
    pen.color("black")
    pen.write(text, align="center", font=font)

def draw_track():
    pen = state["pen"]
    pen.clear()
    pen.hideturtle()
    pen.speed(0)
    pen.up()

    sw = WIDTH // 2
    sh = HEIGHT // 2
    start_x = -sw + MARGIN_X
    finish_x = sw - MARGIN_X
    state["start_x"] = start_x
    state["finish_x"] = finish_x

    # Outer border
    pen.goto(-sw + 20, -sh + 20)
    pen.down()
    pen.pensize(3)
    for _ in range(2):
        pen.forward(WIDTH - 40)
        pen.left(90)
        pen.forward(HEIGHT - 40)
        pen.left(90)
    pen.up()

    # Lanes
    lane_height = (HEIGHT - 2 * MARGIN_Y) / LANES
    top = sh - MARGIN_Y
    pen.pensize(2)
    for i in range(LANES + 1):
        y = top - i * lane_height
        pen.goto(start_x - 30, y)
        pen.setheading(0)
        pen.down()
        pen.forward((finish_x - start_x) + 60)
        pen.up()

    # Start and finish posts
    def vertical_line(x, label):
        pen.goto(x, top + 10)
        pen.setheading(-90)
        pen.down()
        pen.forward((LANES * lane_height) + 20)
        pen.up()
        pen.goto(x, top + 20)
        pen.write(label, align="center", font=FONT)

    pen.pencolor("gray25")
    vertical_line(start_x, "START")
    pen.pencolor("black")
    vertical_line(finish_x, "FINISH")

    # Checkered finish pattern
    cell = 12
    cols = 2
    rows = int((LANES * lane_height) // cell) + 2
    for r in range(rows):
        for c in range(cols):
            x = finish_x + (c * cell) - 12
            y = top - r * cell
            pen.goto(x, y)
            pen.setheading(0)
            pen.fillcolor("black" if (r + c) % 2 == 0 else "white")
            pen.begin_fill()
            for _ in range(4):
                pen.down()
                pen.forward(cell)
                pen.right(90)
            pen.end_fill()
            pen.up()

def spawn_turtles():
    # Clear previous turtles
    for t in state["turtles"]:
        try:
            t.hideturtle()
        except:
            pass
    state["turtles"].clear()

    lane_height = (HEIGHT - 2 * MARGIN_Y) / LANES
    top = HEIGHT // 2 - MARGIN_Y
    start_x = state["start_x"]

    for i in range(LANES):
        racer = T.Turtle(visible=False)
        racer.shape("turtle")
        racer.shapesize(1.6, 1.6)
        racer.color(COLORS[i % len(COLORS)])
        racer.penup()
        y = top - (i + 0.5) * lane_height
        racer.goto(start_x, y)
        racer.setheading(0)
        racer.pendown()
        racer.pensize(3)
        racer.speed(0)
        racer.showturtle()

        # Name label on shell
        label = T.Turtle(visible=False)
        label.hideturtle()
        label.penup()
        label.goto(start_x - 55, y - 10)
        label.write(NAMES[i], align="left", font=("Arial", 12, "bold"))

        state["turtles"].append(racer)

def ask_bet():
    # Optional bet prompt. Returns normalized color string or None.
    colors_str = ", ".join(COLORS)
    try:
        ans = T.textinput("Place your bet",
                          f"Pick a turtle color to cheer ({colors_str}):")
    except Exception:
        ans = None
    if not ans:
        return None
    ans = ans.strip().lower()
    return ans if ans in [c.lower() for c in COLORS] else None

def start_countdown():
    state["running"] = False
    state["winner"] = None
    state["count"] = 3
    if state["banner"] is None:
        state["banner"] = T.Turtle(visible=False)
    center_write(state["banner"], "3")
    state["screen"].ontimer(lambda: countdown_step(2), 700)

def countdown_step(n):
    if n > 0:
        center_write(state["banner"], str(n))
        state["screen"].ontimer(lambda: countdown_step(n - 1), 700)
    else:
        center_write(state["banner"], "Go!", y_offset=0)
        state["screen"].ontimer(lambda: (state["banner"].clear(), begin_race()), 300)

def begin_race():
    state["running"] = True
    for t in state["turtles"]:
        t.clear()  # clear any previous trails
        t.penup()
        t.setx(state["start_x"])
        t.pendown()
    race_tick()

def race_tick():
    if not state["running"]:
        return

    finish_x = state["finish_x"]
    winner = None

    for t in state["turtles"]:
        step = random.randint(STEP_MIN, STEP_MAX)
        t.forward(step)
        if t.xcor() >= finish_x:
            winner = t
            break

    if winner:
        state["running"] = False
        state["winner"] = winner
        show_winner(winner)
    else:
        state["screen"].ontimer(race_tick, TICK_MS)

def show_winner(winner):
    color = winner.pencolor().lower()
    bet = state["bet_color"]
    msg = f"{color.capitalize()} wins!"
    if bet:
        msg += " You guessed right!" if bet == color else f" Your pick was {bet}."
    center_write(state["banner"], msg, font=BIGFONT, y_offset=0)

    # Small hint
    hint = T.Turtle(visible=False)
    hint.penup()
    hint.goto(0, -HEIGHT // 2 + 40)
    hint.write("Press R to race again, Q to quit.", align="center", font=FONT)

    # Remove hint after a moment to keep screen clean
    state["screen"].ontimer(hint.clear, 3500)

# ---------- Controls ----------
def handle_start():
    if state["running"]:
        return
    start_countdown()

def handle_restart():
    state["banner"].clear() if state["banner"] else None
    draw_track()
    spawn_turtles()
    state["bet_color"] = ask_bet()
    handle_start()

def handle_quit():
    try:
        T.bye()
    except:
        pass

# ---------- Main ----------
def main():
    screen = T.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing")
    screen.tracer(False)  # draw track instantly

    state["screen"] = screen
    state["pen"] = T.Turtle(visible=False)

    draw_track()
    spawn_turtles()
    screen.tracer(True)

    # Banner and help text
    if state["banner"] is None:
        state["banner"] = T.Turtle(visible=False)
    center_write(state["banner"], "Turtle Racing", y_offset=20)
    helper = T.Turtle(visible=False)
    helper.penup()
    helper.goto(0, -HEIGHT // 2 + 60)
    helper.write("Press SPACE to start • R to restart • Q to quit",
                 align="center", font=FONT)

    # Optional bet
    state["bet_color"] = ask_bet()

    # Key bindings
    screen.listen()
    screen.onkey(handle_start, "space")
    screen.onkey(handle_restart, "r")
    screen.onkey(handle_quit, "q")

    T.mainloop()

if __name__ == "__main__":
    main()
