# ─── Ro'yxatdan o'tish ───────────────────────────────────────────────────────

WELCOME_CUSTOMER = (
    "👋 Xush kelibsiz, <b>{name}</b>!\n\n"
    "Siz <b>Mijoz</b> sifatida tizimga ulangansiz.\n\n"
    "Quyidagi hodisalar haqida xabar olasiz:\n"
    "• 🛒 Sotilgan mahsulotlar\n"
    "• 💰 Qabul qilingan to'lovlar\n\n"
    "📊 <b>Akt Sverka</b> tugmasini bosing."
)

WELCOME_SUPPLIER = (
    "👋 Xush kelibsiz, <b>{name}</b>!\n\n"
    "Siz <b>Yetkazib beruvchi</b> sifatida tizimga ulangansiz.\n\n"
    "Quyidagi hodisalar haqida xabar olasiz:\n"
    "• 📦 Qabul qilingan mahsulotlar\n"
    "• 💸 Amalga oshirilgan to'lovlar\n\n"
    "📊 <b>Akt Sverka</b> tugmasini bosing."
)

WELCOME_EMPLOYEE = (
    "👋 Xush kelibsiz, <b>{name}</b>!\n\n"
    "Siz <b>Xodim</b> sifatida tizimga ulangansiz.\n\n"
    "Oylik maosh hisoblanganda xabar olasiz.\n\n"
    "📊 <b>Akt Sverka</b> tugmasini bosing."
)

ALREADY_LINKED = (
    "✅ Siz allaqachon tizimga ulangansiз.\n\n"
    "📊 <b>Akt Sverka</b> tugmasini bosing."
)

NOT_LINKED = (
    "🔒 Siz tizimga ulanmağansiz.\n\n"
    "Ro'yxatdan o'tish uchun /start bosing."
)

ASK_PHONE = (
    "📱 Tizimga kirish uchun telefon raqamingizni yuboring:\n\n"
    "Masalan: <code>998901234567</code> yoki <code>901234567</code>"
)

PHONE_INVALID = (
    "❌ Noto'g'ri format.\n\n"
    "Raqamni quyidagi shaklda kiriting: <code>998901234567</code>"
)

PHONE_NOT_FOUND = (
    "❌ Bu telefon raqam tizimda topilmadi.\n\n"
    "Boshqa raqam kiriting yoki admin bilan bog'laning."
)

# ─── Akt Sverka ───────────────────────────────────────────────────────────────

CHOOSE_PERIOD = "📅 <b>Akt Sverka</b> uchun davrni tanlang:"

AKT_SVERKA_GENERATING = "⏳ <b>Akt Sverka tayyorlanmoqda...</b>\n\nBir oz kuting."

AKT_SVERKA_EMPTY = (
    "📭 Tanlangan davrda tranzaksiyalar topilmadi.\n\n"
    "Boshqa davr tanlang."
)

AKT_SVERKA_ERROR = (
    "❌ Hisobot tayyorlashda xatolik.\n\n"
    "Keyinroq urinib ko'ring yoki admin bilan bog'laning."
)

PERIOD_LABELS = {
    "2w":  "2 hafta",
    "1m":  "1 oy",
    "3m":  "3 oy",
    "all": "Barcha vaqt",
}

# ─── Bildirishnomalar ─────────────────────────────────────────────────────────

DIVIDER = "━━━━━━━━━━━━━━━━━━━━"

# ─── Admin ────────────────────────────────────────────────────────────────────

ADMIN_WELCOME = (
    "👨‍💼 <b>Admin paneli</b>\n\n"
    "Quyidagi amallardan birini tanlang."
)

ADMIN_BOT_STATUS = (
    "ℹ️ <b>Bot holati</b>\n\n"
    "🤖 Username: @{username}\n"
    "🆔 Bot ID: <code>{bot_id}</code>\n"
    "👥 Ulangan mijozlar: <b>{customers}</b>\n"
    "🏭 Ulangan yetkazib beruvchilar: <b>{suppliers}</b>"
)

ADMIN_NO_UNLINKED = "✅ Barcha kontragentlar Telegram'ga ulangan!"

ADMIN_UNLINKED_LIST = (
    "📋 <b>Telegram'siz kontragentlar ({count} ta)</b>\n\n"
    "{list}"
)
