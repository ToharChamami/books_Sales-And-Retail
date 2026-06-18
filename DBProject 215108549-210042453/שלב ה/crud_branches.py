import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class CrudBranches(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול סניפים - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # --- טופס ---
        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי סניף"), font=("Arial", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מזהה סניף (ID):")).pack(anchor="e", padx=10)
        self.entry_id = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_id.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מיקום/שם הסניף:")).pack(anchor="e", padx=10)
        self.entry_branch_id = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_branch_id.pack(fill="x", padx=10, pady=5)

        # --- כפתורים ---
        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22",
                                      hover_color="#D35400", command=self.load_branch)
        self.btn_load.pack(fill="x", padx=10, pady=10)

        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף סניף"), fg_color="#27AE60",
                                        hover_color="#2ECC71", command=self.insert_branch)
        self.btn_insert.pack(fill="x", padx=10, pady=5)

        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9",
                                        hover_color="#3498DB", command=self.update_branch)
        self.btn_update.pack(fill="x", padx=10, pady=5)

        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק סניף"), fg_color="#C0392B",
                                        hover_color="#E74C3C", command=self.delete_branch)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        # --- תצוגה ---
        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת הסניפים במערכת"), font=("Arial", 20, "bold")).pack(pady=10)

        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה (READ)"),
                                         command=self.read_branches)
        self.btn_refresh.pack(pady=5)

        self.textbox = ctk.CTkTextbox(self.display_frame, width=450, height=350, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.read_branches()

    def clear_entries(self):
        self.entry_id.delete(0, 'end')
        self.entry_branch_id.delete(0, 'end')

    def read_branches(self):
        conn = db_connection.get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            # נניח שלעמודת השם/מיקום קוראים branch_id בטבלה branch (אם קוראים לה branch_name, שנו כאן)
            cursor.execute("SELECT branch_id, branch_id FROM branch ORDER BY branch_id ASC;")
            rows = cursor.fetchall()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "Branch ID | branch_id\n")
            self.textbox.insert("end", "-" * 30 + "\n")

            for row in rows:
                loc = str(row[1]) if row[1] else "N/A"
                line = f"{row[0]:<9} | {loc:<20}\n"
                self.textbox.insert("end", line)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_branch(self):
        b_id = self.entry_id.get()
        if not b_id: return
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT branch_id FROM branch WHERE branch_id = %s", (b_id,))
            row = cursor.fetchone()
            if row:
                self.entry_branch_id.delete(0, 'end')
                self.entry_branch_id.insert(0, str(row[0]))
                messagebox.showinfo("Success", fix_heb("נתונים נטענו"))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_branch(self):
        b_id = self.entry_id.get()
        loc = self.entry_branch_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO branch (branch_id, branch_id) VALUES (%s, %s)", (b_id, loc))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.clear_entries()
            self.read_branches()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_branch(self):
        b_id = self.entry_id.get()
        loc = self.entry_branch_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE branch SET branch_id=%s WHERE branch_id=%s", (loc, b_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.clear_entries()
            self.read_branches()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_branch(self):
        b_id = self.entry_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM branch WHERE branch_id=%s", (b_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.clear_entries()
            self.read_branches()
        except Exception as e:
            messagebox.showerror("Error", fix_heb("לא ניתן למחוק - קיים מלאי לסניף זה!"))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudBranches()
    app.mainloop()