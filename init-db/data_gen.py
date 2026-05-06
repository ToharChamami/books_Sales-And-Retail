import random
from faker import Faker

fake = Faker()
output_file = '../DBProject 215108549-210042453/שלב א/02-seed_data.sql'

def generate_data():
    with open(output_file, 'w', encoding='utf-8') as f:
        # הגדרת כמויות
        NUM_GENRES = 500
        NUM_BOOKS = 500
        NUM_CUSTOMERS = 500
        NUM_SALES = 20000        # טבלה גדולה 1
        NUM_SALE_ITEMS = 25000   # טבלה גדולה 2

        f.write("-- Cleanup (Optional)\nTRUNCATE Sale_Item, Inventory, Sale, Book, Employee, Customer, Branch, Publisher, Genre CASCADE;\n\n")

        # 1. Genres (500)
        f.write("-- Inserting Genres\n")
        for i in range(1, NUM_GENRES + 1):
            f.write(f"INSERT INTO Genre (G_ID, Genre_Name) VALUES ({i}, '{fake.word().capitalize()}');\n")

        # 2. Customers (500) עם ערכי NULL רנדומליים בטלפון/אימייל
        f.write("\n-- Inserting Customers\n")
        for i in range(1, NUM_CUSTOMERS + 1):
            phone = f"'{fake.phone_number()}'" if random.random() > 0.1 else "NULL"
            email = f"'{fake.email()}'" if random.random() > 0.1 else "NULL"
            f.write(f"INSERT INTO Customer (C_ID, Full_Name, Phone, Email, Join_Date) VALUES ({i}, '{fake.name()}', {phone}, {email}, '{fake.date_this_decade()}');\n")

        # 3. Books (500)
        f.write("\n-- Inserting Books\n")
        for i in range(1, NUM_BOOKS + 1):
            price = round(random.uniform(20.0, 150.0), 2)
            g_id = random.randint(1, NUM_GENRES)
            f.write(f"INSERT INTO Book (Book_ID, Title, Author, Price, G_ID) VALUES ({i}, '{fake.catch_phrase()}', '{fake.name()}', {price}, {g_id});\n")

        # 4. Sales (20,000) - טבלה גדולה
        f.write("\n-- Inserting Sales (Large Table)\n")
        for i in range(1, NUM_SALES + 1):
            c_id = random.randint(1, NUM_CUSTOMERS)
            amount = round(random.uniform(20.0, 500.0), 2)
            # NULL רנדומלי בשיטת תשלום
            method = f"'{random.choice(['Credit Card', 'Cash', 'Bit'])}'" if random.random() > 0.1 else "NULL"
            f.write(f"INSERT INTO Sale (S_ID, Sale_Date, Total_Amount, Payment_Method, C_ID) VALUES ({i}, '{fake.date_this_year()}', {amount}, {method}, {c_id});\n")

        # 5. Sale_Item (25,000) - טבלה גדולה
        f.write("\n-- Inserting Sale Items (Large Table)\n")
        for i in range(1, NUM_SALE_ITEMS + 1):
            s_id = random.randint(1, NUM_SALES)
            b_id = random.randint(1, NUM_BOOKS)
            qty = random.randint(1, 5)
            f.write(f"INSERT INTO Sale_Item (S_ID, Book_ID, Quantity) VALUES ({s_id}, {b_id}, {qty}) ON CONFLICT DO NOTHING;\n")

    print(f"Success! {output_file} created with thousands of records.")

if __name__ == "__main__":
    generate_data()