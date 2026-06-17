import customtkinter as ctk
from tkinter import messagebox
import db_connection

# הגדרות עיצוב כלליות
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class ProceduresWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("הפעלת פרוצדורות - שלב ד"))
        self.geometry("600x400")

        ctk.CTkLabel(self, text=fix_heb("פעולות אוטומטיות בבסיס הנתונים"), font=("Arial", 20, "bold")).pack(pady=20)

        # === מסגרת 1: ביצוע מכירה ===
        self.frame_sale = ctk.CTkFrame(self)
        self.frame_sale.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.frame_sale, text=fix_heb("1. ביצוע מכירת ספר בקופה"), font=("Arial", 16, "bold")).pack(pady=5)

        # שדות קלט למכירה
        self.entry_book_id = ctk.CTkEntry(self.frame_sale, placeholder_text="Book ID (מקט)")
        self.entry_book_id.pack(side="left", padx=10, pady=10)

        self.entry_qty = ctk.CTkEntry(self.frame_sale, placeholder_text="Quantity (כמות)")
        self.entry_qty.pack(side="left", padx=10, pady=10)

        self.btn_sale = ctk.CTkButton(self.frame_sale, text=fix_heb("בצע מכירה"), fg_color="#27AE60",
                                      hover_color="#2ECC71", command=self.run_sale)
        self.btn_sale.pack(side="left", padx=10, pady=10)

        # === מסגרת 2: עדכון מחירים ===
        self.frame_price = ctk.CTkFrame(self)
        self.frame_price.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.frame_price, text=fix_heb("2. עדכון מחירים גורף להוצאה לאור"),
                     font=("Arial", 16, "bold")).pack(pady=5)

        # שדות קלט לעדכון
        self.entry_pub_id = ctk.CTkEntry(self.frame_price, placeholder_text="Publisher ID")
        self.entry_pub_id.pack(side="left", padx=10, pady=10)

        self.entry_percent = ctk.CTkEntry(self.frame_price, placeholder_text="Percent % (אחוז)")
        self.entry_percent.pack(side="left", padx=10, pady=10)

        self.btn_price = ctk.CTkButton(self.frame_price, text=fix_heb("עדכן מחירים"), fg_color="#E67E22",
                                       hover_color="#D35400", command=self.run_price_update)
        self.btn_price.pack(side="left", padx=10, pady=10)

    # ================= הפעלת הפרוצדורות מול השרת =================

    def run_sale(self):
        book_id_str = self.entry_book_id.get()
        qty_str = self.entry_qty.get()

        if not book_id_str or not qty_str:
            messagebox.showwarning("חסרים נתונים", fix_heb("נא להזין מקט וכמות למכירה"))
            return

        # המרה וודאית למספרים שלמים
        try:
            book_id = int(book_id_str)
            qty = int(qty_str)
        except ValueError:
            messagebox.showerror("שגיאה", fix_heb("המקט והכמות חייבים להיות מספרים!"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            # שליחה לשרת כמספרים אמיתיים
            cursor.execute("CALL sp_process_book_sale(%s, %s);", (book_id, qty))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("המכירה בוצעה בהצלחה והמלאי הופחת!"))
            self.entry_book_id.delete(0, 'end')
            self.entry_qty.delete(0, 'end')
        except Exception as e:
            # כאן אמורה לקפוץ השגיאה של החוסר במלאי מהשרת
            conn.rollback()
            messagebox.showerror("Server Exception", f"הפעולה נכשלה:\n{e}")
        finally:
            if conn: conn.close()

    def run_price_update(self):
        pub_id = self.entry_pub_id.get()
        percent = self.entry_percent.get()

        if not pub_id or not percent:
            messagebox.showwarning("חסרים נתונים", fix_heb("נא להזין מזהה הוצאה ואחוז העלאה"))
            return

        conn = db_connection.get_connection()
        try:
            cursor = conn.cursor()
            # קריאה לפרוצדורה שכתבנו בשלב 4
            cursor.execute("CALL sp_update_publisher_prices(%s, %s);", (pub_id, percent))
            conn.commit()
            messagebox.showinfo("Success", fix_heb("מחירי הספרים עודכנו בהצלחה!"))
            self.entry_pub_id.delete(0, 'end')
            self.entry_percent.delete(0, 'end')
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Server Exception", f"הפעולה נכשלה:\n{e}")
        finally:
            if conn: conn.close()


if __name__ == "__main__":
    app = ProceduresWindow()
    app.mainloop()