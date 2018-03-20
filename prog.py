# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import Tkinter as tk
import tkMessageBox
LARGE_FONT= ("Verdana", 12)

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()


class CMSapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,PageSix,PageSeven):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        loglabel = tk.Label(self, text="Enter username")
        loglabel.pack(pady=10,padx=10)
        name = tk.Entry(self)
        name.pack(pady=30,padx=40) 
        
        passlabel = tk.Label(self, text="Enter password")
        passlabel.pack(pady=20,padx=20)
        passw = tk.Entry(self,show="*")
        passw.pack(pady=40,padx=40)
        
        v = tk.IntVar()
        stud = tk.Radiobutton(self,text="Student", variable=v,value=1).pack(side="bottom")
        ins =tk.Radiobutton(self,text="Instructor", variable=v,value=2).pack(side="bottom")
        
        
        def log():
            n = name.get()
            p = passw.get()
            name.delete(0, 'end')
            passw.delete(0, 'end')
            
            if n=="" or p=="":
                tkMessageBox.showinfo("Option", "Please enter all login credentials")
            else:
                            
                print(v.get())
                if(v.get()==1):
                    n = (str(n),) 
                    c.execute('SELECT * FROM Student where Name =?',n)
                    r = c.fetchone()
                    if(p==r[2]):
                        t = (r[0],r[1])
                        c.execute('INSERT into Logged VALUES (?,?)', t)
                        conn.commit() 
                        print("Student Logged In")
                        controller.show_frame(PageOne)
                    else:
                        tkMessageBox.showinfo("Nostud", "Invalid Credentials")    
                
                if(v.get()==2):
                    n = (str(n),) 
                    c.execute('SELECT * FROM Instructor where Name =?',n)
                    r = c.fetchone()
                    if(p==r[2]):
                        t = (r[0],r[1])
                        
                        c.execute('INSERT into Logged VALUES (?,?)', t)
                        conn.commit()
                        print("Instructor Logged In")
                        controller.show_frame(PageTwo)
            
                    else:
                        tkMessageBox.showinfo("Nostud", "Invalid Credentials")
                    
                if(v.get()==0):
                    tkMessageBox.showinfo("Option", "Please choose one option(Student/Instructor)")
                
                
         
        login = tk.Button(self, text="Login", command=log)
        login.pack(side="bottom")
        
        
        def sign():
            n = name.get()
            p = passw.get()
            name.delete(0, 'end')
            passw.delete(0, 'end')
            
            if n=="" or p=="":
                tkMessageBox.showinfo("Option", "Please enter all login credentials")
            else:
                            
                print(v.get())
                if(v.get()==1):
                    m = (str(n),) 
                    c.execute('SELECT count(*) FROM Student where Name =?',m)
                    r = c.fetchone()
                    if(r[0]==0):
                        c.execute('SELECT count(*) FROM Student')
                        l = c.fetchone()
                        t = (l[0]+1,str(n),str(p),'IT')
                        c.execute('INSERT into Student VALUES (?,?,?,?)', t)
                        x = (l[0]+1,str(n))
                        c.execute('INSERT into Logged VALUES (?,?)', x)
                        conn.commit() 
                        
                        print("Student Logged In")
                        tkMessageBox.showinfo("stud", "New Student Signed up")
                        controller.show_frame(PageOne)
                    else:
                        tkMessageBox.showinfo("st", "Account already exists")    
                
                if(v.get()==2):
                    m = (str(n),) 
                    c.execute('SELECT count(*) FROM Instructor where Name =?',m)
                    r = c.fetchone()
                    if(r[0]==0):
                        c.execute('SELECT count(*) FROM Instructor')
                        l = c.fetchone()
                        t = (l[0]+1,str(n),str(p))
                        c.execute('INSERT into Instructor VALUES (?,?,?)', t)
                        x = (l[0]+1,str(n))
                        c.execute('INSERT into Logged VALUES (?,?)', x)
                        conn.commit() 
                        
                        print("Instructor Logged In")
                        tkMessageBox.showinfo("in", "New Instructor Signed up")
                        controller.show_frame(PageOne)
                    else:
                        tkMessageBox.showinfo("ins", "Account already exists")    
                
                if(v.get()==0):
                    tkMessageBox.showinfo("Option", "Please choose one option(Student/Instructor)")
                
        
        signup = tk.Button(self, text="Sign Up", command=sign)
        signup.pack(side="bottom")
        
           
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome Student!!!" , font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Logout",
                            command=out)
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="View Available Courses",
                            command=lambda: controller.show_frame(PageThree))
        button2.pack()
        
        
        def show():
            T.delete(1.0,tk.END)
            c.execute('SELECT * from Logged')
            r = c.fetchone()
            print r[0]
            x = (str(r[0]),)
            T.insert(tk.END,"Code  	Name			Credits\n")
            for row in c.execute('SELECT * FROM Studtake where Num=?',x):
                T.insert(tk.END,str(row[2]) + "	" + row[3] + "		" + str(row[5])+"\n")
            
        T = tk.Text(self,height=20, width=40)
        T.pack()            
        button3 = tk.Button(self, text="View your Courses taken",
                            command=lambda: controller.show_frame(PageFive))
        button3.pack()
        

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome Instructor!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Logout",
                            command=out)
        button1.pack(side="bottom")
        
        def show():
            T.delete(1.0,tk.END)
            c.execute('SELECT * from Logged')
            r = c.fetchone()
            print r[0]
            x = (str(r[0]),)
            T.insert(tk.END,"Code  	Name			Credits\n")
            for row in c.execute('SELECT * FROM Course where Ins=?',x):
                T.insert(tk.END,str(row[0]) + "	" + row[1] + "		" + str(row[3])+"\n")
                
        def show_stud():
            T.delete(1.0,tk.END)
            c.execute('SELECT * from Logged')
            r = c.fetchone()
            print r[0]
            x = (str(r[0]),)
            T.insert(tk.END,"id  Name	Course		Credits\n")
            for row in c.execute('SELECT * FROM Studtake where Ins=?',x):
                T.insert(tk.END,str(row[0]) + " " + row[1] + " " + str(row[3])+" " + str(row[5]) +"\n")
                   
            
        T = tk.Text(self,height=20, width=40)
        T.pack()            
        

        button2 = tk.Button(self, text="View Your Courses offered",
                            command=lambda: controller.show_frame(PageSeven))
        button2.pack()
        
        button3 = tk.Button(self, text="Create new course",
                            command=lambda: controller.show_frame(PageSix))
        button3.pack()
        
        button4 = tk.Button(self, text="View students enrolled in your courses",
                            command=lambda: controller.show_frame(PageFour))
        button4.pack()


        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Available Courses(Click to enroll)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        bt = []
        
        def onClick(row):
            c.execute('Select * from Logged')
            r = c.fetchone()
            l = (row[0],)
            c.execute('Select * from Studtake where Code=?',l)
            if(len(c.fetchall())):
                tkMessageBox.showinfo("Course already", "You have already enrolled for " +row[1])
            else:
                t = (r[0],r[1],row[0],row[1],row[2],row[3])
                c.execute('INSERT into Studtake VALUES (?,?,?,?,?,?)', t)
                conn.commit()
                tkMessageBox.showinfo("Course reg", "Successfully enrolled for " +row[1])
                
                #bt[row[0]-1].destroy() 
            
        '''
        c.execute('Select * from Logged')
        r = c.fetchone()
        print r[0]
        '''
        def show():
            for row in c.execute('SELECT * FROM Course'):
                b = tk.Button(self, text=str(row[0]) + " " + str(row[1]) + " (" + str(row[3]) + ")",command=lambda row=row: onClick(row))
                b.pack()
                bt.append(b)
                   
                    
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Logout", command=out)
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Back to Previous",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack(side="bottom")
        button3 = tk.Button(self, text="Show courses",
                            command=show)
        button3.pack(side="bottom")
 

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enrolled Students(Click to remove)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        bt = []
        
        def onClick(row):
            #l = (row[0],row[2],)
            c.execute('select count(*) from Studtake where Num=? and Code=?',(row[0],row[2]))
            x  = c.fetchone()
            c.execute('delete from Studtake where Num=? and Code=?',(row[0],row[2]))
            c.execute('select count(*) from Studtake where Num=? and Code=?',(row[0],row[2]))
            r = c.fetchone()
            if(r[0]==x[0]):
                tkMessageBox.showinfo("Course already", "Student has already been removed: " +row[1])
            else:
                conn.commit()
                tkMessageBox.showinfo("Course drop", "Successfully removed " +row[1])
            '''
            #else:
            t = (r[0],r[1],row[0],row[1],row[2],row[3])
            c.execute('INSERT into Studtake VALUES (?,?,?,?,?,?)', t)
            '''
                
            #bt[row[0]-1].destroy()
        
        def show():
            bt = []
            c.execute('SELECT * from Logged')
                  
            r = c.fetchone()
            x = (r[0],)
            for row in c.execute('SELECT * FROM Studtake where Ins=?',x):
                b = tk.Button(self, text=str(row[0]) + " " + str(row[1]) + " (" + str(row[3]) + ")",command=lambda row=row: onClick(row))
                b.pack()
                bt.append(b)   
        
            
                
        
        
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)
 
        button1 = tk.Button(self, text="Logout",
                            command=out)
        button1.pack(side="bottom")
         
        button2 = tk.Button(self, text="Back to Previous",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(side="bottom")
        
        button3 = tk.Button(self, text="View students enrolled",
                            command=show)
        button3.pack(side="bottom")


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Your courses taken(click to drop)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        bt = []
        
        def onClick(row):
            #l = (row[0],row[2],)
            c.execute('select count(*) from Studtake where Num=? and Code=?',(row[0],row[2]))
            x  = c.fetchone()
            c.execute('delete from Studtake where Num=? and Code=?',(row[0],row[2]))
            c.execute('select count(*) from Studtake where Num=? and Code=?',(row[0],row[2]))
            r = c.fetchone()
            if(r[0]==x[0]):
                tkMessageBox.showinfo("Course already", "Course has already been dropped: " +row[3])
            
            else:
                conn.commit()
                tkMessageBox.showinfo("Course drop", "Successfully dropped " +row[3])
            
            '''
            if(len(c.fetchall())):
                tkMessageBox.showinfo("Course already", "You have already enrolled for " +row[1])
            
            #else:
            t = (r[0],r[1],row[0],row[1],row[2],row[3])
            c.execute('INSERT into Studtake VALUES (?,?,?,?,?,?)', t)
            '''
                
            #bt[row[0]-1].destroy()
        
        def show():
            bt = []
            c.execute('SELECT * from Logged')
                  
            r = c.fetchone()
            x = (r[0],)
            for row in c.execute('SELECT * FROM Studtake where Num=?',x):
                b = tk.Button(self, text=str(row[2]) + " " + str(row[3]) + " (" + str(row[5]) + ")",command=lambda row=row: onClick(row))
                b.pack()
                bt.append(b)   
        
            
                
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)
 
        button1 = tk.Button(self, text="Logout",
                            command=out)
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Back to Previous",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack(side="bottom")
        
        button3 = tk.Button(self, text="Show courses",
                            command=show)
        button3.pack(side="bottom")
        



class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create New Course", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Logout",
                            command=out)
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Back to Previous",command=lambda: controller.show_frame(PageTwo))
        button2.pack(side="bottom")
        
        numlb = tk.Label(self, text="Enter Course Code")
        numlb.pack(pady=10,padx=10)
        num = tk.Entry(self)
        num.pack() 
        
        namelb = tk.Label(self, text="Enter Course Name")
        namelb.pack(pady=20,padx=20)
        name = tk.Entry(self)
        name.pack()
        
        credlb = tk.Label(self, text="Enter Course credits")
        credlb.pack(pady=20,padx=20)
        cred = tk.Entry(self)
        cred.pack()
        
        
        
        def create():
            n = num.get()
            s = name.get()
            r = cred.get()
            num.delete(0, 'end')
            name.delete(0, 'end')
            cred.delete(0, 'end')
            
            if n=="" or s=="" or r=="":
                tkMessageBox.showinfo("Course", "Please enter all course details")
            else:    
                
                
                n = int(n)
                r = int(r)
                
                if n < 0 or r < 0 or n!=int(n) or r!=int(r):
                    tkMessageBox.showinfo("Int err", "Please Enter positive integers only")
                else:    
                    c.execute('Select * from Logged')
                    x = c.fetchone()
                    c.execute('Select * from Course where Code=? or CName=?',(n,s))
                    if(len(c.fetchall())):
                        tkMessageBox.showinfo("Course no", "There is already a course with the same name or code")
                    else:
                        t = (n,s,x[0],r)
                        c.execute('INSERT into Course VALUES (?,?,?,?)', t)
                        conn.commit()
                        tkMessageBox.showinfo("Course add", "Course has been successfully added")
                        controller.show_frame(PageTwo)
          
                    
                
                
        button3 = tk.Button(self, text="Create Course", command=create)
        button3.pack(side="bottom")
        
        
        

class PageSeven(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Your Courses offered(click to Withdraw)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        bt = []
        
        def onClick(row):
            #l = (row[0],row[2],)
            c.execute('select count(*) from Studtake where Ins=? and CName=?',(row[2],row[1]))
            x  = c.fetchone()
            
            c.execute('delete from Studtake where Ins=? and CName=?',(row[2],row[1]))
            c.execute('delete from Course where Ins=? and CName=?',(row[2],row[1]))
            c.execute('select count(*) from Studtake where Ins=? and CName=?',(row[2],row[1]))
            r = c.fetchone()
            if(r[0]==x[0]):
                tkMessageBox.showinfo("Course already", "Course has already been withdrawn: " +row[1])
            
            else:
                conn.commit()
                tkMessageBox.showinfo("Course drop", "Successfully withdrew " +row[1])
            
            '''
            if(len(c.fetchall())):
                tkMessageBox.showinfo("Course already", "You have already enrolled for " +row[1])
            
            #else:
            t = (r[0],r[1],row[0],row[1],row[2],row[3])
            c.execute('INSERT into Studtake VALUES (?,?,?,?,?,?)', t)
            '''
                
            #bt[row[0]-1].destroy()
        
        def show():
            bt = []
            c.execute('SELECT * from Logged')
                  
            r = c.fetchone()
            x = (r[0],)
            for row in c.execute('SELECT * FROM Course where Ins=?',x):
                b = tk.Button(self, text=str(row[0]) + " " + str(row[1]) + " (" + str(row[3]) + ")",command=lambda row=row: onClick(row))
                b.pack()
                bt.append(b) 
        
        def out():
            c.execute('DELETE FROM Logged')
            conn.commit()
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Logout",command=out)
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Back to Previous",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(side="bottom")
        
        button3 = tk.Button(self, text="Show courses",command=show)
        button3.pack(side="bottom")
        


app = CMSapp()
app.mainloop()
