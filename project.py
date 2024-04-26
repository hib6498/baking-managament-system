import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector as conn
from PIL import Image, ImageTk

c = conn.connect(
    host = "localhost",
    user = "root",
    password = "c012"
)

query = c.cursor()
query.execute('''create database if not exists bank''')
query.execute("USE bank")
query.execute('''create table if not exists admin(username varchar(30) PRIMARY KEY, password varchar(30) NOT NULL)''')
c.commit()
query.execute('''create table if not exists customer(
                type varchar(10) not null,
                name varchar(30) not null,
                gender varchar(6),
                nationality varchar(30) not null,
                accountno int primary key,
                pin int not null,
                kyc_document varchar(30) not null,
                DOB date not null,
                mobile_no bigint,
                balance float)''')
c.commit()
query.execute('''insert ignore into customer values("Savings", "Sample", "Male", "Indian", 1, 
              1000, "Aadhar", "2004-11-03", 9623110464, 5000.0)''')
c.commit()
query.execute('''insert ignore into admin values ('root', 'root')''')
c.commit()

#check sign in credentials
def check_credentials(username, password, table):
    if table == "admin":
        query.execute(f'''select * from admin where username="{username}"''')
    else:
        query.execute(f'''select accountno, pin from customer where accountno={username}''')
    credentials = query.fetchone()
    if credentials is None:
        return 404
    else:
        if credentials[1] != password:
            return False
        else:
            return True
        
def create_bank_account(*args):
    query.execute(f'''insert into customer(accountno, name, type, DOB, mobile_no, 
                  gender, nationality, kyc_document, pin, balance) values{args}''')
    c.commit()
    
def is_acc_valid(accountno):
    query.execute(f'''select * from customer where accountno={accountno}''')
    if query.fetchone() is None:
        return True
    else:
        return False
    
def create_admin(*args):
    query.execute(f'''insert into admin(username, password) values{args}''')
    c.commit()
    
def delete_admin(username):
    query.execute(f'''delete from admin where username="{username}"''')
    c.commit()
    
def delete_customer(accountno):
    query.execute(f'''delete from customer where accountno="{accountno}"''')
    c.commit()
    
    
def is_admin_valid(username):
    query.execute(f'''select * from admin where username="{username}"''')
    if query.fetchone() is None:
        return True
    else:
        return False
    
def check_leap(year):
    return ((int(year) % 4 == 0) and (int(year) % 100 != 0)) or (int(year) % 400 == 0)

def check_date(date):
    days_in_months = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    days_in_months_in_leap_year = ["31", "29", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

    if date == "":
        return False

    date_elements = date.split("/")
    day = int(date_elements[0])
    month = int(date_elements[1])
    year = int(date_elements[2])
    if (year > 2021 or year < 0) or (month > 12 or month < 1):
        return False
    else:
        if check_leap(year):
            numOfDays = days_in_months_in_leap_year[month - 1]
        else:
            numOfDays = days_in_months[month - 1]
        return int(numOfDays) >= day >= 1
    
def is_valid_mobile(mobile_number):
    return mobile_number.__len__() == 10 and mobile_number.isnumeric()

def update_account(accountno, name, dob, type, gender, mobileno, kyc_document, nationality, balance):
    query.execute(f'''update customer set type="{type}", name="{name}", gender="{gender}", nationality="{nationality}", 
                  kyc_document="{kyc_document}", DOB="{dob}", mobile_no={mobileno}, balance={balance} where accountno={accountno}''')
    c.commit()

def find_name(accountno):
    query.execute(f'''select name from customer where accountno={accountno}''')
    return query.fetchone()[0]

def add_balance(accountno, amount):
    query.execute(f'''select format(balance,2) from customer where accountno={accountno}''')
    initial = float(query.fetchone()[0].replace(',',''))
    changed = initial+amount
    query.execute(f'''update customer set balance={round(changed, 2)} where accountno={accountno}''')
    c.commit()
    
def check_balance(accountno):
    query.execute(f'''select format(balance,2) from customer where accountno={accountno}''')
    return query.fetchone()[0]

def update_pin(accountno, npin):
    query.execute(f'''update customer set pin={npin} where accountno={accountno}''')
    c.commit()
    
def isfloat(amount):
    amount.replace(',','')
    if amount in ['', '.', '.0', '0.']:
        return False
    else:
        return amount.replace('.', '').isnumeric()
    
class Error:
    def __init__(self, Window = None):
        #==============================Widgets=====================================
        global master
        master = Window
        global Frame1
        Frame1 = ttk.Frame(Window)
        global errLabe2
        img = Image.open(r"./images/cross.png").resize((90,90))
        self.tkimage = ImageTk.PhotoImage(img)
        ttk.Label(Frame1,image = self.tkimage).grid(row = 0, column = 0, pady=(20,0))
        self.button1 = ttk.Button(Frame1, text = "Back", bootstyle="danger-outline",
                                  command = self.back)
        
        #===========================Window_config===================================
        Window.geometry("460x240")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.title("Error")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x240+{xpos}+{ypos}')
        
        #===========================Window_config===================================
        Frame1.columnconfigure(0, weight = 1)
        Frame1.rowconfigure((0,1,2), weight = 1)
        
        #==========================Widgets_Placing==================================
        Frame1.grid(row=0, column=0, sticky="nsew")
        self.button1.grid(row=2, column=0, pady=(0,10), sticky="n")
        
    def setMessage(self, Message):
            errLabe2 = ttk.Label(Frame1, text = f"{Message}", font=("Arial", 15), wraplength=400, justify=CENTER,
                                 foreground="white")
            errLabe2.grid(row=1, column=0, pady=(10,5), sticky="n")
            
    def back(self):
        master.withdraw()
        
class Success:
    def __init__(self, Window = None):
        #==============================Widgets=====================================
        global master
        master = Window
        global Frame1
        Frame1 = ttk.Frame(Window)
        global sucLabel
        img = Image.open(r"./images/tick.png").resize((90,90))
        self.tkimage = ImageTk.PhotoImage(img)
        ttk.Label(Frame1,image = self.tkimage).grid(row = 0, column = 0, pady=(20,0))
        self.button1 = ttk.Button(Frame1, text = "Back", bootstyle="success-outline",
                                  command = self.back)
        
        #===========================Window_config===================================
        Window.geometry("460x240")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.title("Error")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x240+{xpos}+{ypos}')
        
        #==========================Widgets_config==================================
        Frame1.columnconfigure(0, weight = 1)
        Frame1.rowconfigure((0,1,2), weight = 1)
        
        #==========================Widgets_Placing==================================
        self.button1.grid(row=2, column=0, pady=(0,10), sticky="n")
        Frame1.grid(row=0, column=0, sticky="nsew")
        
    def setMessage(self, Message):
            sucLabel = ttk.Label(Frame1, text = f"{Message}", foreground = "white", font=("Arial", 15), wraplength=400, 
                                 justify=CENTER)
            sucLabel.grid(row=1, column=0, pady=(10,5), sticky="n")
            
    def back(self):
        master.withdraw()
        
#Welcome window
class main_window():
    def __init__(self, Window = None):
        #==============================Widgets=====================================
        global master1
        master1 = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        img = Image.open(r"./images/illustration.png")
        self.tkimage = ImageTk.PhotoImage(img)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.button1 = ttk.Button(self.Frame2, text = "Admin", bootstyle = "info-outline", command = self.employeeLogin,
                                  style = "info.Outline.TButton", width = 12)
        self.button2 = ttk.Button(self.Frame2, text = "Customer", bootstyle = "info-outline", command =self.customerLogin,
                                  style = "info.Outline.TButton", width = 12)
        self.Label1 = ttk.Label(self.Frame2, text = "Sign in as", foreground = "white", font=("Merriweather", 28, 'bold'))
        ttk.Label(self.Frame1,image = self.tkimage).grid(row = 1, column = 0, sticky = "w")
        
        #===========================Window_config===================================
        Window.geometry("1000x750")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.title("Welcome")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'1000x750+{xpos}+{ypos}')
        
        #==========================Widgets_config===================================
        self.mainframe.columnconfigure((0,1), weight = 1, minsize = 500)
        self.mainframe.rowconfigure(0, weight = 1)
        self.Frame1.rowconfigure((0,1,2), weight = 1)
        self.Frame1.columnconfigure(0, weight = 1)
        self.Frame2.rowconfigure((0,1,2,3), weight = 1)
        self.Frame2.columnconfigure((0,1), weight = 1)
        self.Frame2.pack_propagate(0)
        my_style = ttk.Style()
        my_style.configure("info.Outline.TButton", font = ("Roboto", 12))
        
        #==========================Widgets_Placing==================================
        self.mainframe.grid(row=0, column=0, sticky = "nsew")
        self.Frame1.grid(row = 0, column = 0, columnspan = 1)
        self.Frame2.grid(row=0, column=1, sticky="nsew")
        self.Label1.grid(row=1, column=0, columnspan = 2, pady = (10,30),sticky="s")
        self.button1.grid(row=2, column=0, sticky='ne', padx = 20)
        self.button2.grid(row=2, column=1, sticky='nw', ipadx=30)
    
    def employeeLogin(self):
        adminSignIn(ttk.Toplevel(master1))
        
    def customerLogin(self):
        customerSignIn(ttk.Toplevel(master1))
        
    def custom_withdraw(self):
        master1.withdraw()
        self.master.destroy()

#Admin sign in window
class adminSignIn():
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Frame3 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self. Frame1, text = "Admin Login", foreground = "white", font=("Merriweather", 25, 'bold'))
        self.Label2 = ttk.Label(self.Frame2, text = "Username", foreground = "white", font=("Merriweather", 11))
        self.Label3 = ttk.Label(self.Frame2, text = "Password", foreground = "white", font=("Merriweather", 11))
        self.username = ttk.Entry(self.Frame2, width=25)
        self.password = ttk.Entry(self.Frame2, width=25, show='*')
        self.button1 = ttk.Button(self.Frame3, text = "Back", bootstyle = "info-outline", width=8, style="info.Outline.TButton",
                                  command = self.back)
        self.button2 = ttk.Button(self.Frame3, text = "Login", bootstyle = "info-outline", width=8, style="info.Outline.TButton",
                                  command = lambda: self.login(self.username.get().lower(), self.password.get()))
        
        #========================Window_config======================================
        Window.geometry("440x460")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.title("Admin Login")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'440x460+{xpos}+{ypos}')
        
        #==========================Widgets_config===================================
        self.Frame1.rowconfigure((0,1,2,3), weight = 1)
        self.Frame1.columnconfigure(0, weight=1)
        self.Frame1.rowconfigure(0, weight = 1)
        self.Frame1.columnconfigure((0,1), weight=1)
        my_style = ttk.Style()
        my_style.configure("info.Outline.TButton", font = ("Roboto", 12))
        self.Frame2.pack_propagate(0)
               
        #==========================Widgets_placing==================================
        self.mainframe.pack(fill=BOTH)
        self.Frame1.pack(pady=40)
        self.Frame2.pack()
        self.Frame3.pack(pady=40)
        self.Label1.grid(row=0, column=0)
        self.Label2.grid(row=0, column=0, sticky="w")
        self.Label3.grid(row=2, column=0, sticky="ws", pady=(15,0))
        self.username.grid(row=1, column=0, sticky="w")
        self.password.grid(row=3, column=0, sticky="w")
        self.button1.grid(row=0, column=0, sticky="nw", padx=(0,15), pady=(20,0))
        self.button2.grid(row=0, column=1, sticky="ne", padx=(15,0), pady=(20,0))
        
    def login(self, username, password):
        match check_credentials(username, password, "admin"):  
            case 404:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "Username does not exists")
            case False:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "Username or password incorrect")
            case True:
                print("SUCCESS!!")
                global activeID
                activeID = username
                main_window.custom_withdraw(self)
                admin_menu(ttk.Toplevel(self.master))
    
    def back(self):
        self.master.withdraw()
            
class admin_menu:
    def __init__(self, Window = None):
        #=========================Widgets===========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Frame3 = ttk.Frame(self.mainframe)
        img = Image.open(r"./images/adminlogo.png").resize((200,200))
        self.tkimage = ImageTk.PhotoImage(img)
        self.Label1 = ttk.Label(self.Frame2, image=self.tkimage)
        self.Label2 = ttk.Label(self.Frame2, text = activeID, foreground = "white", font=("Arial", 20, "bold"))
        self.Button1 = ttk.Button(self.Frame3, text = "Create Bank Account", bootstyle = "info", command = self.create_account,
                                  width=30)
        self.Button2 = ttk.Button(self.Frame3, text = "Close Account", bootstyle = "info", command = self.close_account,
                                  width=30)
        self.Button3 = ttk.Button(self.Frame3, text = "Create Admin Account", bootstyle = "info", command = self.create_admin,
                                  width=30)
        self.Button4 = ttk.Button(self.Frame3, text = "Close Admin Account", bootstyle = "info", command = self.close_admin,
                                  width=30)
        self.Button5 = ttk.Button(self.Frame3, text = "Account Summary", bootstyle = "info", command = self.summary,
                                  width=30)
        self.Button6 = ttk.Button(self.Frame1, text = "< Exit", bootstyle = "info-outline", command = self.back)
        
        #========================Window_config======================================
        Window.geometry('800x600')
        Window.title("Admin Menu")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'800x600+{xpos}+{ypos}')
        
        #========================widgets_Placing====================================
        self.mainframe.pack(fill = BOTH)
        self.Frame1.pack(fill=X, pady=(20,0))
        self.Frame2.pack()
        self.Frame3.pack()
        self.Label1.pack(pady=(15,0))
        self.Label2.pack(pady=(0,40))
        self.Button1.grid(row=0, column=0, pady=15, padx=(0,30))
        self.Button2.grid(row=0, column=1, pady=15, padx=(30,0))
        self.Button3.grid(row=1, column=0, pady=15, padx=(0,30))
        self.Button4.grid(row=1, column=1, pady=15, padx=(30,0))
        self.Button5.grid(row=2, column=0, columnspan=2, pady=15)
        self.Button6.pack(anchor=W, padx=20)
        
    def create_account(self):
        createbankaccount(ttk.Toplevel(self.master))
        
    def close_account(self):
        deleteCustomer(ttk.Toplevel(self.master))
        
    def create_admin(self):
        createAdmin(ttk.Toplevel(self.master))
        
    def close_admin(self):
        deleteAdmin(ttk.Toplevel(self.master))
        
    def summary(self):
        accountSummary(ttk.Toplevel(self.master))
        
    def back(self):
        self.master.withdraw()
        main_window(ttk.Toplevel(self.master))
     
class createbankaccount:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Account type", foreground = "white", font=("Arial", 15))
        self.Label2 = ttk.Label(self.Frame1, text = "Name", foreground = "white", font=("Arial", 15))
        self.Label3 = ttk.Label(self.Frame1, text = "Gender", foreground = "white", font=("Arial", 15))
        self.Label4 = ttk.Label(self.Frame1, text = "Nationality", foreground = "white", font=("Arial", 15))
        self.Label5 = ttk.Label(self.Frame1, text = "Account No.", foreground = "white", font=("Arial", 15))
        self.Label6 = ttk.Label(self.Frame1, text = "PIN", foreground = "white", font=("Arial", 15))
        self.Label7 = ttk.Label(self.Frame1, text = "Confirm PIN", foreground = "white", font=("Arial", 15))
        self.Label8 = ttk.Label(self.Frame1, text = "KYC Document", foreground = "white", font=("Arial", 15))
        self.Label9 = ttk.Label(self.Frame1, text = "Date of Birth(DD/MM/YYYY)", foreground = "white", font=("Arial", 15))
        self.Label10 = ttk.Label(self.Frame1, text = "Mobile No.", foreground = "white", font=("Arial", 15))
        self.Label11 = ttk.Label(self.Frame1, text = "Balance", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Entry2 = ttk.Entry(self.Frame1)
        self.Entry3 = ttk.Entry(self.Frame1)
        self.Entry4 = ttk.Entry(self.Frame1)
        self.Entry5 = ttk.Entry(self.Frame1)
        self.Entry6 = ttk.Entry(self.Frame1)
        self.Entry7 = ttk.Entry(self.Frame1)
        self.Entry8 = ttk.Entry(self.Frame1)
        self.Entry9 = ttk.Entry(self.Frame1)
        self.Button1 = ttk.Button(self.Frame1, text = "Create", bootstyle = "info-outline", 
                                  command = lambda: self.create_acc(self.Entry3.get(), self.Entry1.get(), acc_type.get(), 
                                                                    self.Entry7.get(), self.Entry8.get(), gender.get(),
                                                                    self.Entry2.get(), self.Entry6.get(), self.Entry4.get(),
                                                                    self.Entry5.get(), self.Entry9.get()))
        self.Button2 = ttk.Button(self.Frame1, text = "Cancel", bootstyle = "info-outline", command=self.cancel)
        
        global acc_type
        acc_type = ttk.StringVar(value="")
        self.menu1 = ttk.Menubutton(self.Frame1, textvariable=acc_type)
        inside_menu1 = ttk.Menu(self.menu1)
        for i in ['Savings', 'Current']:
            inside_menu1.add_radiobutton(label=i, command=lambda x=i: acc_type.set(x))
        self.menu1['menu'] = inside_menu1
        
        global gender
        gender = ttk.StringVar()
        self.menu2 = ttk.Menubutton(self.Frame1,textvariable=gender)
        inside_menu2 = ttk.Menu(self.menu2)
        for i in ['Male', 'Female', 'Other']:
            inside_menu2.add_radiobutton(label=i, command=lambda x=i: gender.set(x))
        self.menu2['menu'] = inside_menu2
        
        #========================Window_config======================================
        Window.geometry("820x690")
        Window.title("Create Customer Account")
        Window.rowconfigure(0, weight = 1)
        Window.columnconfigure(0, weight=1)
        Window.update_idletasks()
        Window.resizable(False, False)
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'820x690+{xpos}+{ypos}')
        
        #========================Widgets_placing====================================
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.Frame1.pack(anchor=CENTER)
        self.Label1.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=(20,0))
        self.Label2.grid(row=1, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label3.grid(row=2, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label4.grid(row=3, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label5.grid(row=4, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label6.grid(row=5, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label7.grid(row=6, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label8.grid(row=7, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label9.grid(row=8, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label10.grid(row=9, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Label11.grid(row=10, column=0, sticky="e", padx=(0, 10), pady = 10)
        self.Entry1.grid(row=1, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry2.grid(row=3, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry3.grid(row=4, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry4.grid(row=5, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry5.grid(row=6, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry6.grid(row=7, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry7.grid(row=8, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry8.grid(row=9, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Entry9.grid(row=10, column=1, sticky="w", padx = (10,100), pady = 10)
        self.Button1.grid(row=11, column=1, pady=(20,20), sticky="w", padx=(15,0))
        self.Button2.grid(row=11, column=0, pady=(20,20), sticky="e", padx=(0,15))
        self.menu1.grid(row=0, column=1, sticky="w", padx = (10,0), pady=(20,0))
        self.menu2.grid(row=2, column=1, sticky="w", padx = (10,0))
        
        
    def create_acc(self, customer_account_number, name, account_type, date_of_birth, mobile_number, gender, nationality,
                   KYC_document,
                   PIN, confirm_PIN, initial_balance):

        if is_acc_valid(customer_account_number) and customer_account_number.isnumeric():
            if name != "":
                if account_type == "Savings" or account_type == "Current":
                    if check_date(date_of_birth):
                        if is_valid_mobile(mobile_number):
                            if gender == "Male" or gender == "Female" or "Other":
                                if nationality.__len__() != 0:
                                    if KYC_document.__len__() != 0:
                                        if PIN.isnumeric() and PIN.__len__() == 4:
                                            if confirm_PIN == PIN:
                                                if isfloat(initial_balance):
                                                    output_message = "Customer account created successfully!"
                                                    print(output_message)
                                                    self.master.withdraw()
                                                    Success(ttk.Toplevel(self.master))
                                                    Success.setMessage(self, Message = output_message)
                                                else:
                                                    Error(ttk.Toplevel(self.master))
                                                    Error.setMessage(self, Message="Invalid balance!")
                                                    return
                                            else:
                                                Error(ttk.Toplevel(self.master))
                                                Error.setMessage(self, Message="PIN mismatch!")
                                                return
                                        else:
                                            Error(ttk.Toplevel(self.master))
                                            Error.setMessage(self, Message="Invalid PIN!")
                                            return
                                    else:
                                        Error(ttk.Toplevel(self.master))
                                        Error.setMessage(self, Message="Enter KYC document!")
                                        return
                                else:
                                    Error(ttk.Toplevel(self.master))
                                    Error.setMessage(self, Message="Enter Nationality!")
                                    return
                            else:
                                Error(ttk.Toplevel(self.master))
                                Error.setMessage(self, Message="Select gender!")
                                return
                        else:
                            Error(ttk.Toplevel(self.master))
                            Error.setMessage(self, Message="Invalid mobile number!")
                            return
                    else:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, Message="Invalid date!")
                        return
                else:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, Message="Select account type!")
                    return
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, Message="Name can't be empty!")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, Message="Account number is invalid!")
            return
        
        temp_dob = date_of_birth.split('/')
        temp_dob.reverse()
        print(temp_dob)
        create_bank_account(int(customer_account_number), name, account_type, '-'.join(temp_dob), int(mobile_number), gender, 
                            nationality, KYC_document, int(PIN), float(initial_balance))
        
    def cancel(self):
        self.master.withdraw()
        

class deleteCustomer:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Label1 = ttk.Label(self.mainframe, text = "Account No.", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.mainframe)
        self.Button1 = ttk.Button(self.mainframe, text = "Delete", bootstyle = "info-outline", 
                                  command = lambda: self.delete(self.Entry1.get()))
        self.Button2 = ttk.Button(self.mainframe, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #======================Window_config=======================================
        Window.title("Delete Customer Account")
        Window.geometry("460x240")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x240+{xpos}+{ypos}')
        
        #======================Widgets_config======================================
        self.mainframe.columnconfigure((0,1), weight = 1)
        self.mainframe.rowconfigure((0,1,2,3), weight = 1)
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Label1.grid(row=1, column=0, padx = (0,10), sticky="e")
        self.Entry1.grid(row=1, column=1, padx = (10,0), sticky="w")
        self.Button1.grid(row=2, column=1, sticky="w", padx=(45,0))
        self.Button2.grid(row=2, column=0, sticky="e")
        
    def delete(self, accountno):
        if accountno.isnumeric() and accountno != "":
            match is_acc_valid(int(accountno)):
                case True:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, Message="Account no. does not exists")
                    return
                case False:
                    delete_customer(int(accountno))
                    output_message = "Account deleted!"
                    print(output_message)
                    self.master.withdraw()
                    Success(ttk.Toplevel(self.master))
                    Success.setMessage(self, Message = output_message)
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, Message="Account number should only have numbers.")
            return
            
                
    def cancel(self):
        self.master.withdraw()
        
class createAdmin:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Label1 = ttk.Label(self.mainframe, text = "Username", foreground = "white", font=("Arial", 15))
        self.Label2 = ttk.Label(self.mainframe, text = "Password", foreground = "white", font=("Arial", 15))
        self.Label3 = ttk.Label(self.mainframe, text = "Confirm password", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.mainframe)
        self.Entry2 = ttk.Entry(self.mainframe)
        self.Entry3 = ttk.Entry(self.mainframe)
        self.Button1 = ttk.Button(self.mainframe, text = "Create", bootstyle = "info-outline", 
                                  command=lambda: self.create(self.Entry1.get().lower(), self.Entry2.get(), self.Entry3.get()))
        self.Button2 = ttk.Button(self.mainframe, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #========================Window_config====================================
        Window.title("Create Admin Account")
        Window.geometry("550x300")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'550x300+{xpos}+{ypos}')
        
        #========================Widget_config====================================
        self.mainframe.columnconfigure((0,1), weight = 1)
        self.mainframe.rowconfigure((0,1,2,3,4,5), weight = 1)
        
        #========================Widget_placing===================================
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.Label1.grid(row=1, column=0, sticky="e", padx=(0,10))
        self.Label2.grid(row=2, column=0, sticky="e", padx=(0,10))
        self.Label3.grid(row=3, column=0, sticky="e", padx=(0,10))
        self.Entry1.grid(row=1, column=1, sticky="w", padx=(10,0))
        self.Entry2.grid(row=2, column=1, sticky="w", padx=(10,0))
        self.Entry3.grid(row=3, column=1, sticky="w", padx=(10,0))
        self.Button1.grid(row=4, column=1, sticky="w", padx=(20,0))
        self.Button2.grid(row=4, column=0, sticky="e", padx=(0,20))
        
    def create(self, username, password, cpassword):
        if is_admin_valid(username):
            if password != "":
                if cpassword != "":
                    if password == cpassword:
                        output_message = "Account created!"
                        self.master.withdraw()
                        Success(ttk.Toplevel(self.master))
                        Success.setMessage(self, Message = output_message)
                    else:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, Message="Password and Confirm password do not match")
                        return
                else:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, Message="Confirm Password field is empty!")
                    return
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, Message="Password field is empty!")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, Message="Username akready exists!")
            return
        
        create_admin(username, password)
        print("Added to database")
        
        
    def cancel(self):
        self.master.withdraw()
        
class deleteAdmin:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Label1 = ttk.Label(self.mainframe, text = "Username", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.mainframe)
        self.Button1 = ttk.Button(self.mainframe, text = "Delete", bootstyle = "info-outline", 
                                  command = lambda: self.delete(self.Entry1.get().lower()))
        self.Button2 = ttk.Button(self.mainframe, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #======================Window_config=======================================
        Window.title("Delete Admin Account")
        Window.geometry("460x240")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x240+{xpos}+{ypos}')
        
        #======================Widgets_config======================================
        self.mainframe.columnconfigure((0,1), weight = 1)
        self.mainframe.rowconfigure((0,1,2,3), weight = 1)
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Label1.grid(row=1, column=0, padx = (0,10), sticky="e")
        self.Entry1.grid(row=1, column=1, padx = (10,0), sticky="w")
        self.Button1.grid(row=2, column=1, sticky="w", padx=(45,0))
        self.Button2.grid(row=2, column=0, sticky="e")
        
    def delete(self, username):
        if username == activeID:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Operation Denied!")
            return
        if not is_admin_valid(username):
            Success(ttk.Toplevel(self.master))
            Success.setMessage(self, "Admin account closed.")
            delete_admin(username)
            print("admin deleted")
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Username does not exist")
            
    def cancel(self):
        self.master.withdraw()

class accountSummary:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        global master 
        master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Frame3 = ttk.Frame(self.mainframe)
        self.Frame4 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Account No.", foreground = "white", font=("Arial", 15))
        self.Label2 = ttk.Label(self.Frame3, text = "RECORDS", foreground = "white", font=("Roboto", 12, "bold"))
        self.Label3 = ttk.Label(self.Frame3, text = "Account No.", foreground = "white", font=("Arial", 10))
        self.Label4 = ttk.Label(self.Frame3, text = "Name", foreground = "white", font=("Arial", 10))
        self.Label5 = ttk.Label(self.Frame3, text = "Type", foreground = "white", font=("Arial", 10))
        self.Label6 = ttk.Label(self.Frame3, text = "DOB", foreground = "white", font=("Arial", 10))
        self.Label7 = ttk.Label(self.Frame3, text = "Mobile No.", foreground = "white", font=("Arial", 10))
        self.Label8 = ttk.Label(self.Frame3, text = "Gender", foreground = "white", font=("Arial", 10))
        self.Label9 = ttk.Label(self.Frame3, text = "Nationality", foreground = "white", font=("Arial", 10))
        self.Label10 = ttk.Label(self.Frame3, text = "KYC Document", foreground = "white", font=("Arial", 10))
        self.Label11 = ttk.Label(self.Frame3, text = "PIN", foreground = "white", font=("Arial", 10))
        self.Label12 = ttk.Label(self.Frame3, text = "Balance", foreground = "white", font=("Arial", 10))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Entry2 = ttk.Entry(self.Frame3)
        self.Entry3 = ttk.Entry(self.Frame3)
        self.Entry4 = ttk.Entry(self.Frame3)
        self.Entry5 = ttk.Entry(self.Frame3)
        self.Entry6 = ttk.Entry(self.Frame3)
        self.Entry7 = ttk.Entry(self.Frame3)
        self.Entry8 = ttk.Entry(self.Frame3)
        self.Entry9 = ttk.Entry(self.Frame3, show='*')
        
        enabler = ttk.IntVar()
        self.check = ttk.Checkbutton(self.Frame3, text="Confirm updation", command=lambda: self.enable_update(enabler.get()), 
                                     variable=enabler)
        
        global acc_type
        acc_type = ttk.StringVar(value="")
        self.menu1 = ttk.Menubutton(self.Frame3, textvariable=acc_type)
        inside_menu1 = ttk.Menu(self.menu1)
        for i in ['Savings', 'Current']:
            inside_menu1.add_radiobutton(label=i, command=lambda x=i: acc_type.set(x))
        self.menu1['menu'] = inside_menu1
        
        global gender
        gender = ttk.StringVar()
        self.menu2 = ttk.Menubutton(self.Frame3,textvariable=gender)
        inside_menu2 = ttk.Menu(self.menu2)
        for i in ['Male', 'Female', 'Other']:
            inside_menu2.add_radiobutton(label=i, command=lambda x=i: gender.set(x))
        self.menu2['menu'] = inside_menu2
        
        self.Button1 = ttk.Button(self.Frame1, text = "Fetch", bootstyle = "success-outline", 
                                  command = lambda: self.find(self.Entry1.get()))
        self.Button2 = ttk.Button(self.Frame4, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        self.Button3 = ttk.Button(self.Frame3, text = "Update", bootstyle = "success-outline", state=DISABLED,
                                  command=lambda: self.update(self.Entry3.get(), self.Entry2.get(), acc_type.get(), self.Entry4.get(),
                                                              self.Entry5.get(), gender.get(), self.Entry7.get(), self.Entry6.get(),
                                                              self.Entry8.get()))
        column = ("accountno", "name", "type", "DOB", "mobile_no", "gender", "nationality", "kyc_document", "pin", "balance")
        self.scroll = ttk.Scrollbar(self.Frame2, orient="horizontal")
        
        self.table = ttk.Treeview(self.Frame2, columns=column, show="headings", xscrollcommand=self.scroll.set, height=1, 
                                  style="info.Treeview")
        self.table.column("accountno", width=130, anchor=CENTER)
        self.table.column("name", width=130, anchor=CENTER)
        self.table.column("type", width=130, anchor=CENTER)
        self.table.column("DOB", width=130, anchor=CENTER)
        self.table.column("mobile_no", width=130, anchor=CENTER)
        self.table.column("gender", width=130, anchor=CENTER)
        self.table.column("nationality", width=130, anchor=CENTER)
        self.table.column("kyc_document", width=130, anchor=CENTER)
        self.table.column("pin", width=130, anchor=CENTER)
        self.table.column("balance", width=130, anchor=CENTER)
        self.table.heading("#0", text="")
        self.table.heading("accountno", text="Account No.")
        self.table.heading("name", text="Name")
        self.table.heading("type", text="Account Type")
        self.table.heading("DOB", text="DOB")
        self.table.heading("mobile_no", text="Mobile No.")
        self.table.heading("gender", text="Gender")
        self.table.heading("nationality", text="Nationality")
        self.table.heading("kyc_document", text="KYC Doc.")
        self.table.heading("pin", text="PIN")
        self.table.heading("balance", text="Balance")
        
        #======================Window_config=======================================
        Window.title("Account Summary")
        Window.geometry("900x690")
        Window.pack_propagate(0)
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'900x690+{xpos}+{ypos}')
        
        #======================Widgets_config======================================
        self.Frame1.rowconfigure(0, weight=1)
        self.Frame1.columnconfigure((0,1,2), weight=1)
        self.Frame3.rowconfigure(0, weight=1)
        self.Frame3.columnconfigure(0, weight=1)
        self.scroll.config(command=self.table.xview)
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Frame1.pack()
        self.Frame2.pack()
        self.Frame3.pack()
        self.Frame4.pack()
        self.Label1.grid(row=0, column=0, padx = (0,10), sticky="e", pady=20)
        self.Label2.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.Label3.grid(row=1, column=2, padx=10, pady=10)
        self.Label4.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.Label5.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.Label6.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.Label7.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.Label8.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.Label9.grid(row=4, column=2, padx=10, pady=10, sticky="e")
        self.Label10.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.Label11.grid(row=5, column=2, padx=10, pady=10, sticky="e")
        self.Label12.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.Entry1.grid(row=0, column=1, padx = (10,10), sticky="w", pady=20)
        self.Entry2.grid(row=1, column=1, padx=10, pady=10)
        self.Entry3.grid(row=1, column=3, padx=10, pady=10)
        self.Entry4.grid(row=2, column=1, padx=10, pady=10)
        self.Entry5.grid(row=3, column=3, padx=10, pady=10)
        self.Entry6.grid(row=4, column=1, padx=10, pady=10)
        self.Entry7.grid(row=4, column=3, padx=10, pady=10)
        self.Entry8.grid(row=5, column=1, padx=10, pady=10)
        self.Entry9.grid(row=5, column=3, padx=10, pady=10)
        self.menu1.grid(row=2, column=3, padx=10, pady=10)
        self.menu2.grid(row=3, column=1, padx=10, pady=10)
        self.Button1.grid(row=0, column=2, sticky="w", padx=(25,0), pady=20)
        self.Button2.grid(row=0, column=0, pady=(20,0))
        self.check.grid(row=6, column=0, columnspan=4, pady=(15,8))
        self.Button3.grid(row=7, column=0, columnspan=4, pady=(0, 20))
        self.table.pack(pady=(20,0))
        self.scroll.pack(fill="x", pady=(0, 20))
        
    def find(self, accountno):
        if accountno.isnumeric() and accountno != "":
            if not is_acc_valid(accountno):
                query.execute(f'''select accountno, name, type, DOB, mobile_no, 
                              gender, nationality, kyc_document, pin, balance from customer where accountno = {accountno}''')
                self.table.insert('', END, values=query.fetchone())
                self.table.set(self.table.get_children()[0], "pin", '****')
            else:
                Error(ttk.Toplevel(master))
                Error.setMessage(self, Message="Account No. does not exists.")
                return
        else:
            Error(ttk.Toplevel(master))
            Error.setMessage(self, Message="Account number should be only numeric.")
            return
        
        self.select_record()
    
    def enable_update(self, value):
        if value==1:
            self.Button3.config(state=NORMAL)
        else:
            self.Button3.config(state=DISABLED)
            
    def select_record(self):
        self.Entry3.config(state='normal')
        self.Entry9.config(state='normal')
        gender.set('')
        acc_type.set('')
        self.Entry2.delete(0, END)
        self.Entry3.delete(0, END)
        self.Entry4.delete(0, END)
        self.Entry5.delete(0, END)
        self.Entry6.delete(0, END)
        self.Entry7.delete(0, END)
        self.Entry8.delete(0, END)
        self.Entry9.delete(0, END)
        
        values = self.table.item(self.table.get_children()[0], option='values')
        
        gender.set(values[5])
        acc_type.set(values[2])
        self.Entry2.insert(0, values[1])
        self.Entry3.insert(0, values[0])
        self.Entry3.config(state='readonly')
        temp = values[3].split('-')
        temp.reverse()
        self.Entry4.insert(0, '/'.join(temp))
        self.Entry5.insert(0, values[4])
        self.Entry6.insert(0, values[7])
        self.Entry7.insert(0, values[6])
        self.Entry8.insert(0, values[9])
        self.Entry9.insert(0, values[8])
        self.Entry9.config(state='readonly')
                
    def update(self, customer_account_number, name, account_type, date_of_birth, mobile_number, gender, nationality,
                   KYC_document, initial_balance):
        if name != "":
            if account_type == "Savings" or account_type == "Current":
                if check_date(date_of_birth):
                    if is_valid_mobile(mobile_number):
                        if gender.__len__()!=0:
                            if nationality.__len__() != 0:
                                if KYC_document.__len__() != 0:
                                    if isfloat(initial_balance):
                                        output_message = "Customer account updated successfully!"
                                        print(output_message)
                                        master.withdraw()
                                        Success(ttk.Toplevel(master))
                                        Success.setMessage(self, Message = output_message)
                                    else:
                                        Error(ttk.Toplevel(master))
                                        Error.setMessage(self, Message="Invalid balance!")
                                        return
                                else:
                                    Error(ttk.Toplevel(self.master))
                                    Error.setMessage(self, Message="Enter KYC document!")
                                    return
                            else:
                                Error(ttk.Toplevel(self.master))
                                Error.setMessage(self, Message="Enter Nationality!")
                                return
                        else:
                            Error(ttk.Toplevel(self.master))
                            Error.setMessage(self, Message="Select gender!")
                            return
                    else:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, Message="Invalid mobile number!")
                        return
                else:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, Message="Invalid date!")
                    return
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, Message="Select account type!")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, Message="Name can't be empty!")
            return
        
        temp_dob = date_of_birth.split('/')
        temp_dob.reverse()
        print(temp_dob)
        update_account(int(customer_account_number), name, '-'.join(temp_dob), account_type, gender, int(mobile_number), 
                       KYC_document, nationality, float(initial_balance))
        print("Yes")
        
    def cancel(self):
        master.withdraw()
        
#Customer login window       
class customerSignIn():
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Frame3 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self. Frame1, text = "Customer Login", foreground = "white", font=("Merriweather", 25, 'bold'))
        self.Label2 = ttk.Label(self.Frame2, text = "Account No.", foreground = "white", font=("Merriweather", 11))
        self.Label3 = ttk.Label(self.Frame2, text = "PIN", foreground = "white", font=("Merriweather", 11))
        self.accountno = ttk.Entry(self.Frame2, width=25)
        self.pin = ttk.Entry(self.Frame2, width=25, show='*')
        self.button1 = ttk.Button(self.Frame3, text = "Back", bootstyle = "info-outline", width=8, style="info.Outline.TButton",
                                  command = self.back)
        self.button2 = ttk.Button(self.Frame3, text = "Login", bootstyle = "info-outline", width=8, style="info.Outline.TButton",
                                  command = lambda: self.login(self.accountno.get(), self.pin.get()))
        
        #========================Window_config======================================
        Window.geometry("440x460")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.title("Customer Login")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'440x460+{xpos}+{ypos}')
        
        #==========================Widgets_config===================================
        self.Frame1.rowconfigure((0,1,2,3), weight = 1)
        self.Frame1.columnconfigure(0, weight=1)
        self.Frame1.rowconfigure(0, weight = 1)
        self.Frame1.columnconfigure((0,1), weight=1)
        my_style = ttk.Style()
        my_style.configure("info.Outline.TButton", font = ("Roboto", 12))
        self.Frame2.pack_propagate(0)
               
        #==========================Widgets_placing==================================
        self.mainframe.pack(fill=BOTH)
        self.Frame1.pack(pady=40)
        self.Frame2.pack()
        self.Frame3.pack(pady=40)
        self.Label1.grid(row=0, column=0)
        self.Label2.grid(row=0, column=0, sticky="w")
        self.Label3.grid(row=2, column=0, sticky="ws", pady=(15,0))
        self.accountno.grid(row=1, column=0, sticky="w")
        self.pin.grid(row=3, column=0, sticky="w")
        self.button1.grid(row=0, column=0, sticky="nw", padx=(0,15), pady=(20,0))
        self.button2.grid(row=0, column=1, sticky="ne", padx=(15,0), pady=(20,0))
        
    def login(self, accountno, pin):
        if accountno.isnumeric() and accountno != "":
            if pin.isnumeric() and pin != "":
                match check_credentials(int(accountno), int(pin), "customer"):  
                    case 404:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, "Username does not exists")
                        return
                    case False:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, "Username or password incorrect")
                        return
                    case True:
                        global activeCID
                        activeCID = int(accountno)
                        print("SUCCESS!!")
                        main_window.custom_withdraw(self)
                        customer_menu(ttk.Toplevel(self.master))
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "PIN field should have numeric input")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Account No field should have numeric input")
            return
        
    def back(self):
        self.master.withdraw()
        
class customer_menu:
    def __init__(self, Window = None):
        #=========================Widgets===========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Frame3 = ttk.Frame(self.mainframe)
        img = Image.open(r"./images/userlogo.png").resize((200,200))
        self.tkimage = ImageTk.PhotoImage(img)
        self.Label1 = ttk.Label(self.Frame2, image=self.tkimage)
        self.Label2 = ttk.Label(self.Frame2, text = find_name(activeCID), foreground = "white", font=("Arial", 20, "bold"))
        self.Button1 = ttk.Button(self.Frame3, text = "Deposit", bootstyle = "info", command = self.deposit,
                                  width=30)
        self.Button2 = ttk.Button(self.Frame3, text = "Withdraw", bootstyle = "info", command = self.withdraw,
                                  width=30)
        self.Button3 = ttk.Button(self.Frame3, text = "Change PIN", bootstyle = "info", command = self.change_pin,
                                  width=30)
        self.Button4 = ttk.Button(self.Frame3, text = "Close Account", bootstyle = "info", command = self.close_account,
                                  width=30)
        self.Button5 = ttk.Button(self.Frame3, text = "Check Balance", bootstyle = "info", command = self.check_balance,
                                  width=30)
        self.Button6 = ttk.Button(self.Frame1, text = "< Exit", bootstyle = "info-outline", command = self.back)
        
        #========================Window_config======================================
        Window.geometry('800x600')
        Window.title("Customer Menu")
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'800x600+{xpos}+{ypos}')
        
        #========================widgets_Placing====================================
        self.mainframe.pack(fill = BOTH)
        self.Frame1.pack(fill=X, pady=(20,0))
        self.Frame2.pack()
        self.Frame3.pack()
        self.Label1.pack(pady=(15,0))
        self.Label2.pack(pady=(0,40))
        self.Button1.grid(row=0, column=0, pady=15, padx=(0,30))
        self.Button2.grid(row=0, column=1, pady=15, padx=(30,0))
        self.Button3.grid(row=1, column=0, pady=15, padx=(0,30))
        self.Button4.grid(row=1, column=1, pady=15, padx=(30,0))
        self.Button5.grid(row=2, column=0, columnspan=2, pady=15)
        self.Button6.pack(anchor=W, padx=20)
        
    def deposit(self):
        Deposit(ttk.Toplevel(self.master))
        
    def withdraw(self):
        Withdraw(ttk.Toplevel(self.master))
        
    def change_pin(self):
        Change_pin(ttk.Toplevel(self.master))
        
    def close_account(self):
        self.master.withdraw()
        Close_account(ttk.Toplevel(self.master))
        
    def check_balance(self):
        Balance(ttk.Toplevel(self.master))
        
    def back(self):
        self.master.withdraw()
        main_window(ttk.Toplevel(self.master))
    
class Deposit:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Amount", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Button1 = ttk.Button(self.Frame2, text = "Deposit", bootstyle = "info-outline", 
                                  command = lambda: self.addamount(self.Entry1.get()))
        self.Button2 = ttk.Button(self.Frame2, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #======================Window_config=======================================
        Window.title("Deposit")
        Window.geometry("460x220")
        Window.resizable(False, False)
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x220+{xpos}+{ypos}')
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Frame1.pack()
        self.Frame2.pack()
        self.Label1.grid(row=0, column=0, padx = (0,10),pady=(50,0), sticky="e")
        self.Entry1.grid(row=0, column=1, padx = (10,0),pady=(50,0), sticky="w")
        self.Button1.grid(row=0, column=1, sticky="w", padx=(25,0),pady = (40,0))
        self.Button2.grid(row=0, column=0, sticky="e", padx=(0,25),pady = (40,0))
        
    def addamount(self, amount):
        if amount != "" and isfloat(amount):
            if float(amount)>0:
                add_balance(activeCID, float(amount))
                self.master.withdraw()
                Success(ttk.Toplevel(self.master))
                Success.setMessage(self, "Amount added successfully.")
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "Amount entered should be greater than 0.")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Enter a valid amount.")
            return
            
    def cancel(self):
        self.master.withdraw()
        
class Withdraw:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Amount", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Button1 = ttk.Button(self.Frame2, text = "Withdraw", bootstyle = "info-outline", 
                                  command = lambda: self.subamount(self.Entry1.get()))
        self.Button2 = ttk.Button(self.Frame2, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #======================Window_config=======================================
        Window.title("Withdraw")
        Window.geometry("460x220")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x220+{xpos}+{ypos}')
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Frame1.pack()
        self.Frame2.pack()
        self.Label1.grid(row=0, column=0, padx = (0,10),pady=(50,0), sticky="e")
        self.Entry1.grid(row=0, column=1, padx = (10,0),pady=(50,0), sticky="w")
        self.Button1.grid(row=0, column=1, sticky="w", padx=(25,0),pady = (40,0))
        self.Button2.grid(row=0, column=0, sticky="e", padx=(0,25),pady = (40,0))
        
    def subamount(self, amount):
        if amount != "" and isfloat(amount):
            if float(amount)>0:
                if round(float(check_balance(activeCID).replace(',','')), 2)>=round(float(amount), 2):
                    add_balance(activeCID, -float(amount))
                    self.master.withdraw()
                    Success(ttk.Toplevel(self.master))
                    Success.setMessage(self, "Amount withdrawn successfully.")
                else:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, "Amount entered exceeds your current balance.")
                    return
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "Amount entered should be greater than 0.")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Enter a valid amount.")
            return
            
    def cancel(self):
        self.master.withdraw()
    
class Change_pin:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Old PIN", foreground = "white", font=("Arial", 15))
        self.Label2 = ttk.Label(self.Frame1, text = "New PIN", foreground = "white", font=("Arial", 15))
        self.Label3 = ttk.Label(self.Frame1, text = "Confirm PIN", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Entry2 = ttk.Entry(self.Frame1)
        self.Entry3 = ttk.Entry(self.Frame1)
        self.Button1 = ttk.Button(self.Frame2, text = "Update", bootstyle = "info-outline", 
                                  command=lambda: self.pin_update(self.Entry1.get().lower(), self.Entry2.get(), self.Entry3.get()))
        self.Button2 = ttk.Button(self.Frame2, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        
        #========================Window_config====================================
        Window.title("Change PIN")
        Window.geometry("550x300")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'550x300+{xpos}+{ypos}')
        
        #========================Widget_placing===================================
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.Frame1.pack()
        self.Frame2.pack()
        self.Label1.grid(row=1, column=0, sticky="e", padx=(0,10), pady=(40,8))
        self.Label2.grid(row=2, column=0, sticky="e", padx=(0,10), pady=8)
        self.Label3.grid(row=3, column=0, sticky="e", padx=(0,10), pady=(8,40))
        self.Entry1.grid(row=1, column=1, sticky="w", padx=(10,0), pady=(40,8))
        self.Entry2.grid(row=2, column=1, sticky="w", padx=(10,0), pady=8)
        self.Entry3.grid(row=3, column=1, sticky="w", padx=(10,0), pady=(8,40))
        self.Button1.grid(row=0, column=1, sticky="w", padx=(20,0))
        self.Button2.grid(row=0, column=0, sticky="e", padx=(0,20))
        
    def pin_update(self, oldp, newp, cnewp):
        if oldp != "" and oldp.isnumeric():
            if check_credentials(activeCID, int(oldp), "customer") is True:
                if newp != "" and newp.isnumeric():
                    if newp == cnewp:
                        output_message = "Pin updated!"
                        self.master.withdraw()
                        Success(ttk.Toplevel(self.master))
                        Success.setMessage(self, Message = output_message)
                    else:
                        Error(ttk.Toplevel(self.master))
                        Error.setMessage(self, Message="PIN and Confirm PIN do not match!")
                        return
                else:
                    Error(ttk.Toplevel(self.master))
                    Error.setMessage(self, Message="Enter a 4 digit number!")
                    return
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, Message="Old PIN is incorrect!")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, Message="Enter valid PIN!")
            return
        
        update_pin(activeCID, int(newp))
        print("Database Updated")
        
    def cancel(self):
        self.master.withdraw()
        
class Close_account:
    def __init__(self, Window = None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "PIN", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1, show='*')
        self.Button1 = ttk.Button(self.Frame2, text = "Delete", bootstyle = "info-outline", 
                                  command = lambda: self.delete(self.Entry1.get()), state=DISABLED)
        self.Button2 = ttk.Button(self.Frame2, text = "Cancel", bootstyle = "info-outline", command = self.cancel)
        enabler = ttk.IntVar()
        self.check = ttk.Checkbutton(self.Frame2, text="Confirm updation", command=lambda: self.enable_update(enabler.get()), 
                                     variable=enabler)
        
        #======================Window_config=======================================
        Window.title("Deposit")
        Window.geometry("460x165")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'460x165+{xpos}+{ypos}')
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Frame1.pack()
        self.Frame2.pack()
        self.Label1.grid(row=0, column=0, padx = (0,10),pady=(50,0), sticky="e")
        self.Entry1.grid(row=0, column=1, padx = (10,0),pady=(50,0), sticky="w")
        self.check.grid(row=0, column=0, columnspan=2, pady = (30,0))
        self.Button1.grid(row=1, column=1, sticky="w", padx=(25,0), pady=10)
        self.Button2.grid(row=1, column=0, sticky="e", padx=(0,25), pady=10)
        
    def enable_update(self, value):
        if value==1:
            self.Button1.config(state=NORMAL)
        else:
            self.Button1.config(state=DISABLED)
        
    def delete(self, pin):
        if pin != "" and pin.isnumeric():
            if check_credentials(activeCID, int(pin)):
                delete_customer(activeCID)
                Success(ttk.Toplevel(self.master))
                Success.setMessage(self, "Account Closed!")
                self.master.withdraw()
            else:
                Error(ttk.Toplevel(self.master))
                Error.setMessage(self, "Amount entered should be greater than 0.")
                return
        else:
            Error(ttk.Toplevel(self.master))
            Error.setMessage(self, "Enter a valid amount.")
            return
        
        del activeCID
        main_window(ttk.Toplevel(self.master))
            
    def cancel(self):
        self.master.withdraw()
        customer_menu(ttk.Toplevel(self.master))
        
class Balance:
    def __init__(self, Window=None):
        #=========================Widgets==========================================
        self.master = Window
        self.mainframe = ttk.Frame(Window)
        self.Frame1 = ttk.Frame(self.mainframe)
        self.Frame2 = ttk.Frame(self.mainframe)
        self.Label1 = ttk.Label(self.Frame1, text = "Balance:", foreground = "white", font=("Arial", 15))
        self.Entry1 = ttk.Entry(self.Frame1)
        self.Button1 = ttk.Button(self.Frame2, text = "Back", bootstyle = "info-outline", command = self.back)
        
        #======================Window_config=======================================
        Window.title("Balance")
        Window.geometry("440x175")
        Window.columnconfigure(0, weight = 1)
        Window.rowconfigure(0, weight = 1)
        Window.resizable(False, False)
        Window.update_idletasks()
        w_height = Window.winfo_height()
        w_width = Window.winfo_width()
        s_height = Window.winfo_screenheight()
        s_width = Window.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        Window.geometry(f'440x175+{xpos}+{ypos}')
        
        #======================Widgets_config======================================
        self.Entry1.delete(0, END)
        self.Entry1.insert(0, check_balance(activeCID))
        self.Entry1.config(state=DISABLED, foreground="white")
        
        #=====================Widgets_placing======================================
        self.mainframe.grid(row=0, column=0, sticky='nsew')
        self.Frame1.pack()
        self.Frame2.pack()
        self.Label1.grid(row=0, column=0, padx = (0,10),pady=(40,0), sticky="e")
        self.Entry1.grid(row=0, column=1, padx = (10,0),pady=(40,0), sticky="w")
        self.Button1.grid(row=1, column=1, sticky="w", padx=(25,0), pady=(25,0), columnspan=2)
        
    def back(self):
        self.master.withdraw()

root = ttk.Window(themename="darkly", iconphoto=r"./images/bank.png")
main_window(root)
root.mainloop()