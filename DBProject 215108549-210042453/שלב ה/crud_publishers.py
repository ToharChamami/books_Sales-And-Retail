import customtkinter as ctk
from tkinter import messagebox
import db_connection

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class CrudPublishers(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול הוצאות לאור - CRUD"))
        self.geometry("900x550")

        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # --- טופס (צד ימין) ---
        ctk.CTkLabel(self.form_frame, text=fix_heb("פרטי הוצאה לאור"), font=("Arial", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_frame, text=fix_heb("מזהה הוצאה (ID):")).pack(anchor="e", padx=10)
        self.entry_id = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_id.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text=fix_heb("שם ההוצאה:")).pack(anchor="e", padx=10)
        self.entry_name = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_name.pack(fill="x", padx=10, pady=5)

        # --- כפתורים ---
        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22",
                                      hover_color="#D35400", command=self.load_publisher)
        self.btn_load.pack(fill="x", padx=10, pady=10)

        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף חדש"), fg_color="#27AE60",
                                        hover_color="#2ECC71", command=self.insert_publisher)
        self.btn_insert.pack(fill="x", padx=10, pady=5)

        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9",
                                        hover_color="#3498DB", command=self.update_publisher)
        self.btn_update.pack(fill="x", padx=10, pady=5)

        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק הוצאה"), fg_color="#C0392B",
                                        hover_color="#E74C3C", command=self.delete_publisher)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        # --- תצוגה (צד שמאל) ---
        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת ההוצאות לאור"), font=("Arial", 20, "bold")).pack(pady=10)

        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה (READ)"),
                                         command=self.read_publishers)
        self.btn_refresh.pack(pady=5)

        self.textbox = ctk.CTkTextbox(self.display_frame, width=450, height=350, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.read_publishers()

    def clear_entries(self):
        self.entry_id.delete(0, 'end')
        self.entry_name.delete(0, 'end')

    def read_publishers(self):
        conn = db_connection.get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT publisher_id, publisher_name FROM publishers ORDER BY publisher_id ASC;")
            rows = cursor.fetchall()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID   | Publisher Name\n")
            self.textbox.insert("end", "-" * 40 + "\n")

            for row in rows:
                name = str(row[1]) if row[1] else "N/A"
                line = f"{row[0]:<4} | {name:<30}\n"
                self.textbox.insert("end", line)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_publisher(self):
        pub_id = self.entry_id.get()
        if not pub_id: return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT publisher_name FROM publishers WHERE publisher_id = %s", (pub_id,))
            row = cursor.fetchone()
            if row:
                self.entry_name.delete(0, 'end')
                self.entry_name.insert(0, str(row[0]))
                messagebox.showinfo("Success", fix_heb("נתונים נטענו"))
            else:
                messagebox.showwarning("Not Found", fix_heb("לא נמצא"))
        except Exception as e:
            pass
        finally:
            conn.close()

    def insert_publisher(self):
        pub_id = self.entry_id.get()
        name = self.entry_name.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO publishers (publisher_id, publisher_name) VALUES (%s, %s)", (pub_id, name))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נוסף בהצלחה!"))
            self.clear_entries()
            self.read_publishers()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_publisher(self):
        pub_id = self.entry_id.get()
        name = self.entry_name.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE publishers SET publisher_name=%s WHERE publisher_id=%s", (name, pub_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("עודכן בהצלחה!"))
            self.clear_entries()
            self.read_publishers()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_publisher(self):
        pub_id = self.entry_id.get()
        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            # מחיקה פשוטה (תזרוק שגיאה אם יש ספרים מקושרים להוצאה הזו - שזה מצוין!)
            cursor.execute("DELETE FROM publishers WHERE publisher_id=%s", (pub_id,))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("נמחק בהצלחה!"))
            self.clear_entries()
            self.read_publishers()
        except Exception as e:
            messagebox.showerror("Error", fix_heb("שגיאת מפתח זר: לא ניתן למחוק הוצאה לאור שיש לה ספרים בקטלוג!"))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudPublishers()
    app.mainloop()