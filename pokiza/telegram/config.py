import frappe
from frappe.utils.password import get_decrypted_password


def get_bot_token() -> str | None:
    try:
        return get_decrypted_password("Telegram Bot Settings", "Telegram Bot Settings", "bot_token")
    except Exception:
        return frappe.db.get_single_value("Telegram Bot Settings", "bot_token")


def is_bot_active() -> bool:
    return bool(frappe.db.get_single_value("Telegram Bot Settings", "is_active"))


def get_admin_chat_ids() -> list[str]:
    rows = frappe.db.get_all(
        "Telegram Admin",
        filters={"parenttype": "Telegram Bot Settings"},
        fields=["chat_id"],
    )
    return [r.chat_id for r in rows if r.chat_id]


def is_admin(chat_id: int | str) -> bool:
    return str(chat_id) in get_admin_chat_ids()
