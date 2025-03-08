"""To Download and run the Project follow SetupGuide.txt"""

---ניתן להישתמש בשליחת בקשה עם הכתובת אייפי ופורט שנקבל לדף הבית---

Admin     : http://127.0.0.1:8000/admin/

Home page : http://127.0.0.1:8000/

API       : http://127.0.0.1:8000/api/


📂 Users API
api/users/register/	                        📩 הרשמה - POST עם username, email, password
api/users/login/	                        🔑 התחברות - POST עם identifier (שם משתמש או אימייל) וסיסמה
api/users/logout/	                        🚪 התנתקות - POST (דורש טוקן)
api/users/check-auth/	                        📋 בדיקת התחברות - GET (דורש טוקן)
api/users/forgot-password/	                🔐 שליחת לינק לאיפוס סיסמה (לוג בלבד) - POST עם אימייל
api/users/reset-password/<uidb64>/<token>/	🔑 איפוס סיסמה לפי לינק - POST עם סיסמה חדשה


📂 Todos API    (Token requierd)
api/todos/	        📋 קבלת כל המשימות של המשתמש המחובר - GET (דורש טוקן)
api/todos/	        ➕ יצירת משימה חדשה - POST עם task, completed, date, time (דורש טוקן)
api/todos/<id>/	        📝 קבלת פרטי משימה - GET לפי מזהה (דורש טוקן)
api/todos/<id>/	        ✏️ עדכון משימה - PUT (דורש טוקן)
api/todos/<id>/	        ❌ מחיקת משימה - DELETE (דורש טוקן)


📥 עבודה עם טוקן
אחרי ההתחברות (/api/users/login/), תקבל:
{
    "message": "Login successful",
    "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
את הטוקן הזה צריך לשלוח בכל בקשה מאובטחת, לדוגמה:
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx


Useful Tools (POSTMAN / CURL) 🧰

Todos_API.postman_collection.json
curl_commands.sh