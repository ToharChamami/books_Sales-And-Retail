-- === 1. הכנת הטבלאות וקישורן ===
-- הוספת העמודות החדשות מהמערכת השנייה לטבלת הספרים שלנו
ALTER TABLE book
ADD COLUMN publication_year INT,
ADD COLUMN publisher_id INT;

-- יצירת מפתח זר שמקשר את הספרים שלנו להוצאות לאור
ALTER TABLE book
ADD CONSTRAINT fk_publisher
FOREIGN KEY (publisher_id)
REFERENCES publishers(publisher_id);

-- === 2. העברת נתונים חסרים (כדי למנוע שגיאות מפתח זר) ===
-- העברת כל הספרים של הזוג השני שחסרים אצלנו, תוך מתן מחיר ברירת מחדל של 50
INSERT INTO book (book_id, title, author, publication_year, publisher_id, current_price)
SELECT book_id, title, author, publication_year, publisher_id, 50
FROM books
WHERE book_id NOT IN (SELECT book_id FROM book);

-- העברת כל העובדים החדשים שחסרים אצלנו (מותאם לעמודת e_id שלך)
INSERT INTO employee (e_id, first_name, last_name)
SELECT employee_id, first_name, last_name
FROM employees
WHERE employee_id NOT IN (SELECT e_id FROM employee);

-- === 3. הניקיון הסופי: מחיקת הטבלאות הכפולות וחיבור החוטים מחדש ===
-- טיפול בספרים
DROP TABLE IF EXISTS books CASCADE;
ALTER TABLE stored_in ADD CONSTRAINT fk_book_unified FOREIGN KEY (book_id) REFERENCES book(book_id);

-- טיפול בעובדים
DROP TABLE IF EXISTS employees CASCADE;
ALTER TABLE purchase_orders ADD CONSTRAINT fk_emp_unified FOREIGN KEY (employee_id) REFERENCES employee(e_id);

DROP TABLE IF EXISTS publisher CASCADE;