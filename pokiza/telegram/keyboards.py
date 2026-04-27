def main_menu_keyboard() -> dict:
    return {
        "keyboard": [[{"text": "📊 Akt Sverka"}]],
        "resize_keyboard": True,
        "is_persistent": True,
    }


def akt_sverka_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "📅 2 hafta", "callback_data": "aks:2w"},
                {"text": "📅 1 oy",    "callback_data": "aks:1m"},
            ],
            [
                {"text": "📅 3 oy",    "callback_data": "aks:3m"},
                {"text": "📅 Hammasi", "callback_data": "aks:all"},
            ],
        ]
    }


def admin_menu_keyboard() -> dict:
    return {
        "keyboard": [
            [{"text": "👥 Telegram'siz kontragentlar"}],
            [{"text": "ℹ️ Bot holati"}],
        ],
        "resize_keyboard": True,
        "is_persistent": True,
    }
