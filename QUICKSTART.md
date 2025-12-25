# 🚀 מדריך התחלה מהירה

## 3 צעדים פשוטים להתחיל

### 1️⃣ צור Repository ב-GitHub

1. היכנס ל-[GitHub.com](https://github.com)
2. לחץ על **"New"** (ליד Repositories)
3. שם ל-repository: **`website-monitor`**
4. סמן: ✅ **"Add a README file"**
5. לחץ: **"Create repository"**

### 2️⃣ העלה את הקבצים

**אופציה א': ישירות דרך הדפדפן**
1. לחץ **"Add file"** → **"Upload files"**
2. גרור את כל הקבצים שקיבלת
3. לחץ **"Commit changes"**

**אופציה ב': דרך Git (למתקדמים)**
```bash
git clone https://github.com/YOUR-USERNAME/website-monitor.git
cd website-monitor
# העתק את כל הקבצים לכאן
git add .
git commit -m "הוספת מערכת מעקב"
git push
```

### 3️⃣ הפעל

1. עבור ל-**Actions** (בתפריט העליון)
2. לחץ: **"I understand my workflows, go ahead and enable them"**
3. בחר ב-**"Website Monitor"**
4. לחץ: **"Run workflow"** → **"Run workflow"**

✅ **זהו! הסקריפט רץ**

---

## 📧 רוצה התראות במייל? (אופציונלי)

### הכן App Password ב-Gmail

1. היכנס ל-Gmail שלך
2. עבור ל: https://myaccount.google.com/apppasswords
3. אם מופיעה הודעה "גישה לאפליקציות פחות מאובטחות":
   - עבור ל: https://myaccount.google.com/security
   - הפעל "אימות דו-שלבי" (2-Step Verification)
   - חזור ל-App Passwords
4. בחר "Mail" ו-"Other (Custom name)"
5. תן שם: "Website Monitor"
6. **העתק את הסיסמה בת 16 התווים**

### הוסף Secrets ב-GitHub

1. Repository שלך → **Settings** → **Secrets and variables** → **Actions**
2. לחץ **"New repository secret"** 6 פעמים:

| Name | Value |
|------|-------|
| `EMAIL_ENABLED` | `true` |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `FROM_EMAIL` | `your_email@gmail.com` |
| `EMAIL_PASSWORD` | הסיסמה בת 16 התווים |
| `TO_EMAIL` | `recipient@example.com` |

3. שמור כל Secret

✅ **עכשיו תקבל מיילים כשיש שינויים!**

---

## ⚙️ עריכת מילות החיפוש

1. פתח את `config.json` ב-repository
2. לחץ על עיפרון (✏️ Edit)
3. ערוך את `keywords`:

```json
"keywords": [
  "עדכון",
  "שינוי",
  "חדש",
  "2025",
  "זקנה",
  "סיעוד"
]
```

4. **"Commit changes"**

---

## 📅 שינוי תדירות הבדיקה

ערוך `.github/workflows/monitor.yml`:

```yaml
# כל יום בשעה 10:00
- cron: '0 8 * * *'

# כל 12 שעות
- cron: '0 */12 * * *'

# כל יום ב-8 בבוקר ו-8 בערב
- cron: '0 8,20 * * *'
```

---

## ❓ שאלות נפוצות

**ש: איך אדע שהסקריפט רץ?**
ת: עבור ל-Actions ותראה את ההיסטוריה של ההרצות

**ש: איך אראה מה השתנה?**
ת: תקבל מייל עם ההבדלים, או בדוק את תיקיית `history/`

**ש: הסקריפט נכשל - מה לעשות?**
ת: בדוק את הלוגים ב-Actions, רוב הסיכויים שהאתר היה לא זמין זמנית

**ש: אפשר להוסיף אתרים נוספים?**
ת: בטח! פשוט ערוך את `config.json` והוסף אתרים לרשימת `sites`

---

## 🎯 טיפים

✅ **הרץ באופן ידני פעם ראשונה** לוודא שהכל עובד
✅ **בדוק את הלוגים** לאחר הרצה ראשונה
✅ **התחל עם אתר אחד** ואז הוסף עוד
✅ **שמור את ה-App Password** במקום בטוח

---

**צריך עזרה? יש בעיה?** 
פתח Issue ב-GitHub או שאל! 🙂
