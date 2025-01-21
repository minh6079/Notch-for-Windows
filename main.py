import tkinter as tk
from datetime import datetime
import os
import sys

root = tk.Tk()

# Initial states
is_expanded = False
animation_speed = 20  # Speed of the animation (lower is faster)

def smooth_resize(start_width, start_height, end_width, end_height, step=5):
    """Smoothly resize the window between start and end dimensions."""
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    # Calculate the step size for each frame
    step_width = (end_width - current_width) / step
    step_height = (end_height - current_height) / step

    def animate(step_count=0):
        if step_count < step:
            new_width = int(current_width + step_width * (step_count + 1))
            new_height = int(current_height + step_height * (step_count + 1))
            ws = root.winfo_screenwidth()
            leftx = (ws / 2) - (new_width / 2)
            root.geometry(f'{new_width}x{new_height}+{int(leftx)}+0')
            root.after(animation_speed, lambda: animate(step_count + 1))
        else:
            # Finalize to ensure exact size
            ws = root.winfo_screenwidth()
            leftx = (ws / 2) - (end_width / 2)
            root.geometry(f'{end_width}x{end_height}+{int(leftx)}+0')

    animate()

def toggle_dynamic_island():
    """Toggle between the small and expanded views of the Dynamic Island."""
    global is_expanded
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    if is_expanded:
        # Collapse
        notch_width = int(ws / 9)
        notch_height = int(hs / 30)
        smooth_resize(root.winfo_width(), root.winfo_height(), notch_width, notch_height)
        time_label.pack_forget()  # Hide time and date
        canvas.itemconfigure(camera_image_id, state="normal")  # Show the camera in the collapsed state
        canvas.coords(camera_image_id, notch_width // 2, notch_height // 2)
    else:
        # Expand
        expanded_width = int(ws / 3)
        expanded_height = int(hs / 8)
        smooth_resize(root.winfo_width(), root.wfo_height(), expanded_width, expanded_height)
        canvas.itemconfigure(camera_image_id, state="normal")  # Keep the camera at the top
        canvas.coords(camera_image_id, expanded_width // 2, 40)  # Adjust camera position
        time_label.pack(side="bottom", pady=(10, 10))  # Show time and date below the camera
        time_label.config(text=datetime.now().strftime("%Y-%m-%d\n%H:%M:%S"))
    is_expanded = not is_expanded

def update_time():
    """Update the time dynamically in the expanded state."""
    if is_expanded:
        time_label.config(text=datetime.now().strftime("%Y-%m-%d\n%H:%M:%S"))
    root.after(1000, update_time)

# Determine if the application is bundled as a .exe
if getattr(sys, 'frozen', False):
    # If frozen (running as .exe), get the path to the bundled directory
    application_path = sys._MEIPASS
else:
    # Otherwise, get the current working directory
    application_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to cam.png
cam_path = os.path.join(application_path, "cam.png")

# Configure root window
def screen_stuff():
    ws = root.winfo_screenwidth()
    notch_width = int(ws / 9)
    notch_height = int(ws / 30)
    leftx = (ws / 2) - (notch_width / 2)
    root.geometry(f'{notch_width}x{notch_height}+{int(leftx)}+0')

screen_stuff()
root.configure(background='black')
root.protocol('WM_DELETE_WINDOW', lambda: None)
root.overrideredirect(True)
root.attributes('-topmost', True)

# Add an escape key binding to close the application
root.bind('<Escape>', lambda e: root.destroy())

# Hide the cursor when the mouse enters the notch
def hide_cursor(event):
    root.config(cursor="none")

# Show the cursor when the mouse leaves the notch
def show_cursor(event):
    root.config(cursor="arrow")

root.bind("<Enter>", hide_cursor)  # Bind cursor hide on enter
root.bind("<Leave>", show_cursor)  # Bind cursor show on leave

# Create a canvas for rounded corners and camera positioning
canvas = tk.Canvas(root, width=0, height=0, bd=0, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# Load the camera image
camera_img = tk.PhotoImage(file=cam_path)  # Using the full path to cam.png
camera_image_id = canvas.create_image(0, 0, image=camera_img, anchor="center")

# Dynamic Island content
time_label = tk.Label(root, bg="black", fg="white", font=("Helvetica", 12), justify="center")

# Bind left-click to toggle the Dynamic Island
root.bind('<Button-1>', lambda e: toggle_dynamic_island())

# Start updating the time
update_time()

root.mainloop()
