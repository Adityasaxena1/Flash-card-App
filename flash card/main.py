from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = ("Arial", 40, "italic")
FONTS = ("Arial", 60, "bold")
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Hindi.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    english_word = current_card["English"]
    canvas.itemconfig(language, text="English", fill="black")
    canvas.itemconfig(language_word, text=english_word, fill="black")
    canvas.itemconfig(background, image=front_image)
    flip_timer = window.after(3000, flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index= False)
    next_card()


def flip_card():
    canvas.itemconfig(background, image=back_image)
    canvas.itemconfig(language, text="Hindi", fill="white")
    canvas.itemconfig(language_word, text=current_card["Hindi"], fill="white")


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
background = canvas.create_image(400, 263, image=front_image)
language = canvas.create_text(400, 150, text="Text", font=FONT)
language_word = canvas.create_text(400, 263, text="word", font=FONTS)
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
