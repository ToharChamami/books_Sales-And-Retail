-- יצירת מבט 1: נקודת המבט של החנות (זמינות ספרים ומחירים בסניפים)
CREATE OR REPLACE VIEW v_store_inventory AS
SELECT
    b.title AS "Book Title",
    b.author AS "Author",
    b.current_price AS "Price",
    i.quantity AS "Stock Quantity"
FROM
    book b
JOIN
    inventory i ON b.book_id = i.book_id;

-- שאילתה 1 על המבט: הצגת כל הספרים שהמלאי שלהם נמוך מ-10 (לצורך הזמנה)
SELECT * FROM v_store_inventory
WHERE "Stock Quantity" < 10;

-- שאילתה 2 על המבט: הצגת הספרים היקרים ביותר (מעל 100 שקלים) שיש כרגע במלאי
SELECT * FROM v_store_inventory
WHERE "Price" > 100
ORDER BY "Price" DESC;

-- יצירת מבט 2: נקודת המבט של הלוגיסטיקה (מעקב אחרי הזמנות רכש)
CREATE OR REPLACE VIEW v_purchase_logistics AS
SELECT
    po.order_id AS "Order Number",
    po.order_date AS "Date",
    s.supplier_name AS "Supplier Name",
    e.first_name || ' ' || e.last_name AS "Ordered By"
FROM
    purchase_orders po
JOIN
    suppliers s ON po.supplier_id = s.supplier_id
JOIN
    employee e ON po.employee_id = e.e_id;

-- שאילתה 1: הצגת כל ההזמנות שבוצעו מספק מסוים
SELECT * FROM v_purchase_logistics
WHERE "Supplier Name" = 'Penguin';

-- שאילתה 2: הצגת כל ההזמנות מסודרות מהחדשה ביותר לישנה ביותר
SELECT * FROM v_purchase_logistics
ORDER BY "Date" DESC;