from tkinter import *

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Course Management System")

        self.label = Label(master, text="Login Page")
        self.label.pack()
        
        self.loglabel = Label(master, text="Enter username")
        self.loglabel.pack(side="left")
        self.name = Entry(master)
        self.name.pack(side="left")
        
        self.passlabel = Label(master, text="Enter username")
        self.passlabel.pack(side="left")
        self.passw = Entry(master,show="*")
        self.passw.pack(side="left")


        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(side="bottom")
        
        self.v = IntVar()
        self.stud =Radiobutton(master,text="Student", variable=self.v,value=1).pack(side="bottom")
        self.ins =Radiobutton(master,text="Instructor", variable=self.v,value=2).pack(side="bottom")
        
        self.login = Button(master, text="Login", command=self.log)
        self.login.pack(side="bottom")
   
    def log(self):
        print(self.name.get())
        print(self.passw.get())
        print(self.v.get())
        
        print("Logged In")

root = Tk()
root.minsize(200,200)
my_gui = MyFirstGUI(root)
root.mainloop()
