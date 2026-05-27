
SELECT C_ID, first_name, last_name, Email
FROM Customer
WHERE C_ID IN (
    SELECT C_ID FROM Sale WHERE S_ID IN (
        SELECT S_ID FROM Sale_Item WHERE Book_ID IN (
            SELECT Book_ID FROM Book WHERE G_ID = 1
        )
    )
)
ORDER BY first_name, last_name;

SELECT DISTINCT c.C_ID, c.first_name, c.last_name, b.Title
FROM Customer c
JOIN Sale s ON c.C_ID = s.C_ID
JOIN Sale_Item si ON s.S_ID = si.S_ID
JOIN Book b ON si.Book_ID = b.Book_ID
WHERE b.G_ID = 1
ORDER BY c.first_name, c.last_name;

SELECT s.S_ID, s.Sale_Date, s.Total_Amount, br.Branch_Name, e.First_Name, e.Last_Name
FROM Sale s
JOIN Employee e ON s.E_ID = e.E_ID
JOIN Branch br ON e.Branch_ID = br.Branch_ID
WHERE s.Total_Amount > (SELECT AVG(Total_Amount) FROM Sale)
ORDER BY s.Total_Amount DESC;

SELECT s.S_ID, s.Sale_Date, s.Total_Amount, br.Branch_Name, e.First_Name, e.Last_Name
FROM Sale s
JOIN Employee e ON s.E_ID = e.E_ID
JOIN Branch br ON e.Branch_ID = br.Branch_ID
JOIN (SELECT AVG(Total_Amount) AS AvgAmount FROM Sale) AS DerivedTable
ON s.Total_Amount > DerivedTable.AvgAmount
ORDER BY s.Total_Amount DESC;

SELECT b.Book_ID, b.Title, b.Price, g.Genre_Name, b.Author
FROM Book b
JOIN Genre g ON b.G_ID = g.G_ID
WHERE b.Price = (
    SELECT MAX(b2.Price)
    FROM Book b2
    WHERE b2.G_ID = b.G_ID
)
ORDER BY g.Genre_Name;

SELECT b.Book_ID, b.Title, b.Price, g.Genre_Name, b.Author
FROM Book b
JOIN Genre g ON b.G_ID = g.G_ID
JOIN (
    SELECT G_ID, MAX(Price) AS MaxPrice
    FROM Book
    GROUP BY G_ID
) AS MaxBooks ON b.G_ID = MaxBooks.G_ID AND b.Price = MaxBooks.MaxPrice
ORDER BY g.Genre_Name;

SELECT br.Branch_Name, br.City, b.Title, b.Author, i.Quantity
FROM Inventory i
JOIN Branch br ON i.Branch_ID = br.Branch_ID
JOIN Book b ON i.Book_ID = b.Book_ID
WHERE i.Quantity = 0 AND br.City = 'Tel Aviv'
ORDER BY br.Branch_Name;

SELECT br.Branch_Name, br.City, b.Title, b.Author, i.Quantity
FROM Inventory i
JOIN Book b ON i.Book_ID = b.Book_ID
JOIN Branch br ON i.Branch_ID = br.Branch_ID
WHERE i.Quantity = 0 AND i.Branch_ID IN (
    SELECT Branch_ID
    FROM Branch
    WHERE City = 'Tel Aviv'
)
ORDER BY br.Branch_Name;

SELECT
    EXTRACT(YEAR FROM s.Sale_Date) AS Sale_Year,
    EXTRACT(MONTH FROM s.Sale_Date) AS Sale_Month,
    br.Branch_Name,
    COUNT(s.S_ID) AS Total_Sales_Count,
    SUM(s.Total_Amount) AS Total_Revenue
FROM Sale s
JOIN Employee e ON s.E_ID = e.E_ID
JOIN Branch br ON e.Branch_ID = br.Branch_ID
GROUP BY
    EXTRACT(YEAR FROM s.Sale_Date),
    EXTRACT(MONTH FROM s.Sale_Date),
    br.Branch_Name
ORDER BY
    Sale_Year DESC,
    Sale_Month DESC,
    Total_Revenue DESC;

SELECT e.E_ID, e.First_Name, e.Last_Name, br.Branch_Name, COUNT(s.S_ID) AS Number_Of_Sales, SUM(s.Total_Amount) AS Total_Generated_Revenue
FROM Employee e
JOIN Sale s ON e.E_ID = s.E_ID
JOIN Branch br ON e.Branch_ID = br.Branch_ID
GROUP BY e.E_ID, e.First_Name, e.Last_Name, br.Branch_Name
HAVING SUM(s.Total_Amount) > 5000.00
ORDER BY Total_Generated_Revenue DESC;

SELECT c.C_ID, c.Full_Name, c.Email, c.Join_Date
FROM Customer c
WHERE c.Join_Date < '2026-01-01'
  AND NOT EXISTS (
      SELECT 1
      FROM Sale s
      WHERE s.C_ID = c.C_ID
  )
ORDER BY c.Join_Date ASC;

SELECT p.Publisher_Name, g.Genre_Name, COUNT(DISTINCT b.Book_ID) AS Distinct_Books_Count, SUM(i.Quantity) AS Total_Stock_In_Network
FROM Book b
JOIN Publisher p ON b.P_ID = p.P_ID
JOIN Genre g ON b.G_ID = g.G_ID
JOIN Inventory i ON b.Book_ID = i.Book_ID
GROUP BY p.Publisher_Name, g.Genre_Name
ORDER BY p.Publisher_Name, Total_Stock_In_Network DESC;

