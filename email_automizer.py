from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb


import os
import pickle
import helper


class App:
    def __init__(self, master):
        self.master = master

        self.email_subject_label = Label(
            self.master, text="Enter email subject")
        self.email_subject_label.pack()
        self.email_subject_text = Text(self.master, height=1, width=40)
        self.email_subject_text.pack()

        self.email_receiver_label = Label(
            self.master, text="Enter email of receiver")
        self.email_receiver_label.pack()
        self.email_receiver_text = Text(self.master, height=1, width=40)
        self.email_receiver_text.pack()
        self.email_contents_label = Label(
            self.master, text="Enter email contents here")
        self.email_contents_label.pack()
        self.email_contents_text = Text(self.master, height=10, width=40)
        self.email_contents_text.pack()

        self.recipents_list_label = Label(
            self.master, text="Please supply a list of cc, seperate recipients with a ','")
        self.recipents_list_label.pack()
        self.recipents_list_text = Text(self.master, height=4, width=40)
        self.recipents_list_text.pack()

        self.frame1 = Frame(self.master)
        self.frame1.pack()
        self.day_of_week_label = Label(self.frame1, text="Chose day of week")
        days_of_week = ["", "SUN", "MON", "TUS", "WED", "THU", "FRI", "SAT"]
        x = StringVar(self.frame1)
        x.set(days_of_week[1])
        self.day_of_week_optionmenu = OptionMenu(self.frame1, x, *days_of_week)
        self.day_of_week_label.pack(side=LEFT, padx=2)
        self.day_of_week_optionmenu.pack(side=LEFT)

        self.frame2 = Frame(self.master)
        self.frame2.pack()
        self.time_label = Label(
            self.frame2, text="Enter time in this format hh:mm")
        self.time_entry = Text(self.frame2, height=1, width=5)
        self.time_label.pack(side=LEFT, padx=2)
        self.time_entry.pack(side=LEFT)
        
        self.automate_button = Button(self.master, text="Automate", command=lambda: helper.handel_inputs(
            self.email_contents_text.get("1.0", "end-1c"),
            self.email_receiver_text.get("1.0", "end-1c"),
            self.email_subject_text.get("1.0", "end-1c"),
            self.recipents_list_text.get("1.0", "end-1c"),
            x.get(),
            self.time_entry.get("1.0", "end").strip()
        ))
              
        self.automate_button.pack()


def main():
    if not os.path.exists(os.path.realpath("...")+"\\saved_data.pickle"):
        if not os.path.exists(os.path.realpath("...")+"\\credentials.json"):
            mb.showerror(
                title="Error", message="Supply a credentials.json file")
            exit()
        root = Tk()

        root.title("Email Automizer")
        root.geometry("400x450")
        root.resizable(False, False)
        my_gui = App(root)
        root.mainloop()
    else:
        saved_data = pickle.load(open(os.path.realpath("...")+"\\saved_data.pickle", "rb"))
        helper.handel_inputs(saved_data["email_contents"], saved_data["to"],
                             saved_data["subject"], saved_data["cc"], saved_data["day"], saved_data["time"])

if __name__ == "__main__":
    main()
