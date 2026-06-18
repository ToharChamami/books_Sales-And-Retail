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

        self.title(fix_heb("מערכת ERP מלאה - רשת הספרים"))
        self.geometry("1100x750")

        self.title_label = ctk.CTkLabel(self, text=fix_heb("לוח בקרה ראשי (ERP)"),
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=20)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        # --- טור 1: קטלוג וספרים ---
        ctk.CTkLabel(self.btn_frame, text=fix_heb("קטלוג ומלאי"), font=ctk.CTkFont(size=18, weight="bold")).grid(row=0,
                                                                                                                 column=3,
                                                                                                                 pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("ספרים (Book)"), width=220, height=40,
                      command=lambda: self.open_window("crud_books.py")).grid(row=1, column=3, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("הוצאות לאור (Publishers)"), width=220, height=40,
                      command=lambda: self.open_window("crud_publishers.py")).grid(row=2, column=3, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("ז'אנרים (Genre)"), width=220, height=40,
                      command=lambda: self.open_window("crud_genre.py")).grid(row=3, column=3, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("מלאי (Inventory)"), width=220, height=40,
                      command=lambda: self.open_window("crud_inventory.py")).grid(row=4, column=3, padx=15, pady=10)

        # --- טור 2: ארגון ומשאבי אנוש ---
        ctk.CTkLabel(self.btn_frame, text=fix_heb("ארגון ומשאבים"), font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=2, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("סניפים (Branch)"), width=220, height=40,
                      command=lambda: self.open_window("crud_branches.py")).grid(row=1, column=2, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("עובדים (Employee)"), width=220, height=40,
                      command=lambda: self.open_window("crud_employee.py")).grid(row=2, column=2, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("תפקידים (Position)"), width=220, height=40,
                      command=lambda: self.open_window("crud_position.py")).grid(row=3, column=2, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("לקוחות (Customer)"), width=220, height=40,
                      command=lambda: self.open_window("crud_customer.py")).grid(row=4, column=2, padx=15, pady=10)

        # --- טור 3: לוגיסטיקה (ספקים ומחסנים) ---
        ctk.CTkLabel(self.btn_frame, text=fix_heb("לוגיסטיקה"), font=ctk.CTkFont(size=18, weight="bold")).grid(row=0,
                                                                                                               column=1,
                                                                                                               pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("מחסנים (Warehouses)"), width=220, height=40,
                      command=lambda: self.open_window("crud_warehouses.py")).grid(row=1, column=1, padx=15, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("ספקים (Suppliers)"), width=220, height=40,
                      command=lambda: self.open_window("crud_suppliers.py")).grid(row=2, column=1, padx=15, pady=10)

        # --- טור 4: דוחות מיוחדים (שלב ב+ד) ---
        ctk.CTkLabel(self.btn_frame, text=fix_heb("פעולות מתקדמות"), font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("דוחות מערכת (READ)"), width=220, height=40, fg_color="#E67E22",
                      hover_color="#D35400", command=lambda: self.open_window("reports_window.py")).grid(row=1,
                                                                                                         column=0,
                                                                                                         padx=15,
                                                                                                         pady=10)
        ctk.CTkButton(self.btn_frame, text=fix_heb("הפעלת פרוצדורות שרת"), width=220, height=40, fg_color="#E67E22",
                      hover_color="#D35400", command=lambda: self.open_window("procedures_window.py")).grid(row=2,
                                                                                                            column=0,
                                                                                                            padx=15,
                                                                                                            pady=10)

        # יציאה
        self.btn_exit = ctk.CTkButton(self, text=fix_heb("יציאה מהמערכת"), font=ctk.CTkFont(size=16), width=300,
                                      height=45, fg_color="#C21807", hover_color="#8B0000", command=self.destroy)
        self.btn_exit.pack(pady=40)

    def open_window(self, filename):
        subprocess.Popen([sys.executable, filename])


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()