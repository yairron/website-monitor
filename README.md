# 🔔 מעקב שינויים באתרי ביטוח לאומי

סקריפט Python אוטומטי למעקב אחרי שינויים באתרי הביטוח הלאומי ואתרים ממשלתיים נוספים, עם התראות במייל והרצה אוטומטית דרך GitHub Actions.

## ✨ יכולות

- ✅ מעקב אחרי מספר אתרים בו-זמנית
- ✅ חיפוש מילות מפתח ספציפיות
- ✅ זיהוי שינויים בתוכן
- ✅ התראות במייל כשיש שינוי
- ✅ שמירת היסטוריה מלאה של כל השינויים
- ✅ הרצה אוטומטית יומית דרך GitHub Actions
- ✅ קובץ תצורה נפרד שקל לעריכה

## 📋 דרישות מקדימות

- חשבון GitHub (יש לך!)
- Python 3.8 ומעלה (להרצה מקומית)
- חשבון Gmail (אופציונלי - להתראות מייל)

## 🚀 התקנה והגדרה

### שלב 1: יצירת Repository ב-GitHub

1. היכנס ל-GitHub והתחבר לחשבון שלך
2. לחץ על **"New repository"**
3. תן שם ל-repository: `website-monitor`
4. סמן ✅ **"Add a README file"**
5. לחץ **"Create repository"**

### שלב 2: העלאת הקבצים

1. בעמוד ה-repository, לחץ על **"Add file" → "Upload files"**
2. גרור את הקבצים הבאים:
   - `website_monitor.py`
   - `config.json`
   - `requirements.txt`
3. צור תיקייה `.github/workflows/` והעלה את הקובץ `monitor.yml`

### שלב 3: הגדרת Secrets (להתראות מייל)

**אם אתה רוצה לקבל התראות במייל:**

1. עבור ל-**Settings** → **Secrets and variables** → **Actions**
2. לחץ על **"New repository secret"** והוסף:

```
EMAIL_ENABLED = true
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
FROM_EMAIL = your_email@gmail.com
EMAIL_PASSWORD = your_app_password_here
TO_EMAIL = recipient@example.com
```

**⚠️ חשוב:** עבור Gmail, אתה צריך **App Password** ולא הסיסמה הרגילה:
1. עבור ל: https://myaccount.google.com/apppasswords
2. צור App Password חדש
3. העתק את הסיסמה ל-SECRET

### שלב 4: הפעלת GitHub Actions

1. עבור ללשונית **Actions** ב-repository
2. אשר שאתה רוצה להפעיל workflows
3. הסקריפט ירוץ אוטומטית כל יום בשעה 10:00 בוקר (שעון ישראל)

## ⚙️ עריכת קובץ התצורה

כל ההגדרות נמצאות בקובץ `config.json`. אתה יכול לערוך אותו ישירות ב-GitHub:

### להוספת אתר חדש:

```json
{
  "name": "שם_האתר",
  "url": "https://example.com/page",
  "keywords": [
    "מילת_חיפוש_1",
    "מילת_חיפוש_2"
  ]
}
```

### לשינוי מילות החיפוש:

פשוט ערוך את רשימת ה-`keywords` באתר הרלוונטי:

```json
"keywords": [
  "עדכון",
  "שינוי",
  "חדש",
  "2025"
]
```

### דוגמה מלאה:

```json
{
  "sites": [
    {
      "name": "עדכון_קצבאות",
      "url": "http://www.btl.gov.il/Publications/benefits_update/Pages/default.aspx",
      "keywords": [
        "עדכון",
        "שינוי",
        "קצבה",
        "זקנה",
        "2025"
      ]
    }
  ],
  "email": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_email": "your_email@gmail.com",
    "password": "your_app_password",
    "to_email": "recipient@example.com"
  }
}
```

## 🏃 הרצה ידנית

### דרך GitHub:
1. עבור ללשונית **Actions**
2. בחר ב-workflow **"Website Monitor"**
3. לחץ **"Run workflow"** → **"Run workflow"**

### הרצה מקומית (על המחשב):

```bash
# התקנת תלויות
pip install -r requirements.txt

# הרצת הסקריפט
python website_monitor.py
```

## 📊 צפייה בתוצאות

### בגרסת GitHub Actions:
1. עבור ל-**Actions** → בחר בהרצה האחרונה
2. לחץ על **"monitor"** לראות את הלוגים
3. היסטוריית השינויים נשמרת בתיקייה `history/`

### בהרצה מקומית:
- תיקיית `history/` תכיל:
  - קבצי טקסט עם התוכן האחרון של כל אתר
  - גיבויים עם חותמת זמן
  - דוחות הבדלים כשיש שינויים

## 📧 דוגמת התראה במייל

כשיש שינוי, תקבל מייל עם:
```
נושא: 🔔 שינוי זוהה: עדכון_קצבאות

זוהה שינוי באתר: עדכון_קצבאות
כתובת: http://www.btl.gov.il/Publications/...
תאריך: 2025-12-25 10:30:15

הבדלים שנמצאו:
+ עדכון חדש: העלאת קצבאות ינואר 2026
+ סכום חדש: 1,234 ₪
- סכום ישן: 1,200 ₪
...
```

## 🔧 הגדרות מתקדמות

### שינוי תדירות הבדיקה

ערוך את הקובץ `.github/workflows/monitor.yml`:

```yaml
on:
  schedule:
    # כל 6 שעות
    - cron: '0 */6 * * *'
    
    # כל יום בשעה 8 בבוקר ו-8 בערב
    - cron: '0 8,20 * * *'
    
    # רק בימי חול (ב-ה) בשעה 9 בבוקר
    - cron: '0 9 * * 1-5'
```

### כיבוי מעקב אחרי אתר מסוים

ב-`config.json`, פשוט מחק או הוסף `//` בתחילת השורות:

```json
// {
//   "name": "אתר_שלא_רוצה_לעקוב_אחריו",
//   "url": "...",
//   ...
// }
```

## 🐛 פתרון בעיות נפוצות

### הסקריפט לא רץ אוטומטית
- ודא ש-Actions מופעל ב-Settings → Actions
- בדוק שה-workflow file נמצא ב-`.github/workflows/monitor.yml`

### לא מגיעות התראות מייל
- ודא שיצרת App Password ב-Gmail (לא סיסמה רגילה)
- בדוק ש-Secrets מוגדרים נכון
- ודא ש-`EMAIL_ENABLED` מוגדר ל-`true`

### "שגיאה בטעינת האתר"
- יכול להיות שהאתר חסום או איטי
- הסקריפט ינסה שוב בהרצה הבאה

## 📝 רישיון

קוד זה נמצא בנחלת הכלל ופתוח לשימוש חופשי.

## 🆘 תמיכה

יש בעיה? צור Issue ב-GitHub או שלח מייל.

---

**נוצר עבור מעקב זכויות אזרחים ותיקים** 🇮🇱
