CREATE OR REPLACE PROCEDURE sp_process_book_sale(p_book_id INT, p_qty_sold INT)
LANGUAGE plpgsql AS $$
DECLARE
    v_current_stock INT;
BEGIN
    SELECT quantity INTO v_current_stock
    FROM inventory
    WHERE book_id = p_book_id;

    IF v_current_stock IS NULL THEN
        v_current_stock := 0;
    END IF;

    IF v_current_stock < p_qty_sold THEN
        RAISE EXCEPTION 'Not enough stock to complete the sale. In stock: %, Requested: %', v_current_stock, p_qty_sold;
    END IF;

    UPDATE inventory
    SET quantity = quantity - p_qty_sold
    WHERE book_id = p_book_id;

    RAISE NOTICE 'Sale processed successfully! Sold % copies of book ID %.', p_qty_sold, p_book_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Sale Transaction failed: %', SQLERRM;
END;
$$;