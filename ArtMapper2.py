import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui
import time
import pyperclip
import keyboard
import webbrowser

# Version
VERSION = "v2.4"

# All valid canvas sizes in the game
VALID_CANVAS_SIZES = {(11, 11), (19, 19), (23, 19), (23, 23), (24, 24), (36, 24), (45, 27)}
# The width and height of the window
WIND_WIDTH, WIND_HEIGHT = 400, 400
# Rate at which the program does its tasks in ms. Going too fast risks desync from the server you're on.
TRANSRATE = 50
# Key to stop the program
STOPKEY = "k"

# Do we have an image?
image_selected = False
# Position of the button to open the color picker
spraycolor_pos = None
# Position of the hex input area in the color picker
hexput_pos  = None
# Position of the canvas on the screen
topleft_pos = None
bottomright_pos = None
# Array of each pixel's hex color, used to remake the picture
image_hex_array = [] 
# Array of every unique color hex, used to limit the amount of times we need to swap colors
image_unique_hex = []
# Image Size
image_size = [0, 0]
# The loaded image
loaded_image = None
# Halting the program
stop_flag = False
# Are we running right now
processing_pic = False

# Converts seconds to ms just for easier reading
SECONDS = lambda x : int(x*1000)

# Used to tell you how long it took to transfer your piece
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
    return "#000000" if (r*0.299 + g*0.587 + b*0.114) > 155 else "#ffffff"

# Open our lovely art
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
    root.geometry(f"{pixel_canvas.winfo_reqwidth()+10 if image_size[0] > 24 else WIND_WIDTH}x{WIND_HEIGHT+image_size[1]*10}")

# Makes a list of all the unique color hexes
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

# Instead of messing around with annoying input buttons we're using a full window now.
def create_draggable_window(update_pos_callback):
    overlay = tk.Toplevel(root)
    overlay.geometry(f"200x200+{root.winfo_rootx()}+{root.winfo_rooty()}")
    overlay.title("Drag to position")
    overlay.resizable(False, False)
    overlay.attributes("-topmost", True)
    overlay.config(bg="white")
    overlay.attributes("-transparentcolor", "white")

    # Draw a "+" sign in the center of the window
    canvas = tk.Canvas(overlay, width=200, height=200, bg="white", bd=0, highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(25,25,175,175,outline="red")
    canvas.create_line(100, 50, 100, 150, fill="red", width=2)
    canvas.create_line(50, 100, 150, 100, fill="red", width=2)
    
    coords_label = tk.Label(overlay, text="", bg="black", fg="#fffff1", font=("Helvetica", 12, "bold"))
    coords_label.place(relx=0.5, rely=0.1, anchor="center")
    
    def grab_pos():
        overlay_x = overlay.winfo_rootx()
        overlay_y = overlay.winfo_rooty()

        canvas_center_x = overlay_x + 100
        canvas_center_y = overlay_y + 100
        
        return canvas_center_x, canvas_center_y
    
    # Update the label with the current coordinates
    def update_coords_label():
        newposx, newposy = grab_pos()
        coords_label.config(text=f"({newposx}, {newposy})")
        overlay.after(100, update_coords_label)

    update_coords_label()

    # Capture the position and close the overlay window
    def on_close():
        newposx, newposy = grab_pos()
        update_pos_callback(newposx, newposy)

        overlay.destroy()

    
    capture_button = tk.Button(overlay, text="Capture Position", command=on_close)
    capture_button.place(relx=0.5, rely=0.9, anchor="center")
    overlay.mainloop()

def spraycolor_callback(x,y):
    global spraycolor_pos
    spraycolor_pos = (x,y)
    spraycolor_desc.config(text=f"Color Menu Pos: ({x},{y})", fg="green")
    
def get_spraycolor():
    create_draggable_window(spraycolor_callback)

def hexput_callback(x,y):
    global hexput_pos
    hexput_pos = (x,y)
    hexput_desc.config(text=f"Hex Input Pos: ({x},{y})", fg="green")

def get_hexput():
    create_draggable_window(hexput_callback)

# A window to grab the position of the canvas.
def create_resizable_window(update_pos_callback):
    overlay = tk.Toplevel(root)
    overlay.geometry(f"500x500+{root.winfo_rootx()}+{root.winfo_rooty()}")
    overlay.title("Resize to Canvas")
    
    overlay.attributes("-transparentcolor", "white")
    overlay.config(bg="white")
    
    canvas = tk.Canvas(overlay, bg="white", bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    rect_ids = []
    
    # Shared state for grid cell dimensions
    grid_state = {"width": 0, "height": 0}

    def update_rectangle(event=None):
        # Clear everything so resizing doesn't make those damn ghosts
        canvas.delete("all") 
        rect_ids.clear()
        
        canvas_width = overlay.winfo_width()
        canvas_height = overlay.winfo_height()
    
        # Make 4 rectangles to make a center, transparent one.
        margin = 5
        top_rect = canvas.create_rectangle(0, 0, canvas_width, margin, outline="", fill="red")
        rect_ids.append(top_rect)
        
        bottom_rect = canvas.create_rectangle(0, canvas_height - margin, canvas_width, canvas_height, outline="", fill="red")
        rect_ids.append(bottom_rect)

        left_rect = canvas.create_rectangle(0, margin, margin, canvas_height - margin, outline="", fill="red")
        rect_ids.append(left_rect)

        right_rect = canvas.create_rectangle(canvas_width - margin, margin, canvas_width, canvas_height - margin, outline="", fill="red")
        rect_ids.append(right_rect)

        if not image_selected:
            return
        # Make the pixel grid
        grid_width = image_size[0]
        grid_height = image_size[1]
        grid_state["width"] = (canvas_width - 2 * margin) / grid_width
        grid_state["height"] = (canvas_height - 2 * margin) / grid_height
        for i in range(grid_width):
            for j in range(grid_height):
                x1 = margin + i * grid_state["width"]
                y1 = margin + j * grid_state["height"]
                x2 = x1 + grid_state["width"]
                y2 = y1 + grid_state["height"]
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)
        

    overlay.bind("<Configure>", update_rectangle)
    
    def capture_corners():
        overlay_x = overlay.winfo_rootx()
        overlay_y = overlay.winfo_rooty()

        # Get the bounding box coordinates for the left and bottom rectangles
        left_rect_coords = canvas.bbox(rect_ids[2])  # Left rectangle
        bottom_rect_coords = canvas.bbox(rect_ids[1])  # Bottom rectangle

        # Calculate the center of the top-left grid cell
        top_left_x = overlay_x + left_rect_coords[2]  # Right edge of left rectangle
        top_left_y = overlay_y + left_rect_coords[1] + grid_state["height"] / 2

        # Calculate the center of the bottom-right grid cell
        bottom_right_x = overlay_x + bottom_rect_coords[2] - grid_state["width"] / 2
        bottom_right_y = overlay_y + bottom_rect_coords[3] - grid_state["height"] / 2

        # Round and update the positions
        update_pos_callback(
            (round(top_left_x), round(top_left_y)),
            (round(bottom_right_x), round(bottom_right_y))
        )
        overlay.destroy()
    
    capture_button = tk.Button(overlay, text="Capture Position", command=capture_corners)
    capture_button.place(relx=0.5, rely=0.9, anchor="center")  # Center the button at the bottom
    
    overlay.mainloop()


# Update the 2 corners of the canvas
def update_positions(topleft, bottomright):
    global topleft_pos, bottomright_pos
    topleft_pos = topleft
    topleft_desc.config(text=f"Top Left Pos: {topleft_pos}", fg="green")
    bottomright_pos = bottomright
    bottomright_desc.config(text=f"Bottom Right Pos: {bottomright_pos}", fg="green")

def get_canvas():
    create_resizable_window(update_positions)

# Update the finished hexbox with our colors.
def update_finhexbox_color(color):
    if color in finhexbox.get(0,tk.END):
        return
    finhexbox.insert(tk.END, color)
    finhexbox.itemconfig(finhexbox.size()-1, bg=color, fg=contrast_color(color))
    finhexbox.update()
    finhexbox.update_idletasks()

# Turn on the flag
def toggle_stop_flag():
    global stop_flag
    if processing_pic:
        stop_flag = True
        title_label.config(text=f"Halting!", fg="green")

# Binds STOPKEY so you just need to tap it instead of hold it
def update_stopkey(newkey):
    global STOPKEY
    keyboard.remove_hotkey(STOPKEY)
    STOPKEY = newkey
    keyboard.add_hotkey(STOPKEY, toggle_stop_flag)
# Binds our default
keyboard.add_hotkey(STOPKEY, toggle_stop_flag)

# Continue from where we left off
def continue_mapping():
    start_mapping(True)

# The actual mapping segment
def start_mapping(continueprogress = False):
    global bottomright_pos, topleft_pos, hexput_pos, spraycolor_pos, image_selected, image_size, stop_flag, processing_pic
    if not all([bottomright_pos, topleft_pos, hexput_pos, spraycolor_pos, image_selected]):
        startbutton.config(text="Insufficient Data!")
        root.after(SECONDS(3), lambda: startbutton.config(text="Start"))
        return
    title_label.config(text=f"Press {STOPKEY} to halt the program!", fg="red")
    if not continueprogress:
        finhexbox.delete(0, tk.END)
    root.update_idletasks()  # Update the GUI
    stop_flag = False
    processing_pic = True

    incrementX = (bottomright_pos[0] - topleft_pos[0]) / (image_size[0] - 1)
    incrementY = (bottomright_pos[1] - topleft_pos[1]) / (image_size[1] - 1)
    start_time = time.time()
    for color in image_unique_hex:
        if continueprogress and (color in finhexbox.get(0, finhexbox.size()-2)):
            continue
        if stop_flag:
            break
        if color == "#ffffff":
            update_finhexbox_color(color)
            continue
        pyperclip.copy(str(color))
        root.after(TRANSRATE)
        pyautogui.click(spraycolor_pos)
        root.after(TRANSRATE)
        pyautogui.click(hexput_pos)
        root.after(TRANSRATE)
        pyautogui.click(hexput_pos)
        root.after(TRANSRATE)
        pyautogui.hotkey("ctrlleft", "v")
        root.after(TRANSRATE)
        pyautogui.hotkey("enter")
        for sysX in range(image_size[0]):
            if stop_flag:
                break
            for sysY in range(image_size[1]):
                if stop_flag:
                    break
                if image_hex_array[sysX][sysY] == color:
                    pyautogui.click((incrementX * sysX) + topleft_pos[0], (incrementY * sysY) + topleft_pos[1])
                    root.after(TRANSRATE)
                    pyautogui.click
                    root.after(TRANSRATE)
        update_finhexbox_color(color)

    processing_pic = False
    if stop_flag:
        stop_flag = False
        root.after(TRANSRATE, lambda: title_label.config(text=f"SS13 ArtMapper {VERSION}", fg="white"))
        contbutton.config(state=tk.ACTIVE)
        return

    contbutton.config(state=tk.DISABLED)
    end_time = time.time()
    title_label.config(text=f"SS13 ArtMapper {VERSION}\n{time_convert(end_time - start_time)}", fg="white")

# Opens the git
def open_url(event, url):
    webbrowser.open(url)

# About menu
def about_app():
    overlay = tk.Toplevel(root, bg="#1e1e1e")
    overlay.geometry("500x100")
    overlay.title("About")

    abouttext = tk.Text(overlay, wrap=tk.WORD, bd=4, relief="raised", bg="#1e1e1e", fg="#ffffff")
    fulltext = (
        "Created with Python using pyautogui and tkinter.\n"
        "Our Git:\n"
        "https://github.com/Wallemations/ss13_artmapper\n"
        f"{VERSION}"
        )
    abouttext.insert(tk.INSERT, fulltext)
    # Open my git when the url is clicked
    giturl = "https://github.com/Wallemations/ss13_artmapper"
    url_start = fulltext.find("https")
    url_end = url_start + len(giturl)
    abouttext.tag_add("url", f"1.0 + {url_start} chars", f"1.0 + {url_end} chars")
    abouttext.tag_configure("url", foreground="light blue", underline=True)
    abouttext.tag_bind("url", "<Button-1>", lambda event: open_url(event, giturl))
    
    abouttext.config(state=tk.DISABLED)
    abouttext.pack(expand=True, fill=tk.BOTH)
    
    overlay.mainloop()

# Instructions menu
def help_instructions():
    overlay = tk.Toplevel(root, bg="#1e1e1e")
    overlay.geometry("900x300")
    overlay.title("Instructions")

    abouttext = tk.Text(overlay, wrap=tk.WORD, bd=4, relief="raised", bg="#1e1e1e", fg="#ffffff")
    fulltext = (
        "To use this program, just follow these steps!\n"
        "1) Set up in-game with a canvas and spraycan/palette. Make sure you're somewhere safe!\n"
        "2) Upload your art into the program. Be sure it's a .png/.jpg, and that it's the right size!\n"
        "   Note: Lower color amounts = faster paintings. Index your pictures!\n"
        "3) Set the location of the color picker button by dragging the transparent window's + on top of the corresponding area.\n"
        "   Spraycan: In the spraycan's menu, it is the \"Custom Color\" button. DO NOT CLOSE THE SPRAYCAN MENU!\n"
        "   Palette: The palette item itself, in your mainhand.\n"
        "4) Set the location of the your canvas. Drag the opened window until it matches the gridlines on your canvas, then confirm.\n"
        "5) Press Start!\n"
        "The program will start transferring your art in-game color-by-color.\n\n"
        f"If you want to stop the program mid-paint, press \"{STOPKEY}\". This can be rebound in your preferences.\n"
        "If you want to resume after stopping, click the \"Continue\" button.")
    abouttext.insert(tk.INSERT,fulltext)
    
    abouttext.tag_add("bold", "2.0", "2.2")
    abouttext.tag_add("bold", "3.0", "3.2")
    abouttext.tag_add("bold", "4.3", "4.7")
    abouttext.tag_add("bold", "5.0", "5.2")
    abouttext.tag_add("bold", "6.3", "6.12") 
    abouttext.tag_add("bold", "7.3", "7.11")
    abouttext.tag_add("bold", "8.0", "8.2")
    abouttext.tag_add("bold", "9.0", "9.2")
    abouttext.tag_add("bold", "12.49","12.53")
    abouttext.tag_configure("bold", font=("Helvetica", 12, "bold"))
    
    abouttext.config(state=tk.DISABLED)
    abouttext.pack(expand=True, fill=tk.BOTH)
    
    overlay.mainloop()

# Preference menu
def help_prefs():
    overlay = tk.Toplevel(root, bg="#1e1e1e")
    overlay.geometry("400x300")
    overlay.title("Preferences")

    prefs_title = tk.Label(overlay, text="Preferences", font=("Franklin Gothic Medium", 15), fg="#ffffff", bg="#1e1e1e")
    prefs_desc = tk.Label(overlay, text="There's no way to save these without making an external\nfile, so you need to reset these every time you open the app.", font=("Franklin Gothic Medium", 8), fg="#ffffff", bg="#1e1e1e")
    prefs_title.pack()
    prefs_desc.pack(pady=(0,10))

    # STOPKEY
    stopkey_label = tk.Label(overlay, text="Stop Key (e.g., 'k'):", fg="#ffffff", bg="#1e1e1e", font=("Helvetica", 12, "bold"))
    stopkey_desc = tk.Label(overlay, text="Press this key to halt the program.", fg="#ffffff", bg="#1e1e1e", font=("Helvetica", 10))
    stopkey_label.pack()
    stopkey_desc.pack(pady=(0,5))
    stopkey_entry = tk.Entry(overlay, bg="#444444", fg="#ffffff")
    stopkey_entry.insert(0, STOPKEY)
    stopkey_entry.pack(pady=(0,5))
    
    # TRANSRATE
    transrate_label = tk.Label(overlay, text="Transfer Rate in Milliseconds (e.g., '50'):", fg="#ffffff", bg="#1e1e1e", font=("Helvetica", 12, "bold"))
    transrate_desc = tk.Label(overlay, text="Lower numbers can lead to desync from\nservers due to too many inputs too fast.", fg="#ffffff", bg="#1e1e1e", font=("Helvetica", 10))
    transrate_label.pack()
    transrate_desc.pack(pady=(0,5))
    transrate_entry = tk.Entry(overlay, bg="#444444", fg="#ffffff")
    transrate_entry.insert(0, str(TRANSRATE))
    transrate_entry.pack(pady=(0,5))

    def save_preferences():
        global STOPKEY
        global TRANSRATE
        new_stopkey = stopkey_entry.get()
        if new_stopkey:
            update_stopkey(new_stopkey)
        new_transrate = transrate_entry.get()
        if new_transrate:
            TRANSRATE = new_transrate
    
        overlay.destroy()

    save_button = tk.Button(overlay, text="Save Preferences", command=save_preferences, bg="#444444", fg="#ffffff")
    save_button.pack()

    overlay.mainloop()

# Copies the hex of the item we selected to our clipboard
def copyhex(event, listbox):
    selected_item = listbox.get(tk.ACTIVE)
    
    if selected_item:
        # Clear the clipboard and append the selected item
        root.clipboard_clear()
        root.clipboard_append(selected_item)
        root.update()

# Create the main application window
root = tk.Tk()
root.title(f"SS13 ArtMapper {VERSION}")
root.geometry("400x400")
root.configure(bg="#1e1e1e")

#! Menu toolbar
toolbar = tk.Menu(root)

helpmenu = tk.Menu(toolbar, tearoff=False)
helpmenu.add_command(label="Instructions", command=help_instructions)
helpmenu.add_command(label="Preferences", command=help_prefs)
helpmenu.add_command(label="About", command=about_app)

toolbar.add_cascade(label="Tools", menu=helpmenu)
root.config(menu=toolbar)

#! Main Frame
frame_1 = tk.Frame(root, bd=4, relief="raised", bg="#1e1e1e")
frame_1.pack(fill=tk.BOTH, expand=1)

# Title Label
title_label = tk.Label(frame_1, text=f"SS13 ArtMapper {VERSION}", font=("Franklin Gothic Medium", 15), fg="#ffffff", bg="#1e1e1e")
title_label.pack(side=tk.TOP)

# Create a canvas to draw the pixel grid
pixel_canvas = tk.Canvas(frame_1, bd=0, highlightthickness=0, width=0, height=0, bg="#1e1e1e")
pixel_canvas.pack(side=tk.TOP)

# Create a label to display the dimensions of the uploaded image
dimensions_label = tk.Label(frame_1, text="Valid canvas sizes: 11x11, 19x19, 23x19, 23x23, 24x24, 36x24, 45x27", fg="#ffffff", bg="#1e1e1e")
dimensions_label.pack()

# Create a button to open the file dialog
upload_button = tk.Button(frame_1, text="Upload Image", command=open_image, bg="#444444", fg="#ffffff")
upload_button.pack()

#! Makes a frame for the lower section
frame_2 = tk.Frame(root, bd=4, relief=tk.SUNKEN, bg="#1e1e1e")
frame_2.pack(fill=tk.BOTH, expand=1)

#* Frame for our list
frame_list = tk.Frame(frame_2, bd=4, relief=tk.RAISED, bg="#1e1e1e")
frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# List description
listdesc = tk.Label(frame_list, text="No Colors Yet!", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")

# Create a Listbox to display to the right
hexbox = tk.Listbox(frame_list, bg="#444444", fg="#ffffff")

# Listbox of colors we've finished transferring onto the canvas
findesc = tk.Label(frame_list, text="Finished Colors:", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")

# Finished hexes
finhexbox = tk.Listbox(frame_list, bg="#444444", fg="#ffffff")

# Using a grid because frames were making it not look nice
frame_list.grid_rowconfigure(0, weight=0)
frame_list.grid_rowconfigure(1, weight=1)
frame_list.grid_rowconfigure(2, weight=0)
frame_list.grid_rowconfigure(3, weight=1)
frame_list.grid_columnconfigure(0, weight=1)

listdesc.grid(row=0, column=0, sticky="ew")
hexbox.grid(row=1, column=0, sticky="nsew")
findesc.grid(row=2, column=0, sticky="ew")
finhexbox.grid(row=3, column=0, sticky="nsew")

hexbox.bind("<ButtonRelease-1>", lambda event: copyhex(event, hexbox))
finhexbox.bind("<ButtonRelease-1>", lambda event: copyhex(event, finhexbox))

#! Makes a frame for the lower section's buttons
frame_3 = tk.Frame(frame_2, bd=4, relief="raised", bg="#1e1e1e")
frame_3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Instructions
instructions = tk.Label(frame_3, text="Set the required positions!", fg="#ffffff", bg="#1e1e1e")
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

# Canvas Label
canvas_desc = tk.Label(frame_3, text="Canvas Positions", font=("Franklin Gothic Medium", 12), fg="#ffffff", bg="#1e1e1e")
canvas_desc.pack()

#! I'm so rich I got a frame for my frames
frame_4 = tk.Frame(frame_3, bd=4, relief="raised", bg="#1e1e1e")
frame_4.pack(fill=tk.BOTH, expand=1)

# Input for Canvas
topleft_desc = tk.Label(frame_4, text="Top Left Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
topleft_desc.pack()

bottomright_desc = tk.Label(frame_4, text="Bottom Right Not Set", font=("Franklin Gothic Medium", 10), fg="red", bg="#1e1e1e")
bottomright_desc.pack()

canvasloc = tk.Button(frame_4, text="Set Location", command=get_canvas, bg="#444444", fg="#ffffff")
canvasloc.pack()

#! Buttons
frame_5 = tk.Frame(frame_3, bg="#1e1e1e")
frame_5.pack(fill=tk.BOTH,expand=True)

#* Start Frame
startframe = tk.Frame(frame_5, bd=4, relief="raised", bg="green")
startframe.grid(row=0, column=0, sticky="ew")

# Start Button
startbutton = tk.Button(startframe, text="Start", command=start_mapping, bg="#444444", fg="#ffffff")
startbutton.pack()

#* Continue Frame
contframe = tk.Frame(frame_5, bd=4, relief="raised", bg="blue")
contframe.grid(row=0, column=2, sticky="ew")

# Continue Button
contbutton = tk.Button(contframe, text="Continue", state = tk.DISABLED, command=continue_mapping, bg="#444444", fg="#ffffff")
contbutton.pack()

#* Because even the quit button needs a frame
quitframe = tk.Frame(frame_5, bd=4, relief="raised", bg="red")
quitframe.grid(row=0, column=4, sticky="ew")

# Create a button to quit the program
quit_button = tk.Button(quitframe, text="Quit", command=quit_program, bg="#444444", fg="#ffffff")
quit_button.pack()


frame_5.grid_columnconfigure(0, weight=0)  # Start frame
frame_5.grid_columnconfigure(1, weight=1)  # Spacer
frame_5.grid_columnconfigure(2, weight=0)  # Continue frame
frame_5.grid_columnconfigure(3, weight=1)  # Spacer
frame_5.grid_columnconfigure(4, weight=0)  # Quit frame

root.mainloop()
