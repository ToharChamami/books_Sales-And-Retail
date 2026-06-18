import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def fix_heb(text):
    return " ".join(text.split()[::-1])

class CrudInventory(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול מלאי - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # --- טופס ---
        ctk.CTkLabel(self.form_frame, text=fix_heb("הגדרות מלאי"), font=("Arial", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מזהה סניף:")).pack(anchor="e", padx=10)
        self.entry_branch = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_branch.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מקט ספר:")).pack(anchor="e", padx=10)
        self.entry_book = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_book.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text=fix_heb("כמות יח' במלאי:")).pack(anchor="e", padx=10)
        self.entry_qty = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_qty.pack(fill="x", padx=10, pady=5)

        # --- כפתורים ---
        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22", hover_color="#D35400", command=self.load_inv)
        self.btn_load.pack(fill="x", padx=10, pady=10)

        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף רשומת מלאי"), fg_color="#27AE60", hover_color="#2ECC71", command=self.insert_inv)
        self.btn_insert.pack(fill="x", padx=10, pady=5)

        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. עדכן כמות"), fg_color="#2980B9", hover_color="#3498DB", command=self.update_inv)
        self.btn_update.pack(fill="x", padx=10, pady=5)

        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק מספר/סניף"), fg_color="#C0392B", hover_color="#E74C3C", command=self.delete_inv)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        # --- תצוגה ---
        ctk.CTkLabel(self.display_frame, text=fix_heb("מלאי הספרים בסניפים"), font=("Arial", 20, "bold")).pack(pady=10)
        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה (READ)"), command=self.read_inv)
        self.btn_refresh.pack(pady=5)
        self.textbox = ctk.CTkTextbox(self.display_frame, width=450, height=350, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.read_inv()

    def clear_entries(self):
        self.entry_branch.delete(0, 'end')
        self.entry_book.delete(0, 'end')
        self.entry_qty.delete(0, 'end')

    def read_inv(self):
        conn = db_connection.get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT branch_id, book_id, quantity FROM inventory ORDER BY branch_id, book_id LIMIT 30;")
            rows = cursor.fetchall()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "Branch | Book ID | Quantity\n")
            self.textbox.insert("end", "-"*30 + "\n")
            for row in rows:
                self.textbox.insert("end", f"{row[0]:<6} | {row[1]:<7} | {row[2]}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_inv(self):
        b_id = self.entry_branch.get()
        book_id = self.entry_book.get()
        if not b_id or not book_id:
            messagebox.showwarning("שגיאה", fix_heb("יש להזין סניף וספר כדי למשוך נתונים"))
            return
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM inventory WHERE branch_id=%s AND book_id=%s", (b_id, book_id))
            row = cursor.fetchone()
            if row:
                self.entry_qty.delete(0, 'end')
                self.entry_qty.insert(0, str(row[0]))
                messagebox.showinfo("Success", fix_heb("נתונים נטענו"))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_inv(self):
        b_id = self.entry_branch.get()
        book_id = self.entry_book.get()
        qty = self.entry_qty.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventory (branch_id, book_id, quantity) VALUES (%s, %s, %s)", (b_id, book_id, qty))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.clear_entries()
            self.read_inv()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_inv(self):
        b_id = self.entry_branch.get()
        book_id = self.entry_book.get()
        qty = self.entry_qty.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET quantity=%s WHERE branch_id=%s AND book_id=%s", (qty, b_id, book_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.clear_entries()
            self.read_inv()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_inv(self):
        b_id = self.entry_branch.get()
        book_id = self.entry_book.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE branch_id=%s AND book_id=%s", (b_id, book_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.clear_entries()
            self.read_inv()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    app = CrudInventory()
    app.mainloop()
