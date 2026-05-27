
UPDATE book
SET current_price = current_price * 1.10
WHERE g_id = 1;

UPDATE inventory
SET quantity = quantity + 10
WHERE branch_id = 1 AND book_id = 1;

UPDATE customer
SET email = 'yossi.new.email@email.com'
WHERE c_id = 901;