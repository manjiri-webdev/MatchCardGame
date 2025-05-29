import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Initialize the main window
root = tk.Tk()
root.title("Memory Match Game")
root.geometry("650x700")
root.config(bg="#265242")

# Centering everything
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a frame to center all widgets
main_frame = tk.Frame(root, bg="#265242")
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.columnconfigure(0, weight=1)

#varaibles
image_files = [f"{i}.jpg" for i in range(1,9)] * 2
random.shuffle(image_files)
buttons=[]
flipped_cards=[]
matches_found=0
moves=0
images={}

def load_images():
    for file in image_files:
        img = Image.open(file)
        img = img.resize((130, 130), Image.LANCZOS)
        images[file] = ImageTk.PhotoImage(img)

def flip_card(index):
    global flipped_cards, matches_found, moves

    if len(flipped_cards) < 2 and buttons[index]['state'] == 'normal':
        buttons[index].config(image=images[image_files[index]], state='disabled')
        flipped_cards.append(index)

        if len(flipped_cards) == 2:
            moves += 1
            update_score()
            if image_files[flipped_cards[0]] == image_files[flipped_cards[1]]:
                matches_found += 1
                flipped_cards = []
                if matches_found == len(image_files) // 2:
                    messagebox.showinfo("Congratulations!", f"You won in {moves} moves!")
                    reset_game()
            else:
                root.after(1000, flip_back)


def flip_back():
    global flipped_cards
    for index in flipped_cards:
        buttons[index].config(image=card_back_image, state='normal')
    flipped_cards = []


def reset_game():
    global image_files, buttons, flipped_cards, matches_found, moves
    random.shuffle(image_files)
    for button in buttons:
        button.config(image=card_back_image, state='normal')
    flipped_cards = []
    matches_found = 0
    moves = 0
    update_score()


def update_score():
    score_label.config(text=f"Moves: {moves} | Matches: {matches_found}")


# Load card images
load_images()
card_back_image = ImageTk.PhotoImage(Image.open("card_back.png").resize((130, 130), Image.LANCZOS))

# Title Label
title_label = tk.Label(
    main_frame,
    text="Memory Match Game",
    bg="#265242",
    fg="#FFFFFF",
    font=("Helvetica", 24, "bold"),
)
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Score Label
score_label = tk.Label(
    main_frame,
    text="Moves: 0 | Matches: 0",
    bg="#265242",
    fg="#FFFFFF",
    font=("Arial", 14),
)
score_label.grid(row=1, column=0, columnspan=4, pady=5)

# Create grid of buttons
buttons_frame = tk.Frame(main_frame, bg="#265242")
buttons_frame.grid(row=2, column=0, columnspan=4)

for i in range(4):
    for j in range(4):
        index = i * 4 + j
        button = tk.Button(
            buttons_frame,
            image=card_back_image,
            bg="#265242",  # Match the background color
            highlightthickness=2,  # Add a border
            highlightbackground="#FFFFFF",  # Border color
            relief="flat",  # Make it visually minimal
            command=lambda idx=index: flip_card(idx),
        )
        button.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(button)

# Reset Button
reset_button = tk.Button(
    main_frame,
    text="Reset",
    command=reset_game,
    bg="#FFFFFF",
    fg="#265242",
    font=("Arial", 14, "bold"),
    relief="raised",
    borderwidth=3,
)
reset_button.grid(row=3, column=0, columnspan=4, pady=20)

# Start the main event loop
root.mainloop()
