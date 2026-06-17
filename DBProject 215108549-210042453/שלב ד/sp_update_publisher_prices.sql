CREATE OR REPLACE PROCEDURE sp_update_publisher_prices(p_publisher_id INT, p_percent_increase NUMERIC)
LANGUAGE plpgsql AS $$
DECLARE
    v_rows_updated INT;
BEGIN
    UPDATE book
    SET current_price = current_price * (1 + (p_percent_increase / 100.0))
    WHERE publisher_id = p_publisher_id;

    GET DIAGNOSTICS v_rows_updated = ROW_COUNT;

    IF v_rows_updated = 0 THEN
        RAISE EXCEPTION 'No books found for publisher ID % to update.', p_publisher_id;
    ELSE
        RAISE NOTICE 'Successfully updated prices for % books.', v_rows_updated;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error during price update: %', SQLERRM;
END;
$$;