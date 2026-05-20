# גרסת פייתון קלה
FROM python:3.10-slim

# הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# העתקת כל קבצי הפרויקט פנימה
COPY . .

# התקנת כל הספריות הדרושות
RUN pip install -r requirements.txt

# הפקודה שמריצה את הפרויקט (יש לשנות את main.py לשם הקובץ שלך)
CMD ["python", "main.py"]