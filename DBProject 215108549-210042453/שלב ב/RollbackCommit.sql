--rollback
SELECT book_id, title, current_price FROM book WHERE book_id = 1;

BEGIN;
UPDATE book SET current_price = current_price + 50 WHERE book_id = 1;

SELECT book_id, title, current_price FROM book WHERE book_id = 1;

ROLLBACK;

SELECT book_id, title, current_price FROM book WHERE book_id = 1;

--commit
SELECT book_id, title, current_price FROM book WHERE book_id = 2;

BEGIN;
UPDATE book SET current_price = current_price - 10 WHERE book_id = 2;

SELECT book_id, title, current_price FROM book WHERE book_id = 2;

COMMIT;

SELECT book_id, title, current_price FROM book WHERE book_id = 2;

