import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui
import time
import pyperclip
import keyboard

# All valid canvas sizes in the game
VALID_CANVAS_SIZES = {(11, 11), (19, 19), (23, 19), (23, 23), (24, 24), (36, 24), (45, 27)}
# The width and height of the window
WIND_WIDTH, WIND_HEIGHT = 400, 600
# Time for each countdown, must be an int
COUNTDOWN_TIME = 3
# Rate at which the program does its tasks. Going too fast risks lag between client and server
TRANSRATE = 0.05
# Key to stop the program
STOPKEY = "k"

# Do we have an image?
image_selected = False
# Position of the button to open the color picker
spraycolor_pos = None
# Position of the confirm button in the color picker
confirm_pos  = None
# Position of the hex input area in the color picker
hexput_pos  = None
# Positions of pixels on the canvas
bottomleft_pos = None
topright_pos = None
topleft_pos = None
# Array of each pixel's hex color, used to remake the picture
image_hex_array = [] 
# Array of every unique color hex, used to limit the amount of times we need to swap colors
image_unique_hex = []
# Image Size
image_size = [0, 0]
# The loaded image
loaded_image = None

def time_convert(sec):
    mins = sec // 60
    hours = mins // 60
    return f"Time Lapsed = {round(hours)}h:{round(mins % 60)}m:{round(sec % 60)}s"

# Converts RGB values into hex codes, disregarding alpha
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

# Calculates the contrast color based on the background color
def contrast_color(hex_color):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return "#000000" if (r*0.299 + g*0.587 + b*0.114) > 186 else "#ffffff"

def open_image():
    global image, photo, loaded_image, image_selected, image_size
    dimensions_label.config(text="Valid canvas sizes: 11x11, 19x19, 23x19, 23x23, 24x24, 36x24, 45x27")
    filepath = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg")])
    if filepath:
        image = Image.open(filepath)
        # Only allow valid SS13 canvas sizes
        if image.size not in VALID_CANVAS_SIZES:
            dimensions_label.config(text="This is not a valid image size!")
            return
        loaded_image = image.convert("RGB").load()
        image_selected = True
        image_size = image.size
        # Resize so it's easier to see
        resize_image = image.resize((image_size[0]*10, image_size[1]*10))
        photo = ImageTk.PhotoImage(resize_image)
        dimensions_label.config(text=f"Canvas Size: {image_size[0]}x{image_size[1]}")
        draw_grid()
        hexbox.delete(0, tk.END)
        get_unique_hexes()

def quit_program():
    root.destroy()

def draw_grid():
    pixel_canvas.config(width=image_size[0]*10, height=image_size[1]*10)
    pixel_canvas.create_image(0, 0, image=photo, anchor=tk.NW, tags="IMG")
    root.geometry(f"{WIND_WIDTH}x{WIND_HEIGHT+image_size[1]*10}")
    
def get_unique_hexes():
    global image_hex_array, image_unique_hex
    # Create an array of all of our hex values & a list of all unique hex values
    for x in range(image_size[0]):
        x_px = []
        for y in range(image_size[1]):
            pixel = loaded_image[x, y]
            x_px.append(rgb_to_hex(pixel))
            if rgb_to_hex(pixel) not in image_unique_hex:
                image_unique_hex.append(rgb_to_hex(pixel))
                hexbox.insert(tk.END, rgb_to_hex(pixel))
        image_hex_array.append(x_px)
    
    # Set background and foreground colors for listbox items
    for i in range(hexbox.size()):
        hex_color = hexbox.get(i)
        hexbox.itemconfig(i, bg=hex_color, fg=contrast_color(hex_color))
    listdesc.config(text=f"{hexbox.size()} Colors")

def get_spraycolor(countdown=COUNTDOWN_TIME):
    global spraycolor_pos
    if countdown == 0:
        spraycolor_pos = pyautogui.position()
        spraycolor_desc.config(text=f"Color-Picker Pos: ({spraycolor_pos.x},{spraycolor_pos.y})", fg="green")
        return
    spraycolor_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_spraycolor(countdown - 1))


def get_hexput(countdown=COUNTDOWN_TIME):
    global hexput_pos
    if countdown == 0:
        hexput_pos = pyautogui.position()
        hexput_desc.config(text=f"Hex Input Pos: ({hexput_pos.x},{hexput_pos.y})", fg="green")
        return
    hexput_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_hexput(countdown - 1))

def get_confirm(countdown=COUNTDOWN_TIME):
    global confirm_pos
    if countdown == 0:
        confirm_pos = pyautogui.position()
        confirm_desc.config(text=f"Confirm Button Pos: ({confirm_pos.x},{confirm_pos.y})", fg="green")
        return
    confirm_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_confirm(countdown - 1))
    
def get_topleft(countdown=COUNTDOWN_TIME):
    global topleft_pos
    if countdown == 0:
        topleft_pos = pyautogui.position()
        topleft_desc.config(text=f"Top Left Canvas Pos: ({topleft_pos.x},{topleft_pos.y})", fg="green")
        return
    topleft_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_topleft(countdown - 1))

def get_topright(countdown=COUNTDOWN_TIME):
    global topright_pos
    if countdown == 0:
        topright_pos = pyautogui.position()
        topright_desc.config(text=f"Top Right Canvas Pos: ({topright_pos.x},{topright_pos.y})", fg="green")
        return
    topright_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_topright(countdown - 1))

def get_bottomleft(countdown=COUNTDOWN_TIME):
    global bottomleft_pos
    if countdown == 0:
        bottomleft_pos = pyautogui.position()
        bottomleft_desc.config(text=f"Bottom Left Canvas Pos: ({bottomleft_pos.x},{bottomleft_pos.y})", fg="green")
        return
    bottomleft_desc.config(text=f"Put Cursor on location in: {countdown}", fg="black")
    root.after(1000, lambda: get_bottomleft(countdown - 1))

def start_mapping():
    global bottomleft_pos, topright_pos, topleft_pos, confirm_pos, hexput_pos, spraycolor_pos, image_selected, image_size
    if not (bottomleft_pos or topright_pos or topleft_pos or confirm_pos or hexput_pos or spraycolor_pos or image_selected):
        startbutton.config(text="Insufficient Data!")
        time.sleep(COUNTDOWN_TIME)
        startbutton.config(text="START")
        return
    title_label.config(text=f"Press {STOPKEY} to halt the program!", fg="red")
    finhexbox.delete(0, tk.END)
    root.update_idletasks()  # Update the GUI
    time.sleep(COUNTDOWN_TIME)
    incrementX = (topright_pos[0] - topleft_pos[0]) / (image_size[0] - 1)
    incrementY = (bottomleft_pos[1] - topleft_pos[1]) / (image_size[1] - 1)
    start_time = time.time()
    for color in image_unique_hex:
        if color == "#ffffff":
            continue
        pyperclip.copy(str(color))
        time.sleep(TRANSRATE)
        pyautogui.click(spraycolor_pos)
        time.sleep(TRANSRATE)
        pyautogui.doubleClick(hexput_pos)
        time.sleep(TRANSRATE)
        pyautogui.hotkey("ctrlleft", "v")
        time.sleep(TRANSRATE)
        pyautogui.click(confirm_pos)
        time.sleep(TRANSRATE + 0.5)
        for sysX in range(image_size[0]):
            for sysY in range(image_size[1]):
                if keyboard.is_pressed(STOPKEY):
                    title_label.config(text=f"SS13 ArtMapper v2.0", fg="black")
                    return
                if image_hex_array[sysX][sysY] == color:
                    pyautogui.click((incrementX * sysX) + topleft_pos[0], (incrementY * sysY) + topleft_pos[1])
                    time.sleep(TRANSRATE)
                    pyautogui.click
                    time.sleep(TRANSRATE * 2)
        update_finhexbox_color(color)

    end_time = time.time()
    title_label.config(text=f"SS13 ArtMapper v2.0\n{time_convert(end_time - start_time)}", fg="black")


def update_finhexbox_color(color):
    finhexbox.insert(tk.END, color)
    lastindex = finhexbox.size() - 1
    finhexbox.itemconfig(lastindex, bg=color, fg=contrast_color(color))
    finhexbox.update()
    finhexbox.update_idletasks()

# Create the main application window
root = tk.Tk()
root.title("SS13 ArtMapper v2.0")
root.geometry("400x600")
root.configure(bg="#1e1e1e")

#! Create a main Frame
frame_1 = tk.Frame(root, bd=4, relief="raised", bg="#1e1e1e")
frame_1.pack(fill=tk.BOTH, expand=1)

# Title Label
title_label = tk.Label(frame_1, text="SS13 ArtMapper v2.0", font=("Franklin Gothic Medium", 15), fg="#ffffff", bg="#1e1e1e")
title_label.pack(side=tk.TOP)

# Create a canvas to draw the pixel grid
pixel_canvas = tk.Canvas(frame_1, bd=0, highlightthickness=0, width=0, height=0, bg="#1e1e1e")
pixel_canvas.pack(side=tk.TOP)

# Create a label to display the dimensions of the uploaded image
dimensions_label = tk.Label(frame_1, text="Valid canvas sizes: 11x11, 19x19, 23x19, 23x23, 24x24, 36x24, 45x27", fg="#ffffff", bg="#1e1e1e")
dimensions_label.pack()

# Create a button to open the file dialog
upload_button = tk.Button(frame_1, text="Upload Image", command=open_image, bg="#444444", fg="#ffffff")
upload_button.pack(side=tk.BOTTOM)

#! Makes a frame for the lower section
frame_2 = tk.Frame(root, bd=4, relief=tk.SUNKEN, bg="#1e1e1e")
frame_2.pack(fill=tk.BOTH, expand=1)

#* Frame for our list
frame_list = tk.Frame(frame_2, bd=4, relief=tk.RAISED, bg="#1e1e1e")
frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# List description
listdesc = tk.Label(frame_list, text="No Colors Yet!", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")
listdesc.pack(side=tk.TOP)

# Create a Listbox to display to the right
hexbox = tk.Listbox(frame_list, bg="#444444", fg="#ffffff")
hexbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Listbox of colors we've finished transferring onto the canvas
findesc = tk.Label(frame_list, text="Finished Colors:", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")
findesc.pack(side=tk.TOP)

# Finished hexes
finhexbox = tk.Listbox(frame_list, bg="#444444", fg="#ffffff")
finhexbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#! Makes a frame for the lower section's buttons
frame_3 = tk.Frame(frame_2, bd=4, relief="raised", bg="#1e1e1e")
frame_3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Instructions
instructions = tk.Label(frame_3, text="Put your mouse over the specified locations,\n once done press Start!", fg="#ffffff", bg="#1e1e1e")
instructions.pack()

# Input for spraycolor
spraycolor_desc = tk.Label(frame_3, text="Color-Picker Button Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
spraycolor_desc.pack()

get_spraycolor_button = tk.Button(frame_3, text="Set Location", command=get_spraycolor, bg="#444444", fg="#ffffff")
get_spraycolor_button.pack()

# Input for hexput
hexput_desc = tk.Label(frame_3, text="Hex Input Field Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
hexput_desc.pack()

get_hexput_button = tk.Button(frame_3, text="Set Location", command=get_hexput, bg="#444444", fg="#ffffff")
get_hexput_button.pack()

# Input for confirm
confirm_desc = tk.Label(frame_3, text="Confirm Button Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
confirm_desc.pack()

get_confirm_button = tk.Button(frame_3, text="Set Location", command=get_confirm, bg="#444444", fg="#ffffff")
get_confirm_button.pack()

# Canvas Label
canvas_desc = tk.Label(frame_3, text="Canvas Positions", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")
canvas_desc.pack()

#! I'm so rich I got a frame for my frames
frame_4 = tk.Frame(frame_3, bd=4, relief="raised", bg="#1e1e1e")
frame_4.pack(fill=tk.BOTH, expand=1)

# Inputs for Canvas
topleft_desc = tk.Label(frame_4, text="Top Left Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
topleft_desc.pack()

topleft = tk.Button(frame_4, text="Set Location", command=get_topleft, bg="#444444", fg="#ffffff")
topleft.pack()

topright_desc = tk.Label(frame_4, text="Top Right Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
topright_desc.pack()

topright = tk.Button(frame_4, text="Set Location", command=get_topright, bg="#444444", fg="#ffffff")
topright.pack()

bottomleft_desc = tk.Label(frame_4, text="Bottom Left Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
bottomleft_desc.pack()

bottomleft = tk.Button(frame_4, text="Set Location", command=get_bottomleft, bg="#444444", fg="#ffffff")
bottomleft.pack()

# Start Button
startbutton = tk.Button(frame_3, text="START", command=start_mapping, bg="#444444", fg="#ffffff")
startbutton.pack()

# Create a button to quit the program
quit_button = tk.Button(frame_3, text="Quit", command=quit_program, bg="#444444", fg="#ffffff")
quit_button.pack(side=tk.BOTTOM, anchor=tk.SE)

# Run the Tkinter event loop
root.mainloop()
