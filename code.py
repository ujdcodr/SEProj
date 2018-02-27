from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Course Management System")

        self.label = Label(master, text="Login Page")
        self.label.pack()

        self.greet_button = Button(master, text="Login", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Logged In")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
