import customtkinter as ctk
import sys
import subprocess

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fix_heb(text):
    return " ".join(text.split()[::-1])


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(fix_heb("מערכת ניהול רשת ספרים - מסך ראשי"))
        self.geometry("600x450")

        self.title_label = ctk.CTkLabel(self, text=fix_heb("ברוכים הבאים למערכת הרשת המאוחדת"),
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=40)

        # כפתור 1
        self.btn_crud = ctk.CTkButton(self, text=fix_heb("ניהול ספרים ומלאי (CRUD)"), font=ctk.CTkFont(size=16),
                                      width=300, height=45, command=self.open_crud_window)
        self.btn_crud.pack(pady=15)

        # כפתור 2
        self.btn_queries = ctk.CTkButton(self, text=fix_heb("דוחות ושאילתות מערכת"), font=ctk.CTkFont(size=16),
                                         width=300, height=45, command=self.open_queries_window)
        self.btn_queries.pack(pady=15)

        # כפתור 3
        self.btn_procedures = ctk.CTkButton(self, text=fix_heb("פעולות אוטומטיות (פרוצדורות)"),
                                            font=ctk.CTkFont(size=16), width=300, height=45,
                                            command=self.open_procedures_window)
        self.btn_procedures.pack(pady=15)

        # כפתור יציאה
        self.btn_exit = ctk.CTkButton(self, text=fix_heb("יציאה מהמערכת"), font=ctk.CTkFont(size=16), width=300,
                                      height=45, fg_color="#C21807", hover_color="#8B0000", command=self.destroy)
        self.btn_exit.pack(pady=30)

    # --- פונקציות הניווט (הפעם מריצות את הקבצים כתוכנות נפרדות) ---
    def open_crud_window(self):
        subprocess.Popen([sys.executable, "crud_books.py"])

    def open_queries_window(self):
        subprocess.Popen([sys.executable, "reports_window.py"])

    def open_procedures_window(self):
        subprocess.Popen([sys.executable, "procedures_window.py"])


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()