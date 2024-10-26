from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector
import os

class login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg = "#fafafa")

        # Images

        self.image = ImageTk.PhotoImage(file = "imgs/login.jpg")
        self.lbl_image = Label(self.root, image = self.image, bd = 0) .place(x = 200, y = 50)

        # Login Frame

        self.employee_email = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        login_frame.place(x = 800, y = 90, width = 350, height = 460)

        title = Label(login_frame, text = "Login", font = ("Elephant", 30, "bold"), bg = "White") .place(x = 0, y = 30, relwidth = 1)

        lbl_user = Label(login_frame, text = "Email", font = ("Andalus", 15), bg = "white", fg = "#767171") .place(x = 50, y = 100)
        txt_user = Entry(login_frame, textvariable = self.employee_email, font = ("times new roman", 15), bg = "#ECECEC") .place(x = 50, y = 140, width = 250)

        lbl_pass = Label(login_frame, text = "Password", font = ("Andalus", 15), bg = "white", fg = "#767171") .place(x = 50, y = 200)
        txt_pass = Entry(login_frame, textvariable = self.password, show = "*", font = ("times new roman", 15), bg = "#ECECEC") .place(x = 50, y = 240, width = 250)

        btn_login = Button(login_frame, command = self.login, text = "Log In", font = ("Arial Rounded MT Bold", 15), bg  = "#00B0F0", activebackground = "#00b0f0", fg = "white", activeforeground = "white", cursor = "hand2") .place(x = 50, y = 300, width = 250, height = 35)

        hr = Label(login_frame, bg = "lightgray") .place(x = 50, y = 370, width = 250, height = 2)
        or_ = Label(login_frame, text = "OR", bg = "white", fg = "lightgray", font = ("times new roman", 15, "bold")) .place(x = 150, y = 355)

        btn_forget = Button(login_frame, text = "Forget Password?", command = self.forget_window, font = ("times new roman", 13), bg = "white", fg = "#00759E", bd = 0, activebackground = "white", activeforeground = "#00759E") .place(x = 100, y = 390)

    # Functions

    def login(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.employee_email.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent = self.root)
            else:    
                cur.execute("select utype from employee where email = %s and password = %s", (self.employee_email.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Email / Password", parent = self.root)
                else:
                    if user[0] == "Admin": 
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Forget Window

    def forget_window(self):
        conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.employee_email.get() == "":
                messagebox.showerror("Error", "Email must be required", parent = self.root)
            else:
                cur.execute("select email from employee where email = %s", (self.employee_email.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid Email, try again", parent = self.root)
                else:

                    # Forget Window

                    self.var_otp = StringVar()
                    self.var_new_password = StringVar()
                    self.var_confirm_password = StringVar()

                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title("Reset Password")
                    self.forget_win.geometry("400x350+500+100")
                    self.forget_win.focus_force()

                    title = Label(self.forget_win, text = "Reset Password", font = ("goudy old style", 15, "bold"), bg = "#3f51b5", fg = "white") .pack(side = TOP, fill = X)
                    lbl_reset = Label(self.forget_win, text = "Enter OTP Sent on registered email", font = ("times new roman", 15)) .place(x = 20, y = 60)
                    txt_reset = Entry(self.forget_win, textvariable = self.var_otp, font = ("times new roman", 15), bg = "lightyellow") .place(x = 20, y = 100, width = 250, height = 30)
                    self.btn_reset = Button(self.forget_win, text = "Submit", font = ("times new roman", 15), bg = "lightblue")
                    self.btn_reset.place(x = 280, y = 100, width = 100, height = 30)

                    lbl_new_password = Label(self.forget_win, text = "New Password", font = ("times new roman", 15)) .place(x = 20, y = 160)
                    txt_new_password = Entry(self.forget_win, textvariable = self.var_new_password, font = ("times new roman", 15), bg = "lightyellow") .place(x = 20, y = 190, width = 250, height = 30)

                    lbl_confirm_password = Label(self.forget_win, text = "Confirm Password", font = ("times new roman", 15)) .place(x = 20, y = 225)
                    txt_confirm_password = Entry(self.forget_win, textvariable = self.var_confirm_password, font = ("times new roman", 15), bg = "lightyellow") .place(x = 20, y = 255, width = 250, height = 30)

                    self.btn_update = Button(self.forget_win, text = "Update", state = DISABLED, font = ("times new roman", 15), bg = "lightblue")
                    self.btn_update.place(x = 150, y = 300, width = 100, height = 30)
               
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

root = Tk()
obj = login(root)
root.mainloop()