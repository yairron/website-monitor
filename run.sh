#!/bin/bash

# סקריפט הפעלה ידנית להרצה מקומית
# Manual run script for local testing

echo "==================================="
echo "מעקב שינויים באתרי ביטוח לאומי"
echo "Website Monitor - Local Run"
echo "==================================="
echo ""

# בדיקת Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 לא מותקן!"
    echo "התקן Python מ: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python נמצא"

# יצירת סביבה וירטואלית (אופציונלי)
if [ ! -d "venv" ]; then
    echo "יוצר סביבה וירטואלית..."
    python3 -m venv venv
fi

# הפעלת הסביבה
if [ -d "venv" ]; then
    echo "✓ מפעיל סביבה וירטואלית"
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
fi

# התקנת תלויות
echo "מתקין תלויות..."
pip install -q -r requirements.txt

echo ""
echo "מריץ את הסקריפט..."
echo "==================================="
echo ""

# הרצת הסקריפט
python3 website_monitor.py

echo ""
echo "==================================="
echo "✓ הרצה הושלמה"
echo "בדוק את תיקיית history/ לתוצאות"
echo "==================================="
