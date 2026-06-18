import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def fix_heb(text):
    return " ".join(text.split()[::-1])

class CrudGenre(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול ז'אנרים - CRUD"))
        self.geometry("800x450")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.display_frame = ctk.CTkFrame(self, width=450)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי ז'אנר"), font=("Arial", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מזהה (G_ID):")).pack(anchor="e", padx=10)
        self.entry_id = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_id.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text=fix_heb("שם הז'אנר:")).pack(anchor="e", padx=10)
        self.entry_name = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_name.pack(fill="x", padx=10, pady=5)

        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22", hover_color="#D35400", command=self.load_data)
        self.btn_load.pack(fill="x", padx=10, pady=10)
        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף חדש"), fg_color="#27AE60", hover_color="#2ECC71", command=self.insert_data)
        self.btn_insert.pack(fill="x", padx=10, pady=5)
        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9", hover_color="#3498DB", command=self.update_data)
        self.btn_update.pack(fill="x", padx=10, pady=5)
        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק ז'אנר"), fg_color="#C0392B", hover_color="#E74C3C", command=self.delete_data)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת הז'אנרים"), font=("Arial", 20, "bold")).pack(pady=10)
        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה (READ)"), command=self.read_data)
        self.btn_refresh.pack(pady=5)
        self.textbox = ctk.CTkTextbox(self.display_frame, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.read_data()

    def read_data(self):
        conn = db_connection.get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT G_ID, Genre_Name FROM Genre ORDER BY G_ID ASC;")
            rows = cursor.fetchall()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID   | Genre Name\n" + "-"*30 + "\n")
            for row in rows:
                self.textbox.insert("end", f"{row[0]:<4} | {row[1]}\n")
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: conn.close()

    def load_data(self):
        g_id = self.entry_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Genre_Name FROM Genre WHERE G_ID = %s", (g_id,))
            row = cursor.fetchone()
            if row:
                self.entry_name.delete(0, 'end')
                self.entry_name.insert(0, str(row[0]))
            else: messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: conn.close()

    def insert_data(self):
        g_id, name = self.entry_id.get(), self.entry_name.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Genre (G_ID, Genre_Name) VALUES (%s, %s)", (g_id, name))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.read_data()
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: conn.close()

    def update_data(self):
        g_id, name = self.entry_id.get(), self.entry_name.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Genre SET Genre_Name=%s WHERE G_ID=%s", (name, g_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.read_data()
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: conn.close()

    def delete_data(self):
        g_id = self.entry_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Genre WHERE G_ID=%s", (g_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.read_data()
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: conn.close()

if __name__ == "__main__":
    app = CrudGenre()
    app.mainloop()