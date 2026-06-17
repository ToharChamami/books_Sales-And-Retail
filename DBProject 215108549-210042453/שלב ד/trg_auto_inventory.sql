CREATE OR REPLACE FUNCTION trg_auto_init_inventory()
RETURNS TRIGGER AS $$
DECLARE
    v_first_branch_id INT;
BEGIN
    SELECT branch_id INTO v_first_branch_id FROM branch LIMIT 1;

    IF v_first_branch_id IS NULL THEN
        v_first_branch_id := 1;
    END IF;

    INSERT INTO inventory (branch_id, book_id, quantity)
    VALUES (v_first_branch_id, NEW.book_id, 0);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_new_book_insert
AFTER INSERT ON book
FOR EACH ROW
EXECUTE FUNCTION trg_auto_init_inventory();