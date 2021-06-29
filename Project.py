# ====================================== PYTHON PROJECT ==========================================
# Billing System and Income Tracker


from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time
from tkcalendar import DateEntry
from PIL import ImageTk, Image
import sqlite3

con = sqlite3.connect("Bill_mangement.db")
con.commit()
con.close()


# Hotel Billing Application
def mainfunction():
    menu_category = ["Tea & Coffee", "Beverages", "Fast Food", "Starters", "Main Course", "Dessert"]

    menu_category_dict = {"Tea & Coffee": "1 Tea & Coffee.txt", "Beverages": "2 Beverages.txt",
                          "Fast Food": "3 Fast Food.txt",
                          "Starters": "4 Starters.txt", "Main Course": "5 Main Course.txt",
                          "Dessert": "6 Dessert.txt"}

    order_dict = {}
    for i in menu_category:
        order_dict[i] = {}

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def load_menu():
        menuCategory.set("")
        menu_tabel.delete(*menu_tabel.get_children())
        menu_file_list = os.listdir("Menu")
        for file in menu_file_list:
            f = open("Menu\\" + file, "r")
            category = ""
            while True:
                line = f.readline()
                if (line == ""):
                    menu_tabel.insert('', END, values=["", "", ""])
                    break
                elif (line == "\n"):
                    continue
                elif (line[0] == '#'):
                    category = line[1:-1]
                    name = "\t\t" + line[:-1]
                    price = ""
                elif (line[0] == '*'):
                    name = line[:-1]
                    price = ""
                else:
                    name = line[:line.rfind(" ")]
                    price = line[line.rfind(" ") + 1:-3]

                menu_tabel.insert('', END, values=[name, price, category])

    def load_order():
        order_tabel.delete(*order_tabel.get_children())
        for category in order_dict.keys():
            if order_dict[category]:
                for lis in order_dict[category].values():
                    order_tabel.insert('', END, values=lis)
        update_total_price()

    def add_button_operation():
        name = itemName.get()
        rate = itemRate.get()
        category = itemCategory.get()
        quantity = itemQuantity.get()

        if name in order_dict[category].keys():
            tmsg.showinfo("Error", "Item already exist in your order")
            return
        if not quantity.isdigit():
            tmsg.showinfo("Error", "Please Enter Valid Quantity")
            return
        lis = [name, rate, quantity, str(int(rate) * int(quantity)), category]
        order_dict[category][name] = lis
        load_order()

    def load_item_from_menu(event):
        cursor_row = menu_tabel.focus()
        contents = menu_tabel.item(cursor_row)
        row = contents["values"]

        itemName.set(row[0])
        itemRate.set(row[1])
        itemCategory.set(row[2])
        itemQuantity.set("1")

    def load_item_from_order(event):
        cursor_row = order_tabel.focus()
        contents = order_tabel.item(cursor_row)
        row = contents["values"]

        itemName.set(row[0])
        itemRate.set(row[1])
        itemQuantity.set(row[2])
        itemCategory.set(row[4])

    def show_button_operation():
        category = menuCategory.get()
        if category not in menu_category:
            tmsg.showinfo("Error", "Please select valid Choice")
        else:
            menu_tabel.delete(*menu_tabel.get_children())
            f = open("Menu\\" + menu_category_dict[category], "r")
            while True:
                line = f.readline()
                if (line == ""):
                    break
                if (line[0] == '#' or line == "\n"):
                    continue
                if (line[0] == '*'):
                    name = "\t" + line[:-1]
                    menu_tabel.insert('', END, values=[name, "", ""])
                else:
                    name = line[:line.rfind(" ")]
                    price = line[line.rfind(" ") + 1:-3]
                    menu_tabel.insert('', END, values=[name, price, category])

    def clear_button_operation():
        itemName.set("")
        itemRate.set("")
        itemQuantity.set("")
        itemCategory.set("")

    def cancel_button_operation():
        names = []
        for i in menu_category:
            names.extend(list(order_dict[i].keys()))
        if len(names) == 0:
            tmsg.showinfo("Error", "Your order list is Empty")
            return
        ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
        if ans == "no":
            return
        order_tabel.delete(*order_tabel.get_children())
        customerName.set("")
        customerContact.set("")
        customer_name_entry.focus()

        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()

    def update_button_operation():
        name = itemName.get()
        rate = itemRate.get()
        category = itemCategory.get()
        quantity = itemQuantity.get()

        if category == "":
            return
        if name not in order_dict[category].keys():
            tmsg.showinfo("Error", "Item is not in your order list")
            return
        if order_dict[category][name][2] == quantity:
            tmsg.showinfo("Error", "No changes in Quantity")
            return
        order_dict[category][name][2] = quantity
        order_dict[category][name][3] = str(int(rate) * int(quantity))
        load_order()

    def remove_button_operation():
        name = itemName.get()
        category = itemCategory.get()

        if category == "":
            return
        if name not in order_dict[category].keys():
            tmsg.showinfo("Error", "Item is not in your order list")
            return
        del order_dict[category][name]
        load_order()

    def update_total_price():
        price = 0
        for i in menu_category:
            for j in order_dict[i].keys():
                price += int(order_dict[i][j][3])
        if price == 0:
            totalPrice.set("")
        else:
            totalPrice.set("Rs " + str(price) + "  /-")

    def bill_button_operation():
        customer_name = customerName.get()
        customer_contact = customerContact.get()
        names = []
        for i in menu_category:
            names.extend(list(order_dict[i].keys()))
        if len(names) == 0:
            tmsg.showinfo("Error", "Your order list is Empty")
            return
        if customer_name == "" or customer_contact == "":
            tmsg.showinfo("Error", "Customer Details Required")
            return
        if not customerContact.get().isdigit():
            tmsg.showinfo("Error", "Invalid Customer Contact")
            return
        ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")

        if ans == "yes":
            bill = Toplevel()
            bill.title("Bill")
            bill.geometry("670x500+300+100")
            bill_text_area = Text(bill, font=("arial", 12))

            st = "-" * 61 + "BILL" + "-" * 61 + "\nDate:- "

            t = time.localtime(time.time())
            week_day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday",
                             6: "Sunday"}
            st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
            st += " " * 10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

            st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\n"
            st += "-" * 130 + "\n" + " " * 4 + "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
            st += "-" * 130 + "\n"

            for i in menu_category:
                for j in order_dict[i].keys():
                    lis = order_dict[i][j]
                    name = lis[0]
                    rate = lis[1]
                    quantity = lis[2]
                    price = lis[3]
                    st += name + "\t\t\t\t\t" + rate + "\t      " + quantity + "\t\t  " + price + "\n\n"
                    import sqlite3
                    t = time.localtime(time.time())
                    st1 = f"{t.tm_mon}/{t.tm_mday}/"
                    st1 = st1 + "21"
                    st2 = f"{t.tm_hour} : {t.tm_min} : {t.tm_sec}"

                    con = sqlite3.connect("Bill_mangement.db")
                    query = "insert into customer_table values('" + customer_contact + "', '" + customer_name + "', '" + st1 + "','" + st2 + "','" + name + "','" + rate + "','" + quantity + "','" + price + "')"
                    con.execute(query)
                    con.commit()
                    con.close()
            st += "-" * 130

            st += f"\n\t\t\t\t\t\tTotal price :\t\t{totalPrice.get()}\n"
            st += "-" * 130

            bill_text_area.insert(1.0, st)
            bill_text_area['state'] = DISABLED

            folder = f"{t.tm_mday},{t.tm_mon},{t.tm_year}"
            if not os.path.exists(f"Bill Records\\{folder}"):
                os.makedirs(f"Bill Records\\{folder}")
            file = open(f"Bill Records\\{folder}\\{customer_name + customer_contact}.txt", "w")
            file.write(st)
            file.close()

            order_tabel.delete(*order_tabel.get_children())
            for i in menu_category:
                order_dict[i] = {}
            clear_button_operation()
            update_total_price()
            customerName.set("")
            customerContact.set("")

            bill_text_area.pack(expand=True, fill=BOTH)
            bill.focus_set()

    def backInBilling():
        basefunction()

    # GUI
    root = Toplevel()
    root.geometry("1x1+9000+3000")
    w, h = base.winfo_screenwidth(), base.winfo_screenheight()
    base.geometry("%dx%d+0+0" % (w, h))
    img = Image.open("icon/bckg.png")
    a = img.resize((1400, 690))
    a.save("icon/bckg.png")
    b = Image.open("icon/bckg.png")
    c = ImageTk.PhotoImage(b)
    d = Label(image=c)
    d.image = c
    d.place(x=0, y=0)
    base.title("Hotel billing Application")

    style_button = ttk.Style()
    style_button.configure("TButton", font=("arial", 10, "bold"),
                           background="lightgreen")
    img4 = PhotoImage(file="icon/bck3.png")
    img2 = PhotoImage(file="icon/img2.png")

    customer_frame = Label(base, text="Customer Details", font=("times new roman", 13, "bold"), bg="sienna4",
                           relief=GROOVE, fg="white")
    customer_frame.place(x=80, y=25, width=500, height=30)

    customer_name_label = Label(base, text="Name:",
                                font=("arial", 14, "bold"), bg="sienna4", fg="white", compound=TOP)
    customer_name_label.place(x=110, y=100, height=30, width=80)

    customerName = StringVar()
    customerName.set("")
    customer_name_entry = Entry(base, width=30, font="arial 14",
                                textvariable=customerName)
    customer_name_entry.place(x=200, y=100)

    customer_contact_label = Label(base, text="Contact:",
                                   font=("arial", 14, "bold"), bg="sienna4", fg="white")
    customer_contact_label.place(x=105, y=180, height=30, width=85)

    customerContact = StringVar()
    customerContact.set("")
    customer_contact_entry = Entry(base, width=30, font="arial 14",
                                   textvariable=customerContact)
    customer_contact_entry.place(x=200, y=180)

    menu_frame = Frame(base, bd=2, bg="sienna4", relief=GROOVE)
    menu_frame.place(x=660, y=10, height=500, width=680)

    menu_label = Label(menu_frame, text="Menu",
                       font=("times new roman", 20, "bold"), bg="sienna4", fg="white", pady=0)

    menu_label.pack(side=TOP, fill="x")

    menu_category_frame = Frame(menu_frame, bg="sienna4")

    menu_category_frame.pack(fill="x")

    combo_lable = Label(menu_category_frame, text="Select Type",
                        font=("arial", 12, "bold"), bg="sienna4", fg="white")

    combo_lable.grid(row=0, column=0, padx=10)

    menuCategory = StringVar()
    combo_menu = ttk.Combobox(menu_category_frame, values=menu_category,
                              textvariable=menuCategory)
    combo_menu.grid(row=0, column=1, padx=30)

    show_button = Button(menu_category_frame, text="Show", width=10,
                         command=show_button_operation, bg="bisque", bd=1)
    show_button.grid(row=0, column=2, padx=60)

    show_all_button = Button(menu_category_frame, text="Show All",
                             width=10, command=load_menu, bg="bisque", bd=1)
    show_all_button.grid(row=0, column=3)

    ############################# Menu Tabel ##########################################
    menu_tabel_frame = Frame(menu_frame)
    menu_tabel_frame.pack(fill=BOTH, expand=1)

    scrollbar_menu_x = Scrollbar(menu_tabel_frame, orient=HORIZONTAL)
    scrollbar_menu_y = Scrollbar(menu_tabel_frame, orient=VERTICAL)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("arial", 13, "bold"))
    style.configure("Treeview", font=("arial", 12), rowheight=25)

    menu_tabel = ttk.Treeview(menu_tabel_frame, style="Treeview",
                              columns=("name", "price", "category"), xscrollcommand=scrollbar_menu_x.set,
                              yscrollcommand=scrollbar_menu_y.set)

    menu_tabel.heading("name", text="Name")
    menu_tabel.heading("price", text="Price")
    menu_tabel["displaycolumns"] = ("name", "price")
    menu_tabel["show"] = "headings"
    menu_tabel.column("price", width=50, anchor='center')

    scrollbar_menu_x.pack(side=BOTTOM, fill=X)
    scrollbar_menu_y.pack(side=RIGHT, fill=Y)

    scrollbar_menu_x.configure(command=menu_tabel.xview)
    scrollbar_menu_y.configure(command=menu_tabel.yview)

    menu_tabel.pack(fill=BOTH, expand=1)

    load_menu()
    menu_tabel.bind("<ButtonRelease-1>", load_item_from_menu)

    item_frame = Frame(base, bg="lightSalmon4", relief=GROOVE)
    item_frame.place(x=700, y=518, height=165, width=630)
    canvas = Label(item_frame, image=img2)
    canvas.configure(width=630, height=165)
    canvas.pack()

    item_title_label = Label(item_frame, text="Item",
                             font=("times new roman", 20, "bold"), bg="sienna4", fg="red")
    item_title_label.place(x=800, y=600)

    item_name_label = Label(item_frame, text="Name:",
                            font=("arial", 12, "bold"), bg="sienna4", fg="white")
    item_name_label.place(x=20, y=30)

    itemCategory = StringVar()
    itemCategory.set("")

    itemName = StringVar()
    itemName.set("")
    item_name = Entry(item_frame, font="arial 12", textvariable=itemName, state=DISABLED, width=25)
    item_name.place(x=80, y=30)

    item_rate_label = Label(item_frame, text="Price:",
                            font=("arial", 12, "bold"), bg="sienna4", fg="white")
    item_rate_label.place(x=390, y=30)

    itemRate = StringVar()
    itemRate.set("")
    item_rate = Entry(item_frame, font="arial 12", textvariable=itemRate, state=DISABLED, width=10)
    item_rate.place(x=450, y=30)

    item_quantity_label = Label(item_frame, text="Quantity:",
                                font=("arial", 12, "bold"), bg="sienna4", fg="white")
    item_quantity_label.place(x=205, y=75)

    itemQuantity = StringVar()
    itemQuantity.set("")
    item_quantity = Entry(item_frame, font="arial 12", textvariable=itemQuantity, width=15)
    item_quantity.place(x=290, y=75)

    add_button = Button(item_frame, text="Add Item"
                        , command=add_button_operation, bg="bisque", bd=5)
    add_button.place(x=70, y=120, height=30)

    remove_button = Button(item_frame, text="Remove Item"
                           , command=remove_button_operation, bg="bisque", bd=5)
    remove_button.place(x=200, y=120, height=30)

    update_button = Button(item_frame, text="Update Quantity"
                           , command=update_button_operation, bg="bisque", bd=5)
    update_button.place(x=340, y=120, height=30)

    clear_button = Button(item_frame, text="Clear",
                          width=8, command=clear_button_operation, bg="bisque", bd=5)
    clear_button.place(x=480, y=120, height=30)

    order_frame = Frame(base, bd=2, bg="sienna4", relief=GROOVE)
    order_frame.place(x=20, y=235, height=450, width=633)
    canvas = Label(order_frame, image=img2)
    canvas.configure(width=630, height=470)
    canvas.place(x=0, y=0)

    order_title_label = Label(order_frame, text="Order",
                              font=("times new roman", 16, "bold"), bg="sienna4", fg="white")
    order_title_label.place(x=0, y=0, width=633)  # pack(side=TOP,fill="x")

    order_tabel_frame = Frame(order_frame)
    order_tabel_frame.place(x=0, y=40, height=300, width=630)

    scrollbar_order_x = Scrollbar(order_tabel_frame, orient=HORIZONTAL)
    scrollbar_order_y = Scrollbar(order_tabel_frame, orient=VERTICAL)

    order_tabel = ttk.Treeview(order_tabel_frame,
                               columns=("name", "rate", "quantity", "price", "category"),
                               xscrollcommand=scrollbar_order_x.set,
                               yscrollcommand=scrollbar_order_y.set)

    order_tabel.heading("name", text="Name")
    order_tabel.heading("rate", text="Rate")
    order_tabel.heading("quantity", text="Quantity")
    order_tabel.heading("price", text="Price")
    order_tabel["displaycolumns"] = ("name", "rate", "quantity", "price")
    order_tabel["show"] = "headings"
    order_tabel.column("rate", width=100, anchor='center', stretch=NO)
    order_tabel.column("quantity", width=100, anchor='center', stretch=NO)
    order_tabel.column("price", width=100, anchor='center', stretch=NO)

    order_tabel.bind("<ButtonRelease-1>", load_item_from_order)

    scrollbar_order_x.pack(side=BOTTOM, fill=X)
    scrollbar_order_y.pack(side=RIGHT, fill=Y)

    scrollbar_order_x.configure(command=order_tabel.xview)
    scrollbar_order_y.configure(command=order_tabel.yview)

    order_tabel.pack(fill=BOTH, expand=1)

    total_price_label = Label(order_frame, text="Total Price:",
                              font=("arial", 12, "bold"), bg="sienna4", fg="white")
    total_price_label.place(x=165, y=360)

    totalPrice = StringVar()
    totalPrice.set("")
    total_price_entry = Entry(order_frame, font="arial 12", textvariable=totalPrice, state=DISABLED,
                              width=20)
    total_price_entry.place(x=270, y=360)

    bill_button = Button(order_frame, text="Bill", width=20,
                         command=bill_button_operation, bg="bisque", bd=5)
    bill_button.place(x=350, y=400)

    cancel_button = Button(order_frame, width=20, text="Cancel Order", command=cancel_button_operation, bg="bisque",
                           bd=5)
    cancel_button.place(x=100, y=400)

    btnback = Button(base, text="back", bg="bisque", bd=5, command=backInBilling)
    btnback.place(x=10, y=10)

    root.mainloop()


# Income Tracker Application
flag1 = True


def incm_track():
    def submit():
        clear()
        global flag1
        if flag1:
            txtbox.insert(INSERT, "\n\n")

        flag1 = False

        db = DateEntry.get(dateEntry)
        con = sqlite3.connect("Bill_mangement.db")
        query = "select sum(price) from customer_table where date='" + str(db) + "'"

        cur = con.cursor()
        cur.execute(query)
        data = (cur.fetchone())
        con.execute(query)
        con.commit()
        con.close()
        if data != None:
            data1 = list(data)
            txtbox.insert(END, "\t" + str(db) + "\t\t\t\t\t" + str(data1[0]) + "\n")

    def allRecord():
        clear()
        con = sqlite3.connect("Bill_mangement.db")
        query1 = "select date from customer_table"
        cur = con.cursor()

        cur.execute(query1)
        data1 = list(set(cur.fetchall()))
        txtbox.insert(INSERT, "\n\n")

        for d in data1:
            query2 = "select sum(price) from customer_table where date = '" + str(d[0]) + "' "
            cur.execute(query2)
            data2 = (cur.fetchall())
            # print(data2)
            if data2 != None:
                txtbox.insert(END, "\t" + str(d[0]) + "\t\t\t\t\t" + str(data2[0][0]) + "\n")

        con.commit()
        con.close()

    def clear():
        global flag1
        flag1 = True
        txtbox.delete(1.0, END)

    def backInIncome():
        basefunction()
        base.mainloop()

    # GUI
    base.title("Income Tracker Application")
    base.geometry("700x700+400+10")
    img = Image.open("icon/bckg.png")
    a = img.resize((1400, 690))
    a.save("icon/bckg.png")
    b = Image.open("icon/bckg.png")
    c = ImageTk.PhotoImage(b)
    d = Label(image=c)
    d.image = c
    d.place(x=0, y=0)

    lb1 = Label(base, text="Income Tracker", font=("Imprint MT shadow", 25, "bold"), bg="coral4", fg="white", pady=0)
    lb1.place(x=0, y=0, height=47, width=700)

    lb2 = Label(base, text="  Select date  ", font=("arial", 14, "bold"), bg="coral4", fg="white")
    lb2.place(x=30, y=70)

    dateEntry = DateEntry(base, width=12, font=('arial', 15, 'bold'), bg="orange")
    dateEntry.place(x=170, y=68)

    submitbtn = Button(base, text="Submit", font=('arial', 12, 'bold'), bg="coral3", fg="white", command=submit)
    submitbtn.place(x=500, y=65, height=40, width=100)

    txtbox = Text(base, width=65, height=27, font=12)
    txtbox.place(x=50, y=130)

    lb3 = Label(txtbox, text="Date\t\t\t\tIncome", font=("arial", 14, "bold"), width=48, bg="coral4", fg="white")
    lb3.place(x=0, y=0)

    btnallrecord = Button(base, text="All record", font=('arial', 12, 'bold'), bg="coral3", fg="white",
                          command=allRecord)
    btnallrecord.place(x=45, y=635, height=40, width=100)

    btnclr = Button(base, text="Clear", font=('arial', 12, 'bold'), bg="coral3", fg="white",
                    command=clear)
    btnclr.place(x=560, y=635, height=40, width=100)

    btnback2 = Button(lb1, text="back", bg="bisque", bd=3, command=backInIncome)
    btnback2.place(x=3, y=3)

    base.mainloop()


# GUI
base = Tk()


def basefunction():
    base.title("Billing System and Income Tracker")
    base.geometry("1500x900+0+0")
    icon = PhotoImage(file="icon/a.png")
    base.iconphoto(False, icon)
    img = Image.open("icon/bc.png")
    a = img.resize((1502, 900))
    a.save("icon/bc.png")
    b = Image.open("icon/bc.png")
    c = ImageTk.PhotoImage(b)
    d = Label(image=c)
    d.image = c
    d.place(x=0, y=0)
    menu_label = Label(base, text="Hotel Billing and Income Tracker ",
                       font=("Imprint MT shadow", 25, "bold"), bg="coral4", fg="white", pady=0)

    def call():
        pass

    menu_label.place(x=380, y=220, width=700, height=60)
    add_button = Button(base, text="Billing System"
                        , bg="coral3", bd=3, command=mainfunction)
    add_button.place(x=630, y=330, height=40, width=150)

    remove_button = Button(base, text="Income Tracker"
                           , bg="coral3", bd=3, command=incm_track)
    remove_button.place(x=630, y=410, height=40, width=150)


basefunction()
base.mainloop()