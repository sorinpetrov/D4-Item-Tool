import tkinter as tk
from tkinter import Canvas

def create_overlay():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")
    root.geometry("2560x1440")
    root.configure(background='white')

    canvas = Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create a circle for the capturing state
    state_circle = canvas.create_oval(20, 20, 50, 50, fill='red', outline='red')

    return root, canvas, state_circle

def draw_circle(canvas, color, pos, radius=6.25):  # Increased radius by 25%
    x, y = pos
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color, tags='stat_circle')

def update_overlay(canvas, stats_with_priority):
    items = canvas.find_withtag('stat_circle')
    for item in items:
        canvas.delete(item)

    for text, priority, bbox in stats_with_priority:
        x, y, w, h = bbox
        # Position circle to the left of the text, adjusted by -13 px left and -7 px up
        circle_pos = (x - 13, y + h // 2 - 7)
        print(f"Drawing circle for {text} at {circle_pos} with priority {priority}")
        if priority == 1:
            draw_circle(canvas, "green", circle_pos)  # Green for Priority 1
        elif priority == 2:
            draw_circle(canvas, "yellow", circle_pos)  # Yellow for Priority 2
        elif priority == 3:
            draw_circle(canvas, "orange", circle_pos)  # Orange for Priority 3
    canvas.update()

def update_state_circle(canvas, state_circle, capturing):
    color = "green" if capturing else "red"
    canvas.itemconfig(state_circle, fill=color, outline=color)
