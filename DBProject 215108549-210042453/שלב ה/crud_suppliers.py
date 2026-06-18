import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text): return " ".join(text.split()[::-1])


class CrudSuppliers(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול ספקים - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)
        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי ספק"), font=("Arial", 20, "bold")).pack(pady=10)

        self.entries = {}
        fields = {"supplier_id": fix_heb("מזהה ספק:"), "supplier_name": fix_heb("שם הספק:"),
                  "phone": fix_heb("טלפון:"), "email": fix_heb("אימייל:"), "address": fix_heb("כתובת:")}

        for key, label in fields.items():
            ctk.CTkLabel(self.form_frame, text=label).pack(anchor="e", padx=10)
            entry = ctk.CTkEntry(self.form_frame, justify="right")
            entry.pack(fill="x", padx=10, pady=2)
            self.entries[key] = entry

        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22",
                                      command=self.load_data)
        self.btn_load.pack(fill="x", padx=10, pady=10)
        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף חדש"), fg_color="#27AE60",
                                        command=self.insert_data)
        self.btn_insert.pack(fill="x", padx=10, pady=5)
        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9",
                                        command=self.update_data)
        self.btn_update.pack(fill="x", padx=10, pady=5)
        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק ספק"), fg_color="#C0392B",
                                        command=self.delete_data)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת הספקים"), font=("Arial", 20, "bold")).pack(pady=10)
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
            cursor.execute("SELECT supplier_id, supplier_name, phone FROM suppliers ORDER BY supplier_id ASC;")
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID | Supplier Name | Phone\n" + "-" * 40 + "\n")
            for row in cursor.fetchall():
                self.textbox.insert("end", f"{row[0]:<3}| {str(row[1]):<14} | {row[2]}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_data(self):
        s_id = self.entries["supplier_id"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT supplier_name, phone, email, address FROM suppliers WHERE supplier_id = %s", (s_id,))
            row = cursor.fetchone()
            if row:
                for idx, key in enumerate(["supplier_name", "phone", "email", "address"]):
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, str(row[idx]))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_data(self):
        vals = [self.entries[k].get() for k in ["supplier_id", "supplier_name", "phone", "email", "address"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO suppliers (supplier_id, supplier_name, phone, email, address) VALUES (%s, %s, %s, %s, %s)",
                vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_data(self):
        vals = [self.entries[k].get() for k in ["supplier_name", "phone", "email", "address", "supplier_id"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE suppliers SET supplier_name=%s, phone=%s, email=%s, address=%s WHERE supplier_id=%s",
                           vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_data(self):
        s_id = self.entries["supplier_id"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (s_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudSuppliers()
    app.mainloop()