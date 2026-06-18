import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text): return " ".join(text.split()[::-1])


class CrudEmployee(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול עובדים - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)
        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי עובד"), font=("Arial", 20, "bold")).pack(pady=10)

        self.entries = {}
        fields = {"E_ID": fix_heb("מזהה עובד:"), "First_Name": fix_heb("שם פרטי:"),
                  "Last_Name": fix_heb("שם משפחה:"), "position_id": fix_heb("תפקיד:"), "Branch_ID": fix_heb("מזהה סניף:")}

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
        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק עובד"), fg_color="#C0392B",
                                        command=self.delete_data)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת העובדים"), font=("Arial", 20, "bold")).pack(pady=10)
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
            cursor.execute("SELECT E_ID, First_Name, Last_Name, position_id, Branch_ID FROM Employee ORDER BY E_ID ASC;")
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID | First Name | Last Name | position_id | Branch\n" + "-" * 55 + "\n")
            for row in cursor.fetchall():
                self.textbox.insert("end", f"{row[0]:<3}| {row[1]:<10} | {row[2]:<9} | {row[3]:<8} | {row[4]}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_data(self):
        e_id = self.entries["E_ID"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT First_Name, Last_Name, position_id, Branch_ID FROM Employee WHERE E_ID = %s", (e_id,))
            row = cursor.fetchone()
            if row:
                for idx, key in enumerate(["First_Name", "Last_Name", "position_id", "Branch_ID"]):
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, str(row[idx]))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_data(self):
        vals = [self.entries[k].get() for k in ["E_ID", "First_Name", "Last_Name", "position_id", "Branch_ID"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Employee (E_ID, First_Name, Last_Name, position_id, Branch_ID) VALUES (%s, %s, %s, %s, %s)",
                vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_data(self):
        vals = [self.entries[k].get() for k in ["First_Name", "Last_Name", "position_id", "Branch_ID", "E_ID"]]
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Employee SET First_Name=%s, Last_Name=%s, position_id=%s, Branch_ID=%s WHERE E_ID=%s",
                           vals)
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_data(self):
        e_id = self.entries["E_ID"].get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Employee WHERE E_ID=%s", (e_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.read_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudEmployee()
    app.mainloop()