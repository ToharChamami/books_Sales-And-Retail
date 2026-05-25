-- אינדקס 1: חיפוש מהיר לפי תאריך מכירה
CREATE INDEX idx_sale_date ON sale(sale_date);

-- אינדקס 2: חיפוש מהיר לפי שם הספר
CREATE INDEX idx_book_title ON book(title);

-- אינדקס 3: חיפוש מהיר לפי אימייל לקוח
CREATE INDEX idx_customer_email ON customer(email);