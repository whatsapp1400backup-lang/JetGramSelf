# JetGram Self — تنظیمات سلف (دستیار اکانت)
# همه‌ی این‌ها را می‌توانید عوض کنید. True یعنی روشن، False یعنی خاموش.
# هیچ رمز و api در این فایل نیست — api فقط از Environment می‌آید.

# --- جواب خودکار ---
AUTO_REPLY = True
# متن جواب خودکار (فارسی، دوستانه)
AUTO_REPLY_TEXT = "سلام! الان پشت گوشی نیستم، به‌محض اینکه برگردم جوابت رو می‌دم. ❤️"
# به هر نفر فقط هر چند دقیقه یک بار جواب بده (جلوگیری از اسپم)
AUTO_REPLY_COOLDOWN_MINUTES = 10
# فقط به پیام خصوصی جواب بده؟ (True = فقط خصوصی، False = گروه هم)
AUTO_REPLY_PRIVATE_ONLY = True

# --- ضد حذف (Anti-Delete) ---
ANTI_DELETE = True
# پیام‌های حذف‌شده کجا بروند؟ Saved Messages خودت
ANTI_DELETE_TARGET = "me"

# --- ذخیره خودکار مدیا ---
AUTO_SAVE_MEDIA = True          # عکس/فیلم/ویس را در پوشه downloads ذخیره کن
AUTO_SAVE_MEDIA_FOLDER = "downloads"
FORWARD_MEDIA_TO_SAVED = False  # مدیا را به Saved Messages هم فوروارد کن؟

# --- فوروارد خودکار ---
# از کدام چت به کدام چت؟ خالی = خاموش.
# مثال: FORWARD_FROM = -1001234567890  (آیدی گروه/کانال)
#        FORWARD_TO = "me"  یا آیدی چت مقصد
FORWARD_FROM = None
FORWARD_TO = None

# --- بقیه ---
SESSION_NAME = "jetgram_self"  # نام فایل سشن (بدون پسوند)
COMMAND_PREFIX = "."           # دستورها با . شروع می‌شوند: .ping و ...
