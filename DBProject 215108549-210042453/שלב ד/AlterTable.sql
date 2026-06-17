-- טבלה שנוצרה לצורך שמירת היסטוריית מחירים עבור הטריגר
CREATE TABLE price_audit_log (
    log_id SERIAL PRIMARY KEY,
    book_id INT,
    old_price NUMERIC,
    new_price NUMERIC,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);