from tkinter import *
from tkinter import messagebox  # messagebox is not a class, so * didnt cover it
from pass_word_gen import password_gen
import pyperclip
import json
from difflib import get_close_matches  # A function for finding close match in a list of strings

# from PIL import Image, ImageTk
# from datetime import datetime

# BG_color = "#FFF2F2"
FONT = ("arial", 9, "normal")


# ---------------------------- SEARCH FUNCTION  -------------------------------- #
def search():
    try:
        # Try to open the file if it exists
        with open("data.json", mode="r") as file:
            # Search data
            data = json.load(file)

    except FileNotFoundError:
        # If the file is not found, show a pop-up
        messagebox.showerror(message="No data file found")

    else:
        # If the data file can be found
        user_search = website_entry.get()
        # convert data's keys to all lower case and search that way
        data_lower = {key.lower(): value for key, value in data.items()}

        # Try to find an exact match (not case-sensitive)
        if user_search.lower() in data_lower:

            search_result = data_lower[user_search.lower()]
            pyperclip.copy(search_result["password"])
            # Show result in pop-up
            messagebox.showinfo(title=user_search, message=f"Email: {search_result['email']}\n\n"
                                                           f"Password: {search_result['password']}\n\n"
                                                           f"password copied to clipboard")
            # update email field to the searched result
            username_entry.delete(0, END)
            username_entry.insert(END, search_result['email'])

        # If not exact match, try to suggest close matches
        else:
            website_list = data.keys()
            suggestion = get_close_matches(word=user_search, possibilities=website_list)
            if len(suggestion) == 0:
                messagebox.showinfo(message=f"No exact match")
            else:
                messagebox.showinfo(message=f"No exact match, did you mean any of "
                                            f"the following ones?\n{suggestion}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def populate_password():
    password = password_gen()
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    pyperclip.copy(password)
    messagebox.showinfo(message="Password generated and copied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website_data = website_entry.get()
    username_data = username_entry.get()
    password_data = password_entry.get()

    # now = datetime.now()
    # file_name = now.strftime("%Y_%m_%d__%H_%M_%S.txt")

    new_data = {
        website_data: {
            "email": username_data,
            "password": password_data,
        }
    }

    if len(username_data)*len(password_data) == 0:
        messagebox.showwarning(title="Oops", message="You've left a field empty")

    else:

        try:
            with open('data.json', mode='r') as file:
                # 1.Read old data
                data = json.load(file)
                # 2.Update old data
                data.update(new_data)

        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                # 3.if file not found, create file and save new_data
                json.dump(new_data, file, indent=4)  # (data, location)

        else:
            with open("data.json", mode="w") as file:
                # 3.if file is found, save updated data
                json.dump(data, file, indent=4)  # (data, location)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Pass")
window.config(padx=50, pady=50,)

# -------------- Canvas
canvas = Canvas(width=210, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(115, 100, image=lock_img)
canvas.grid(row=1, column=2)

# --------------- Labels
label_width = 12
website_label = Label(text="Website:", font=FONT, width=label_width)
website_label.grid(row=2, column=1)

username_label = Label(text="Username/Email:", font=FONT, width=label_width)
username_label.grid(row=3, column=1)

password_label = Label(text="Password:", font=FONT, width=label_width)
password_label.grid(row=4, column=1)

# --------------- Entries
website_entry = Entry(width=28)
website_entry.grid(row=2, column=2, columnspan=1)
website_entry.focus()

username_entry = Entry(width=50)
username_entry.grid(row=3, column=2, columnspan=2)
username_entry.insert(END, "bbkes@outlook.com")

password_entry = Entry(width=28)
password_entry.grid(row=4, column=2)

# ---------------- Buttons
# loading an image to use for the button
gen_password_button = Button(text="Generate Password", font=FONT, width=16)
gen_password_button.config(command=populate_password)
gen_password_button.grid(row=4, column=3)

add_button = Button(text="Add", width=42)
add_button.config(command=save_data)
add_button.grid(row=5, column=2, columnspan=2)

search_button = Button(text="Search", width=16)
search_button.config(command=search)
search_button.grid(row=2, column=3)

window.mainloop()
