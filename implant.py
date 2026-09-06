import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk  # pip install pillow

class ImplantClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x620+70+80")
        self.root.title("Implant Clinic Management")
        self.root.config(bg="#EDF2F7")  # Soft light gray modern background
        self.root.resizable(False, False)
        
        self.base_dir = Path(__file__).resolve().parent

        #========================== Variables ==========================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_name = StringVar()
        self.var_gender = StringVar()
        self.var_age = StringVar()
        self.var_date = StringVar()
        self.var_state = StringVar()
        self.var_price = StringVar()
        self.var_contact = StringVar()
        self.var_address = StringVar()
        self.var_id = StringVar()

        #========================== Modern Header ==========================
        header_frame = Frame(self.root, bg='#0f172a', bd=0)
        header_frame.place(x=0, y=0, width=1100, height=55)

        lbl_title = Label(
            header_frame, 
            text="🦷 Implant & Surgery Management", 
            font=("Segoe UI", 13, 'bold'), 
            bg='#0f172a', 
            fg='#38bdf8'
        )
        lbl_title.pack(side=LEFT, padx=20)

        #========================== Search Frame ==========================
        search_frame = Frame(self.root, bg="white", bd=0)
        search_frame.place(x=20, y=70, width=1060, height=65)

        lbl_search_title = Label(search_frame, text="Search By:", font=("Segoe UI", 11, "bold"), bg="white", fg="#334155")
        lbl_search_title.place(x=15, y=17)

        cmb_search = ttk.Combobox(
            search_frame, textvariable=self.var_searchby, 
            values=("Select", "Name", "Contact"),
            state="readonly", justify=CENTER, font=("Segoe UI", 11)
        )
        cmb_search.place(x=110, y=15, width=150, height=35)
        cmb_search.current(0)

        self.txt_search = Entry(search_frame, textvariable=self.var_searchtxt, font=('Segoe UI', 11), bg='#f8fafc', justify=CENTER)
        self.txt_search.place(x=275, y=15, width=250, height=35)

        btn_search = Button(
            search_frame, text="Search", font=("Segoe UI", 11, "bold"),
            bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white",
            bd=0, cursor="hand2", command=self.search
        )
        btn_search.place(x=540, y=15, width=120, height=35)

        btn_show_all = Button(
            search_frame, text="Show All", font=("Segoe UI", 11, "bold"),
            bg="#64748b", fg="white", activebackground="#475569", activeforeground="white",
            bd=0, cursor="hand2", command=self.show
        )
        btn_show_all.place(x=675, y=15, width=120, height=35)

        #========================== Data Entry Frame ==========================
        data_frame = Frame(self.root, bg="white", bd=0)
        data_frame.place(x=20, y=145, width=1060, height=185)

        fields = [
            ("Name", self.var_name, 20, 15, Entry),
            ("Gender", self.var_gender, 370, 15, lambda p, v: ttk.Combobox(p, textvariable=v, values=("Select", "Male", "Female"), state="readonly", justify=CENTER)),
            ("Age", self.var_age, 720, 15, Entry),
            ("Date", self.var_date, 20, 65, Entry),
            ("State", self.var_state, 370, 65, Entry),
            ("Price", self.var_price, 720, 65, Entry),
            ("Contact", self.var_contact, 20, 115, Entry),
            ("Address", self.var_address, 370, 115, Entry)
        ]

        for label_text, var_name_ref, px, py, widget_type in fields:
            lbl = Label(data_frame, text=label_text, font=('Segoe UI', 10, 'bold'), bg='white', fg='#475569')
            lbl.place(x=px, y=py)
            
            if widget_type == Entry:
                ent = Entry(data_frame, textvariable=var_name_ref, font=('Segoe UI', 11), bg='#f8fafc', justify=CENTER)
                ent.place(x=px + 90, y=py - 3, width=230, height=32)
            else:
                cmb = widget_type(data_frame, var_name_ref)
                cmb.config(font=('Segoe UI', 11))
                cmb.place(x=px + 90, y=py - 3, width=230, height=32)
                if label_text == "Gender":
                    cmb.current(0)

        #========================== Action Buttons ==========================
        btn_frame = Frame(self.root, bg="white", bd=0)
        btn_frame.place(x=20, y=340, width=1060, height=50)

        def create_action_btn(parent, text, cmd, bg_col, hover_col):
            btn = Button(
                parent, text=text, command=cmd,
                font=('Segoe UI', 11, 'bold'),
                bg=bg_col, fg="white",
                activebackground=hover_col, activeforeground="white",
                bd=0, cursor="hand2"
            )
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_col))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_col))
            return btn

        btn_add = create_action_btn(btn_frame, "➕ Add", self.add, "#10b981", "#059669")
        btn_add.place(x=10, y=8, width=150, height=35)

        btn_update = create_action_btn(btn_frame, "✏️ Update", self.update, "#0ea5e9", "#0284c7")
        btn_update.place(x=175, y=8, width=150, height=35)

        btn_delete = create_action_btn(btn_frame, "🗑️ Delete", self.delete, "#ef4444", "#dc2626")
        btn_delete.place(x=340, y=8, width=150, height=35)

        btn_clear = create_action_btn(btn_frame, "🧹 Clear", self.clear, "#64748b", "#475569")
        btn_clear.place(x=505, y=8, width=150, height=35)

        #========================== Treeview Table ==========================
        table_frame = Frame(self.root, bg="white", bd=0)
        table_frame.place(x=20, y=400, width=1060, height=205)
        
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)
        
        self.implant_table = ttk.Treeview(
            table_frame,
            columns=("name", "gender", "age", "date", "state", "price", "contact", "address", "id"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set,
        )
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.implant_table.xview)
        scrolly.config(command=self.implant_table.yview)
        
        headers = [
            ("name", "Name", 130),
            ("gender", "Gender", 90),
            ("age", "Age", 70),
            ("date", "Date", 100),
            ("state", "State", 110),
            ("price", "Price", 90),
            ("contact", "Contact", 110),
            ("address", "Address", 140),
            ("id", "ID", 50)
        ]

        for col_id, heading_text, width in headers:
            self.implant_table.heading(col_id, text=heading_text)
            self.implant_table.column(col_id, width=width, anchor=CENTER)
        
        self.implant_table["show"] = "headings"
        self.implant_table.pack(fill=BOTH, expand=1)
        
        self.show()
        self.implant_table.bind("<ButtonRelease-1>", self.get_data)

    def reco_id(self):
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        try:
            cur.execute("""
                WITH cte AS (
                    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num 
                    FROM implant
                )
                UPDATE implant
                SET id = (SELECT row_num FROM cte WHERE cte.id = implant.id);
            """)
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error in re-indexing: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        if self.var_name.get() == "" or self.var_gender.get() == "Select" or self.var_age.get() == "" or self.var_date.get() == "" or self.var_state.get() == "" or self.var_price.get() == "" or self.var_contact.get() == "" or self.var_address.get() == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)  
        else:
            try:
                cur.execute("INSERT INTO implant (name, gender, age, date, state, price, contact, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_age.get(),
                    self.var_date.get(),
                    self.var_state.get(),
                    self.var_price.get(),
                    self.var_contact.get(),
                    self.var_address.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Implant record added successfully", parent=self.root)
                self.reco_id()
                self.show()
                self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def show(self):
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS implant (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            gender TEXT,
                            age TEXT,
                            date TEXT,
                            state TEXT,
                            price TEXT,
                            contact TEXT,
                            address TEXT)""")
            cur.execute("SELECT id, name, gender, age, date, state, price, contact, address FROM implant")
            rows = cur.fetchall()
            self.implant_table.delete(*self.implant_table.get_children())
             
            for row in rows:
                self.implant_table.insert('', END, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0]))
        except Exception as ex:
            messagebox.showerror("Error", f"Error in implant: {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.var_gender.set("Select")
        self.var_age.set("")
        self.var_date.set("")   
        self.var_state.set("")
        self.var_price.set("")
        self.var_contact.set("")
        self.var_address.set("")
        self.var_id.set("")
        
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def get_data(self, ev):
        f = self.implant_table.focus()
        content = (self.implant_table.item(f))
        row = content['values']
        if row:
            self.var_name.set(row[0])
            self.var_gender.set(row[1])
            self.var_age.set(row[2])
            self.var_date.set(row[3])
            self.var_state.set(row[4])
            self.var_price.set(row[5])
            self.var_contact.set(row[6])
            self.var_address.set(row[7])
            self.var_id.set(row[8])

    def update(self):
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Please select a patient from the list first", parent=self.root)
        else:
            try:
                cur.execute("update implant set name=?, gender=?, age=?, date=?, state=?, price=?, contact=?, address=? where id=?", (
                    self.var_name.get(),
                    self.var_gender.get(),
                    self.var_age.get(),
                    self.var_date.get(),
                    self.var_state.get(),
                    self.var_price.get(),
                    self.var_contact.get(),
                    self.var_address.get(),
                    self.var_id.get()
                ))
                con.commit()
                self.reco_id()
                messagebox.showinfo("Success", "Record updated successfully", parent=self.root)
                self.show()
                self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def delete(self):
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Please select a patient from the list first", parent=self.root)
            return
             
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?", parent=self.root)
            if op == True:
                cur.execute("delete from implant where id=?", (self.var_id.get(),))
                con.commit()
                self.reco_id()
                messagebox.showinfo("Deleted", "Record deleted successfully", parent=self.root)
                self.show()
                self.clear() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect('clinic.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Please select a search by option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Please enter a value to search", parent=self.root)
            else:
                cur.execute("select * from implant where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.implant_table.delete(*self.implant_table.get_children())
                    for row in rows:
                        self.implant_table.insert('', END, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0]))
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)            
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = ImplantClass(root)
    root.mainloop()