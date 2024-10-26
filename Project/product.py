from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.root.focus_force()

        # Variables

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_supp = StringVar()
        self.cat_list = []
        self.supp_list = []
        self.fetch_cat_supp()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # Frame

        product_Frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        product_Frame.place(x = 10, y = 10, width = 450, height = 480)

        # Title

        title = Label(product_Frame, text = "Manage Products", font  = ("times new roman", 18), bg = "#0f4d7d", fg = "white") .pack(side = TOP, fill = X)

        # Column 1

        lbl_cat = Label(product_Frame, text = "Category", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 60)
        lbl_supp = Label(product_Frame, text = "Supplier", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 110)
        lbl_name = Label(product_Frame, text = "Name", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 160)
        lbl_price = Label(product_Frame, text = "Price", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 210)
        lbl_qty = Label(product_Frame, text = "Quantity", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 260)
        lbl_status = Label(product_Frame, text = "Status", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 310)

        txt_category = Label(product_Frame, text = "Category", font  = ("times new roman", 18), bg = "white") .place(x = 30, y = 60)
        
        # Column 2

        cmb_cat = ttk.Combobox(product_Frame, textvariable = self.var_cat, values = self.cat_list, state = 'readonly', justify = CENTER, font = ("times new roman", 15))
        cmb_cat.place(x = 150, y =60, width = 200)
        cmb_cat.current(0)

        cmb_supp = ttk.Combobox(product_Frame, textvariable = self.var_supp, values = self.supp_list, state = 'readonly', justify = CENTER, font = ("times new roman", 15))
        cmb_supp.place(x = 150, y = 110, width = 200)
        cmb_supp.current(0)

        txt_name = Entry(product_Frame, textvariable = self.var_name, font = ("times new roman", 15), bg = "lightyellow") .place(x = 150, y = 160, width = 200)
        txt_price = Entry(product_Frame, textvariable = self.var_price, font = ("times new roman", 15), bg = "lightyellow") .place(x = 150, y = 210, width = 200)
        txt_qty = Entry(product_Frame, textvariable = self.var_qty, font = ("times new roman", 15), bg = "lightyellow") .place(x = 150, y = 260, width = 200)
        
        cmb_status = ttk.Combobox(product_Frame, textvariable = self.var_status, values = ("Active", "Inactive"), state = 'readonly', justify = CENTER, font = ("times new roman", 15))
        cmb_status.place(x = 150, y = 310, width = 200)
        cmb_status.current(0)

        # Buttons

        btn_add = Button(product_Frame, text = "Save", command = self.add, font = ("times new roman", 15), bg = "#2196f3", fg = "white", cursor = "hand2") .place(x = 10, y = 400, width = 100, height = 40)
        btn_update = Button(product_Frame, text = "Update", command = self.update, font = ("times new roman", 15), bg = "#4caf50", fg = "white", cursor = "hand2") .place(x = 120, y = 400, width = 100, height = 40)
        btn_delete = Button(product_Frame, text = "Delete", command = self.delete, font = ("times new roman", 15), bg = "#f44336", fg = "white", cursor = "hand2") .place(x = 230, y = 400, width = 100, height = 40)
        btn_clear = Button(product_Frame, text = "Clear", command = self.clear, font = ("times new roman", 15), bg = "#607d8b", fg = "white", cursor = "hand2") .place(x = 340, y = 400, width = 100, height = 40)

        
        # Search Frame

        SearchFrame = LabelFrame(self.root, text = "Search Employee", font = ("times new roman", 12, "bold"), bd = 2, relief = RIDGE, bg = "white")
        SearchFrame.place(x = 480, y = 10, width = 600, height = 80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable = self.var_searchby, values = ("Select", "Category", "Supplier", "Name"), state = 'readonly', justify = CENTER, font = ("times new roman", 15))
        cmb_search.place(x = 10, y = 10, width = 180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable = self.var_searchtxt, font = ("times new roman", 15), bg = "lightyellow") .place(x = 200, y = 10)
        btn_search = Button(SearchFrame, text = "Search", command = self.search, font = ("times new roman", 15), bg = "#4caf50", fg = "white", cursor = "hand2") .place(x = 410, y = 9, width = 150, height = 30)

        # Product Details

        pro_frame = Frame(self.root, bd = 3, relief = RIDGE)
        pro_frame.place(x = 480, y = 100, width = 600, height = 390)

        scrolly = Scrollbar(pro_frame, orient = VERTICAL)
        scrollx = Scrollbar(pro_frame, orient = HORIZONTAL)

        self.ProductTable = ttk.Treeview(pro_frame, columns = ("pid", "category", "supplier", "name", "price", "qty", "status"), yscrollcommand = scrolly.set, xscrollcommand = scrollx.set)
        
        scrollx.pack(side = BOTTOM, fill = X)
        scrolly.pack(side = RIGHT, fill = Y)

        scrollx.config(command = self.ProductTable.xview)
        scrolly.config(command = self.ProductTable.yview)

        self.ProductTable.heading("pid", text = "Product ID")
        self.ProductTable.heading("category", text = "Category")
        self.ProductTable.heading("supplier", text = "Supplier")
        self.ProductTable.heading("name", text = "Name")
        self.ProductTable.heading("price", text = "Price")
        self.ProductTable.heading("qty", text = "Qty")
        self.ProductTable.heading("status", text = "Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width = 90)
        self.ProductTable.column("category", width = 100)
        self.ProductTable.column("supplier", width = 100)
        self.ProductTable.column("name", width = 100)
        self.ProductTable.column("price", width = 100)
        self.ProductTable.column("qty", width = 100)
        self.ProductTable.column("status", width = 100)

        self.ProductTable.pack(fill = BOTH, expand = 1)
        self.ProductTable.bind("<ButtonRelease - 1>", self.get_data)

        self.show()

    # Fetch

    def fetch_cat_supp(self):
        
        self.cat_list.append("Empty")
        self.supp_list.append("Empty")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            cur.execute("select name from category")
            cat = cur.fetchall()

            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("select name from supplier")
            supp = cur.fetchall()

            if len(supp) > 0:
                del self.supp_list[:]
                self.supp_list.append("Select")
                for i in supp:
                    self.supp_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Save

    def add(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.var_cat.get() == "Select" or self.var_supp.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent = self.root)
            else:
                cur.execute("select * from product where name = %s", (self.var_name.get(),))

                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product already present, try different", parent = self.root)
                else:
                    cur.execute("insert into product(category, supplier, name, price, qty, status)" "values(%s, %s, %s, %s, %s, %s)", (
                        self.var_cat.get(),
                        self.var_supp.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))

                    conn.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent = self.root)
                    
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Show

    def show(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values = row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Get Data

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_supp.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6])

    # Update

    def update(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please seletc product from list", parent = self.root)
            else:
                cur.execute("select * from product where pid = %s", (self.var_pid.get(),))

                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent = self.root)
                else:
                    cur.execute("update product set category = %s, supplier = %s, name = %s, price = %s, qty = %s, status = %s where pid = %s", (
                        self.var_cat.get(),
                        self.var_supp.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))

                    conn.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent = self.root)
                    
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Delete

    def delete(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from the list", parent = self.root)
            else:
                cur.execute("select * from product where pid = %s", (self.var_pid.get(),))

                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("delete from product where pid = %s", (self.var_pid.get(),))

                        conn.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent = self.root)     

                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Clear

    def clear(self):
        self.var_cat.set("Select"),
        self.var_supp.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.show()

    # Search

    def search(self):
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ims"
        )

        cur = conn.cursor()

        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select search by option", parent = self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Select input should be required", parent = self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values = row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent = self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()