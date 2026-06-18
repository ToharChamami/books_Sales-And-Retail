CREATE OR REPLACE FUNCTION trg_log_price_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.current_price <> OLD.current_price THEN
        INSERT INTO price_audit_log (book_id, old_price, new_price)
        VALUES (OLD.book_id, OLD.current_price, NEW.current_price);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_book_price_update
AFTER UPDATE OF current_price ON book
FOR EACH ROW
EXECUTE FUNCTION trg_log_price_change();
