from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.root.focus_force()

        # All Variables

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_supp_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # Options

        lbl_search = Label(self.root, text = "Supplier Id", bg = "white", font = ("times new roman", 15))
        lbl_search.place(x = 700, y = 80)

        txt_search = Entry(self.root, textvariable = self.var_searchtxt, font = ("times new roman", 15), bg = "lightyellow") .place(x = 800, y = 80, width = 160)
        btn_search = Button(self.root, text = "Search", command = self.search, font = ("times new roman", 15), bg = "#4caf50", fg = "white", cursor = "hand2") .place(x = 980, y = 79, width = 100, height = 28)

        # Title

        title = Label(self.root, text = "Supplier Details", font  = ("times new roman", 20, "bold"), bg = "#0f4d7d", fg = "white") .place(x = 50, y = 10, width = 1000, height = 40)

        # Content - Row 1

        lbl_supplier_invoice = Label(self.root, text = "Supplier Id", font  = ("times new roman", 15), bg = "white") .place(x = 50, y = 80)
        txt_supplier_invoice = Entry(self.root, textvariable = self.var_supp_invoice, font  = ("times new roman", 15), bg = "lightyellow") .place(x = 180, y = 80, width = 180)

        # Content - Row 2

        lbl_name = Label(self.root, text = "Name", font  = ("times new roman", 15), bg = "white") .place(x = 50, y = 120)
        txt_name = Entry(self.root, textvariable = self.var_name, font  = ("times new roman", 15), bg = "lightyellow") .place(x = 180, y = 120, width = 180)

        # Content - Row 3

        lbl_contact = Label(self.root, text = "Contact", font  = ("times new roman", 15), bg = "white") .place(x = 50, y = 160)
        txt_contact = Entry(self.root, textvariable = self.var_contact, font  = ("times new roman", 15), bg = "lightyellow") .place(x = 180, y = 160, width = 180)

        # Content - Row 4

        lbl_descr = Label(self.root, text = "Description", font  = ("times new roman", 15), bg = "white") .place(x = 50, y = 200)
        self.txt_descr = Text(self.root, font  = ("times new roman", 15), bg = "lightyellow")
        self.txt_descr.place(x = 180, y = 200, width = 470, height = 120)

        # Buttons

        btn_add = Button(self.root, text = "Save", command = self.add, font = ("times new roman", 15), bg = "#2196f3", fg = "white", cursor = "hand2") .place(x = 180, y = 370, width = 110, height = 35)
        btn_update = Button(self.root, text = "Update", command = self.update, font = ("times new roman", 15), bg = "#4caf50", fg = "white", cursor = "hand2") .place(x = 300, y = 370, width = 110, height = 35)
        btn_delete = Button(self.root, text = "Delete", command = self.delete, font = ("times new roman", 15), bg = "#f44336", fg = "white", cursor = "hand2") .place(x = 420, y = 370, width = 110, height = 35)
        btn_clear = Button(self.root, text = "Clear", command = self.clear, font = ("times new roman", 15), bg = "#607d8b", fg = "white", cursor = "hand2") .place(x = 540, y = 370, width = 110, height = 35)

        # Supplier Details

        supp_frame = Frame(self.root, bd = 3, relief = RIDGE)
        supp_frame.place(x = 700, y = 120, width = 380, height = 350)

        scrolly = Scrollbar(supp_frame, orient = VERTICAL)
        scrollx = Scrollbar(supp_frame, orient = HORIZONTAL)

        self.SupplierTable = ttk.Treeview(supp_frame, columns = ("invoice", "name", "contact", "descr"), yscrollcommand = scrolly.set, xscrollcommand = scrollx.set)
        
        scrollx.pack(side = BOTTOM, fill = X)
        scrolly.pack(side = RIGHT, fill = Y)

        scrollx.config(command = self.SupplierTable.xview)
        scrolly.config(command = self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text = "Supplier Id")
        self.SupplierTable.heading("name", text = "Name")
        self.SupplierTable.heading("contact", text = "Contact")
        self.SupplierTable.heading("descr", text = "Description")

        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width = 90)
        self.SupplierTable.column("name", width = 100)
        self.SupplierTable.column("contact", width = 100)
        self.SupplierTable.column("descr", width = 100)

        self.SupplierTable.pack(fill = BOTH, expand = 1)
        self.SupplierTable.bind("<ButtonRelease - 1>", self.get_data)

        self.show()

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
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = %s", (self.var_supp_invoice.get(),))

                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Invoice No. already assigned, try different", parent = self.root)
                else:
                    cur.execute("insert into supplier(invoice, name, contact, descr)" "values(%s, %s, %s, %s)", (
                        self.var_supp_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_descr.get('1.0', END)
                    ))

                    conn.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent = self.root)
                    
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
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values = row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Get Data

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        self.var_supp_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_descr.delete('1.0', END)
        self.txt_descr.insert(END, row[3])

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
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = %s", (self.var_supp_invoice.get(),))

                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)
                else:
                    cur.execute("update supplier set name = %s, contact = %s, descr = %s where invoice = %s", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_descr.get('1.0', END),
                        self.var_supp_invoice.get()
                    ))

                    conn.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent = self.root)
                    
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
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = %s", (self.var_supp_invoice.get(),))

                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice = %s", (self.var_supp_invoice.get(),))

                        conn.commit()
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent = self.root)     

                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    # Clear

    def clear(self):
        self.var_supp_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_descr.delete('1.0', END)
        self.var_searchtxt.set("")

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
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = %s", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('', END, values = row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent = self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()