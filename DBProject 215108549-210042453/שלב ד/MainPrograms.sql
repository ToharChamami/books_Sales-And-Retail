-- תוכנית ראשית 1: עדכון שווי מלאי של הוצאה לאור
DO $$
DECLARE
    v_publisher_id INT := 1;
    v_total_value NUMERIC;
BEGIN
    v_total_value := fn_calculate_publisher_stock_value(v_publisher_id);
    RAISE NOTICE 'Stock value BEFORE price update: %', v_total_value;

    CALL sp_update_publisher_prices(v_publisher_id, 5.0);

    v_total_value := fn_calculate_publisher_stock_value(v_publisher_id);
    RAISE NOTICE 'Stock value AFTER price update: %', v_total_value;
END;
$$;

-- תוכנית ראשית 2: ביצוע מכירה ובדיקת חוסרים
DO $$
DECLARE
    v_ref_cursor refcursor;
    v_book_id INT;
    v_title VARCHAR;
    v_qty BIGINT;
BEGIN
    RAISE NOTICE '--- Processing Daily Sale ---';
    CALL sp_process_book_sale(101, 1);

    RAISE NOTICE '--- Checking For Low Stock ---';
    v_ref_cursor := fn_get_low_stock_books(20);

    FETCH NEXT FROM v_ref_cursor INTO v_book_id, v_title, v_qty;

    IF FOUND THEN
        RAISE NOTICE 'ALERT: Book "%" (ID: %) has low stock! Only % copies left.', v_title, v_book_id, v_qty;
    ELSE
        RAISE NOTICE 'All books have sufficient stock today.';
    END IF;

    CLOSE v_ref_cursor;
END;
$$;