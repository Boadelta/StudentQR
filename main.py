import pymysql
import qrcode
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import threading
import sendM
import upload
from PIL import Image, ImageTk
import re
import hashlib
from dotenv import load_dotenv
import os
from pymysql.err import MySQLError as Error

load_dotenv()
DB_HOST= os.getenv("DB_HOST")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DEFAULT_FONT = ("Arial", 11)
HEADER_FONT = ("Arial", 11, "bold")

class StudentRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Registration Form")
        self.root.geometry("500x500")
        self.root.geometry("300x200")
        self.root.config(bg="#eaffea")
        self.root.resizable(False, False)
        self.log_frame = Frame(bg="#eaffea")
        self.reg_frame = Frame(bg="#eaffea")
        self.verify_frame = Frame(bg="#eaffea")

        self.entries = []
        self.filename = ""
        

        self.build_login_page()

    def build_login_page(self):
        self.root.geometry("300x200")
        self.log_frame= Frame(bg="#eaffea")
        Label(self.log_frame, text="Username: ", bg="#eaffea", fg="#0a2342", font = HEADER_FONT).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = Entry(self.log_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())

        Label(self.log_frame, text="Password: ", bg="#eaffea", fg="#0a2342",font = HEADER_FONT).grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(self.log_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.logBtn = Button(self.log_frame, text="Login", command=self.login, bg="#ff4b5c", bd=4, relief=RAISED, font=HEADER_FONT)
        self.logBtn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.log_frame.pack(padx=10, pady=10)

    def login(self):
    
        username = self.username_entry.get()
        password = self.password_entry.get()
        

        try:
            self.logBtn.config(state=DISABLED)
            conn = pymysql.connect(host=DB_HOST, user=DB_NAME, password=DB_PASSWORD, database=DB_NAME, port=3306)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.log_frame.pack_forget()
                self.log_frame.destroy()
                self.root.geometry("500x500")
                self.build_menu()
                self.build_registration_page()
            else:
                messagebox.showinfo("Login Failed", "Incorrect username or password. Please try again.")
                self.logBtn.config(state=NORMAL)

        except pymysql.err.MySQLError:
            messagebox.showinfo("Connection Error", "Unable to connect to the database. Please check your internet connection or try again later.")
            self.logBtn.config(state=NORMAL)

            
    def onReturn(self):
        self.verify_frame.pack_forget()
        self.verify_frame.destroy()
        self.reg_frame.pack(padx=10, pady=10)
        

    def build_menu(self):
        mymenu = Menu(self.root)
        mymenu.config(bg= "#2e8b57")
        mymenu.add_command(label="Log out", command=self.logout, font=HEADER_FONT)
        mymenu.add_command(label="Quit!", command=self.root.quit, font=HEADER_FONT)
        self.root.config(menu=mymenu)

    def build_registration_page(self):
        self.reg_frame = Frame(bg="#eaffea")
        labels = ["SURNAME", "FIRSTNAME", "SECONDNAME", "MAT-NUMBER", "EMAIL"]
        self.entries = [Entry(self.reg_frame) for _ in labels]
        for i, label in enumerate(labels):
            Label(self.reg_frame, text=label, bg="#eaffea", fg="#0a2342", font = HEADER_FONT).grid(row=i+1, column=0, pady=5, sticky="w")
            self.entries[i].grid(row=i+1, column=1, ipadx=80, pady=5, sticky="w")
            if i < len(labels)-1:
                self.entries[i].bind("<Return>", lambda e, nf=self.entries[i+1]: nf.focus_set())

        self.bloodOpt = ttk.Combobox(self.reg_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=40)
        self.bloodOpt.set("Select a blood group")
        self.bloodOpt.grid(row=6, column=1, pady=5, sticky="w")
        Label(self.reg_frame, text="BLOOD GROUP", bg="#eaffea", fg="#0a2342",font = HEADER_FONT).grid(row=6, column=0, pady=5, sticky="w")

        self.gOpt = ttk.Combobox(self.reg_frame, values=["Male", "Female"], width=40)
        self.gOpt.set("Select a gender")
        self.gOpt.grid(row=7, column=1, pady=5, sticky="w")
        Label(self.reg_frame, text="GENDER", bg="#eaffea", fg="#0a2342", font = HEADER_FONT).grid(row=7, column=0, pady=5, sticky="w")

        self.lOpt = ttk.Combobox(self.reg_frame, values=["ND", "HND"], width=40)
        self.lOpt.set("Select a level")
        self.lOpt.grid(row=8, column=1, pady=5, sticky="w")
        Label(self.reg_frame, text="LEVEL", bg="#eaffea", fg="#0a2342",font = HEADER_FONT).grid(row=8, column=0, pady=5, sticky="w")

        programme = ["Electrical & Electronic Engineering Technology", "Petroleum Engineering Technology", "Petroleum and Natural Gas Processing Technology", "Mechanical Engineering Technology", "Welding Engineering & Offshore Technology", "Computer Science and Information Technology", "Petroleum Marketing & Business Studies", "Science Laboratory Technology", "Industrial Safety & Environmental Technology", "Computer engineering Technology"]
        self.progOpt = ttk.Combobox(self.reg_frame, values=programme, width=40)
        self.progOpt.set("Select a programme")
        self.progOpt.grid(row=9, column=1, pady=5, sticky="w")
        Label(self.reg_frame, text="PROGRAMME", bg="#eaffea", fg="#0a2342",font = HEADER_FONT).grid(row=9, column=0, pady=5, sticky="w")

        department = ["EED", "PET", "PNGPD", "MET", "WEOT", "CSIT", "PMBS", "SLT", "ISET", "CETD"]
        self.depOpt = ttk.Combobox(self.reg_frame, values=department, width=40)
        self.depOpt.set("Select a Department")
        self.depOpt.grid(row=10, column=1, pady=5, sticky="w")
        Label(self.reg_frame, text="DEPARTMENT", bg="#eaffea", fg="#0a2342",font = HEADER_FONT).grid(row=10, column=0, pady=5, sticky="w")

        Button(self.reg_frame, text="Attach Student Image", fg="#0a2342", bg="#e0a800", command=self.browse_file, bd=4, relief=RAISED,font = HEADER_FONT).grid(row=11, column=1, pady=10, sticky="s")

        self.next_btn = Button(self.reg_frame, text="NEXT", fg="#0a2342", bg="#ff4b5c", command=self.next, bd=4, relief=RAISED,font = HEADER_FONT)
        self.next_btn.grid(row=12, column=1, columnspan=1, pady=10)

        self.reg_frame.pack(padx=10, pady=10)
    def build_verify_frame(self):
        self.verify_frame=Frame(bg="#eaffea")
        self.tk_image = self.toFit(self.studImage)
        Label(self.verify_frame, image = self.tk_image).grid(row=0, column=0, sticky = 'w', padx =10, pady=5)
        Label(self.verify_frame, text = "SURNAME: "+ self.entries[0].get(), bg="#eaffea", font=DEFAULT_FONT).grid(row =1, column = 0, sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "FIRSTNAME: "+self.entries[1].get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=2, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "SECONDNAME: "+self.entries[2].get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=3, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "MAT-NUMBER: "+ self.entries[3].get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=4, column = 0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "EMAIL: "+ self.entries[4].get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=5, column =0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "BLOOD GROUP: "+self.bloodOpt.get(), bg="#eaffea", font=DEFAULT_FONT).grid(row= 6, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "GENDER: "+self.gOpt.get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=7, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "LEVEL: " +self.lOpt.get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=8, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "PROGRAMME: "+self.progOpt.get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=9, column=0,sticky='w', padx =10, pady=5)
        Label(self.verify_frame, text = "DEPARTMENT: "+self.depOpt.get(), bg="#eaffea", font=DEFAULT_FONT).grid(row=10, column=0,sticky='w', padx =10, pady=5)
        self.butn_frame = Frame(self.verify_frame, bg = "#eaffea")
        self.submit_btn = Button(self.butn_frame, text="SUBMIT", fg="#0a2342", bg="#ff4b5c", command=self.submit_data, bd=4, relief=RAISED, font=HEADER_FONT)
        self.submit_btn.grid(row=0,column=1, padx =10)
        goBack = Button(self.butn_frame, text = "RETURN",command = self.onReturn, fg="#0a2342", bg="#ff4b5c", bd=4, relief=RAISED, font=HEADER_FONT)
        goBack.grid(row=0,column =0, padx = 101)
        self.verify_frame.pack(padx=10, pady=10, side = LEFT)
        self.butn_frame.grid(row=11, column=0)
        

    def browse_file(self):
        self.filename = filedialog.askopenfilename(title="Select a File", filetypes=[("Image files", "*.jpg*"), ("all files", "*.*")])
        if not self.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            messagebox.showinfo("Invalid File", "Only image files are allowed.")
        else:
            self.studImage = Image.open(self.filename)

            messagebox.showinfo("Success", "Image successfully attached")

    def submit_data(self):
        self.progress_bar = ttk.Progressbar(self.butn_frame, mode='indeterminate', length=200)
        self.progress_bar.grid(row=13, column=1, pady=5)
        self.submit_btn.config(state='disabled')
        threading.Thread(target=self.insert_data).start()
        
    def next(self):
        if self.complete():
            self.build_verify_frame()
            self.reg_frame.pack_forget()
           
        else:
            messagebox.showinfo("Error", "Fill all fields. Second name is optional")
        
    def complete(self):
        
        if self.entries[0].get()!="" and self.entries[1].get()!="" and self.entries[3].get()!='' and self.entries[4].get()!='' and self.bloodOpt.get()!="Select a blood group" and self.gOpt.get()!="Select a gender" and self.lOpt.get()!="Select a level" and self.progOpt.get()!="Select a programme" and self.depOpt.get()!="Select a department" and self.filename!="":
            return True
            
    def insert_data(self):
        self.progress_bar.start()
        try:
            qr = self.create_qr()
            img = upload.uploadImage(self.filename, self.structMat())
            qrImg = upload.uploadImage(qr, self.structMat()+"QRCODE")
            conn = pymysql.connect(host=DB_HOST, user=DB_NAME, password=DB_PASSWORD, database=DB_NAME, port=3306)
            cursor = conn.cursor()
            sql = ("INSERT INTO student(SurName, FirstName, SecondName, MatNumber, Email, BloodGroup, Gender, Level, Programme, Department, StudImage, StudQr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = self.create_data_tuple() +(img, qrImg)
            cursor.execute(sql, data)
            self.send_qr(qr)
            conn.commit()
            self.clear_fields()
            messagebox.showinfo("Success", "Information successfully uploaded. Click \"RETURN\" to continue regstraton.")
        except Error as e:
            err_code = e.args[0] if len(e.args) > 0 else None

            # Connection-related errors (2003, 2005, 2013, 2006)
            if err_code in (2003, 2005, 2013, 2006):
                messagebox.showinfo("Error", "No internet Connection")

                # Duplicate entry error (1062)
            elif err_code == 1062:
                messagebox.showinfo("Error", "This student already exists in the database")

            else:
                messagebox.showinfo("Error", f"Database Error occurred. ({err_code})")

        except ConnectionError as e:
            messagebox.showinfo("Error", str(e))

        finally:
            if self.progress_bar.winfo_exists():
                self.progress_bar.stop()
                self.progress_bar.destroy()
                self.submit_btn.config(state='normal')
           
       
    def create_qr(self):
        mat_no = self.entries[3].get()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(mat_no)
        qr.make(fit=True)
        img = qr.make_image(fill_color='red', back_color='white')
        file_path = self.structMat()+"qr.png"
        img.save(file_path)
        return file_path
        
    def send_qr(self, file_path):
        try:
            sendM.sendMail(self.entries[4].get(), self.entries[0].get(), file_path)
        except Exception as e:
            raise ConnectionError("Failed to send email. Check Internet Connection and make sure you entered a valid email")

    def clear_fields(self):
        for f in self.entries:
            f.delete(0, END)
        self.bloodOpt.set("Select a blood group")
        self.gOpt.set("Select a gender")
        self.lOpt.set("Select a level")
        self.progOpt.set("Select a programme")
        self.depOpt.set("Select a Department")

    def create_data_tuple(self):
        values = [f.get().lower() for f in self.entries]
        values += [self.bloodOpt.get(), self.gOpt.get(), self.lOpt.get(), self.progOpt.get(), self.depOpt.get()]
        return tuple(values)
        
    def structMat(self):
        x = re.findall("[a-zA-Z0-9]", self.entries[3].get())
        newMat = ''.join(x)
        return newMat
        
    def toFit(self, img):
        if img.width>= img.height:
            scaleFactor = 100 / img.width
            newWidth = 100
            newHeight = int(img.height * scaleFactor)
        else:
            scaleFactor = 100/img.height
            newHeight = 100
            newWidth = int(img.width * scaleFactor)
        resized = img.resize((newWidth, newHeight))
        tk_image = ImageTk.PhotoImage(resized)
        return tk_image
    
        
    def logout(self):
        # Destroy all current frames
        if hasattr(self, 'reg_frame'):
            self.reg_frame.pack_forget()
            self.reg_frame.destroy()
        if hasattr(self, 'verify_frame'):
            self.verify_frame.pack_forget()
            self.verify_frame.destroy()
    
        # Clear any entries (optional)
        self.entries = []
        self.filename = ""

        # Destroy menu
        self.root.config(menu=Menu(self.root))  # Reset menu bar

        # Rebuild login page
        self.build_login_page()


        
        


if __name__ == "__main__":
    root = Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()


