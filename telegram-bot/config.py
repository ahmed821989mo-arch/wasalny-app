"""إعدادات وصلني.

ضع القيم في Environment Variables داخل لوحة الاستضافة:
BOT_TOKEN=توكن البوت الجديد من BotFather
ADMIN_IDS=YOUR_TELEGRAM_USER_ID,ANOTHER_TELEGRAM_USER_ID

لا تضع التوكن داخل الملفات أو ترفعه إلى مستودع عام.
"""

import os


TOKEN = os.getenv("BOT_TOKEN", "").strip()


def _admin_ids():
    raw = os.getenv("ADMIN_IDS", "").strip()
    if not raw:
        return []
    ids = []
    for item in raw.split(","):
        item = item.strip()
        if item.isdigit():
            ids.append(int(item))
    return ids


ADMIN_IDS = _admin_ids()
