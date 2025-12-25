#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מעקב שינויים באתרי ביטוח לאומי ואתרים ממשלתיים
Website Change Monitor for Government Sites
"""

import requests
import hashlib
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import difflib
import re

class WebsiteMonitor:
    def __init__(self, config_file='config.json'):
        """אתחול המעקב"""
        self.config_file = config_file
        self.config = self.load_config()
        self.history_dir = Path('history')
        self.history_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """טעינת קובץ התצורה"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"שגיאה: קובץ {self.config_file} לא נמצא")
            return None
    
    def fetch_page(self, url):
        """שליפת תוכן העמוד"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"שגיאה בטעינת {url}: {e}")
            return None
    
    def extract_relevant_text(self, html, keywords):
        """חילוץ טקסט רלוונטי מה-HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # הסרת סקריפטים וסגנונות
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        # אם יש מילות חיפוש, נסנן רק שורות רלוונטיות
        if keywords:
            relevant_lines = []
            for line in lines:
                if any(keyword.lower() in line.lower() for keyword in keywords):
                    relevant_lines.append(line)
            return '\n'.join(relevant_lines) if relevant_lines else '\n'.join(lines)
        
        return '\n'.join(lines)
    
    def get_content_hash(self, content):
        """חישוב hash לתוכן"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def load_previous_content(self, site_name):
        """טעינת תוכן קודם"""
        history_file = self.history_dir / f"{site_name}.txt"
        if history_file.exists():
            return history_file.read_text(encoding='utf-8')
        return None
    
    def save_content(self, site_name, content):
        """שמירת תוכן נוכחי"""
        history_file = self.history_dir / f"{site_name}.txt"
        history_file.write_text(content, encoding='utf-8')
        
        # שמירת עותק עם תאריך
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.history_dir / f"{site_name}_{timestamp}.txt"
        backup_file.write_text(content, encoding='utf-8')
    
    def generate_diff(self, old_content, new_content, site_name):
        """יצירת דוח הבדלים"""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        diff = list(difflib.unified_diff(
            old_lines, 
            new_lines,
            fromfile=f'{site_name} (קודם)',
            tofile=f'{site_name} (נוכחי)',
            lineterm=''
        ))
        
        return '\n'.join(diff)
    
    def send_email_alert(self, subject, body):
        """שליחת התראה במייל"""
        if not self.config.get('email', {}).get('enabled', False):
            print("התראות מייל לא מופעלות")
            return
        
        email_config = self.config['email']
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = email_config['from_email']
            msg['To'] = email_config['to_email']
            
            # יצירת גרסת HTML
            html_body = f"""
            <html dir="rtl">
            <head>
                <meta charset="UTF-8">
            </head>
            <body style="font-family: Arial, sans-serif;">
                <h2>{subject}</h2>
                <pre style="background: #f5f5f5; padding: 15px; direction: ltr;">{body}</pre>
                <hr>
                <p><small>נשלח מ: מערכת מעקב אתרי ביטוח לאומי</small></p>
            </body>
            </html>
            """
            
            text_part = MIMEText(body, 'plain', 'utf-8')
            html_part = MIMEText(html_body, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # שליחת המייל
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['from_email'], email_config['password'])
                server.send_message(msg)
            
            print(f"✓ התראה נשלחה ל-{email_config['to_email']}")
            
        except Exception as e:
            print(f"שגיאה בשליחת מייל: {e}")
    
    def check_site(self, site):
        """בדיקת אתר בודד"""
        site_name = site['name']
        url = site['url']
        keywords = site.get('keywords', [])
        
        print(f"\n{'='*60}")
        print(f"בודק: {site_name}")
        print(f"כתובת: {url}")
        
        # שליפת התוכן
        html = self.fetch_page(url)
        if not html:
            return
        
        # חילוץ טקסט רלוונטי
        current_content = self.extract_relevant_text(html, keywords)
        current_hash = self.get_content_hash(current_content)
        
        # טעינת תוכן קודם
        previous_content = self.load_previous_content(site_name)
        
        if previous_content is None:
            # ריצה ראשונה
            self.save_content(site_name, current_content)
            print(f"✓ תוכן ראשוני נשמר עבור {site_name}")
            return
        
        previous_hash = self.get_content_hash(previous_content)
        
        if current_hash != previous_hash:
            # נמצא שינוי!
            print(f"🔔 נמצא שינוי באתר: {site_name}")
            
            # יצירת דוח הבדלים
            diff = self.generate_diff(previous_content, current_content, site_name)
            
            # שמירת תוכן חדש
            self.save_content(site_name, current_content)
            
            # שליחת התראה
            subject = f"🔔 שינוי זוהה: {site_name}"
            body = f"""זוהה שינוי באתר: {site_name}
כתובת: {url}
תאריך: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

הבדלים שנמצאו:
{diff[:2000]}

{"..." if len(diff) > 2000 else ""}
"""
            
            self.send_email_alert(subject, body)
            
            # שמירת דוח
            report_file = self.history_dir / f"report_{site_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report_file.write_text(diff, encoding='utf-8')
            
        else:
            print(f"✓ אין שינויים באתר: {site_name}")
    
    def run(self):
        """הרצת הבדיקה על כל האתרים"""
        if not self.config:
            return
        
        print("\n" + "="*60)
        print("התחלת מעקב אתרים")
        print(f"תאריך: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        sites = self.config.get('sites', [])
        
        if not sites:
            print("שגיאה: לא נמצאו אתרים לבדיקה בקובץ התצורה")
            return
        
        for site in sites:
            try:
                self.check_site(site)
            except Exception as e:
                print(f"שגיאה בבדיקת {site.get('name', 'לא ידוע')}: {e}")
        
        print("\n" + "="*60)
        print("סיום הבדיקה")
        print("="*60)

if __name__ == "__main__":
    monitor = WebsiteMonitor()
    
    print("שולח מייל בדיקה...")
    monitor.send_email_alert(
        subject="בדיקת מערכת מעקב - הכל עובד!",
        body="זהו מייל בדיקה. אם קיבלת מייל זה - המערכת עובדת מצוין!"
    )
    print("מייל נשלח!")
    
    monitor.run()
