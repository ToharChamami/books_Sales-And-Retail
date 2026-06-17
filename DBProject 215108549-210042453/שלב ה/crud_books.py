import customtkinter as ctk
from tkinter import messagebox
import db_connection

# הגדרות עיצוב כלליות
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class CrudWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("ניהול ספרים - CRUD"))
        self.geometry("900x550")

        # --- יצירת חלוקה למסך: צד ימין לטופס, צד שמאל לתצוגה ---
        self.form_frame = ctk.CTkFrame(self, width=300)
        self.form_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.display_frame = ctk.CTkFrame(self, width=500)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # --- בניית הטופס (צד ימין) ---
        ctk.CTkLabel(self.form_frame, text=fix_heb("טופס פרטי ספר"), font=("Arial", 20, "bold")).pack(pady=10)

        # שדה מזהה ספר (ID)
        ctk.CTkLabel(self.form_frame, text=fix_heb("מקט ספר (ID):")).pack(anchor="e", padx=10)
        self.entry_id = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_id.pack(fill="x", padx=10, pady=5)

        # שדה כותרת
        ctk.CTkLabel(self.form_frame, text=fix_heb("שם הספר:")).pack(anchor="e", padx=10)
        self.entry_title = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_title.pack(fill="x", padx=10, pady=5)

        # שדה מחבר
        ctk.CTkLabel(self.form_frame, text=fix_heb("שם המחבר:")).pack(anchor="e", padx=10)
        self.entry_author = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_author.pack(fill="x", padx=10, pady=5)

        # שדה מחיר
        ctk.CTkLabel(self.form_frame, text=fix_heb("מחיר נוכחי:")).pack(anchor="e", padx=10)
        self.entry_price = ctk.CTkEntry(self.form_frame, justify="right")
        self.entry_price.pack(fill="x", padx=10, pady=5)

        # --- כפתורי הפעולות (CRUD) ---
        self.btn_load = ctk.CTkButton(self.form_frame, text=fix_heb("1. הבא נתונים לעדכון"), fg_color="#E67E22",
                                      hover_color="#D35400", command=self.load_book_by_id)
        self.btn_load.pack(fill="x", padx=10, pady=10)

        self.btn_insert = ctk.CTkButton(self.form_frame, text=fix_heb("2. הוסף ספר חדש"), fg_color="#27AE60",
                                        hover_color="#2ECC71", command=self.insert_book)
        self.btn_insert.pack(fill="x", padx=10, pady=5)

        self.btn_update = ctk.CTkButton(self.form_frame, text=fix_heb("3. שמור עדכונים"), fg_color="#2980B9",
                                        hover_color="#3498DB", command=self.update_book)
        self.btn_update.pack(fill="x", padx=10, pady=5)

        self.btn_delete = ctk.CTkButton(self.form_frame, text=fix_heb("4. מחק ספר"), fg_color="#C0392B",
                                        hover_color="#E74C3C", command=self.delete_book)
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        # --- תצוגת הנתונים (צד שמאל) ---
        ctk.CTkLabel(self.display_frame, text=fix_heb("רשימת הספרים במערכת"), font=("Arial", 20, "bold")).pack(pady=10)

        self.btn_refresh = ctk.CTkButton(self.display_frame, text=fix_heb("רענן רשימה (READ)"), command=self.read_books)
        self.btn_refresh.pack(pady=5)

        self.textbox = ctk.CTkTextbox(self.display_frame, width=450, height=350, font=("Courier", 14))
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        # טעינה ראשונית של הנתונים כשהחלון נפתח
        self.read_books()

    # ================== פונקציות ה-CRUD מול ה-DB ==================

    def clear_entries(self):
        self.entry_id.delete(0, 'end')
        self.entry_title.delete(0, 'end')
        self.entry_author.delete(0, 'end')
        self.entry_price.delete(0, 'end')

    def read_books(self):
        """שליפת נתונים - R"""
        conn = db_connection.get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            # שליפה שמציגה את הנתונים בצורה יפה (שולמית תאהב את זה)
            cursor.execute("SELECT book_id, title, author, current_price FROM book ORDER BY book_id DESC LIMIT 20;")
            rows = cursor.fetchall()

            self.textbox.delete("1.0", "end")  # ניקוי המסך
            self.textbox.insert("end", "ID   | Title                     | Author          | Price\n")
            self.textbox.insert("end", "-" * 60 + "\n")

            for row in rows:
                line = f"{row[0]:<4} | {str(row[1])[:23]:<25} | {str(row[2])[:13]:<15} | ₪{row[3]}\n"
                self.textbox.insert("end", line)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_book_by_id(self):
        """משיכת נתונים לשדות לפני עדכון (לפי דרישת שולמית)"""
        book_id = self.entry_id.get()
        if not book_id:
            messagebox.showwarning("Warning", fix_heb("נא להזין מקט ספר"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title, author, current_price FROM book WHERE book_id = %s", (book_id,))
            row = cursor.fetchone()

            if row:
                self.entry_title.delete(0, 'end')
                self.entry_title.insert(0, str(row[0]))

                self.entry_author.delete(0, 'end')
                self.entry_author.insert(0, str(row[1]) if row[1] else "")

                self.entry_price.delete(0, 'end')
                self.entry_price.insert(0, str(row[2]))

                messagebox.showinfo("Success", fix_heb("הנתונים נטענו בהצלחה. ניתן לערוך ולשמור."))
            else:
                messagebox.showwarning("Not Found", fix_heb("הספר לא נמצא"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def insert_book(self):
        """הוספת נתונים - C"""
        book_id = self.entry_id.get()
        title = self.entry_title.get()
        author = self.entry_author.get()
        price = self.entry_price.get()

        if not book_id or not title:
            messagebox.showwarning("Warning", fix_heb("חובה להזין מקט ושם ספר"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO book (book_id, title, author, current_price) VALUES (%s, %s, %s, %s)",
                           (book_id, title, author, price))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("הספר נוסף בהצלחה!"))
            self.clear_entries()
            self.read_books()  # רענון המסך
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def update_book(self):
        """עדכון נתונים - U"""
        book_id = self.entry_id.get()
        title = self.entry_title.get()
        author = self.entry_author.get()
        price = self.entry_price.get()

        if not book_id:
            messagebox.showwarning("Warning", fix_heb("חובה להזין מקט לעדכון"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE book SET title=%s, author=%s, current_price=%s WHERE book_id=%s",
                           (title, author, price, book_id))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("הספר עודכן בהצלחה!"))
            self.clear_entries()
            self.read_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_book(self):
        """מחיקת נתונים - D"""
        book_id = self.entry_id.get()
        if not book_id:
            messagebox.showwarning("Warning", fix_heb("נא להזין מקט למחיקה"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            # 1. קודם כל נמחק את הספר מטבלת המלאי (לפתרון בעיית המפתח הזר)
            cursor.execute("DELETE FROM inventory WHERE book_id=%s", (book_id,))

            # 2. למקרה ששינית לו מחיר לפני המחיקה, נמחק גם מטבלת הלוג
            cursor.execute("DELETE FROM price_audit_log WHERE book_id=%s", (book_id,))

            # 3. עכשיו שהשטח נקי, אפשר למחוק את הספר עצמו!
            cursor.execute("DELETE FROM book WHERE book_id=%s", (book_id,))

            conn.commit()
            messagebox.showinfo("Success", fix_heb("הספר נמחק בהצלחה!"))
            self.clear_entries()
            self.read_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CrudWindow()
    app.mainloop()