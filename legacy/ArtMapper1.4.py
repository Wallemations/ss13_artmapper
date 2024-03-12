# A tool to take a .jpg and translate that into an SS13 painting using a spraycan
# Created by: DEEP RED (ft. Wallem)
#! RED : HOLDING THE 'STOPKEY' BUTTON WILL SHUT OFF THE PROGRAM DURING TRANSFER


# The size of our initial image
SIZE = [0, 0]
# All valid canvas sizes in the game
VALID_CANVAS_SIZES = {(11,11), (19,19), (23,19), (23,23), (24,24), (36,24), (45,27)}
# How long we sleep when speaking
SPEAKRATE = 0.25
TRANSRATE = 0.05 # RED : 0.05 MAY BE too fast for the server
#! Key used to stop the program during drawing process
STOPKEY = "k"
# Key used to input positions of elements on your screen
SCANKEY = "i"

print("RED: Testing Diagnostics...")
import pyautogui
import time
#from pysine import sine
import keyboard
from PIL import Image
import pyperclip
import os
import colorama
from termcolor import colored

colorama.init()

# Used for text added by Wallem
def wallem_speak(speech):
    print(colored("Wallem : ", "blue", attrs = ["bold"]) + speech)

# Used for text added by RED
def red_speak(speech):
    print(colored("RED : ", "red", attrs = ["bold"]) + speech)

# Used for basic dotted seperator lines
def dots():
    print(colored("- - - - - - - - - - - - - - - - - - - - - - - - -", "yellow"))

# Converts RGB values into hex codes, disregarding alpha
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

# Function to list and allow the user to select an image file
def select_image_file():
    current_directory = os.getcwd()

    # List all files in the current directory with the .png and .jpg extensions
    image_files = [filename for filename in os.listdir(current_directory) if filename.endswith(('.png', '.jpg'))]

    if not image_files:
        print("No .png or .jpg files found in the current directory.")
        time.sleep(10)
        quit()

    print("List of image files in the current directory:")
    for i, filename in enumerate(image_files, start=1):
        print(f"{i}. {filename}")

    while True:
        try:
            user_choice = int(input(colored("Enter the number of the image file you want to use: \n", attrs = ["bold"])))
            if 1 <= user_choice <= len(image_files):
                selected_image_filename = image_files[user_choice - 1]
                break
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return selected_image_filename

def load_image():
    global SIZE
    try:
        image = Image.open(select_image_file()).convert("RGB")
    except:
        print("File not found or unsupported format! Supported formats: .jpg, .png")
        time.sleep(10)
        quit()
    im = image.load()
    SIZE = image.size
    return im

def time_convert(sec):
    mins = sec // 60
    hours = mins // 60
    return f"Time Lapsed = {hours}:{mins % 60}:{sec % 60}"

red_speak("Screen Resolution > " + str(pyautogui.size()) + ".")
red_speak("Looks like stuff works, let's get moving.")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
# Load our image
wallem_speak("Time to open your file!")
wallem_speak("Note that while it can take .jpg files, .png files run far faster.")
wallem_speak("(File must be stored in the same folder as this executable.)")
original_image = load_image()
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("This is your pixelart's X size > " + str(SIZE[0]))
red_speak("...and this is your pixelart's Y size > " + str(SIZE[1]))
wallem_speak(f"That's {SIZE[0] * SIZE[1]} pixels!")
# Check if we're a valid canvas size
if SIZE not in VALID_CANVAS_SIZES:
    print("- - - - - - - - - E R R O R - - - - - - - - - - -")
    wallem_speak("This is not a valid canvas size!")
    wallem_speak("Check the VALID_CANVAS_SIZES list for all the possible canvas sizes!")
    time.sleep(10)
    quit()
# Create an array of all of our hex values & a list of all unique hex values
image_hex_array = []
image_unique_hex = []
for x in range(SIZE[0]):
    x_px = []
    for y in range(SIZE[1]):
        pixel = original_image[x, y]
        x_px.append(rgb_to_hex(pixel))
        if rgb_to_hex(pixel) not in image_unique_hex:
            image_unique_hex.append(rgb_to_hex(pixel))
    image_hex_array.append(x_px)
time.sleep(SPEAKRATE)
wallem_speak("Your photo has been analyzed!")
wallem_speak(f"It has {len(image_unique_hex)} unique color values!")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Okay, I need you to open your SS13 art tab.")
red_speak("I've made this program based on TGStation and Pixilart editor, so it might not work for other servers...")
red_speak("Oh, and I need a spraycan in your hand.")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Word of note: I detect the TOP RIGHT of your cursor; the tip of the arrow, so put THAT bit in the center of the canvas pixels.")
red_speak("Now, to the game...")
red_speak("Let's see...")
red_speak("Have your spraypaint in hand.")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Show me where your color picker is in the spraycan.")
red_speak(colored(f"Press {SCANKEY} when you're ready to grab location...", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
spraycolor = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(spraycolor[0]) + ", > " + str(spraycolor[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("...also the MIDDLE (where the text is) of the HEX input field.")
red_speak(colored(f"Press {SCANKEY} when you're ready to grab location...", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
hexinput = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(hexinput[0]) + ", > " + str(hexinput[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Color accept button.")
red_speak(colored(f"Press {SCANKEY} when you're ready to grab location...", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
accept = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(accept[0]) + ", > " + str(accept[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Now, show me your TOP LEFT pixel of the SS13 editor, and click as close as you can to the middle of it.")
red_speak(colored(f"Hover your mouse on that pixel and I'll grab the location of your mouse when you press {SCANKEY}.", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
topleft = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(topleft[0]) + ", > " + str(topleft[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Now do the same but with your SS13's TOP RIGHT PIXEL.")
red_speak(colored(f"Press {SCANKEY} when you're ready to grab location...", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
topright = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(topright[0]) + ", > " + str(topright[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("Again, but with your SS13's BOTTOM LEFT PIXEL.")
red_speak(colored(f"Press {SCANKEY} when you're ready to grab location...", attrs = ["bold"]))
while not keyboard.is_pressed(SCANKEY):
    time.sleep(TRANSRATE)
bottomleft = pyautogui.position()
#sine(frequency=600.0, duration=0.5)
red_speak("Location got at > " + str(bottomleft[0]) + ", > " + str(bottomleft[1]) + ".")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("That's all of the inputs.")
red_speak("It's my turn to do some work.")
red_speak("Calculating operations...")
incrementX = (topright[0] - topleft[0]) / (SIZE[0] - 1)
incrementY = (bottomleft[1] - topleft[1]) / (SIZE[1] - 1)
red_speak("It's gotime.")
time.sleep(SPEAKRATE)
dots()
print(colored(f"Hold {STOPKEY} to stop the program manually!", attrs = ["bold"]))
time.sleep(SPEAKRATE)
start_time = time.time()
for color in image_unique_hex:
    if color == "#ffffff":
        continue
    pyperclip.copy(str(color))
    time.sleep(TRANSRATE)
    pyautogui.click(spraycolor)
    time.sleep(TRANSRATE)
    pyautogui.click(hexinput)
    time.sleep(TRANSRATE)
    pyautogui.click(hexinput)
    time.sleep(TRANSRATE)
    pyautogui.hotkey("ctrlleft", "v")
    time.sleep(TRANSRATE)
    pyautogui.click(accept)
    time.sleep(TRANSRATE + 0.5)
    for sysX in range(SIZE[0]):
        for sysY in range(SIZE[1]):
            if keyboard.is_pressed(STOPKEY):
                red_speak("EMERGENCY SHUTOFF.")
                time.sleep(10)
                quit()
            if image_hex_array[sysX][sysY] == color:
                pyautogui.click((incrementX * sysX) + topleft[0], (incrementY * sysY) + topleft[1])
                time.sleep(TRANSRATE)
                pyautogui.click
                time.sleep(TRANSRATE * 2)
                #sine(frequency=600.0, duration=0.2)
end_time = time.time()
time.sleep(TRANSRATE + 0.5)
wallem_speak(f"{time_convert(end_time - start_time)}")
time.sleep(SPEAKRATE)
dots()
time.sleep(SPEAKRATE)
red_speak("I hope that worked.")
red_speak("I'm done here.")
red_speak("You can rerun this program, or don't.")
red_speak("Oh, and ping me on discord if stuff breaks.")
time.sleep(10)