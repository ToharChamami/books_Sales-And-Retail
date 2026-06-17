CREATE OR REPLACE FUNCTION fn_get_low_stock_books(p_min_quantity INT)
RETURNS refcursor AS $$
DECLARE
    ref_cur refcursor := 'my_cursor';
BEGIN
    OPEN ref_cur FOR
        SELECT b.book_id, b.title, COALESCE(SUM(i.quantity), 0) AS total_qty
        FROM book b
        LEFT JOIN inventory i ON b.book_id = i.book_id
        GROUP BY b.book_id, b.title
        HAVING COALESCE(SUM(i.quantity), 0) < p_min_quantity
        ORDER BY total_qty ASC;

    RETURN ref_cur;
END;
$$ LANGUAGE plpgsql;