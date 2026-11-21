"""
JetGram Self — سلف تلگرام (یوزربات) با Telethon
------------------------------------------------
با اکانت خودت وارد تلگرام می‌شود (نه ربات Bot API) و این کارها را می‌کند:
  1. جواب خودکار به پیام‌های خصوصی وقتی نیستی
  2. ضد حذف: پیام/مدیای حذف‌شده را در Saved Messages نگه می‌دارد
  3. ذخیره خودکار مدیای ورودی در پوشه downloads
  4. فوروارد خودکار از یک چت به چت دیگر (اگر تنظیم شده باشد)
  5. دستورها از خودت در Saved Messages: .ping .help .stats
     .autoreply on/off  .antidelete on/off  .autosave on/off

ورود: فقط با Environment Variables:
  TELEGRAM_API_ID, TELEGRAM_API_HASH
  (اختیاری) TELEGRAM_PHONE, TELEGRAM_SESSION_STRING

هیچ رمز / api / شماره‌ای در این کد نیست.
اولین ورود باید روی کامپیوتر خودت انجام شود (کد تلگرام می‌خواهد)،
بعد فایل سشن یا رشته‌ی سشن (StringSession) را برای Railway استفاده کن.
"""

import asyncio
import logging
import os
import time
from collections import defaultdict
from datetime import datetime

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import Message

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("jetgram-self")

# ---------- تنظیمات از Environment ----------
API_ID = int(os.environ.get("TELEGRAM_API_ID", "0") or 0)
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
PHONE = os.environ.get("TELEGRAM_PHONE", "") or None
SESSION_STRING = os.environ.get("TELEGRAM_SESSION_STRING", "") or None

# وضعیت (در حافظه، با دستور عوض می‌شود)
state = {
    "auto_reply": config.AUTO_REPLY,
    "anti_delete": config.ANTI_DELETE,
    "auto_save": config.AUTO_SAVE_MEDIA,
    "started_at": time.time(),
    "replies_sent": 0,
    "saved_deleted": 0,
    "media_saved": 0,
    "forwarded": 0,
    "messages_seen": 0,
}

# کش پیام‌ها برای ضد حذف: id -> (فرستنده، متن، مسیر فایل مدیا)
message_cache = {}
last_reply_at = defaultdict(float)  # sender_id -> زمان آخرین جواب خودکار


def get_client():
    """ساخت کلاینت: اگر رشته‌ی سشن هست از آن استفاده کن، وگرنه فایل سشن."""
    if SESSION_STRING:
        return TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    return TelegramClient(config.SESSION_NAME, API_ID, API_HASH)


async def send_to_saved(client, text):
    """پیام به Saved Messages خودت."""
    try:
        await client.send_message("me", text)
    except Exception as e:  # noqa: BLE001 - فقط لاگ کن، کرش نکن
        log.warning("Could not send to Saved Messages: %s", e)


async def run_once():
    if not API_ID or not API_HASH:
        log.error(
            "TELEGRAM_API_ID / TELEGRAM_API_HASH تنظیم نشده! "
            "آن‌ها را در Railway → Variables یا در فایل .env بگذار."
        )
        return

    client = get_client()

    # ---------- دستورها: فقط از خودت، فقط در Saved Messages ----------
    @client.on(events.NewMessage(outgoing=True, pattern=r"^\.(ping|help|stats|status|autoreply|antidelete|autosave)(?:\s+(.*))?$"))
    async def commands(event):
        cmd = (event.pattern_match.group(1) or "").lower()
        arg = (event.pattern_match.group(2) or "").strip().lower()
        # فقط در Saved Messages (چت با خودت): آنجا chat_id همان id خودت است
        if event.chat_id != event.sender_id:
            return
        if cmd == "ping":
            await event.reply("🏓 پونگ! سلف JetGram روشن است ✅")
        elif cmd == "help":
            await event.reply(
                "🤖 دستورهای سلف JetGram:\n"
                ".ping — چک روشن بودن\n"
                ".help — همین راهنما\n"
                ".stats — آمار سلف\n"
                ".autoreply on / off — جواب خودکار\n"
                ".antidelete on / off — ضد حذف\n"
                ".autosave on / off — ذخیره خودکار مدیا"
            )
        elif cmd in ("stats", "status"):
            uptime = int(time.time() - state["started_at"])
            await event.reply(
                "📊 آمار سلف JetGram:\n"
                f"⏱ روشن از: {uptime // 60} دقیقه پیش\n"
                f"💬 پیام دیده‌شده: {state['messages_seen']}\n"
                f"↩️ جواب خودکار: {state['replies_sent']}\n"
                f"🗑 پیام حذف‌شده‌ی نجات‌یافته: {state['saved_deleted']}\n"
                f"🖼 مدیای ذخیره‌شده: {state['media_saved']}\n"
                f"➡️ فورواردشده: {state['forwarded']}\n"
                f"جواب خودکار: {'✅ روشن' if state['auto_reply'] else '❌ خاموش'}\n"
                f"ضد حذف: {'✅ روشن' if state['anti_delete'] else '❌ خاموش'}\n"
                f"ذخیره مدیا: {'✅ روشن' if state['auto_save'] else '❌ خاموش'}"
            )
        elif cmd == "autoreply":
            if arg in ("on", "on!", "روشن"):
                state["auto_reply"] = True
                await event.reply("✅ جواب خودکار روشن شد.")
            elif arg in ("off", "خاموش"):
                state["auto_reply"] = False
                await event.reply("❌ جواب خودکار خاموش شد.")
            else:
                await event.reply(f"جواب خودکار الان: {'روشن ✅' if state['auto_reply'] else 'خاموش ❌'}\nبزن: .autoreply on  یا  .autoreply off")
        elif cmd == "antidelete":
            if arg in ("on", "روشن"):
                state["anti_delete"] = True
                await event.reply("✅ ضد حذف روشن شد.")
            elif arg in ("off", "خاموش"):
                state["anti_delete"] = False
                await event.reply("❌ ضد حذف خاموش شد.")
            else:
                await event.reply(f"ضد حذف الان: {'روشن ✅' if state['anti_delete'] else 'خاموش ❌'}")
        elif cmd == "autosave":
            if arg in ("on", "روشن"):
                state["auto_save"] = True
                await event.reply("✅ ذخیره خودکار مدیا روشن شد.")
            elif arg in ("off", "خاموش"):
                state["auto_save"] = False
                await event.reply("❌ ذخیره خودکار مدیا خاموش شد.")
            else:
                await event.reply(f"ذخیره مدیا الان: {'روشن ✅' if state['auto_save'] else 'خاموش ❌'}")

    # ---------- پیام‌های ورودی: جواب خودکار + ذخیره + فوروارد ----------
    @client.on(events.NewMessage(incoming=True))
    async def incoming(event):
        state["messages_seen"] += 1
        sender = await event.get_sender()
        sender_name = getattr(sender, "first_name", None) or "ناشناس"
        if getattr(sender, "username", None):
            sender_name += f" (@{sender.username})"

        # 1) کش برای ضد حذف (متن + دانلود مدیا قبل از حذف)
        media_path = None
        if state["anti_delete"] and event.message:
            if event.message.media and state["auto_save"]:
                try:
                    os.makedirs(config.AUTO_SAVE_MEDIA_FOLDER, exist_ok=True)
                    media_path = await event.message.download_media(
                        file=config.AUTO_SAVE_MEDIA_FOLDER
                    )
                    if media_path:
                        state["media_saved"] += 1
                except Exception as e:  # noqa: BLE001
                    log.warning("Media download failed: %s", e)
            message_cache[event.message.id] = (
                sender_name,
                event.message.text or "",
                media_path,
            )
            # کش را کوچک نگه دار (آخرین 500 پیام)
            if len(message_cache) > 500:
                message_cache.pop(next(iter(message_cache)))

        # 2) ذخیره مدیا حتی اگر ضد حذف خاموش است
        elif event.message and event.message.media and state["auto_save"]:
            try:
                os.makedirs(config.AUTO_SAVE_MEDIA_FOLDER, exist_ok=True)
                path = await event.message.download_media(file=config.AUTO_SAVE_MEDIA_FOLDER)
                if path:
                    state["media_saved"] += 1
                    log.info("Saved media: %s", path)
            except Exception as e:  # noqa: BLE001
                log.warning("Media download failed: %s", e)

        # 3) فوروارد خودکار (فقط اگر تنظیم شده)
        if config.FORWARD_FROM and config.FORWARD_TO:
            try:
                chat = await event.get_chat()
                chat_id = getattr(chat, "id", None)
                # Telethon: آیدی کانال/گروه معمولاً منفی است؛ هر دو شکل را چک کن
                if chat_id == config.FORWARD_FROM or event.chat_id == config.FORWARD_FROM:
                    await client.forward_messages(config.FORWARD_TO, event.message)
                    state["forwarded"] += 1
            except Exception as e:  # noqa: BLE001
                log.warning("Auto-forward failed: %s", e)

        # 4) فوروارد مدیا به Saved Messages (اگر روشن است)
        if config.FORWARD_MEDIA_TO_SAVED and event.message and event.message.media:
            try:
                await client.forward_messages("me", event.message)
            except Exception as e:  # noqa: BLE001
                log.warning("Forward media to Saved failed: %s", e)

        # 5) جواب خودکار (فقط خصوصی، فقط اگر روشن است، با فاصله زمانی)
        if not state["auto_reply"]:
            return
        if config.AUTO_REPLY_PRIVATE_ONLY and not event.is_private:
            return
        if event.outgoing:
            return
        now = time.time()
        sender_id = event.sender_id
        if now - last_reply_at[sender_id] < config.AUTO_REPLY_COOLDOWN_MINUTES * 60:
            return
        last_reply_at[sender_id] = now
        try:
            await event.reply(config.AUTO_REPLY_TEXT)
            state["replies_sent"] += 1
            log.info("Auto-replied to %s", sender_name)
        except Exception as e:  # noqa: BLE001
            log.warning("Auto-reply failed: %s", e)

    # ---------- ضد حذف: وقتی پیامی حذف شد ----------
    @client.on(events.MessageDeleted)
    async def on_deleted(event):
        if not state["anti_delete"]:
            return
        for msg_id in event.deleted_ids:
            cached = message_cache.pop(msg_id, None)
            if not cached:
                continue
            sender_name, text, media_path = cached
            state["saved_deleted"] += 1
            note = (
                f"🗑 یک پیام حذف شد\n"
                f"👤 از: {sender_name}\n"
                f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"💬 متن: {text or '(بدون متن)'}"
            )
            try:
                if media_path and os.path.exists(media_path):
                    await client.send_file("me", media_path, caption=note)
                else:
                    await send_to_saved(client, note)
                log.info("Saved a deleted message from %s", sender_name)
            except Exception as e:  # noqa: BLE001
                log.warning("Anti-delete save failed: %s", e)

    # ---------- یک بار وصل شو و تا قطع‌شدن کار کن ----------
    log.info("Connecting to Telegram as user account…")
    await client.start(phone=PHONE)
    me = await client.get_me()
    log.info("✅ Logged in as %s (@%s)", me.first_name, me.username)
    log.info(
        "Self-bot is running. Auto-reply=%s Anti-delete=%s Auto-save=%s",
        state["auto_reply"], state["anti_delete"], state["auto_save"],
    )
    await client.run_until_disconnected()


async def main():
    """حلقه وصل‌شدن دوباره: اگر قطع شد، 10 ثانیه صبر کن و از اول وصل شو."""
    if not API_ID or not API_HASH:
        log.error(
            "TELEGRAM_API_ID / TELEGRAM_API_HASH تنظیم نشده! "
            "آن‌ها را در Railway → Variables یا در فایل .env بگذار."
        )
        return
    while True:
        try:
            await run_once()
            log.warning("Disconnected — reconnecting in 10s…")
        except (KeyboardInterrupt, asyncio.CancelledError):
            log.info("Stopped by user.")
            break
        except Exception as e:  # noqa: BLE001 - قطع شد؟ دوباره وصل شو
            log.warning("Error: %s — reconnecting in 10s…", e)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
