# JetGram Self — سلف تلگرام (دستیار همه‌کاره اکانت)

سلف JetGram با اکانت **خودت** وارد تلگرام می‌شود (نه ربات جدا) و همه‌ی کارها را خودکار می‌کند.

## چه کارهایی می‌کند؟

| قابلیت | وضعیت |
|---|---|
| جواب خودکار به پیام خصوصی وقتی نیستی | ✅ روشن (هر نفر هر ۱۰ دقیقه یک بار) |
| ضد حذف — پیام/عکس حذف‌شده را در Saved Messages نگه می‌دارد | ✅ روشن |
| ذخیره خودکار عکس/فیلم/ویس در پوشه `downloads` | ✅ روشن |
| فوروارد خودکار از یک چت به چت دیگر | ❌ خاموش (باید در `config.py` تنظیم کنی) |
| دستورها در Saved Messages | ✅ روشن |

## دستورها (در Saved Messages بنویس)

```
.ping              — چک کن سلف روشن است؟
.help              — راهنما
.stats             — آمار سلف
.autoreply on      — جواب خودکار روشن
.autoreply off     — جواب خودکار خاموش
.antidelete on     — ضد حذف روشن
.antidelete off    — ضد حذف خاموش
.autosave on       — ذخیره مدیا روشن
.autosave off      — ذخیره مدیا خاموش
```

همه‌ی تنظیم‌ها در فایل `config.py` است — متن جواب خودکار، زمان انتظار، فوروارد و...

## اجرای محلی (اولین ورود)

```bash
cp .env.example .env
# در .env بنویس:
# TELEGRAM_API_ID=24399967
# TELEGRAM_API_HASH=... (همانی که در JetGram استفاده کردی)
# TELEGRAM_PHONE=+989123456789
pip install -r requirements.txt
python bot.py
```

اولین بار تلگرام یک **کد** به گوشی‌ات می‌فرستد — کد را وارد کن تا فایل سشن ساخته شود.
بعد از آن دیگر کد نمی‌خواهد.

## اجرا روی Railway (همیشه روشن)

1. این پوشه را به گیت‌هاب بفرست و در Railway یک پروژه جدید از آن بساز.
2. در Railway → Variables بگذار:
   - `TELEGRAM_API_ID` — همان api_id جت‌گرام
   - `TELEGRAM_API_HASH` — همان api_hash جت‌گرام
   - `TELEGRAM_SESSION_STRING` — رشته‌ی سشن (به‌جای فایل سشن، چون Railway فایل را نگه نمی‌دارد)
3. Deploy کن. اگر قطع شود خودش دوباره وصل می‌شود.

**ساختن رشته سشن (روی کامپیوتر خودت):**
```bash
python -c "from telethon.sync import TelegramClient; from telethon.sessions import StringSession; c = TelegramClient(StringSession(), 24399967, 'API_HASH_خودت'); c.start(); print(c.session.save())"
```
خروجی را کپی کن و در Railway به‌عنوان `TELEGRAM_SESSION_STRING` بگذار.

⚠️ **هیچ رمز / api / شماره‌ای در کد نیست.** همه‌چیز فقط با Environment Variable می‌آید.
`.env` و فایل سشن را هرگز در گیت‌هاب نگذار (در `.gitignore` هستند).

## ⚠️ هشدار مهم — خطر بن شدن

سلف یعنی تلگرام فکر می‌کند **تو** داری کار می‌کنی. اگر سلف:
- به خیلی‌ها پشت سر هم پیام بدهد (اسپم)،
- جواب خودکار به همه بدهد،
- یا خیلی سریع کار کند،

تلگرام ممکن است اکانتت را **محدود یا بن** کند. پس:
- جواب خودکار فقط به پیام خصوصی است و هر نفر هر ۱۰ دقیقه یک بار.
- سلف را برای اسپم و تبلیغات استفاده نکن.
- اگر تلگرام هشدار داد، سلف را خاموش کن.

## فایل‌ها

- `bot.py` — سلف (Telethon)
- `config.py` — همه‌ی تنظیم‌ها
- `requirements.txt` — telethon
- `Dockerfile` + `railway.json` + `Procfile` — اجرای Railway
- `.env.example` — نمونه‌ی خالی، بدون مقدار واقعی
- `downloads/` — مدیای ذخیره‌شده
