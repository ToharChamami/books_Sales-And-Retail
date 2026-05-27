DELETE FROM customer
WHERE c_id = 904;

DELETE FROM inventory
WHERE quantity = 0 AND branch_id = 1;

DELETE FROM customer
WHERE c_id = 903;