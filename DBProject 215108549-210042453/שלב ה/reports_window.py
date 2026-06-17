import customtkinter as ctk
from tkinter import messagebox
import db_connection

# הגדרות עיצוב כלליות
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class ReportsWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(fix_heb("מערכת דוחות ושאילתות"))
        self.geometry("800x500")

        # כותרת המסך
        ctk.CTkLabel(self, text=fix_heb("דוחות מערכת (שאילתות שלב ב)"), font=("Arial", 24, "bold")).pack(pady=20)

        # אזור הכפתורים
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        # שאילתה 1: מציגה ספרים כולל שם ההוצאה לאור (JOIN למניעת הצגת ID)
        self.btn_query1 = ctk.CTkButton(self.btn_frame, text=fix_heb("דוח ספרים והוצאות לאור (JOIN)"), width=250,
                                        command=self.run_query_1)
        self.btn_query1.pack(side="right", padx=20)

        # שאילתה 2: מציגה את כמות המלאי הכוללת לפי סניף
        self.btn_query2 = ctk.CTkButton(self.btn_frame, text=fix_heb("דוח מלאי מרוכז לפי סניפים"), width=250,
                                        command=self.run_query_2)
        self.btn_query2.pack(side="left", padx=20)

        # תצוגת התוצאות
        self.textbox = ctk.CTkTextbox(self, width=700, height=300, font=("Courier", 14))
        self.textbox.pack(pady=20, fill="both", expand=True)

    def run_query_1(self):
        """מריץ שאילתה שמחברת את טבלת הספרים וטבלת ההוצאות לאור"""
        conn = db_connection.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # מביאים את שם ההוצאה לאור במקום את ה-ID שלה! (דרישה של שולמית)
            query = """
                SELECT b.book_id, b.title, p.publisher_name, b.current_price
                FROM book b
                LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
                ORDER BY b.book_id ASC LIMIT 20;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "ID   | Book Title                | Publisher Name      | Price\n")
            self.textbox.insert("end", "-" * 70 + "\n")

            for row in rows:
                publisher = str(row[2])[:18] if row[2] else "N/A"
                line = f"{row[0]:<4} | {str(row[1])[:23]:<25} | {publisher:<19} | ₪{row[3]}\n"
                self.textbox.insert("end", line)

        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {e}")
        finally:
            conn.close()

    def run_query_2(self):
        """מריץ שאילתה שמקבצת מלאי לפי סניפים"""
        conn = db_connection.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            query = """
                SELECT branch_id, SUM(quantity) as total_items
                FROM inventory
                GROUP BY branch_id
                ORDER BY branch_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "Branch ID | Total Books in Stock\n")
            self.textbox.insert("end", "-" * 30 + "\n")

            for row in rows:
                line = f"Branch {row[0]:<2} | {row[1]} items\n"
                self.textbox.insert("end", line)

        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = ReportsWindow()
    app.mainloop()