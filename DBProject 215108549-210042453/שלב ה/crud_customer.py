import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text): return " ".join(text.split()[::-1])


class CrudCustomer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול לקוחות - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)
        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי לקוח"), font=("Arial", 20, "bold")).pack(pady=10)

        self.entries = {}
        fields = {"C_ID": fix_heb("מזהה (C_ID):"), "first_name": fix_heb("שם פרטי:"),
                  "last_name": fix_heb("שם משפחה:"), "Phone": fix_heb("טלפון:")}

        for key, label in fields.items():
            ctk.CTkLabel(self.form_frame, text=label).pack(anchor="e", padx=10)
            entry = ctk.CTkEntry(self.form_frame, justify="right")
            entry.pack(fill="x", padx=10, pady=2)
            self.entries[key] = entry

        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22",
                                      command=self.load_data)
        self.btn_load.pack(fill="x", padx=10, pady=10)
        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף לקוח"), fg_color="#27AE60",
                                        command=self.insert_data)
        self.btn_insert.pack(fill="x", padx=10, pady=5)
        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9",
                                        command=self.update_data)
        self.btn_update.pack(fill="x", padx=10, pady=5)
        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק לקוח"), fg_color="#C0392B",
                                        command=self.delete_data)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.display_frame, text=fix_heb("מועדון הלקוחות"), font=("Arial", 20, "bold")).pack(pady=10)
        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה"), command=self.read_data)
        self.btn_refresh.pack(pady=5)
        self.textbox = ctk.CTkTextbox(self.display_frame, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.read_data()

    def read_data(self):
        conn = db_connection.get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT C_ID, first_name, last_name, Phone FROM Customer ORDER BY C_ID ASC;")
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID | First Name | Last Name | Phone\n" + "-" * 45 + "\n")
            for row in cursor.fetchall():
                self.textbox.insert("end", f"{row[0]:<3}| {row[1]:<10} | {row[2]:<9} | {row[3]}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_data(self):
        c_id = self.entries["C_ID"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, last_name, Phone FROM Customer WHERE C_ID = %s", (c_id,))
            row = cursor.fetchone()
            if row:
                for idx, key in enumerate(["first_name", "last_name", "Phone"]):
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, str(row[idx]))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_data(self):
        vals = [self.entries[k].get() for k in ["C_ID", "first_name", "last_name", "Phone"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Customer (C_ID, first_name, last_name, Phone) VALUES (%s, %s, %s, %s)", vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_data(self):
        vals = [self.entries[k].get() for k in ["first_name", "last_name", "Phone", "C_ID"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Customer SET first_name=%s, last_name=%s, Phone=%s WHERE C_ID=%s", vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_data(self):
        c_id = self.entries["C_ID"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customer WHERE C_ID=%s", (c_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudCustomer()
    app.mainloop()