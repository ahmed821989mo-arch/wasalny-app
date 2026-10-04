"""
================================================================================
🕌 وصلني - سيدي سالم - V15 ULTIMATE COMPLETE EDITION 🚕
================================================================================
بسم الله الرحمن الرحيم - "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا"

✨ النسخة الكاملة الشاملة - كل الميزات من V1 حتى V15!

🔥 كل ميزات V14 (802 سطر) + التحديثات الجديدة:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V1-V14: كل الميزات الأساسية محفوظة 100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 13 بند للسواق + 9 بنود للراكب
✅ 3 طرق تحديد الموقع (يدوي + GPS + أماكن مشهورة)
✅ 60+ مكان في سيدي سالم والقرى والعزب
✅ بحث ذكي تدريجي (500م→1كم→2كم→5كم)
✅ 3 أنواع رحلات (حالاً + بموعد + مدارس)
✅ كود أمان 4 أرقام + طوارئ SOS
✅ لوحة أدمن كاملة
✅ نظام العروض والمزايدة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆕 الجديد في V15 (بدون حذف أي شيء قديم!):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ نظام التقييم ⭐ (1-5 نجوم للسواق والراكب)
2️⃣ نظام الشكاوى 📢 (موثق ومنظم للأدمن)
3️⃣ حساب السعر التلقائي 💰 (شفافية كاملة)
4️⃣ تاريخ الرحلات 📜 (آخر 10 رحلات)
5️⃣ حماية من السبام 🛡️ (3 رحلات/10 دقائق)
6️⃣ إحصائيات للسواق 📊 (ربح يومي + تقييم)
7️⃣ رسائل إسلامية متنوعة 🕌 (عشوائية ومضحكة)
8️⃣ أزرار كبيرة وواضحة 👆 (نصوص مفصلة)
9️⃣ تتبع شامل لكل شيء 📈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
المجموع: 1200+ سطر من الكود المحسّن والمنظم
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤲 توكلنا على الله - الحمد لله رب العالمين
================================================================================
"""

import config, database, urllib.parse, traceback, math, random, datetime, re, asyncio, os, logging
from datetime import datetime as dt, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

# ═══════════════════════════════════════════════════════════════════════════
# 🗄️ DATABASE SETUP V15 - كل الجداول (القديمة + الجديدة)
# ═══════════════════════════════════════════════════════════════════════════

try:
    database.init()
except Exception as e:
    print(f"⚠️ OLD database.py fallback {e}")
    import sqlite3, os
    DB_PATH_FB = os.path.join(os.path.dirname(__file__), "wasalny.db")
    database.con = sqlite3.connect(DB_PATH_FB, check_same_thread=False)
    database.cur = database.con.cursor()

try:
    # ─────────────────────────────────────────────────────────────────────
    # الجداول الأساسية من V14 (محفوظة 100%)
    # ─────────────────────────────────────────────────────────────────────
    
    database.cur.execute("""CREATE TABLE IF NOT EXISTS driver_profiles (
        driver_id INTEGER PRIMARY KEY, 
        personal_photo TEXT, 
        toktok_photo TEXT, 
        id_card_photo TEXT, 
        phone TEXT, 
        full_name TEXT, 
        approved_by_admin INTEGER DEFAULT 0, 
        status TEXT DEFAULT 'pending', 
        agreed_terms INTEGER DEFAULT 0, 
        agreed_at TEXT,
        avg_rating REAL DEFAULT 0.0,
        total_ratings INTEGER DEFAULT 0,
        complaints_count INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    database.cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        user_id INTEGER PRIMARY KEY, 
        name TEXT, 
        phone TEXT, 
        agreed_terms INTEGER DEFAULT 0, 
        agreed_at TEXT,
        avg_rating REAL DEFAULT 0.0,
        total_ratings INTEGER DEFAULT 0,
        complaints_count INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    database.cur.execute("""CREATE TABLE IF NOT EXISTS drivers (
        user_id INTEGER PRIMARY KEY, 
        name TEXT, 
        phone TEXT, 
        last_lat REAL, 
        last_lon REAL, 
        available INTEGER DEFAULT 0, 
        approved INTEGER DEFAULT 0,
        total_rides INTEGER DEFAULT 0,
        total_earnings REAL DEFAULT 0.0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    database.cur.execute("""CREATE TABLE IF NOT EXISTS rides (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        customer_id INTEGER, 
        from_loc TEXT, 
        to_loc TEXT, 
        from_lat REAL, 
        from_lon REAL, 
        to_lat REAL, 
        to_lon REAL, 
        distance REAL, 
        driver_id INTEGER, 
        status TEXT DEFAULT 'pending', 
        ride_type TEXT DEFAULT 'now', 
        scheduled_at TEXT, 
        school_days TEXT, 
        school_time_go TEXT, 
        school_time_back TEXT, 
        security_code TEXT, 
        emergency INTEGER DEFAULT 0,
        final_price REAL DEFAULT 0.0,
        suggested_price REAL DEFAULT 0.0,
        customer_rating INTEGER DEFAULT 0,
        driver_rating INTEGER DEFAULT 0,
        customer_comment TEXT,
        driver_comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        completed_at TEXT
    )""")
    
    database.cur.execute("""CREATE TABLE IF NOT EXISTS bids (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        ride_id INTEGER, 
        driver_id INTEGER, 
        driver_name TEXT, 
        phone TEXT, 
        price REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # ─────────────────────────────────────────────────────────────────────
    # 🆕 الجداول الجديدة في V15
    # ─────────────────────────────────────────────────────────────────────
    
    # جدول التقييمات
    database.cur.execute("""CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ride_id INTEGER,
        rater_id INTEGER,
        rated_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        rater_type TEXT CHECK(rater_type IN ('customer','driver')),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ride_id) REFERENCES rides(id)
    )""")
    
    # جدول الشكاوى
    database.cur.execute("""CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ride_id INTEGER,
        complainant_id INTEGER,
        complained_against_id INTEGER,
        complaint_type TEXT,
        description TEXT,
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending','reviewed','resolved','rejected')),
        admin_notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        resolved_at TEXT,
        FOREIGN KEY (ride_id) REFERENCES rides(id)
    )""")
    
    # ─────────────────────────────────────────────────────────────────────
    # إضافة الأعمدة الجديدة للجداول القديمة (ALTER TABLE)
    # ─────────────────────────────────────────────────────────────────────
    
    alterations = [
        # driver_profiles
        ("driver_profiles", "avg_rating", "REAL DEFAULT 0.0"),
        ("driver_profiles", "total_ratings", "INTEGER DEFAULT 0"),
        ("driver_profiles", "complaints_count", "INTEGER DEFAULT 0"),
        ("driver_profiles", "is_banned", "INTEGER DEFAULT 0"),
        ("driver_profiles", "created_at", "TEXT DEFAULT CURRENT_TIMESTAMP"),
        ("driver_profiles", "status", "TEXT DEFAULT 'pending'"),
        ("driver_profiles", "approved_by_admin", "INTEGER DEFAULT 0"),
        ("driver_profiles", "full_name", "TEXT"),
        ("driver_profiles", "personal_photo", "TEXT"),
        ("driver_profiles", "toktok_photo", "TEXT"),
        ("driver_profiles", "id_card_photo", "TEXT"),
        ("driver_profiles", "phone", "TEXT"),
        ("driver_profiles", "agreed_terms", "INTEGER DEFAULT 0"),
        ("driver_profiles", "agreed_at", "TEXT"),
        # customers
        ("customers", "avg_rating", "REAL DEFAULT 0.0"),
        ("customers", "total_ratings", "INTEGER DEFAULT 0"),
        ("customers", "complaints_count", "INTEGER DEFAULT 0"),
        ("customers", "is_banned", "INTEGER DEFAULT 0"),
        ("customers", "created_at", "TEXT DEFAULT CURRENT_TIMESTAMP"),
        ("customers", "agreed_terms", "INTEGER DEFAULT 0"),
        ("customers", "agreed_at", "TEXT"),
        # drivers
        ("drivers", "total_rides", "INTEGER DEFAULT 0"),
        ("drivers", "total_earnings", "REAL DEFAULT 0.0"),
        ("drivers", "created_at", "TEXT DEFAULT CURRENT_TIMESTAMP"),
        # rides
        ("rides", "final_price", "REAL DEFAULT 0.0"),
        ("rides", "suggested_price", "REAL DEFAULT 0.0"),
        ("rides", "customer_rating", "INTEGER DEFAULT 0"),
        ("rides", "driver_rating", "INTEGER DEFAULT 0"),
        ("rides", "customer_comment", "TEXT"),
        ("rides", "driver_comment", "TEXT"),
        ("rides", "created_at", "TEXT DEFAULT CURRENT_TIMESTAMP"),
        ("rides", "completed_at", "TEXT"),
        ("rides", "ride_type", "TEXT DEFAULT 'now'"),
        ("rides", "scheduled_at", "TEXT"),
        ("rides", "school_days", "TEXT"),
        ("rides", "school_time_go", "TEXT"),
        ("rides", "school_time_back", "TEXT"),
        ("rides", "security_code", "TEXT"),
        ("rides", "emergency", "INTEGER DEFAULT 0"),
    ]
    
    for tbl, col, typ in alterations:
        try:
            database.cur.execute(f"ALTER TABLE {tbl} ADD COLUMN {col} {typ}")
        except:
            pass  # العمود موجود مسبقاً
    
    # ─────────────────────────────────────────────────────────────────────
    # إنشاء Indexes للأداء السريع
    # ─────────────────────────────────────────────────────────────────────
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_rides_customer ON rides(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_rides_driver ON rides(driver_id)",
        "CREATE INDEX IF NOT EXISTS idx_rides_status ON rides(status)",
        "CREATE INDEX IF NOT EXISTS idx_rides_created ON rides(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_ratings_ride ON ratings(ride_id)",
        "CREATE INDEX IF NOT EXISTS idx_ratings_rated ON ratings(rated_id)",
        "CREATE INDEX IF NOT EXISTS idx_complaints_ride ON complaints(ride_id)",
        "CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status)",
        "CREATE INDEX IF NOT EXISTS idx_bids_ride ON bids(ride_id)",
        "CREATE INDEX IF NOT EXISTS idx_bids_driver ON bids(driver_id)",
    ]
    
    for idx in indexes:
        try:
            database.cur.execute(idx)
        except:
            pass
    
    database.con.commit()
    print("✅ Database V15 ULTIMATE initialized successfully - All tables ready!")
    
except Exception as e:
    print(f"❌ DB MIGRATION ERROR: {e}")
    traceback.print_exc()

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION & SETUP
# ═══════════════════════════════════════════════════════════════════════════

req = HTTPXRequest(connect_timeout=60, read_timeout=60, write_timeout=60, pool_timeout=60)
ADMIN_IDS = list(getattr(config, "ADMIN_IDS", []))


def is_banned(user_id):
    """التحقق من الحظر قبل السماح بأي عملية حساسة."""
    driver = database.cur.execute(
        "SELECT is_banned FROM driver_profiles WHERE driver_id=?",
        (user_id,)
    ).fetchone()
    customer = database.cur.execute(
        "SELECT is_banned FROM customers WHERE user_id=?",
        (user_id,)
    ).fetchone()
    return bool((driver and driver[0]) or (customer and customer[0]))


def clear_ride_location_state(user_data):
    """منع بقاء خطوات رحلة قديمة والتسبب في تداخل طلبات المستخدم."""
    for key in (
        "awaiting_manual_from", "awaiting_manual_to",
        "awaiting_gps_from", "awaiting_gps_to",
        "manual_from_text", "manual_to_text",
        "from_loc_text", "to_loc_text",
        "from_lat", "from_lon", "to_lat", "to_lon",
    ):
        user_data.pop(key, None)

# ═══════════════════════════════════════════════════════════════════════════
# 🛠️ CORE UTILITY FUNCTIONS (محفوظة من V14 + إضافات جديدة)
# ═══════════════════════════════════════════════════════════════════════════

def haversine(lat1, lon1, lat2, lon2):
    """حساب المسافة بين نقطتين على الأرض بالكيلومترات"""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 9999
    R = 6371.0  # نصف قطر الأرض بالكيلومتر
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def gen_code():
    """توليد كود أمان 4 أرقام عشوائي"""
    return str(random.randint(1000, 9999))

def make_live_link(lat, lon):
    """إنشاء رابط Google Maps للموقع المباشر"""
    return f"https://www.google.com/maps?q={lat},{lon}"


def parse_bid_price(raw_value):
    """تحويل إدخال السعر العربي إلى رقم صالح."""
    value = str(raw_value or "").strip()
    value = value.translate(str.maketrans(
        "٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹",
        "01234567890123456789"
    ))
    value = value.replace("٫", ".").replace("،", ",")
    value = re.sub(r"(جنيه(?:اً)?|جنيه|ج)\s*$", "", value, flags=re.IGNORECASE).strip()

    # السماح بـ 30 أو 30.5 أو 30,5، مع إزالة فواصل الآلاف عند الحاجة.
    if value.count(",") == 1 and "." not in value:
        value = value.replace(",", ".")
    else:
        value = value.replace(",", "")

    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", value):
        return None

    price = float(value)
    return price if price > 0 else None


async def submit_driver_bid(update, context, ride_id, raw_price):
    """حفظ عرض السائق وإرساله للراكب بعد التحقق من كامل السياق."""
    uid = update.effective_user.id
    user_data = context.user_data
    price = parse_bid_price(raw_price)

    if price is None:
        await update.message.reply_text(
            "❌ اكتب السعر كرقم فقط، مثل: 25 أو 30.5\n"
            "ويمكنك أيضاً كتابة: 30 جنيه"
        )
        return False

    driver = database.cur.execute(
        "SELECT approved FROM drivers WHERE user_id=?",
        (uid,)
    ).fetchone()
    if is_banned(uid) or not driver or driver[0] != 1:
        user_data.pop("awaiting_bid_price", None)
        await update.message.reply_text("❌ لا يمكن إرسال عرض إلا من سائق معتمد.")
        return True

    ride = database.cur.execute(
        "SELECT customer_id, from_loc, to_loc, status FROM rides WHERE id=?",
        (ride_id,)
    ).fetchone()
    if not ride or ride[3] != "pending":
        user_data.pop("awaiting_bid_price", None)
        await update.message.reply_text(
            "⚠️ هذه الرحلة لم تعد متاحة لاستقبال عروض جديدة."
        )
        return True

    if database.cur.execute(
        "SELECT 1 FROM bids WHERE ride_id=? AND driver_id=?",
        (ride_id, uid)
    ).fetchone():
        user_data.pop("awaiting_bid_price", None)
        await update.message.reply_text("ℹ️ سبق أن أرسلت عرضاً لهذه الرحلة.")
        return True

    allowed, count = check_spam_protection(uid, "bid")
    if not allowed:
        await update.message.reply_text(
            f"⚠️ قدمت {count} عروض في آخر دقيقة.\n"
            "الحد الأقصى 10 عروض في الدقيقة؛ انتظر قليلاً ثم حاول مرة أخرى."
        )
        return True

    driver_info = database.cur.execute(
        "SELECT name, phone FROM drivers WHERE user_id=?",
        (uid,)
    ).fetchone()
    if not driver_info:
        user_data.pop("awaiting_bid_price", None)
        await update.message.reply_text("❌ بيانات السائق غير مكتملة. استخدم /start ثم حاول.")
        return True

    d_name, d_phone = driver_info
    database.cur.execute(
        "INSERT INTO bids (ride_id, driver_id, driver_name, phone, price) VALUES (?,?,?,?,?)",
        (ride_id, uid, d_name or "سائق وصلني", d_phone or "", price)
    )
    database.con.commit()
    user_data.pop("awaiting_bid_price", None)

    cust_id, from_loc, to_loc, _ = ride
    try:
        await context.bot.send_message(
            cust_id,
            comedy_card(
                f"عرض جديد لرحلة #{ride_id}",
                f"🛺 السائق: {d_name or 'سائق وصلني'}\n"
                f"💰 السعر: {price:.2f} جنيه\n"
                f"📱 الهاتف: {d_phone or 'غير متوفر'}\n\n"
                f"📍 من: {from_loc}\n"
                f"📍 إلى: {to_loc}"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    f"✅ قبول العرض {price:.0f} جنيه",
                    callback_data=f"accept_bid_{ride_id}_{uid}"
                )
            ]])
        )
    except Exception as exc:
        logging.exception("Could not notify customer about bid: %s", exc)

    await update.message.reply_text(
        f"✅ تم إرسال عرضك ({price:.2f} جنيه) للراكب.\n"
        "سيصلك إشعار فور قبول العرض.",
        reply_markup=ReplyKeyboardRemove()
    )
    return True

# ─────────────────────────────────────────────────────────────────────
# 🆕 V15: حساب السعر التلقائي
# ─────────────────────────────────────────────────────────────────────

def calculate_price(distance_km, ride_type="now"):
    """
    حساب السعر المقترح بناءً على المسافة ونوع الرحلة
    
    التسعير:
    - سعر الفتح: 10 جنيه
    - سعر الكيلو: 5 جنيه/كم
    - رحلات المدارس: خصم 20%
    - رحلات بموعد: سعر عادي
    
    مثال: 3 كم = 10 + (3 × 5) = 25 جنيه
    """
    base_price = 10  # سعر الفتح
    per_km = 5       # سعر الكيلومتر
    
    # الحساب الأساسي
    price = base_price + (distance_km * per_km)
    
    # خصم للمدارس
    if ride_type == "school":
        price = price * 0.8  # خصم 20%
        price = max(price, 15)  # الحد الأدنى 15 جنيه
    
    # تقريب لأقرب 5 جنيهات
    price = round(price / 5) * 5
    
    return max(price, 10)  # الحد الأدنى 10 جنيه

# ─────────────────────────────────────────────────────────────────────
# 🆕 V15: حماية من السبام
# ─────────────────────────────────────────────────────────────────────

def check_spam_protection(user_id, action_type="ride"):
    """
    التحقق من السبام والاستخدام المفرط
    
    القيود:
    - الراكب: 3 رحلات كحد أقصى في 10 دقائق
    - السواق: 10 عروض سعر في دقيقة واحدة
    
    Returns:
        tuple: (is_allowed: bool, current_count: int)
    """
    try:
        if action_type == "ride":
            # التحقق من عدد الرحلات في آخر 10 دقائق
            ten_min_ago = (dt.now() - timedelta(minutes=10)).isoformat()
            count = database.cur.execute(
                "SELECT COUNT(*) FROM rides WHERE customer_id=? AND created_at > ?",
                (user_id, ten_min_ago)
            ).fetchone()[0]
            return count < 3, count
        
        elif action_type == "bid":
            # التحقق من عدد العروض في آخر دقيقة
            one_min_ago = (dt.now() - timedelta(minutes=1)).isoformat()
            count = database.cur.execute(
                "SELECT COUNT(*) FROM bids WHERE driver_id=? AND created_at > ?",
                (user_id, one_min_ago)
            ).fetchone()[0]
            return count < 10, count
        
        return True, 0
    except Exception as e:
        print(f"⚠️ spam check error: {e}")
        return True, 0  # في حالة الخطأ، نسمح بالعملية

# ─────────────────────────────────────────────────────────────────────
# 🆕 V15: تحديث متوسط التقييم
# ─────────────────────────────────────────────────────────────────────

def update_rating_average(user_id, user_type="driver"):
    """
    تحديث متوسط التقييم لسواق أو راكب
    
    Args:
        user_id: رقم المستخدم
        user_type: "driver" أو "customer"
    
    Returns:
        tuple: (avg_rating: float, total_ratings: int)
    """
    try:
        # حساب المتوسط من جدول ratings
        result = database.cur.execute(
            "SELECT AVG(rating), COUNT(*) FROM ratings WHERE rated_id=?",
            (user_id,)
        ).fetchone()
        
        avg_rating = round(result[0], 1) if result[0] else 0.0
        total_ratings = result[1] or 0
        
        # تحديث الجدول المناسب
        table = "driver_profiles" if user_type == "driver" else "customers"
        id_col = "driver_id" if user_type == "driver" else "user_id"
        
        database.cur.execute(
            f"UPDATE {table} SET avg_rating=?, total_ratings=? WHERE {id_col}=?",
            (avg_rating, total_ratings, user_id)
        )
        database.con.commit()
        
        return avg_rating, total_ratings
    except Exception as e:
        print(f"⚠️ rating update error: {e}")
        return 0.0, 0

# ─────────────────────────────────────────────────────────────────────
# 🆕 V15: رسائل إسلامية عشوائية ومضحكة
# ─────────────────────────────────────────────────────────────────────

ISLAMIC_GREETINGS = [
    "🕌 بسم الله الرحمن الرحيم",
    "🤲 توكلنا على الله",
    "✨ الحمد لله على السلامة",
    "💫 بإذن الله هنوصل بالسلامة",
    "🌙 الله يوفقك يا معلم",
    "⭐ ربنا يسهل ويعدّيها على خير",
    "🌟 الله معاك في الطريق",
    "💚 بالتوفيق إن شاء الله",
    "🙏 يا رب تكون رحلة آمنة",
    "✨ والله يوصلك بالسلامة",
]

ISLAMIC_ENDINGS = [
    "🤲 توكلنا على الله",
    "✨ الله يوفقك",
    "💚 الله معاك",
    "🌙 ربنا يسهل",
    "⭐ الحمد لله",
    "💫 بإذن الله تمام",
    "🙏 يا رب السلامة",
]

def get_random_greeting():
    """اختيار رسالة ترحيب عشوائية"""
    return random.choice(ISLAMIC_GREETINGS)

def get_random_ending():
    """اختيار رسالة ختامية عشوائية"""
    return random.choice(ISLAMIC_ENDINGS)

def comedy_card(title, body, show_greeting=True, show_ending=True):
    """
    بطاقة رسالة مضحكة بأسلوب إسلامي
    
    Args:
        title: عنوان الرسالة
        body: محتوى الرسالة
        show_greeting: إظهار الترحيب (افتراضي: True)
        show_ending: إظهار الختام (افتراضي: True)
    """
    parts = []
    
    if show_greeting:
        parts.append(get_random_greeting())
    
    parts.append("═" * 40)
    parts.append(f"📢 {title}")
    parts.append("═" * 40)
    parts.append(body)
    parts.append("═" * 40)
    
    if show_ending:
        parts.append(get_random_ending())
    
    return "\n".join(parts)

# ─────────────────────────────────────────────────────────────────────
# Safe Edit Function (محفوظة من V14)
# ─────────────────────────────────────────────────────────────────────

async def safe_edit(q, *a, **k):
    """تعديل آمن للرسائل مع معالجة الأخطاء"""
    text = k.get("text", a[0] if a else "")
    try:
        await q.edit_message_text(*a, **k)
    except Exception as e:
        if "not modified" in str(e).lower():
            return  # الرسالة لم تتغير
        try:
            # محاولة إرسال رسالة جديدة بدلاً من التعديل
            await q.message.reply_text(
                text,
                reply_markup=k.get("reply_markup")
            )
        except:
            pass

# ═══════════════════════════════════════════════════════════════════════════
# 📝 WELCOME MESSAGES & TERMS (محفوظة من V14 + تحديثات)
# ═══════════════════════════════════════════════════════════════════════════

WELCOME_GENERAL = """🕌 بسم الله الرحمن الرحيم
"وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا"

═══════════════════════════════════════
🚕 مرحباً بك في وصلني - سيدي سالم
منصة أهل البلد للتوكتوك الآمن
═══════════════════════════════════════

✨ الجديد في V15 ULTIMATE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ نظام تقييم 5 نجوم
📢 نظام شكاوى منظم  
💰 حساب سعر تلقائي شفاف
📜 تاريخ رحلاتك الكامل
📊 إحصائياتك المفصلة
🛡️ حماية من السبام

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤲 توكلنا على الله - منصة آمنة ومضمونة
═══════════════════════════════════════"""

DRIVER_TERMS = """📜 شروط السواق - 13 بند كامل (إلزامي):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 المستندات المطلوبة:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ صورة شخصية واضحة
2️⃣ صورة التوكتوك واضحة (تظهر للراكب)
3️⃣ صورة البطاقة الشخصية (سرية - لا تظهر للراكب أبداً)
4️⃣ رقم هاتف صحيح (يتم تنسيقه تلقائياً +20)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤝 الالتزامات الأخلاقية:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5️⃣ آداب واحترام الراكب وعدم التلفظ
6️⃣ الالتزام بكود الأمان 4 أرقام - ممنوع منعاً باتاً الركوب بدون التحقق من الكود
7️⃣ التسعير العادل وعدم الاستغلال (السعر المقترح إرشادي)
8️⃣ نظافة التوكتوك والمحافظة عليه

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ القواعد والمسؤوليات:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9️⃣ المنصة وسيط فقط وليست مسؤولة عن الاتفاق المالي
🔟 3 شكاوى موثقة = إيقاف مؤقت ومراجعة من الأدمن
1️⃣1️⃣ للراكب يظهر صورة التوكتوك ورقم الهاتف فقط
1️⃣2️⃣ المسؤولية الجنائية والقانونية كاملة على السواق
1️⃣3️⃣ عدم اكتمال أي بند = عدم الاعتماد وعدم ظهورك

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆕 الجديد: نظام تقييم 5 نجوم
احترم الراكب تحصل على ⭐⭐⭐⭐⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤲 "وَقُل رَّبِّ أَدْخِلْنِي مُدْخَلَ صِدْقٍ" """

CUSTOMER_TERMS = """📜 شروط الراكب - 9 بنود كامل:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 نظام الأمان (إلزامي):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ كود الأمان 4 أرقام - اسأل عليه قبل الركوب
2️⃣ مشاركة موقعك المباشر (Live Location) للعائلة عبر Google Maps
3️⃣ زر طوارئ SOS متاح - يُرسل موقعك للأدمن فوراً

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤝 الالتزامات:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4️⃣ الالتزام بالسعر المتفق عليه قبل الركوب
5️⃣ الحفاظ على التوكتوك ونظافته
6️⃣ ممنوع منعاً باتاً طلب توصيل مواد مخالفة أو خطرة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ الشكاوى والتقييم:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7️⃣ المنصة وسيط فقط - لسنا مسؤولين عن الاتفاق
8️⃣ الشكوى خلال 24 ساعة مع رقم الرحلة والتفاصيل
9️⃣ احترام السواق وعدم الإساءة - قيّمه بإنصاف

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆕 الجديد: قيّم السواق بعد كل رحلة ⭐
ساعدنا نحسّن الخدمة!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💚 "إِنَّ اللَّهَ يُحِبُّ الْمُحْسِنِينَ" """

# يتبع في الجزء التالي...

# ═══════════════════════════════════════════════════════════════════════════
# 🗺️ PLACES DATABASE - كل أماكن سيدي سالم (محفوظة 100% من V14)
# ═══════════════════════════════════════════════════════════════════════════

PLACES_DB = {
    "central": [
        {"id": "hosp_central", "name": "🏥 مستشفى سيدي سالم العام (المركزي)", "lat": 31.2685, "lon": 30.7852, "address": "شارع المستشفى - بندر سيدي سالم"},
        {"id": "hosp_aboghenima", "name": "🏥 مستشفى أبوغنيمة طب الأسرة", "lat": 31.285, "lon": 30.81, "address": "قرية أبوغنيمة"},
        {"id": "hosp_damro", "name": "🏥 مستشفى دمرو", "lat": 31.25, "lon": 30.75, "address": "قرية دمرو"},
        {"id": "mawqef_gharb", "name": "🚌 موقف قرى غرب سيدي سالم", "lat": 31.27, "lon": 30.782, "address": "طريق القصابي"},
        {"id": "mawqef_3am", "name": "🚌 الموقف العمومي الرئيسي", "lat": 31.268, "lon": 30.785, "address": "وسط البلد"},
        {"id": "souk", "name": "🛒 السوق الحضري", "lat": 31.2695, "lon": 30.783, "address": "جنب الموقف"},
        {"id": "bank_ahly", "name": "🏦 البنك الأهلي", "lat": 31.2688, "lon": 30.7845, "address": "شارع 23 يوليو"},
        {"id": "masjed_kebir", "name": "🕌 المسجد الكبير", "lat": 31.2682, "lon": 30.7855, "address": "وسط البلد"},
        {"id": "kornish", "name": "🌊 كورنيش الزهراء", "lat": 31.269, "lon": 30.7835, "address": "كورنيش ترعة الزهراء"},
    ],
    "schools": [
        {"id": "school_teda", "name": "🏫 مجمع مدارس تيدا", "lat": 31.271, "lon": 30.787, "address": "تيدا - سيدي سالم"},
        {"id": "school_tafteesh", "name": "🏫 مدارس التفتيش", "lat": 31.2708, "lon": 30.7865, "address": "منطقة التفتيش"},
        {"id": "school_sidi", "name": "🏫 مدرسة سيدي سالم الثانوية بنين", "lat": 31.2698, "lon": 30.7852, "address": "شارع المدارس"},
        {"id": "school_banat", "name": "🏫 مدرسة سيدي سالم الثانوية بنات", "lat": 31.2689, "lon": 30.7842, "address": "شارع المدارس"},
    ],
    "villages": [
        {"id": "v_qassabi", "name": "🏘️ قرية القصابي", "lat": 31.28, "lon": 30.77, "address": "غرب سيدي سالم"},
        {"id": "v_ghayta", "name": "🏘️ قرية الغيته", "lat": 31.275, "lon": 30.765, "address": "مركز سيدي سالم"},
        {"id": "v_halajen", "name": "🏘️ قرية الحلاجين", "lat": 31.285, "lon": 30.76, "address": "مركز سيدي سالم"},
        {"id": "v_wakeela", "name": "🏘️ قرية الوكيلة", "lat": 31.26, "lon": 30.76, "address": "مركز سيدي سالم"},
        {"id": "v_abusrour", "name": "🏘️ قرية أبو سرور", "lat": 31.295, "lon": 30.795, "address": "مركز سيدي سالم"},
        {"id": "v_bandar", "name": "🏘️ بندر سيدي سالم", "lat": 31.268, "lon": 30.785, "address": "المدينة"},
    ],
    "ezab": [
        {"id": "e_salam", "name": "🏡 عزبة السلام", "lat": 31.275, "lon": 30.775, "address": "من عزب سيدي سالم"},
        {"id": "e_saad", "name": "🏡 عزبة سعد حمد", "lat": 31.274, "lon": 30.775, "address": "عزبة سعد حمد"},
        {"id": "e_giaa", "name": "🏡 عزبة جيعة", "lat": 31.272, "lon": 30.79, "address": "عزبة جيعة"},
        {"id": "e_3", "name": "🏡 عزبة 3 الكبير", "lat": 31.26, "lon": 30.795, "address": "عزبة 3"},
    ]
}

def get_place_by_id(pid):
    """البحث عن مكان بالـ ID"""
    for cat in PLACES_DB.values():
        for p in cat:
            if p["id"] == pid:
                return p
    return None

# ═══════════════════════════════════════════════════════════════════════════
# ⌨️ KEYBOARDS V15 - أزرار كبيرة وواضحة مع نصوص مفصلة
# ═══════════════════════════════════════════════════════════════════════════

def main_kb():
    """الشاشة الرئيسية - أزرار كبيرة"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚕 أنا راكب - طلب توكتوك", callback_data="role_customer")],
        [InlineKeyboardButton("🛺 أنا سواق - تسجيل سواق جديد", callback_data="role_driver")],
    ])

def customer_kb():
    """لوحة الراكب - شاملة مع كل الميزات"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚕 طلب حالاً (فوري الآن)", callback_data="c_now")],
        [InlineKeyboardButton("📅 حجز بموعد محدد", callback_data="c_sched")],
        [InlineKeyboardButton("🎒 حجز مدارس (رخيص وآمن)", callback_data="c_school")],
        [InlineKeyboardButton("📜 رحلاتي السابقة", callback_data="c_history")],
        [InlineKeyboardButton("📊 إحصائياتي وتقييمي", callback_data="c_stats")],
        [InlineKeyboardButton("🆘 طوارئ SOS", callback_data="c_emergency")],
    ])

def driver_kb(available):
    """لوحة السواق - مفصلة"""
    txt = "🟢 متاح للعمل الآن" if available else "🔴 غير متاح حالياً"
    return ReplyKeyboardMarkup([
        [KeyboardButton("📍 تحديث موقعي الحالي"), KeyboardButton(txt)],
        [KeyboardButton("📋 طلبات قريبة مني"), KeyboardButton("📊 إحصائياتي وأرباحي")],
        [KeyboardButton("📜 رحلاتي السابقة"), KeyboardButton("🏠 القائمة الرئيسية")]
    ], resize_keyboard=True)

def phone_kb():
    """طلب رقم الهاتف"""
    return ReplyKeyboardMarkup([
        [KeyboardButton("📱 مشاركة رقم هاتفي", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)

def loc_kb(txt):
    """طلب الموقع"""
    return ReplyKeyboardMarkup([
        [KeyboardButton(txt, request_location=True)]
    ], resize_keyboard=True, one_time_keyboard=True)

def agree_kb(role):
    """الموافقة على الشروط"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ موافق على الشروط كاملة (أقسم بالله)", callback_data=f"agree_{role}")],
        [InlineKeyboardButton("❌ غير موافق (للأسف لن تستطيع استخدام المنصة)", callback_data=f"disagree_{role}")],
    ])

def location_method_kb(purpose):
    """اختيار طريقة تحديد الموقع - 3 طرق"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ 1️⃣ إدخال يدوي (اكتب العنوان بنفسك)", callback_data=f"loc_manual_{purpose}")],
        [InlineKeyboardButton("📍 2️⃣ فتح الخريطة GPS (موقعك الحقيقي)", callback_data=f"loc_gps_{purpose}")],
        [InlineKeyboardButton("🏘️ 3️⃣ اختيار مكان مشهور من القائمة", callback_data=f"loc_places_{purpose}")],
    ])

def places_categories_kb(purpose):
    """فئات الأماكن المشهورة"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏛️ أماكن مركزية (مستشفى، موقف، بنك، مسجد...)", callback_data=f"cat_central_{purpose}")],
        [InlineKeyboardButton("🏫 مدارس ومستشفيات سيدي سالم", callback_data=f"cat_schools_{purpose}")],
        [InlineKeyboardButton("🏘️ قرى سيدي سالم الرئيسية", callback_data=f"cat_villages_{purpose}")],
        [InlineKeyboardButton("🏡 عزب وقرى صغيرة", callback_data=f"cat_ezab_{purpose}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"loc_back_{purpose}")],
    ])

def places_list_kb(category, purpose, page=0):
    """قائمة الأماكن مع pagination"""
    places = PLACES_DB.get(category, [])
    per_page = 8
    start = page * per_page
    slice_places = places[start:start+per_page]
    kb = []
    for p in slice_places:
        kb.append([InlineKeyboardButton(p["name"], callback_data=f"place_{p['id']}_{purpose}")])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"page_{category}_{purpose}_{page-1}"))
    if start + per_page < len(places):
        nav.append(InlineKeyboardButton("التالي ➡️", callback_data=f"page_{category}_{purpose}_{page+1}"))
    if nav:
        kb.append(nav)
    kb.append([InlineKeyboardButton("🔙 رجوع للفئات", callback_data=f"loc_places_{purpose}")])
    return InlineKeyboardMarkup(kb)

# ─────────────────────────────────────────────────────────────────────
# 🆕 V15: كيبوردات التقييم والشكاوى
# ─────────────────────────────────────────────────────────────────────

def rating_kb(ride_id, rated_id, rater_type):
    """أزرار التقييم - 5 نجوم"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐ 1", callback_data=f"rate_{ride_id}_{rated_id}_{rater_type}_1"),
            InlineKeyboardButton("⭐⭐ 2", callback_data=f"rate_{ride_id}_{rated_id}_{rater_type}_2"),
            InlineKeyboardButton("⭐⭐⭐ 3", callback_data=f"rate_{ride_id}_{rated_id}_{rater_type}_3"),
        ],
        [
            InlineKeyboardButton("⭐⭐⭐⭐ 4", callback_data=f"rate_{ride_id}_{rated_id}_{rater_type}_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐ 5", callback_data=f"rate_{ride_id}_{rated_id}_{rater_type}_5"),
        ],
        [InlineKeyboardButton("📢 تقديم شكوى", callback_data=f"open_complaint_{ride_id}_{rated_id}")],
        [InlineKeyboardButton("⏭️ تخطي (لاحقاً)", callback_data=f"skip_rating_{ride_id}")],
    ])

def complaint_type_kb(ride_id, complained_id):
    """أنواع الشكاوى"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏰ تأخر كثير جداً", callback_data=f"comp_{ride_id}_{complained_id}_late")],
        [InlineKeyboardButton("😠 سلوك سيء ومعاملة غير لائقة", callback_data=f"comp_{ride_id}_{complained_id}_behavior")],
        [InlineKeyboardButton("💰 سعر غالي واستغلال", callback_data=f"comp_{ride_id}_{complained_id}_price")],
        [InlineKeyboardButton("🚫 رفض الرحلة بدون سبب", callback_data=f"comp_{ride_id}_{complained_id}_refused")],
        [InlineKeyboardButton("🔐 لم يلتزم بكود الأمان", callback_data=f"comp_{ride_id}_{complained_id}_nocode")],
        [InlineKeyboardButton("📝 شكوى أخرى (اكتب التفاصيل)", callback_data=f"comp_{ride_id}_{complained_id}_other")],
        [InlineKeyboardButton("🔙 إلغاء", callback_data="cancel_complaint")],
    ])

def admin_kb():
    """لوحة الأدمن - شاملة"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚕 كل الرحلات", callback_data="admin_rides")],
        [InlineKeyboardButton("🛺 السواقين المعتمدين", callback_data="admin_drivers"), 
         InlineKeyboardButton("⏳ انتظار موافقة", callback_data="admin_pending")],
        [InlineKeyboardButton("📢 الشكاوى المعلقة", callback_data="admin_complaints"),
         InlineKeyboardButton("👤 الركاب", callback_data="admin_customers")],
        [InlineKeyboardButton("📊 إحصائيات شاملة", callback_data="admin_stats"),
         InlineKeyboardButton("⭐ أعلى التقييمات", callback_data="admin_top_rated")],
    ])

def admin_driver_detail_kb(did):
    """تفاصيل السواق للأدمن"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 صورة شخصية", callback_data=f"ad_file_personal_{did}"),
         InlineKeyboardButton("🛺 صورة التوكتوك", callback_data=f"ad_file_toktok_{did}")],
        [InlineKeyboardButton("🪪 البطاقة (سرية)", callback_data=f"ad_file_id_{did}"),
         InlineKeyboardButton("📱 رقم الهاتف", callback_data=f"ad_file_phone_{did}")],
        [InlineKeyboardButton("⭐ التقييمات", callback_data=f"ad_ratings_{did}"),
         InlineKeyboardButton("📢 الشكاوى", callback_data=f"ad_complaints_{did}")],
        [InlineKeyboardButton("✅ موافقة واعتماد", callback_data=f"ad_approve_{did}"),
         InlineKeyboardButton("🚫 حظر", callback_data=f"ad_ban_{did}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="admin_drivers")],
    ])

# ═══════════════════════════════════════════════════════════════════════════
# 📡 BROADCAST & SMART SEARCH (محفوظة 100% من V14 + تحسينات)
# ═══════════════════════════════════════════════════════════════════════════

async def send_ride_to_drivers(ride_id, from_loc_text, pickup_lat, pickup_lon, code, ride_type_label, driver_ids_with_dist, bot_app, suggested_price):
    """إرسال الطلب للسواقين مع السعر المقترح"""
    for did, dist in driver_ids_with_dist:
        try:
            dist_text = f"{int(dist*1000)} متر" if dist < 1 else f"{dist:.1f} كم"
            message = comedy_card(
                f"طلب {ride_type_label} #{ride_id}",
                f"📍 من: {from_loc_text}\n"
                f"📏 المسافة منك: {dist_text}\n"
                f"💰 السعر المقترح: {suggested_price:.0f} جنيه\n"
                f"(يمكنك تقديم سعر مختلف)\n"
                f"🔒 كود الأمان يبقى مع الراكب ويُتحقق منه عند بدء الرحلة",
                show_ending=True
            )
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(
                f"💰 قدم سعرك لرحلة #{ride_id}",
                callback_data=f"bid_{ride_id}"
            )]])
            await bot_app.bot.send_message(did, message, reply_markup=kb)
        except Exception as e:
            print(f"⚠️ send to driver {did} error: {e}")

async def auto_expand_search(ride_id, pickup_lat, pickup_lon, from_loc_text, code, bot_app, suggested_price):
    """البحث التدريجي الذكي 500م→1كم→2كم→5كم"""
    tiers = [0.5, 1.0, 2.0, 5.0]
    for idx in range(1, len(tiers)):
        await asyncio.sleep(45)  # انتظار 45 ثانية
        
        # التحقق من حالة الرحلة
        row = database.cur.execute(
            "SELECT status, customer_id FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not row:
            return
        status, cust_id = row
        if status != 'pending':
            return  # تم قبول الرحلة
        
        next_radius = tiers[idx]
        prev_radius = tiers[idx-1]
        
        # البحث عن سواقين جدد في النطاق الجديد
        all_drivers = database.cur.execute(
            "SELECT user_id, last_lat, last_lon FROM drivers "
            "WHERE approved=1 AND available=1 AND last_lat IS NOT NULL"
        ).fetchall()
        
        new_batch = []
        for did, dlat, dlon in all_drivers:
            d = haversine(pickup_lat, pickup_lon, dlat, dlon)
            if prev_radius < d <= next_radius:
                new_batch.append((did, d))
        
        if new_batch:
            new_batch.sort(key=lambda x: x[1])
            await send_ride_to_drivers(
                ride_id, from_loc_text, pickup_lat, pickup_lon,
                code, "حالاً", new_batch, bot_app, suggested_price
            )
            try:
                await bot_app.bot.send_message(
                    cust_id,
                    comedy_card(
                        f"توسيع البحث لـ {next_radius} كم",
                        f"🔍 بنبعت لـ {len(new_batch)} سواقين إضافيين\n"
                        f"📍 رحلة #{ride_id}\n"
                        f"⏱️ ما زلنا نبحث عن أفضل سعر لك"
                    )
                )
            except:
                pass

# يتبع الجزء الثالث...

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 COMMAND HANDLERS (محفوظة 100% من V14 + إضافات V15)
# ═══════════════════════════════════════════════════════════════════════════

async def start(update, context):
    """أمر /start - الشاشة الرئيسية"""
    # رسالة الترحيب مع التحديثات الجديدة
    await update.message.reply_text(
        WELCOME_GENERAL,
        reply_markup=main_kb()
    )

async def admin_cmd(update, context):
    """أمر /admin - لوحة تحكم الأدمن الكاملة"""
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        await update.message.reply_text("❌ غير مصرح لك")
        return
    
    # إحصائيات سريعة
    total_rides = database.cur.execute("SELECT COUNT(*) FROM rides").fetchone()[0]
    total_drivers = database.cur.execute("SELECT COUNT(*) FROM driver_profiles WHERE approved_by_admin=1").fetchone()[0]
    pending_drivers = database.cur.execute("SELECT COUNT(*) FROM driver_profiles WHERE approved_by_admin=0").fetchone()[0]
    total_customers = database.cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    pending_complaints = database.cur.execute("SELECT COUNT(*) FROM complaints WHERE status='pending'").fetchone()[0]
    
    msg = f"""🕌 {get_random_greeting()}

═══════════════════════════════════
👑 لوحة تحكم الأدمن V15
═══════════════════════════════════

📊 الإحصائيات السريعة:
━━━━━━━━━━━━━━━━━━━━━━━
🚕 إجمالي الرحلات: {total_rides}
🛺 السواقين المعتمدين: {total_drivers}
⏳ انتظار موافقة: {pending_drivers}
👤 إجمالي الركاب: {total_customers}
📢 شكاوى معلقة: {pending_complaints}

اختر من القائمة أدناه:
{get_random_ending()}"""
    
    await update.message.reply_text(msg, reply_markup=admin_kb())

async def emergency_cmd(update, context):
    """أمر /emergency - طوارئ SOS للراكب"""
    uid = update.effective_user.id
    message = update.effective_message
    
    # التحقق من أن المستخدم راكب
    cust = database.cur.execute("SELECT name, phone FROM customers WHERE user_id=?", (uid,)).fetchone()
    if not cust:
        await message.reply_text("❌ يجب التسجيل كراكب أولاً")
        return
    
    cust_name, cust_phone = cust
    
    # البحث عن آخر رحلة نشطة
    ride = database.cur.execute(
        "SELECT id, driver_id, from_loc, to_loc, status FROM rides "
        "WHERE customer_id=? AND status IN ('accepted','ongoing') "
        "ORDER BY id DESC LIMIT 1",
        (uid,)
    ).fetchone()
    
    if not ride:
        await message.reply_text(
            "⚠️ ليس لديك رحلة نشطة حالياً\n"
            "في حالة الطوارئ اتصل بالشرطة: 122"
        )
        return
    
    ride_id, driver_id, from_loc, to_loc, status = ride
    
    # وضع علامة طوارئ على الرحلة
    database.cur.execute("UPDATE rides SET emergency=1 WHERE id=?", (ride_id,))
    database.con.commit()
    
    # إرسال تنبيه للأدمن
    alert_msg = f"""🚨🚨 طوارئ SOS 🚨🚨
━━━━━━━━━━━━━━━━━━━━━━━
⚠️ راكب في حالة طوارئ!

👤 الراكب: {cust_name}
📱 الهاتف: {cust_phone}
🆔 ID: {uid}

🚕 رحلة #{ride_id}
📍 من: {from_loc}
📍 إلى: {to_loc}
🛺 السواق ID: {driver_id}
📊 الحالة: {status}

⏰ الوقت: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}

🚨 يُرجى التدخل فوراً!"""
    
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(admin_id, alert_msg)
        except:
            pass
    
    await message.reply_text(
        "🚨 تم إرسال تنبيه الطوارئ للإدارة!\n\n"
        "سيتم التواصل معك فوراً\n"
        "في حالة الخطر الشديد اتصل بالشرطة: 122"
    )

# ═══════════════════════════════════════════════════════════════════════════
# 📱 MESSAGE HANDLERS (محفوظة 100% من V14)
# ═══════════════════════════════════════════════════════════════════════════

async def handle_contact(update, context):
    """معالجة مشاركة رقم الهاتف"""
    uid = update.effective_user.id
    contact = update.message.contact
    
    if contact.user_id != uid:
        await update.message.reply_text("❌ يجب إرسال رقمك الشخصي فقط")
        return
    
    # تنسيق رقم الهاتف (إضافة +20 إذا لزم)
    phone = contact.phone_number
    if not phone.startswith("+"):
        if phone.startswith("0"):
            phone = "+20" + phone[1:]
        else:
            phone = "+20" + phone
    
    name = contact.first_name or "مستخدم"
    
    # حفظ حسب الدور المؤقت
    user_data = context.user_data
    role = user_data.get("registering_as")
    
    if role == "customer":
        # حفظ بيانات الراكب مع إبقاء الموافقة على الشروط حتى يضغطها بعد الهاتف.
        database.cur.execute(
            "INSERT INTO customers (user_id, name, phone) VALUES (?,?,?) "
            "ON CONFLICT(user_id) DO UPDATE SET name=excluded.name, phone=excluded.phone",
            (uid, name, phone)
        )
        database.con.commit()
        user_data["phone_shared"] = True
        
        # عرض الشروط
        await update.message.reply_text(
            CUSTOMER_TERMS,
            reply_markup=agree_kb("customer")
        )
    
    elif role == "driver":
        user_data["driver_phone"] = phone
        user_data["driver_name"] = name
        user_data["phone_shared"] = True
        
        await update.message.reply_text(
            "✅ تم حفظ رقم الهاتف\n\n"
            "الخطوة التالية: إرسال صورة شخصية واضحة لك",
            reply_markup=ReplyKeyboardRemove()
        )

async def handle_text(update, context):
    """معالجة الرسائل النصية - كل السيناريوهات"""
    uid = update.effective_user.id
    txt = update.message.text.strip()
    user_data = context.user_data

    # يجب أن تكون رسالة السعر مرتبطة بآخر زر "قدم سعرك" قبل أي حالة نصية أخرى.
    # هذا يمنع تداخلها مع تعليق تقييم أو كود أمان قديم في نفس محادثة السائق.
    if user_data.get("awaiting_bid_price") is not None:
        ride_id = user_data["awaiting_bid_price"]
        await submit_driver_bid(update, context, ride_id, txt)
        return
    
    # ─────────────────────────────────────────────────────────────────
    # السواق: تبديل حالة التوفر
    # ─────────────────────────────────────────────────────────────────
    if txt in ["🟢 متاح للعمل الآن", "🔴 غير متاح حالياً"]:
        if is_banned(uid):
            await update.message.reply_text("⛔ حسابك موقوف ولا يمكنه استقبال أو تنفيذ رحلات.")
            return
        new_state = 1 if "🟢" in txt else 0
        database.cur.execute(
            "UPDATE drivers SET available=? WHERE user_id=?",
            (1-new_state, uid)
        )
        database.con.commit()
        
        # إعادة إرسال الكيبورد
        avail = database.cur.execute("SELECT available FROM drivers WHERE user_id=?", (uid,)).fetchone()
        if avail:
            await update.message.reply_text(
                f"✅ تم التحديث - أنت الآن {'🟢 متاح' if 1-new_state else '🔴 غير متاح'}",
                reply_markup=driver_kb(1-new_state)
            )
        return
    
    # ─────────────────────────────────────────────────────────────────
    # السواق: الطلبات القريبة
    # ─────────────────────────────────────────────────────────────────
    if txt == "📋 طلبات قريبة مني":
        driver = database.cur.execute(
            "SELECT last_lat, last_lon, available, approved FROM drivers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if not driver:
            await update.message.reply_text("❌ يجب التسجيل كسواق أولاً")
            return
        
        dlat, dlon, avail, appr = driver
        
        if not appr:
            await update.message.reply_text("⏳ حسابك تحت المراجعة من الأدمن")
            return
        
        if not dlat or not dlon:
            await update.message.reply_text("📍 يجب تحديث موقعك أولاً")
            return
        
        # البحث عن الرحلات المعلقة القريبة
        pending = database.cur.execute(
            "SELECT id, from_loc, from_lat, from_lon, ride_type FROM rides WHERE status='pending'"
        ).fetchall()
        
        if not pending:
            await update.message.reply_text("😔 لا توجد طلبات متاحة حالياً")
            return
        
        nearby = []
        for rid, floc, flat, flon, rtype in pending:
            if flat and flon:
                dist = haversine(dlat, dlon, flat, flon)
                if dist <= 5:  # 5 كم
                    nearby.append((rid, floc, dist, rtype))
        
        if not nearby:
            await update.message.reply_text("😔 لا توجد طلبات قريبة منك (ضمن 5 كم)")
            return
        
        nearby.sort(key=lambda x: x[2])
        
        msg_parts = [get_random_greeting(), "═" * 40, "📋 الطلبات القريبة منك:", "═" * 40]
        for rid, floc, dist, rtype in nearby[:10]:
            dist_txt = f"{int(dist*1000)} م" if dist < 1 else f"{dist:.1f} كم"
            type_txt = {"now": "حالاً", "scheduled": "بموعد", "school": "مدارس"}.get(rtype, "حالاً")
            msg_parts.append(f"🚕 رحلة #{rid} ({type_txt})")
            msg_parts.append(f"📍 من: {floc}")
            msg_parts.append(f"📏 المسافة: {dist_txt}")
            msg_parts.append("─" * 20)
        
        msg_parts.append(get_random_ending())
        
        await update.message.reply_text("\n".join(msg_parts))
        return

    if txt == "📍 تحديث موقعي الحالي":
        user_data["awaiting_driver_location"] = True
        await update.message.reply_text(
            "📍 اضغط زر مشاركة الموقع من تيليجرام لإرسال موقعك الحالي.",
            reply_markup=loc_kb("📍 مشاركة موقعي الحالي")
        )
        return
    
    # ─────────────────────────────────────────────────────────────────
    # السواق: الإحصائيات
    # ─────────────────────────────────────────────────────────────────
    if txt == "📊 إحصائياتي وأرباحي":
        driver = database.cur.execute(
            "SELECT total_rides, total_earnings FROM drivers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if not driver:
            await update.message.reply_text("❌ يجب التسجيل كسواق أولاً")
            return
        
        total_rides, total_earnings = driver or (0, 0.0)
        
        # التقييم
        profile = database.cur.execute(
            "SELECT avg_rating, total_ratings FROM driver_profiles WHERE driver_id=?",
            (uid,)
        ).fetchone()
        
        avg_rating, total_ratings = profile if profile else (0.0, 0)
        
        # الأرباح اليوم
        today = dt.now().date().isoformat()
        today_earnings = database.cur.execute(
            "SELECT COALESCE(SUM(final_price), 0) FROM rides "
            "WHERE driver_id=? AND status='completed' AND DATE(completed_at)=?",
            (uid, today)
        ).fetchone()[0] or 0.0
        
        msg = f"""{get_random_greeting()}

═══════════════════════════════════
📊 إحصائياتك يا كابتن
═══════════════════════════════════

🚕 إجمالي الرحلات: {total_rides}
💰 إجمالي الأرباح: {total_earnings:.2f} جنيه
💵 أرباح اليوم: {today_earnings:.2f} جنيه

⭐ التقييم: {avg_rating:.1f}/5.0
📊 عدد التقييمات: {total_ratings}

{get_random_ending()}"""
        
        await update.message.reply_text(msg)
        return

    if txt == "📜 رحلاتي السابقة":
        rides = database.cur.execute(
            "SELECT id, from_loc, to_loc, status, final_price, created_at "
            "FROM rides WHERE driver_id=? ORDER BY id DESC LIMIT 10",
            (uid,)
        ).fetchall()
        if not rides:
            await update.message.reply_text("😔 لا توجد رحلات سابقة مسجلة لك.")
            return
        parts = [comedy_card("رحلاتك السابقة", "", show_greeting=False, show_ending=False)]
        for rid, from_loc, to_loc, status, price, created in rides:
            emoji = {"accepted": "🚕", "ongoing": "🛣️", "completed": "✅", "cancelled": "❌"}.get(status, "⏳")
            parts.append(
                f"{emoji} رحلة #{rid}\n📍 {from_loc} → {to_loc}\n"
                f"💰 {float(price or 0):.0f} جنيه | {created[:10]}"
            )
        await update.message.reply_text("\n────────────\n".join(parts))
        return
    
    # ─────────────────────────────────────────────────────────────────
    # القائمة الرئيسية
    # ─────────────────────────────────────────────────────────────────
    if txt == "🏠 القائمة الرئيسية":
        await update.message.reply_text(
            WELCOME_GENERAL,
            reply_markup=main_kb()
        )
        return
    
    # ─────────────────────────────────────────────────────────────────
    # 🆕 V15: حماية من السبام - التحقق قبل الإدخال اليدوي
    # ─────────────────────────────────────────────────────────────────

    if user_data.get("awaiting_schedule"):
        try:
            scheduled_at = dt.strptime(txt, "%Y-%m-%d %H:%M")
            if scheduled_at <= dt.now():
                raise ValueError
        except ValueError:
            await update.message.reply_text(
                "❌ الصيغة غير صحيحة أو الموعد في الماضي.\n"
                "اكتب الموعد هكذا: 2026-09-20 18:30"
            )
            return
        user_data["scheduled_at"] = scheduled_at.isoformat()
        user_data.pop("awaiting_schedule", None)
        await update.message.reply_text(
            f"✅ تم حفظ الموعد: {scheduled_at.strftime('%Y-%m-%d %H:%M')}\n"
            "اضغط تأكيد لإنشاء الرحلة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأكيد الحجز", callback_data="finalize_scheduled")],
                [InlineKeyboardButton("❌ إلغاء", callback_data="cancel_ride_setup")]
            ])
        )
        return
    
    # ─────────────────────────────────────────────────────────────────
    # الإدخال اليدوي للموقع
    # ─────────────────────────────────────────────────────────────────
    if user_data.get("awaiting_manual_from"):
        user_data["manual_from_text"] = txt
        user_data["awaiting_manual_from"] = False
        
        await update.message.reply_text(
            f"✅ تم حفظ الموقع: {txt}\n\n"
            "الآن اختر طريقة إدخال موقع الوصول:",
            reply_markup=location_method_kb("to")
        )
        return
    
    if user_data.get("awaiting_manual_to"):
        user_data["manual_to_text"] = txt
        user_data["awaiting_manual_to"] = False
        
        # 🆕 التحقق من السبام قبل إنشاء الرحلة
        allowed, count = check_spam_protection(uid, "ride")
        if not allowed:
            await update.message.reply_text(
                f"⚠️ تحذير: لقد طلبت {count} رحلات في آخر 10 دقائق!\n\n"
                f"الحد الأقصى: 3 رحلات كل 10 دقائق\n"
                f"يُرجى الانتظار قليلاً قبل طلب رحلة جديدة\n\n"
                f"{get_random_ending()}"
            )
            return
        
        # المتابعة لاختيار نوع الرحلة
        await update.message.reply_text(
            f"✅ تم حفظ الوجهة: {txt}\n\n"
            "اختر نوع الرحلة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚕 حالاً (الآن فوراً)", callback_data="finalize_now")],
                [InlineKeyboardButton("📅 بموعد محدد", callback_data="finalize_sched")],
                [InlineKeyboardButton("🎒 مدارس", callback_data="finalize_school")],
            ])
        )
        return
    
    # ─────────────────────────────────────────────────────────────────
    # 🆕 V15: معالجة تعليق التقييم أو الشكوى
    # ─────────────────────────────────────────────────────────────────
    if user_data.get("awaiting_rating_comment"):
        ride_id, rated_id, rating, rater_type = user_data["awaiting_rating_comment"]
        
        # التقييم حُفظ عند الضغط على النجمة؛ هنا نضيف التعليق فقط.
        database.cur.execute(
            "UPDATE ratings SET comment=? WHERE ride_id=? AND rater_id=? AND rated_id=?",
            (txt, ride_id, uid, rated_id)
        )
        database.con.commit()
        user_data.pop("awaiting_rating_comment", None)
        
        await update.message.reply_text(
            f"✅ شكراً! تم حفظ تقييمك ({rating}⭐) مع التعليق\n\n"
            f"{get_random_ending()}",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    if user_data.get("awaiting_start_code"):
        ride_id = user_data["awaiting_start_code"]
        code = txt.strip()
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status, security_code FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not ride or ride[1] != uid or ride[2] != "accepted":
            user_data.pop("awaiting_start_code", None)
            await update.message.reply_text("❌ الرحلة لم تعد جاهزة للبدء.")
            return
        if not re.fullmatch(r"\d{4}", code) or code != str(ride[3]):
            await update.message.reply_text("❌ كود الأمان غير صحيح. اطلب الكود من الراكب وحاول مرة أخرى.")
            return
        database.cur.execute("UPDATE rides SET status='ongoing' WHERE id=?", (ride_id,))
        database.con.commit()
        user_data.pop("awaiting_start_code", None)
        await update.message.reply_text(
            f"🛣️ بدأت الرحلة #{ride_id} بنجاح.\n"
            "الحمد لله على السلامة — لا تضغط إنهاء إلا بعد الوصول.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ إنهاء الرحلة عند الوصول", callback_data=f"finish_ride_{ride_id}")
            ]])
        )
        try:
            await context.bot.send_message(
                ride[0],
                f"🛣️ بدأ السائق الرحلة #{ride_id} بعد التحقق من كود الأمان.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ وصلت — إنهاء الرحلة", callback_data=f"finish_ride_{ride_id}"),
                    InlineKeyboardButton("🆘 طوارئ", callback_data="c_emergency")
                ]])
            )
        except Exception:
            pass
        return
    
    if user_data.get("awaiting_complaint_details"):
        ride_id, complained_id, comp_type = user_data["awaiting_complaint_details"]
        
        # حفظ الشكوى
        database.cur.execute(
            "INSERT INTO complaints (ride_id, complainant_id, complained_against_id, complaint_type, description, status) "
            "VALUES (?,?,?,?,?,'pending')",
            (ride_id, uid, complained_id, comp_type, txt)
        )
        database.con.commit()
        
        # زيادة عداد الشكاوى
        database.cur.execute(
            "UPDATE driver_profiles SET complaints_count = complaints_count + 1 WHERE driver_id=?",
            (complained_id,)
        )
        database.cur.execute(
            "UPDATE customers SET complaints_count = complaints_count + 1 WHERE user_id=?",
            (complained_id,)
        )
        database.con.commit()
        
        user_data.pop("awaiting_complaint_details", None)
        
        # إرسال للأدمن
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"📢 شكوى جديدة!\n"
                    f"رحلة #{ride_id}\n"
                    f"من: {uid}\n"
                    f"ضد: {complained_id}\n"
                    f"النوع: {comp_type}\n"
                    f"التفاصيل: {txt}"
                )
            except:
                pass
        
        await update.message.reply_text(
            "✅ تم إرسال الشكوى للإدارة\n"
            "سيتم المراجعة والرد خلال 24 ساعة\n\n"
            f"{get_random_ending()}",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # رسالة افتراضية
    await update.message.reply_text(
        f"{get_random_greeting()}\n\n"
        "استخدم /start للقائمة الرئيسية\n\n"
        f"{get_random_ending()}"
    )

async def handle_photo(update, context):
    """معالجة الصور - تسجيل السواق"""
    uid = update.effective_user.id
    photo = update.message.photo[-1]
    file_id = photo.file_id
    user_data = context.user_data
    
    role = user_data.get("registering_as")
    
    if role != "driver":
        await update.message.reply_text("❌ غير مطلوب صورة حالياً")
        return
    
    # تحديد نوع الصورة
    if not user_data.get("driver_personal_photo"):
        user_data["driver_personal_photo"] = file_id
        await update.message.reply_text(
            "✅ تم حفظ الصورة الشخصية\n\n"
            "الخطوة التالية: إرسال صورة التوكتوك واضحة"
        )
    
    elif not user_data.get("driver_toktok_photo"):
        user_data["driver_toktok_photo"] = file_id
        await update.message.reply_text(
            "✅ تم حفظ صورة التوكتوك\n\n"
            "الخطوة الأخيرة: إرسال صورة البطاقة الشخصية (سرية تماماً)"
        )
    
    elif not user_data.get("driver_id_card_photo"):
        user_data["driver_id_card_photo"] = file_id
        
        # حفظ كل البيانات
        database.cur.execute(
            "INSERT OR REPLACE INTO driver_profiles "
            "(driver_id, personal_photo, toktok_photo, id_card_photo, phone, full_name, status, approved_by_admin) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (uid, 
             user_data.get("driver_personal_photo"),
             user_data.get("driver_toktok_photo"),
             file_id,
             user_data.get("driver_phone"),
             user_data.get("driver_name"),
             "pending",
             0)
        )
        database.con.commit()
        
        # عرض الشروط
        await update.message.reply_text(
            DRIVER_TERMS,
            reply_markup=agree_kb("driver")
        )

# يتبع الجزء الرابع - callback handler الضخم...

# ═══════════════════════════════════════════════════════════════════════════
# 🎮 CALLBACK QUERY HANDLER - الضخم والشامل (V14 + V15)
# ═══════════════════════════════════════════════════════════════════════════

async def cb(update, context):
    """معالج Callback الرئيسي - كل الأزرار"""
    q = update.callback_query
    await q.answer()
    
    data = q.data
    uid = q.from_user.id
    user_data = context.user_data
    
    # ═══════════════════════════════════════════════════════════════════════
    # 1️⃣ اختيار الدور (راكب/سواق)
    # ═══════════════════════════════════════════════════════════════════════
    
    if data == "role_customer":
        # التحقق من التسجيل
        cust = database.cur.execute(
            "SELECT agreed_terms FROM customers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if cust and cust[0] == 1:
            # مسجل بالفعل
            await safe_edit(q, text=comedy_card(
                "لوحة الراكب",
                "مرحباً بعودتك! اختر ما تريد:"
            ), reply_markup=customer_kb())
        else:
            # تسجيل جديد
            user_data["registering_as"] = "customer"
            await safe_edit(q, text=CUSTOMER_TERMS, reply_markup=agree_kb("customer"))
    
    elif data == "role_driver":
        # التحقق من التسجيل
        drv = database.cur.execute(
            "SELECT approved_by_admin, agreed_terms FROM driver_profiles WHERE driver_id=?",
            (uid,)
        ).fetchone()
        
        if drv and drv[1] == 1:
            if drv[0] == 1:
                # معتمد
                await safe_edit(q, text="✅ أنت مسجل ومعتمد كسواق")
                driver = database.cur.execute(
                    "SELECT available FROM drivers WHERE user_id=?",
                    (uid,)
                ).fetchone()
                avail = driver[0] if driver else 0
                await q.message.reply_text(
                    "اختر من القائمة:",
                    reply_markup=driver_kb(avail)
                )
            else:
                # انتظار
                await safe_edit(q, text="⏳ طلبك تحت المراجعة من الأدمن\nسيتم إشعارك عند الموافقة")
        else:
            # تسجيل جديد
            user_data["registering_as"] = "driver"
            await safe_edit(q, text=DRIVER_TERMS, reply_markup=agree_kb("driver"))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 2️⃣ الموافقة على الشروط
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("agree_"):
        role = data.split("_")[1]
        
        if role == "customer":
            if not user_data.get("phone_shared"):
                # طلب رقم الهاتف أولاً، ثم يعود المستخدم لنفس الزر للموافقة النهائية.
                await safe_edit(q, text="📱 يُرجى مشاركة رقم هاتفك للتواصل:")
                await q.message.reply_text(
                    "اضغط الزر أدناه لمشاركة رقمك، ثم اضغط موافق مرة أخرى:",
                    reply_markup=phone_kb()
                )
            else:
                database.cur.execute(
                    "UPDATE customers SET agreed_terms=1, agreed_at=? WHERE user_id=?",
                    (dt.now().isoformat(), uid)
                )
                database.con.commit()
                user_data.pop("registering_as", None)
                await safe_edit(q, text=comedy_card(
                    "تم تفعيل حساب الراكب",
                    "ربنا يوصلك بالسلامة! اختر الخدمة التي تريدها."
                ), reply_markup=customer_kb())
        
        elif role == "driver":
            # التحقق من اكتمال البيانات
            if not user_data.get("driver_phone"):
                await safe_edit(q, text="📱 الخطوة الأولى: شارك رقم هاتفك للتواصل:")
                await q.message.reply_text(
                    "اضغط مشاركة رقم هاتفي، وبعدها أرسل الصور بالترتيب.",
                    reply_markup=phone_kb()
                )
                return
            if not user_data.get("driver_personal_photo"):
                await safe_edit(q, text="📸 أرسل صورة شخصية واضحة لك.")
                return
            if not user_data.get("driver_toktok_photo"):
                await safe_edit(q, text="🛺 أرسل صورة التوكتوك واضحة.")
                return
            if not user_data.get("driver_id_card_photo"):
                await safe_edit(q, text="🪪 أرسل صورة البطاقة الشخصية (سرية ولا تظهر للراكب).")
                return
            
            # حفظ الموافقة
            database.cur.execute(
                "UPDATE driver_profiles SET agreed_terms=1, agreed_at=? WHERE driver_id=?",
                (dt.now().isoformat(), uid)
            )
            database.cur.execute(
                "INSERT OR IGNORE INTO drivers (user_id, name, phone, approved) VALUES (?,?,?,?)",
                (uid, user_data.get("driver_name"), user_data.get("driver_phone"), 0)
            )
            database.con.commit()
            
            # إشعار الأدمن
            for admin_id in ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        admin_id,
                        f"🆕 سواق جديد ينتظر الموافقة!\n"
                        f"الاسم: {user_data.get('driver_name')}\n"
                        f"ID: {uid}\n"
                        f"استخدم /admin للمراجعة"
                    )
                except:
                    pass
            
            await safe_edit(q, text=comedy_card(
                "تم التسجيل بنجاح!",
                "طلبك الآن تحت مراجعة الإدارة\n"
                "سيتم إشعارك خلال 24 ساعة\n\n"
                "شكراً لانضمامك لعائلة وصلني 🚕"
            ))
    
    elif data.startswith("disagree_"):
        await safe_edit(q, text="😔 للأسف لا يمكنك استخدام المنصة بدون الموافقة على الشروط")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 3️⃣ الراكب: طلب رحلة
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data in ["c_now", "c_sched", "c_school"]:
        # التحقق من التسجيل
        cust = database.cur.execute(
            "SELECT agreed_terms FROM customers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if not cust or cust[0] != 1:
            await safe_edit(q, text="❌ يجب الموافقة على الشروط أولاً")
            return
        
        ride_type = {"c_now": "now", "c_sched": "scheduled", "c_school": "school"}[data]
        user_data["ride_type"] = ride_type
        
        type_label = {"now": "حالاً", "scheduled": "بموعد", "school": "مدارس"}[ride_type]
        
        await safe_edit(q, text=comedy_card(
            f"طلب رحلة {type_label}",
            "اختر طريقة تحديد موقع الانطلاق:"
        ), reply_markup=location_method_kb("from"))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 4️⃣ تحديد الموقع (3 طرق)
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("loc_manual_"):
        purpose = data.split("_")[2]  # from/to
        
        if purpose == "from":
            user_data["awaiting_manual_from"] = True
            await safe_edit(q, text="✍️ اكتب موقع الانطلاق (مثال: شارع 23 يوليو - سيدي سالم)")
            await q.message.reply_text(
                "انتظر رسالتك...",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            user_data["awaiting_manual_to"] = True
            await safe_edit(q, text="✍️ اكتب موقع الوصول:")
            await q.message.reply_text(
                "انتظر رسالتك...",
                reply_markup=ReplyKeyboardRemove()
            )
    
    elif data.startswith("loc_gps_"):
        purpose = data.split("_")[2]
        
        if purpose == "from":
            await safe_edit(q, text="📍 افتح موقعك GPS بالضغط على الزر:")
            await q.message.reply_text(
                "اضغط لمشاركة موقعك:",
                reply_markup=loc_kb("📍 مشاركة موقع الانطلاق")
            )
            user_data["awaiting_gps_from"] = True
        else:
            await safe_edit(q, text="📍 افتح موقع الوصول GPS:")
            await q.message.reply_text(
                "اضغط لمشاركة موقع الوصول:",
                reply_markup=loc_kb("📍 مشاركة موقع الوصول")
            )
            user_data["awaiting_gps_to"] = True

    elif data.startswith("loc_back_"):
        purpose = data.split("_", 2)[2]
        await safe_edit(
            q,
            text="اختر طريقة تحديد الموقع:",
            reply_markup=location_method_kb(purpose)
        )
    
    elif data.startswith("loc_places_"):
        purpose = data.split("_")[2]
        user_data["loc_purpose"] = purpose
        await safe_edit(q, text="🏘️ اختر الفئة:", reply_markup=places_categories_kb(purpose))
    
    elif data.startswith("cat_"):
        parts = data.split("_")
        category = parts[1]  # central/schools/villages/ezab
        purpose = parts[2]
        
        await safe_edit(q, text="اختر المكان:", reply_markup=places_list_kb(category, purpose, 0))
    
    elif data.startswith("page_"):
        parts = data.split("_")
        category = parts[1]
        purpose = parts[2]
        page = int(parts[3])
        
        await safe_edit(q, text="اختر المكان:", reply_markup=places_list_kb(category, purpose, page))
    
    elif data.startswith("place_"):
        # معرفات الأماكن نفسها قد تحتوي على "_" مثل hosp_central.
        place_id, purpose = data[len("place_"):].rsplit("_", 1)
        
        place = get_place_by_id(place_id)
        if not place:
            await safe_edit(q, text="❌ خطأ: المكان غير موجود")
            return
        
        if purpose == "from":
            user_data["from_loc_text"] = place["name"]
            user_data["from_lat"] = place["lat"]
            user_data["from_lon"] = place["lon"]
            
            await safe_edit(q, text=f"✅ موقع الانطلاق: {place['name']}\n\nاختر موقع الوصول:", 
                           reply_markup=location_method_kb("to"))
        
        else:  # to
            user_data["to_loc_text"] = place["name"]
            user_data["to_lat"] = place["lat"]
            user_data["to_lon"] = place["lon"]
            
            # الانتقال لتحديد نوع الرحلة
            await safe_edit(q, text=f"✅ موقع الوصول: {place['name']}\n\nاختر نوع الرحلة:",
                           reply_markup=InlineKeyboardMarkup([
                               [InlineKeyboardButton("🚕 حالاً", callback_data="finalize_now")],
                               [InlineKeyboardButton("📅 بموعد", callback_data="finalize_sched")],
                               [InlineKeyboardButton("🎒 مدارس", callback_data="finalize_school")],
                           ]))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 5️⃣ إتمام الرحلة وإنشائها
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("finalize_"):
        ride_type = data.split("_", 1)[1]  # now/scheduled/school
        if ride_type == "sched":
            ride_type = "scheduled"

        if ride_type == "scheduled" and not user_data.get("scheduled_at"):
            user_data["awaiting_schedule"] = True
            await safe_edit(
                q,
                text="📅 اكتب موعد الرحلة بصيغة:\n2026-09-20 18:30",
                reply_markup=None
            )
            return
        
        from_text = user_data.get("from_loc_text") or user_data.get("manual_from_text")
        to_text = user_data.get("to_loc_text") or user_data.get("manual_to_text")
        from_lat = user_data.get("from_lat")
        from_lon = user_data.get("from_lon")
        to_lat = user_data.get("to_lat")
        to_lon = user_data.get("to_lon")
        
        if not from_text or not to_text:
            await safe_edit(q, text="❌ يجب تحديد موقع الانطلاق والوصول أولاً")
            return
        
        # 🆕 حماية من السبام
        allowed, count = check_spam_protection(uid, "ride")
        if not allowed:
            await safe_edit(q, text=comedy_card(
                "⚠️ تحذير: كثرة الطلبات!",
                f"لقد طلبت {count} رحلات في آخر 10 دقائق\n\n"
                f"الحد الأقصى: 3 رحلات كل 10 دقائق\n"
                f"يُرجى الانتظار قليلاً"
            ))
            return
        
        # حساب المسافة
        distance = 0
        if from_lat and from_lon and to_lat and to_lon:
            distance = haversine(from_lat, from_lon, to_lat, to_lon)
        
        # 🆕 حساب السعر المقترح
        suggested_price = calculate_price(distance, ride_type) if distance > 0 else 20
        
        # كود الأمان
        code = gen_code()
        
        # إنشاء الرحلة
        database.cur.execute(
            "INSERT INTO rides (customer_id, from_loc, to_loc, from_lat, from_lon, to_lat, to_lon, "
            "distance, status, ride_type, security_code, suggested_price) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (uid, from_text, to_text, from_lat, from_lon, to_lat, to_lon,
             distance, 'pending', ride_type, code, suggested_price)
        )
        database.con.commit()
        
        ride_id = database.cur.lastrowid
        
        # إرسال للسواقين القريبين
        nearby_drivers = []
        if from_lat and from_lon:
            all_drivers = database.cur.execute(
                "SELECT user_id, last_lat, last_lon FROM drivers "
                "WHERE approved=1 AND available=1 AND last_lat IS NOT NULL"
            ).fetchall()
            
            for did, dlat, dlon in all_drivers:
                d = haversine(from_lat, from_lon, dlat, dlon)
                if d <= 0.5:  # 500 متر
                    nearby_drivers.append((did, d))
            
            nearby_drivers.sort(key=lambda x: x[1])
        
        type_label = {"now": "حالاً", "scheduled": "بموعد", "school": "مدارس"}.get(ride_type, "حالاً")
        
        if nearby_drivers:
            await send_ride_to_drivers(
                ride_id, from_text, from_lat, from_lon,
                code, type_label, nearby_drivers, context.application, suggested_price
            )
            
        # بدء البحث التوسعي حتى لو لم يوجد سائق في أول 500 متر.
        if from_lat and from_lon:
            asyncio.create_task(auto_expand_search(
                ride_id, from_lat, from_lon, from_text,
                code, context.application, suggested_price
            ))
        
        live_link = make_live_link(from_lat, from_lon) if from_lat else ""
        
        await safe_edit(q, text=comedy_card(
            f"✅ تم إنشاء رحلة #{ride_id}",
            f"📍 من: {from_text}\n"
            f"📍 إلى: {to_text}\n"
            f"📏 المسافة: {distance:.1f} كم\n"
            f"💰 السعر المقترح: {suggested_price:.0f} جنيه\n"
            f"{'📅 الموعد: ' + user_data.get('scheduled_at', '') + chr(10) if ride_type == 'scheduled' else ''}"
            f"🔐 كود الأمان: {code}\n\n"
            f"{'🔍 تم إرسال الطلب لـ ' + str(len(nearby_drivers)) + ' سواق قريب' if nearby_drivers else '⏳ جاري البحث عن سواقين...'}\n\n"
            f"📱 شارك موقعك المباشر للعائلة:\n{live_link}"
        ))
        clear_ride_location_state(user_data)
        user_data.pop("scheduled_at", None)

    elif data == "cancel_ride_setup":
        clear_ride_location_state(user_data)
        user_data.pop("ride_type", None)
        user_data.pop("scheduled_at", None)
        await safe_edit(q, text="❌ تم إلغاء إعداد الرحلة.", reply_markup=customer_kb())
    
    # ═══════════════════════════════════════════════════════════════════════
    # 6️⃣ السواق: تقديم عرض سعر
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("bid_"):
        try:
            ride_id = int(data[len("bid_"):])
        except (TypeError, ValueError):
            await safe_edit(q, text="❌ زر عرض السعر غير صالح. اطلب إرسال الرحلة مرة أخرى.")
            return
        
        # التحقق من السواق
        driver = database.cur.execute(
            "SELECT approved, available FROM drivers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if is_banned(uid) or not driver or driver[0] != 1:
            await safe_edit(q, text="❌ يجب أن تكون سواقاً معتمداً")
            return
        
        # التحقق من الرحلة
        ride = database.cur.execute(
            "SELECT status, suggested_price FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        
        if not ride:
            await safe_edit(q, text="❌ الرحلة غير موجودة")
            return
        
        if ride[0] != 'pending':
            await safe_edit(q, text="❌ الرحلة لم تعد متاحة")
            return

        if database.cur.execute(
            "SELECT 1 FROM bids WHERE ride_id=? AND driver_id=?",
            (ride_id, uid)
        ).fetchone():
            await safe_edit(q, text="ℹ️ قدمت عرضاً لهذه الرحلة من قبل.")
            return
        
        suggested = ride[1] or 20
        
        # اجعل هذه المحادثة في حالة عرض سعر واحدة فقط، ولا تسمح لحالة قديمة
        # (تعليق/شكوى/كود أمان) بابتلاع السعر الذي سيكتبه السائق.
        for key in (
            "awaiting_rating_comment",
            "awaiting_start_code",
            "awaiting_complaint_details",
            "awaiting_driver_location",
        ):
            user_data.pop(key, None)
        user_data["awaiting_bid_price"] = ride_id
        
        await safe_edit(
            q,
            text=(
                f"💰 السعر المقترح: {suggested:.0f} جنيه\n\n"
                "✍️ اكتب سعرك الآن في رسالة منفصلة.\n"
                "مثال: 25 أو 30 جنيه"
            ),
            reply_markup=None
        )
        try:
            await q.message.reply_text(
                "⌨️ أرسل السعر الآن، وسيصل عرضك للراكب مباشرة.",
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception:
            pass
    
    elif data.startswith("accept_bid_"):
        parts = data.split("_")
        ride_id = int(parts[2])
        driver_id = int(parts[3])
        
        # التحقق من الرحلة
        ride = database.cur.execute(
            "SELECT customer_id, status FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        
        if not ride or ride[1] != 'pending':
            await safe_edit(q, text="❌ الرحلة لم تعد متاحة")
            return
        
        if ride[0] != uid:
            await safe_edit(q, text="❌ ليست رحلتك")
            return
        
        # الحصول على سعر العرض
        bid = database.cur.execute(
            "SELECT price FROM bids WHERE ride_id=? AND driver_id=?",
            (ride_id, driver_id)
        ).fetchone()
        
        if not bid:
            await safe_edit(q, text="❌ العرض غير موجود")
            return
        
        final_price = bid[0]
        
        # تحديث الرحلة
        database.cur.execute(
            "UPDATE rides SET status='accepted', driver_id=?, final_price=? WHERE id=?",
            (driver_id, final_price, ride_id)
        )
        
        # تحديث إحصائيات السواق
        database.cur.execute(
            "UPDATE drivers SET total_rides = total_rides + 1 WHERE user_id=?",
            (driver_id,)
        )
        
        database.con.commit()
        
        # إشعار السواق
        try:
            await context.bot.send_message(
                driver_id,
                comedy_card(
                    f"✅ تم قبول عرضك!",
                    f"🚕 رحلة #{ride_id}\n"
                    f"💰 السعر المتفق: {final_price:.0f} جنيه\n\n"
                    f"🔐 تأكد من كود الأمان قبل بدء الرحلة\n"
                    f"🤝 احترم الراكب وقدم خدمة ممتازة"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🛣️ بدء الرحلة والتحقق من الكود", callback_data=f"start_ride_{ride_id}")
                ]])
            )
        except:
            pass
        
        await safe_edit(q, text=comedy_card(
            "✅ تم قبول العرض!",
            f"🚕 رحلة #{ride_id}\n"
            f"💰 السعر: {final_price:.0f} جنيه\n\n"
            f"السائق سيبدأ الرحلة بعد التحقق من كود الأمان\n"
            f"🔐 لا تركب إلا بعد التحقق من كود الأمان"
        ))

    elif data.startswith("start_ride_"):
        try:
            ride_id = int(data.rsplit("_", 1)[1])
        except (ValueError, IndexError):
            await safe_edit(q, text="❌ طلب غير صالح")
            return
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not ride or ride[1] != uid or ride[2] != "accepted":
            await safe_edit(q, text="❌ لا يمكنك بدء هذه الرحلة أو أنها بدأت بالفعل.")
            return
        user_data["awaiting_start_code"] = ride_id
        await safe_edit(
            q,
            text="🔐 اطلب كود الأمان المكوّن من 4 أرقام من الراكب، ثم اكتبه هنا:"
        )

    elif data.startswith("finish_ride_"):
        try:
            ride_id = int(data.rsplit("_", 1)[1])
        except (ValueError, IndexError):
            await safe_edit(q, text="❌ طلب غير صالح")
            return
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status, final_price FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not ride or uid not in (ride[0], ride[1]) or ride[2] != "ongoing":
            await safe_edit(q, text="❌ لا يمكن إنهاء هذه الرحلة الآن.")
            return
        completed_at = dt.now().isoformat()
        database.cur.execute(
            "UPDATE rides SET status='completed', completed_at=? WHERE id=? AND status='ongoing'",
            (completed_at, ride_id)
        )
        if ride[1]:
            database.cur.execute(
                "UPDATE drivers SET total_earnings=total_earnings + ? WHERE user_id=?",
                (ride[3] or 0, ride[1])
            )
        database.con.commit()
        await safe_edit(q, text="✅ تم إنهاء الرحلة. الحمد لله على السلامة!")
        try:
            await context.bot.send_message(
                ride[0],
                comedy_card(
                    "✅ انتهت الرحلة",
                    f"رحلة #{ride_id}\n💰 السعر المتفق: {float(ride[3] or 0):.0f} جنيه\n"
                    "شاركنا تقييمك، فالسائق لا يعيش على الدعاء وحده 😄",
                    show_ending=False
                ),
                reply_markup=rating_kb(ride_id, ride[1], "customer")
            )
            await context.bot.send_message(
                ride[1],
                "⭐ قيّم الراكب بعد وصوله، فالأخلاق الحلوة توصل قبل التوكتوك.",
                reply_markup=rating_kb(ride_id, ride[0], "driver")
            )
        except Exception:
            pass
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🆕 7️⃣ V15: نظام التقييم
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("rate_"):
        parts = data.split("_")
        try:
            ride_id = int(parts[1])
            rated_id = int(parts[2])
            rater_type = parts[3]  # customer/driver
            rating = int(parts[4])  # 1-5
        except (ValueError, IndexError):
            await safe_edit(q, text="❌ تقييم غير صالح")
            return
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        expected_rated = (
            (ride[1] if rater_type == "customer" else ride[0])
            if ride else None
        )
        if (
            not ride or ride[2] != "completed" or rating not in range(1, 6)
            or uid != (ride[0] if rater_type == "customer" else ride[1])
            or rater_type not in ("customer", "driver")
            or rated_id != expected_rated
            or database.cur.execute(
                "SELECT 1 FROM ratings WHERE ride_id=? AND rater_id=?",
                (ride_id, uid)
            ).fetchone()
        ):
            await safe_edit(q, text="❌ لا يمكن تسجيل هذا التقييم أو تم تسجيله من قبل.")
            return
        
        # حفظ التقييم بدون تعليق
        database.cur.execute(
            "INSERT INTO ratings (ride_id, rater_id, rated_id, rating, rater_type) "
            "VALUES (?,?,?,?,?)",
            (ride_id, uid, rated_id, rating, rater_type)
        )
        database.con.commit()
        
        # تحديث المتوسط
        target_type = "driver" if rater_type == "customer" else "customer"
        avg, total = update_rating_average(rated_id, target_type)
        
        # سؤال عن تعليق اختياري
        await safe_edit(q, text=comedy_card(
            f"شكراً! تقييمك: {rating}⭐",
            f"تم حفظ تقييمك بنجاح\n\n"
            f"{'⭐' * rating}\n\n"
            f"هل تريد إضافة تعليق؟ (اختياري)\n"
            f"اكتب تعليقك أو اضغط تخطي"
        ), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏭️ تخطي", callback_data=f"skip_comment_{ride_id}")]
        ]))
        
        # حفظ في user_data لاستقبال التعليق
        user_data["awaiting_rating_comment"] = (ride_id, rated_id, rating, rater_type)
    
    elif data.startswith("skip_rating_"):
        await safe_edit(q, text=f"{get_random_ending()}\n\nيمكنك التقييم لاحقاً من تاريخ رحلاتك")
    
    elif data.startswith("skip_comment_"):
        user_data.pop("awaiting_rating_comment", None)
        await safe_edit(q, text=f"✅ تم حفظ التقييم\n\n{get_random_ending()}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🆕 8️⃣ V15: نظام الشكاوى
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data.startswith("open_complaint_"):
        try:
            ride_id, complained_id = map(int, data[len("open_complaint_"):].split("_", 1))
        except (ValueError, IndexError):
            await safe_edit(q, text="❌ طلب شكوى غير صالح")
            return
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not ride or ride[2] != "completed" or uid not in ride[:2] or complained_id not in ride[:2] or uid == complained_id:
            await safe_edit(q, text="❌ لا يمكنك تقديم شكوى على هذه الرحلة.")
            return
        await safe_edit(
            q,
            text="📢 اختر سبب الشكوى، وسنراجعها بهدوء وعدل:",
            reply_markup=complaint_type_kb(ride_id, complained_id)
        )

    elif data.startswith("comp_"):
        parts = data.split("_")
        try:
            ride_id = int(parts[1])
            complained_id = int(parts[2])
        except (ValueError, IndexError):
            await safe_edit(q, text="❌ شكوى غير صالحة")
            return
        comp_type = parts[3]  # late/behavior/price/refused/nocode/other
        
        comp_labels = {
            "late": "تأخر كثير",
            "behavior": "سلوك سيء",
            "price": "استغلال في السعر",
            "refused": "رفض الرحلة",
            "nocode": "عدم الالتزام بكود الأمان",
            "other": "أخرى"
        }
        ride = database.cur.execute(
            "SELECT customer_id, driver_id, status FROM rides WHERE id=?",
            (ride_id,)
        ).fetchone()
        if not ride or ride[2] != "completed" or uid not in ride[:2] or complained_id not in ride[:2] or uid == complained_id:
            await safe_edit(q, text="❌ لا يمكنك تقديم شكوى على هذه الرحلة.")
            return
        
        if comp_type == "other":
            # طلب التفاصيل
            user_data["awaiting_complaint_details"] = (ride_id, complained_id, "أخرى")
            await safe_edit(q, text="📝 اكتب تفاصيل الشكوى:")
        else:
            # حفظ الشكوى مباشرة
            database.cur.execute(
                "INSERT INTO complaints (ride_id, complainant_id, complained_against_id, complaint_type, status) "
                "VALUES (?,?,?,?,'pending')",
                (ride_id, uid, complained_id, comp_labels[comp_type])
            )
            database.con.commit()
            
            # زيادة العداد
            database.cur.execute(
                "UPDATE driver_profiles SET complaints_count = complaints_count + 1 WHERE driver_id=?",
                (complained_id,)
            )
            database.con.commit()
            
            # إشعار الأدمن
            for admin_id in ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        admin_id,
                        f"📢 شكوى جديدة!\n"
                        f"رحلة #{ride_id}\n"
                        f"النوع: {comp_labels[comp_type]}\n"
                        f"من: {uid}\n"
                        f"ضد: {complained_id}"
                    )
                except:
                    pass
            
            await safe_edit(q, text=comedy_card(
                "✅ تم إرسال الشكوى",
                "سيتم المراجعة خلال 24 ساعة\n"
                "شكراً لمساعدتنا في تحسين الخدمة"
            ))
    
    elif data == "cancel_complaint":
        await safe_edit(q, text="تم الإلغاء")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🆕 9️⃣ V15: تاريخ الرحلات والإحصائيات
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data == "c_history":
        # آخر 10 رحلات للراكب
        rides = database.cur.execute(
            "SELECT id, from_loc, to_loc, status, final_price, created_at FROM rides "
            "WHERE customer_id=? ORDER BY id DESC LIMIT 10",
            (uid,)
        ).fetchall()
        
        if not rides:
            await safe_edit(q, text="😔 ليس لديك رحلات سابقة")
            return
        
        msg_parts = [get_random_greeting(), "═" * 40, "📜 آخر 10 رحلات:", "═" * 40]
        
        for rid, floc, tloc, status, price, created in rides:
            status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "✔️", "cancelled": "❌"}.get(status, "❓")
            msg_parts.append(f"{status_emoji} رحلة #{rid}")
            msg_parts.append(f"📍 {floc} → {tloc}")
            msg_parts.append(f"💰 {price:.0f} جنيه" if price else "⏳ انتظار عروض")
            msg_parts.append(f"📅 {created[:10]}")
            msg_parts.append("─" * 20)
        
        msg_parts.append(get_random_ending())
        
        await safe_edit(q, text="\n".join(msg_parts))
    
    elif data == "c_stats":
        # إحصائيات الراكب
        cust = database.cur.execute(
            "SELECT avg_rating, total_ratings, complaints_count FROM customers WHERE user_id=?",
            (uid,)
        ).fetchone()
        
        if not cust:
            await safe_edit(q, text="❌ غير مسجل")
            return
        
        avg_rating, total_ratings, complaints = cust
        
        total_rides = database.cur.execute(
            "SELECT COUNT(*) FROM rides WHERE customer_id=?",
            (uid,)
        ).fetchone()[0]
        
        completed_rides = database.cur.execute(
            "SELECT COUNT(*) FROM rides WHERE customer_id=? AND status='completed'",
            (uid,)
        ).fetchone()[0]
        
        total_spent = database.cur.execute(
            "SELECT COALESCE(SUM(final_price), 0) FROM rides WHERE customer_id=? AND status='completed'",
            (uid,)
        ).fetchone()[0] or 0.0
        
        msg = f"""{get_random_greeting()}

═══════════════════════════════════
📊 إحصائياتك كراكب
═══════════════════════════════════

🚕 إجمالي الرحلات: {total_rides}
✅ رحلات مكتملة: {completed_rides}
💰 إجمالي المصروفات: {total_spent:.2f} جنيه

⭐ تقييمك: {avg_rating:.1f}/5.0
📊 عدد التقييمات: {total_ratings}
📢 الشكاوى ضدك: {complaints}

{get_random_ending()}"""
        
        await safe_edit(q, text=msg)
    
    elif data == "d_stats":
        # إحصائيات السواق (من زر الكيبورد)
        # تم معالجتها في handle_text
        pass
    
    # يتبع الجزء الخامس - لوحة الأدمن...

    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔟 لوحة الأدمن - كل الوظائف
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data == "admin_rides":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        rides = database.cur.execute(
            "SELECT id, customer_id, driver_id, from_loc, to_loc, status, final_price, created_at "
            "FROM rides ORDER BY id DESC LIMIT 20"
        ).fetchall()
        
        if not rides:
            await safe_edit(q, text="لا توجد رحلات")
            return
        
        msg_parts = ["═" * 40, "🚕 آخر 20 رحلة:", "═" * 40]
        
        for rid, cid, did, floc, tloc, status, price, created in rides:
            status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "✔️", "cancelled": "❌"}.get(status, "❓")
            msg_parts.append(f"{status_emoji} #{rid} | {status}")
            msg_parts.append(f"👤 C:{cid} | D:{did or 'None'}")
            msg_parts.append(f"📍 {floc[:30]} → {tloc[:30]}")
            msg_parts.append(f"💰 {price or 0:.0f}ج | {created[:10]}")
            msg_parts.append("─" * 20)
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")]
        ]))
    
    elif data == "admin_drivers":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        drivers = database.cur.execute(
            "SELECT driver_id, full_name, phone, status, avg_rating, total_ratings, complaints_count "
            "FROM driver_profiles WHERE approved_by_admin=1 ORDER BY driver_id DESC LIMIT 20"
        ).fetchall()
        
        if not drivers:
            await safe_edit(q, text="لا يوجد سواقين معتمدين")
            return
        
        msg_parts = ["═" * 40, "🛺 السواقين المعتمدين:", "═" * 40]
        kb = []
        
        for did, name, phone, status, rating, total_r, complaints in drivers:
            msg_parts.append(f"🛺 {name} (ID: {did})")
            msg_parts.append(f"📱 {phone}")
            msg_parts.append(f"⭐ {rating:.1f}/5 ({total_r} تقييم)")
            msg_parts.append(f"📢 {complaints} شكوى")
            msg_parts.append("─" * 20)
            
            kb.append([InlineKeyboardButton(f"👤 {name or did}", callback_data=f"ad_review_{did}")])
        
        kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")])
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup(kb))
    
    elif data == "admin_pending":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        pending = database.cur.execute(
            "SELECT driver_id, full_name, phone FROM driver_profiles WHERE approved_by_admin=0"
        ).fetchall()
        
        if not pending:
            await safe_edit(q, text="✅ لا يوجد طلبات انتظار")
            return
        
        msg_parts = ["═" * 40, "⏳ سواقين ينتظرون الموافقة:", "═" * 40]
        kb = []
        
        for did, name, phone in pending:
            msg_parts.append(f"🛺 {name or 'بدون اسم'}")
            msg_parts.append(f"📱 {phone}")
            msg_parts.append(f"🆔 ID: {did}")
            msg_parts.append("─" * 20)
            
            kb.append([InlineKeyboardButton(f"👀 مراجعة {name or did}", callback_data=f"ad_review_{did}")])
        
        kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")])
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup(kb))
    
    elif data.startswith("ad_review_"):
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        did = int(data.split("_")[2])
        
        driver = database.cur.execute(
            "SELECT full_name, phone, personal_photo, toktok_photo, id_card_photo "
            "FROM driver_profiles WHERE driver_id=?",
            (did,)
        ).fetchone()
        
        if not driver:
            await safe_edit(q, text="❌ السواق غير موجود")
            return
        
        name, phone, pp, tp, idp = driver
        
        msg = f"""═══════════════════════════════════
👤 مراجعة السواق
═══════════════════════════════════

🛺 الاسم: {name or 'غير متوفر'}
📱 الهاتف: {phone}
🆔 ID: {did}

📸 الصور: {"✅" if all([pp, tp, idp]) else "❌ ناقصة"}

اختر إجراء:"""
        
        await safe_edit(q, text=msg, reply_markup=admin_driver_detail_kb(did))
    
    elif data.startswith("ad_file_"):
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        parts = data.split("_")
        file_type = parts[2]  # personal/toktok/id/phone
        did = int(parts[3])
        
        if file_type == "phone":
            phone = database.cur.execute(
                "SELECT phone FROM driver_profiles WHERE driver_id=?",
                (did,)
            ).fetchone()
            
            if phone:
                await safe_edit(q, text=f"📱 رقم الهاتف:\n{phone[0]}")
            else:
                await safe_edit(q, text="❌ غير متوفر")
            return
        
        col_map = {"personal": "personal_photo", "toktok": "toktok_photo", "id": "id_card_photo"}
        col = col_map.get(file_type)
        
        if not col:
            return
        
        file_id = database.cur.execute(
            f"SELECT {col} FROM driver_profiles WHERE driver_id=?",
            (did,)
        ).fetchone()
        
        if file_id and file_id[0]:
            try:
                await context.bot.send_photo(uid, file_id[0], caption=f"صورة {file_type} للسواق {did}")
            except Exception as e:
                await safe_edit(q, text=f"❌ خطأ في إرسال الصورة: {e}")
        else:
            await safe_edit(q, text="❌ الصورة غير موجودة")
    
    elif data.startswith("ad_approve_"):
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        did = int(data.split("_")[2])
        
        database.cur.execute(
            "UPDATE driver_profiles SET approved_by_admin=1, status='approved' WHERE driver_id=?",
            (did,)
        )
        database.cur.execute(
            "UPDATE drivers SET approved=1 WHERE user_id=?",
            (did,)
        )
        database.con.commit()
        
        # إشعار السواق
        try:
            await context.bot.send_message(
                did,
                comedy_card(
                    "🎉 مبروك! تم الموافقة",
                    "تم اعتماد حسابك كسواق\n"
                    "يمكنك الآن استقبال الطلبات\n\n"
                    "استخدم /start للبدء"
                )
            )
        except:
            pass
        
        await safe_edit(q, text=f"✅ تم اعتماد السواق {did}")
    
    elif data.startswith("ad_ban_"):
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        did = int(data.split("_")[2])
        
        database.cur.execute(
            "UPDATE driver_profiles SET is_banned=1, status='banned', approved_by_admin=0 WHERE driver_id=?",
            (did,)
        )
        database.cur.execute(
            "UPDATE drivers SET approved=0, available=0 WHERE user_id=?",
            (did,)
        )
        database.con.commit()
        
        # إشعار
        try:
            await context.bot.send_message(
                did,
                "⛔ تم إيقاف حسابك من قبل الإدارة\n"
                "للاستفسار تواصل مع الأدمن"
            )
        except:
            pass
        
        await safe_edit(q, text=f"⛔ تم حظر السواق {did}")
    
    elif data == "admin_complaints":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        complaints = database.cur.execute(
            "SELECT id, ride_id, complainant_id, complained_against_id, complaint_type, description, created_at "
            "FROM complaints WHERE status='pending' ORDER BY id DESC LIMIT 10"
        ).fetchall()
        
        if not complaints:
            await safe_edit(q, text="✅ لا توجد شكاوى معلقة")
            return
        
        msg_parts = ["═" * 40, "📢 الشكاوى المعلقة:", "═" * 40]
        
        for cid, rid, comp_from, comp_against, ctype, desc, created in complaints:
            msg_parts.append(f"📢 شكوى #{cid}")
            msg_parts.append(f"🚕 رحلة #{rid}")
            msg_parts.append(f"من: {comp_from} ضد: {comp_against}")
            msg_parts.append(f"النوع: {ctype}")
            if desc:
                msg_parts.append(f"التفاصيل: {desc[:50]}...")
            msg_parts.append(f"📅 {created[:10]}")
            msg_parts.append("─" * 20)
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")]
        ]))
    
    elif data == "admin_customers":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        customers = database.cur.execute(
            "SELECT user_id, name, phone, avg_rating, total_ratings, complaints_count "
            "FROM customers ORDER BY user_id DESC LIMIT 20"
        ).fetchall()
        
        if not customers:
            await safe_edit(q, text="لا يوجد ركاب")
            return
        
        msg_parts = ["═" * 40, "👤 الركاب المسجلين:", "═" * 40]
        
        for cid, name, phone, rating, total_r, complaints in customers:
            msg_parts.append(f"👤 {name or 'بدون اسم'} (ID: {cid})")
            msg_parts.append(f"📱 {phone}")
            msg_parts.append(f"⭐ {rating:.1f}/5 ({total_r} تقييم)")
            msg_parts.append(f"📢 {complaints} شكوى")
            msg_parts.append("─" * 20)
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")]
        ]))
    
    elif data == "admin_stats":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        total_rides = database.cur.execute("SELECT COUNT(*) FROM rides").fetchone()[0]
        completed = database.cur.execute("SELECT COUNT(*) FROM rides WHERE status='completed'").fetchone()[0]
        pending = database.cur.execute("SELECT COUNT(*) FROM rides WHERE status='pending'").fetchone()[0]
        
        total_drivers = database.cur.execute("SELECT COUNT(*) FROM driver_profiles WHERE approved_by_admin=1").fetchone()[0]
        total_customers = database.cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        
        total_revenue = database.cur.execute("SELECT COALESCE(SUM(final_price), 0) FROM rides WHERE status='completed'").fetchone()[0] or 0.0
        
        total_ratings = database.cur.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
        total_complaints = database.cur.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        
        msg = f"""═══════════════════════════════════
📊 إحصائيات المنصة الشاملة
═══════════════════════════════════

🚕 الرحلات:
  • إجمالي: {total_rides}
  • مكتملة: {completed}
  • معلقة: {pending}

👥 المستخدمين:
  • سواقين: {total_drivers}
  • ركاب: {total_customers}

💰 الإيرادات الإجمالية: {total_revenue:.2f} جنيه

⭐ التقييمات: {total_ratings}
📢 الشكاوى: {total_complaints}

{get_random_ending()}"""
        
        await safe_edit(q, text=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")]
        ]))
    
    elif data == "admin_top_rated":
        if uid not in ADMIN_IDS:
            await safe_edit(q, text="❌ غير مصرح")
            return
        
        top_drivers = database.cur.execute(
            "SELECT driver_id, full_name, avg_rating, total_ratings "
            "FROM driver_profiles WHERE total_ratings >= 3 ORDER BY avg_rating DESC LIMIT 10"
        ).fetchall()
        
        top_customers = database.cur.execute(
            "SELECT user_id, name, avg_rating, total_ratings "
            "FROM customers WHERE total_ratings >= 3 ORDER BY avg_rating DESC LIMIT 10"
        ).fetchall()
        
        msg_parts = ["═" * 40, "⭐ أعلى التقييمات:", "═" * 40]
        
        msg_parts.append("\n🛺 أفضل السواقين:")
        for idx, (did, name, rating, total) in enumerate(top_drivers, 1):
            stars = "⭐" * int(rating)
            msg_parts.append(f"{idx}. {name} - {rating:.1f}/5 {stars}")
            msg_parts.append(f"   ({total} تقييم)")
        
        msg_parts.append("\n👤 أفضل الركاب:")
        for idx, (cid, name, rating, total) in enumerate(top_customers, 1):
            stars = "⭐" * int(rating)
            msg_parts.append(f"{idx}. {name or cid} - {rating:.1f}/5 {stars}")
            msg_parts.append(f"   ({total} تقييم)")
        
        msg_parts.append(f"\n{get_random_ending()}")
        
        await safe_edit(q, text="\n".join(msg_parts), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")]
        ]))
    
    elif data == "admin_back":
        # العودة للوحة الأدمن
        await safe_edit(q, text="👑 لوحة تحكم الأدمن", reply_markup=admin_kb())
    
    # ═══════════════════════════════════════════════════════════════════════
    # 1️⃣1️⃣ طوارئ وأخرى
    # ═══════════════════════════════════════════════════════════════════════
    
    elif data == "c_emergency":
        # نفس وظيفة /emergency
        await emergency_cmd(update, context)

# ═══════════════════════════════════════════════════════════════════════════
# 📍 LOCATION HANDLER (محفوظ 100% من V14 + حساب السعر)
# ═══════════════════════════════════════════════════════════════════════════

async def loc_handler(update, context):
    """معالج الموقع GPS"""
    uid = update.effective_user.id
    user_data = context.user_data
    loc = update.message.location
    lat, lon = loc.latitude, loc.longitude
    
    # ─────────────────────────────────────────────────────────────────────
    # السواق: تحديث الموقع
    # ─────────────────────────────────────────────────────────────────────
    if user_data.get("awaiting_driver_location"):
        database.cur.execute(
            "UPDATE drivers SET last_lat=?, last_lon=? WHERE user_id=?",
            (lat, lon, uid)
        )
        database.con.commit()
        user_data.pop("awaiting_driver_location", None)
        availability = database.cur.execute(
            "SELECT available FROM drivers WHERE user_id=?", (uid,)
        ).fetchone()
        
        await update.message.reply_text(
            f"✅ تم تحديث موقعك\n"
            f"📍 {lat:.6f}, {lon:.6f}\n\n"
            f"{get_random_ending()}",
            reply_markup=driver_kb(availability[0] if availability else 0)
        )
        return
    
    # ─────────────────────────────────────────────────────────────────────
    # الراكب: موقع الانطلاق
    # ─────────────────────────────────────────────────────────────────────
    if user_data.get("awaiting_gps_from"):
        user_data["from_lat"] = lat
        user_data["from_lon"] = lon
        user_data["from_loc_text"] = f"GPS: {lat:.6f}, {lon:.6f}"
        user_data["awaiting_gps_from"] = False
        
        await update.message.reply_text(
            f"✅ تم حفظ موقع الانطلاق\n\n"
            f"اختر طريقة تحديد موقع الوصول:",
            reply_markup=location_method_kb("to")
        )
    
    # ─────────────────────────────────────────────────────────────────────
    # الراكب: موقع الوصول
    # ─────────────────────────────────────────────────────────────────────
    elif user_data.get("awaiting_gps_to"):
        user_data["to_lat"] = lat
        user_data["to_lon"] = lon
        user_data["to_loc_text"] = f"GPS: {lat:.6f}, {lon:.6f}"
        user_data["awaiting_gps_to"] = False
        
        # 🆕 حساب المسافة والسعر المقترح
        from_lat = user_data.get("from_lat")
        from_lon = user_data.get("from_lon")
        
        if from_lat and from_lon:
            distance = haversine(from_lat, from_lon, lat, lon)
            suggested_price = calculate_price(distance, user_data.get("ride_type", "now"))
            
            await update.message.reply_text(
                f"✅ تم حفظ موقع الوصول\n\n"
                f"📏 المسافة: {distance:.2f} كم\n"
                f"💰 السعر المقترح: {suggested_price:.0f} جنيه\n\n"
                f"اختر نوع الرحلة:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚕 حالاً", callback_data="finalize_now")],
                    [InlineKeyboardButton("📅 بموعد", callback_data="finalize_sched")],
                    [InlineKeyboardButton("🎒 مدارس", callback_data="finalize_school")],
                ])
            )
        else:
            await update.message.reply_text(
                "✅ تم حفظ موقع الوصول\n\n"
                "اختر نوع الرحلة:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚕 حالاً", callback_data="finalize_now")],
                    [InlineKeyboardButton("📅 بموعد", callback_data="finalize_sched")],
                    [InlineKeyboardButton("🎒 مدارس", callback_data="finalize_school")],
                ])
            )

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 MAIN FUNCTION - تشغيل البوت
# ═══════════════════════════════════════════════════════════════════════════

async def error_handler(update, context):
    """منع انهيار البوت عند إدخال قديم أو callback غير صالح."""
    logging.exception("Unhandled Telegram update error", exc_info=context.error)
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ حصل خطأ مؤقت. جرّب الزر مرة أخرى أو اكتب /start."
            )
        except Exception:
            pass

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    TOKEN = getattr(config, "TOKEN", "").strip()
    if not TOKEN:
        print("❌ ERROR: ضع BOT_TOKEN في Environment Variables قبل التشغيل.")
        return
    if not ADMIN_IDS:
        print("⚠️ تحذير: ADMIN_IDS فارغة؛ لوحة الإدارة لن تكون متاحة.")
    
    print("""
═══════════════════════════════════════════════════════════════════════════
🕌 بسم الله الرحمن الرحيم
═══════════════════════════════════════════════════════════════════════════

🚕 وصلني - سيدي سالم V15 ULTIMATE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ كل ميزات V14 (802 سطر) + التحديثات الجديدة:
  ✅ 13 بند سواق + 9 بنود راكب
  ✅ 3 طرق تحديد موقع (يدوي + GPS + أماكن)
  ✅ 60+ مكان في سيدي سالم
  ✅ بحث ذكي تدريجي (500م→5كم)
  ✅ 3 أنواع رحلات + كود أمان + طوارئ
  ✅ نظام عروض ومزايدة كامل

🆕 الجديد في V15:
  ⭐ نظام تقييم 5 نجوم
  📢 نظام شكاوى منظم
  💰 حساب سعر تلقائي شفاف
  📜 تاريخ رحلات كامل
  🛡️ حماية من السبام
  📊 إحصائيات مفصلة
  🕌 أسلوب إسلامي مضحك
  👆 أزرار كبيرة وواضحة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤲 توكلنا على الله - منصة آمنة ومضمونة
═══════════════════════════════════════════════════════════════════════════
""")
    
    app = ApplicationBuilder() \
        .token(TOKEN) \
        .request(req) \
        .build()
    
    # تسجيل المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CommandHandler("emergency", emergency_cmd))
    
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.LOCATION, loc_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    app.add_handler(CallbackQueryHandler(cb))
    app.add_error_handler(error_handler)
    
    print("✅ Bot handlers registered successfully!")
    print("🤖 Bot token loaded from environment.")
    print("🔄 Starting polling...")
    print(f"👑 Admin IDs: {ADMIN_IDS}")
    print("═" * 79)
    print("🟢 Bot is LIVE! Press Ctrl+C to stop.")
    print("═" * 79)
    
    # بدء Polling
    app.run_polling(allowed_updates=["message", "callback_query", "inline_query"])

if __name__ == "__main__":
    import asyncio
    main()
