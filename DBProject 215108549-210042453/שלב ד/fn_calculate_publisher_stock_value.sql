CREATE OR REPLACE FUNCTION fn_calculate_publisher_stock_value(p_publisher_id INT)
RETURNS NUMERIC AS $$
DECLARE
    cur_books CURSOR FOR
        SELECT b.book_id, b.title, b.current_price, COALESCE(SUM(s.quantity), 0) as total_qty
        FROM book b
        LEFT JOIN stored_in s ON b.book_id = s.book_id
        WHERE b.publisher_id = p_publisher_id
        GROUP BY b.book_id, b.title, b.current_price;

    r_book RECORD;
    v_total_value NUMERIC := 0;
    v_publisher_exists INT;
BEGIN
    SELECT COUNT(*) INTO v_publisher_exists FROM publishers WHERE publisher_id = p_publisher_id;

    IF v_publisher_exists = 0 THEN
        RAISE EXCEPTION 'Publisher with ID % does not exist.', p_publisher_id;
    END IF;

    OPEN cur_books;
    LOOP
        FETCH cur_books INTO r_book;
        EXIT WHEN NOT FOUND;

        IF r_book.current_price IS NULL OR r_book.current_price <= 0 THEN
            RAISE NOTICE 'Book % (ID: %) has an invalid price. Skipping.', r_book.title, r_book.book_id;
        ELSE
            v_total_value := v_total_value + (r_book.current_price * r_book.total_qty);
        END IF;
    END LOOP;
    CLOSE cur_books;

    RETURN v_total_value;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred in execution: %', SQLERRM;
        RETURN -1;
END;
$$ LANGUAGE plpgsql;