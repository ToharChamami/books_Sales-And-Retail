import csv
import random
from faker import Faker

fake = Faker()


def generate_csvs():
    # 1. טבלת סניפים (Branch) - 500 רשומות
    with open('Branch.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Branch_ID', 'Branch_Name', 'City', 'Address', 'Manager_ID'])
        for i in range(1, 501):
            # Manager_ID יהיה NULL ב-15% מהמקרים
            manager_id = "" if random.random() < 0.15 else random.randint(100, 999)
            writer.writerow([i, f"{fake.city()} Branch", fake.city(), fake.street_address(), manager_id])
    print("Branch.csv created successfully with 500 rows.")

    # 2. טבלת הוצאות לאור (Publisher) - 500 רשומות
    with open('Publisher.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['P_ID', 'Publisher_Name'])
        for i in range(1, 501):
            writer.writerow([i, f"{fake.company()} Publishing"])
    print("Publisher.csv created successfully with 500 rows.")

    # 3. טבלת מלאי (Inventory) - 500 רשומות
    with open('Inventory.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Branch_ID', 'Book_ID', 'Quantity'])

        # נניח שיש לנו 500 סניפים ו-500 ספרים (מהסקריפט הקודם שלך)
        for _ in range(500):
            branch_id = random.randint(1, 500)
            book_id = random.randint(1, 500)
            quantity = random.randint(0, 100)  # 0 מדמה חוסר במלאי
            writer.writerow([branch_id, book_id, quantity])
    print("Inventory.csv created successfully with 500 rows.")


if __name__ == "__main__":
    generate_csvs()