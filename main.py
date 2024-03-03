import tkinter

import customtkinter
from customtkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import random

# selected_button = None
selected_button_frame1 = None
selected_button_frame2 = None


def selected_movie(button, frame):
    global selected_button_frame1, selected_button_frame2

    if frame == "frame1":
        selected_button = selected_button_frame1
    else:
        selected_button = selected_button_frame2

    button_color = button.cget("bg_color")
    if selected_button:
        selected_button.configure(bg_color=button_color, fg_color=button_color)

    button.configure(bg_color="#0f1513", fg_color="#0f1513")

    if frame == "frame1":
        selected_button_frame1 = button
    else:
        selected_button_frame2 = button

buttons = []
watched_buttons =[]

def addMovie():
    new_movie = add_entry.get().strip().lower()
    if new_movie:
        if any(button.cget("text").strip().lower() == new_movie for button in buttons):
            messagebox.showinfo("Duplicate Movie", f"There is already {new_movie} movie in the library!")
        elif len(new_movie) > 28:
            messagebox.showinfo("Too long title!", "Tittle can be maximum of 28 chars!")
        else:
            with open("watched_data.txt", "r") as watched_file:
                watched_movies = [movie.strip().lower() for movie in watched_file.readlines()]
            if new_movie in watched_movies:
                messagebox.showinfo("Duplicate Movie", f"Movie {new_movie} has already been seen!")
            else:
                with open("data.txt", "a") as data_file:
                    data_file.write(f"{new_movie}\n")
                display_movies()
    add_entry.delete(0, 'end')


def create_button(movie_title, frame):
    button = customtkinter.CTkButton(frame, text=movie_title, font=font2, fg_color="#224d6a", bg_color="#224d6a")
    button.configure(command=lambda b=button: selected_movie(b, frame="frame1" if frame == frame1 else "frame2"))
    button.pack(fill="x", padx=5, pady=2)

    if frame == frame1:  # Update selected_button_frame1 only for buttons in frame1
        global selected_button_frame1
        selected_button_frame1 = button

    return button


def display_movies():
    for widget in frame1.winfo_children():
        widget.destroy()
    buttons.clear()
    with open("data.txt", "r") as data_file:
        movies = data_file.readlines()
        for movie in movies:
            button = create_button(movie.strip(), frame1)
            button.update_idletasks()
            frame1_width = frame1.winfo_width()
            button_width = int(frame1_width * 0.8)
            button.configure(width=button_width)
            buttons.append(button)

def create_watched_button(movie_title, frame):
    watched_button = customtkinter.CTkButton(frame, text=movie_title, font=font2, bg_color="#008631", fg_color="#008631")
    watched_button.pack(fill="x", padx=5, pady=2)
    watched_button.configure(command=lambda b=watched_button: selected_movie(b, frame="frame1" if frame == frame1 else "frame2"))
    return watched_button

def populate_watched_movies():
    global watched_buttons
    for widget in frame2.winfo_children():
        widget.destroy()
    watched_buttons.clear()
    with open("watched_data.txt", "r") as watched_file:
        watched_movies = watched_file.readlines()
        for movie in watched_movies:
            movie_title = movie.strip()
            if not any(button.cget("text").strip().lower() == movie_title.lower() for button in watched_buttons):
                watched_button = create_watched_button(movie_title, frame2)
                watched_buttons.append(watched_button)



def movie_watched():
    global selected_button_frame1, selected_button_frame2

    if selected_button_frame1 and selected_button_frame1 in buttons:
        movie_title = selected_button_frame1.cget("text").strip()
        with open("data.txt", "r") as data_file:
            movies = [movie.strip() for movie in data_file.readlines()]

        if movie_title in movies:
            movies.remove(movie_title)

        with open("data.txt", "w") as data_file:
            for movie in movies:
                data_file.write(f"{movie}\n")

        with open("watched_data.txt", "a") as watched_file:
            watched_file.write(f"{movie_title}\n")

        selected_button_frame1.pack_forget()
        selected_button_frame1.destroy()
        buttons.remove(selected_button_frame1)

        selected_button_frame1 = None

        display_movies()
        populate_watched_movies()
    elif selected_button_frame2 and selected_button_frame2 in watched_buttons:
        # Handle the case for moving watched button back to frame1 if needed
        pass


def random_movie():
    actual_movies = []
    with open("data.txt", "r") as data_file:
        movies = [movie.strip() for movie in data_file.readlines()]
        for movie in movies:
            actual_movies.append(movie)
    if len(actual_movies) == 0:
        messagebox.showinfo("Warning", "There are no movies in the library yet!")
    else:
        drawn_movie = random.choice(actual_movies)
        messagebox.showinfo("Random Movie", f"Your movie proposal for this evening is {drawn_movie}")

def show_description():
    description_window = tkinter.Toplevel(app)
    description_window.title("Description")
    description_window.geometry("600x400")

    description_window.configure(bg=app.cget("bg"))

    with open("description_data.txt", "r") as file:
        description_text = file.read()

    description_text_widget = scrolledtext.ScrolledText(description_window, wrap=tkinter.WORD, bg=description_window.cget("bg"), fg="white", font=font2)
    description_text_widget.insert(tkinter.END, description_text)
    description_text_widget.pack(expand=True, fill=tkinter.BOTH, padx=20, pady=20)

def delete_selected_item():
    global selected_button_frame1, selected_button_frame2
    if selected_button_frame1:
        movie_title = selected_button_frame1.cget("text").strip()
        if messagebox.askyesno("Delete Movie", f"Are you sure you want to delete {movie_title}?"):
            selected_button_frame1.pack_forget()
            selected_button_frame1.destroy()
            if selected_button_frame1 in buttons:
                buttons.remove(selected_button_frame1)
                with open("data.txt", "r") as file:
                    lines = file.readlines()
                with open("data.txt", "w") as file:
                    for line in lines:
                        if line.strip() != movie_title:
                            file.write(line)
            elif selected_button_frame1 in watched_buttons:
                watched_buttons.remove(selected_button_frame1)
                with open("watched_data.txt", "r") as file:
                    lines = file.readlines()
                with open("watched_data.txt", "w") as file:
                    for line in lines:
                        if line.strip() != movie_title:
                            file.write(line)
            selected_button_frame1 = None
    elif selected_button_frame2:
        movie_title = selected_button_frame2.cget("text").strip()
        if messagebox.askyesno("Delete Movie", f"Are you sure you want to delete {movie_title}?"):
            selected_button_frame2.pack_forget()
            selected_button_frame2.destroy()
            if selected_button_frame2 in watched_buttons:
                watched_buttons.remove(selected_button_frame2)
                with open("watched_data.txt", "r") as file:
                    lines = file.readlines()
                with open("watched_data.txt", "w") as file:
                    for line in lines:
                        if line.strip() != movie_title:
                            file.write(line)
            selected_button_frame2 = None



app = CTk()
app.geometry("880x570")
app.title("Movies Library")
app.resizable(False, False)
app.config(pady=30, padx=50)
set_appearance_mode("dark")

font1 = ('Arial', 30, 'bold')
font2 = ('Arial', 14, 'bold')

add_entry = customtkinter.CTkEntry(app, placeholder_text="Movie...", width=240)
add_entry.grid(row=0, column=0, sticky="w")
add_button = customtkinter.CTkButton(app, text="Add", command=addMovie, width=60)
add_button.grid(row=0, column=0, sticky="e")

to_watch_label = customtkinter.CTkLabel(app, text="To Watch", font=("Arial", 22))
to_watch_label.grid(row=1, column=0)

movies_seen_label = customtkinter.CTkLabel(app, text="Already Seen", font=("Arial", 22))
movies_seen_label.grid(row=1, column=2)

watched_button = customtkinter.CTkButton(app, text="Watched", command=movie_watched)
watched_button.grid(row=2, column=1, pady=(0, 50), padx=5)

random_button = customtkinter.CTkButton(app, text="Random Movie", command=random_movie)
random_button.grid(row=2, column=1, pady=(50, 0), padx=5)

description_button = customtkinter.CTkButton(app, text="Description", command=show_description)
description_button.grid(row=2, column=1, pady=(0, 350),padx=5)

frame1 = customtkinter.CTkScrollableFrame(app, width=280, height=400)
frame2 = customtkinter.CTkScrollableFrame(app, width=280, height=400)
frame1.grid(row=2, column=0)
frame2.grid(row=2, column=2)

delete_button = customtkinter.CTkButton(app, text="Delete", command=delete_selected_item)
delete_button.grid(row=2, column=1, pady=(150, 0))


app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, pad=30)

display_movies()
populate_watched_movies()

app.mainloop()