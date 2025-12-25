#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בדיקת שליחת מייל - סקריפט פשוט לבדיקה
Email Test Script - Simple debugging
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_email():
    """בדיקת שליחת מייל עם הדפסות debug"""
    
    print("="*60)
    print("🧪 בדיקת מערכת המיילים")
    print("="*60)
    
    # שלב 1: טעינת הגדרות
    print("\n[1/6] טוען הגדרות מ-config.json...")
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ config.json נטען בהצלחה")
    except Exception as e:
        print(f"✗ שגיאה בטעינת config.json: {e}")
        return
    
    # שלב 2: בדיקה אם מייל מופעל
    print("\n[2/6] בודק אם מייל מופעל...")
    email_enabled = config.get('email', {}).get('enabled', False)
    print(f"   Email enabled: {email_enabled}")
    
    if not email_enabled:
        print("✗ מיילים לא מופעלים! שנה enabled ל-true ב-config.json")
        return
    
    email_config = config['email']
    
    # שלב 3: הצגת הגדרות
    print("\n[3/6] הגדרות מייל:")
    print(f"   SMTP Server: {email_config.get('smtp_server', 'לא מוגדר')}")
    print(f"   SMTP Port: {email_config.get('smtp_port', 'לא מוגדר')}")
    print(f"   From Email: {email_config.get('from_email', 'לא מוגדר')}")
    print(f"   To Email: {email_config.get('to_email', 'לא מוגדר')}")
    print(f"   Password: {'*' * len(str(email_config.get('password', ''))) if email_config.get('password') else 'לא מוגדר'}")
    
    # בדיקות בסיסיות
    if not email_config.get('from_email'):
        print("✗ From Email לא מוגדר!")
        return
    if not email_config.get('to_email'):
        print("✗ To Email לא מוגדר!")
        return
    if not email_config.get('password'):
        print("✗ Password לא מוגדר!")
        return
    
    # שלב 4: יצירת המייל
    print("\n[4/6] יוצר הודעת מייל...")
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🧪 בדיקת מערכת - Test Email"
        msg['From'] = email_config['from_email']
        msg['To'] = email_config['to_email']
        
        body = f"""בדיקת מערכת מעקב אתרים

זהו מייל בדיקה שנשלח ב-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

אם קיבלת מייל זה - המערכת עובדת מעולה! ✅

הגדרות:
- SMTP Server: {email_config['smtp_server']}
- Port: {email_config['smtp_port']}
- From: {email_config['from_email']}
- To: {email_config['to_email']}

---
מערכת מעקב זכויות אזרחים ותיקים
"""
        
        html_body = f"""
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif;">
            <h2>🧪 בדיקת מערכת - Test Email</h2>
            <pre style="background: #f5f5f5; padding: 15px;">{body}</pre>
        </body>
        </html>
        """
        
        text_part = MIMEText(body, 'plain', 'utf-8')
        html_part = MIMEText(html_body, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        print("✓ הודעת מייל נוצרה בהצלחה")
        
    except Exception as e:
        print(f"✗ שגיאה ביצירת הודעה: {e}")
        return
    
    # שלב 5: התחברות לשרת SMTP
    print("\n[5/6] מתחבר לשרת SMTP...")
    server = None
    try:
        print(f"   מתחבר ל-{email_config['smtp_server']}:{email_config['smtp_port']}...")
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'], timeout=30)
        print("✓ התחברות לשרת הצליחה")
        
        print("   מפעיל TLS...")
        server.starttls()
        print("✓ TLS הופעל")
        
        print("   מתחבר עם username/password...")
        server.login(email_config['from_email'], email_config['password'])
        print("✓ התחברות הצליחה!")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ שגיאת אימות (Username/Password שגויים): {e}")
        print("\n💡 טיפ: Gmail דורש App Password, לא סיסמה רגילה!")
        print("   צור App Password ב: https://myaccount.google.com/apppasswords")
        if server:
            server.quit()
        return
        
    except smtplib.SMTPConnectError as e:
        print(f"✗ לא ניתן להתחבר לשרת: {e}")
        if server:
            server.quit()
        return
        
    except Exception as e:
        print(f"✗ שגיאה בהתחברות: {e}")
        if server:
            server.quit()
        return
    
    # שלב 6: שליחת המייל
    print("\n[6/6] שולח מייל...")
    try:
        server.send_message(msg)
        print("✓ מייל נשלח בהצלחה!")
        print(f"\n✉️  בדוק את תיבת הדואר: {email_config['to_email']}")
        print("   (בדוק גם ב-Spam/Junk Mail)")
        
    except Exception as e:
        print(f"✗ שגיאה בשליחת מייל: {e}")
        
    finally:
        if server:
            print("\n   סוגר חיבור לשרת...")
            server.quit()
            print("✓ החיבור נסגר")
    
    print("\n" + "="*60)
    print("✅ בדיקה הושלמה!")
    print("="*60)

if __name__ == "__main__":
    test_email()
