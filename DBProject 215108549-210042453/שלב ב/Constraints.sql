-- אילוץ 1: מחיר ספר חייב להיות חיובי
ALTER TABLE book ADD CONSTRAINT chk_positive_price CHECK (current_price > 0);

-- אילוץ 2: כמות במלאי לא יכולה להיות שלילית
ALTER TABLE inventory ADD CONSTRAINT chk_non_negative_quantity CHECK (quantity >= 0);

-- אילוץ 3: אימייל של לקוח חייב להכיל שטרודל
ALTER TABLE customer ADD CONSTRAINT chk_valid_email CHECK (email LIKE '%@%');