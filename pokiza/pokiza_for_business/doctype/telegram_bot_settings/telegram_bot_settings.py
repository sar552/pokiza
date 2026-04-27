import frappe
import requests
from frappe import _
from frappe.model.document import Document
from frappe.utils.password import get_decrypted_password


class TelegramBotSettings(Document):
    pass


@frappe.whitelist()
def set_webhook(webhook_url=None):
    token = _get_token()
    if not webhook_url:
        webhook_url = frappe.db.get_single_value("Telegram Bot Settings", "webhook_url")
    if not webhook_url:
        frappe.throw(_("Webhook URL kiritilmagan"))
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/setWebhook",
            json={"url": webhook_url},
            timeout=10,
        )
        result = r.json()
        if result.get("ok"):
            frappe.msgprint(_("Webhook o'rnatildi: {0}").format(webhook_url))
        else:
            frappe.throw(_("Xato: {0}").format(result.get("description")))
        return result
    except requests.RequestException as e:
        frappe.throw(str(e))


@frappe.whitelist()
def delete_webhook():
    token = _get_token()
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/deleteWebhook",
            timeout=10,
        )
        result = r.json()
        if result.get("ok"):
            frappe.msgprint(_("Webhook o'chirildi"))
        return result
    except requests.RequestException as e:
        frappe.throw(str(e))


def _get_token():
    try:
        return get_decrypted_password("Telegram Bot Settings", "Telegram Bot Settings", "bot_token")
    except Exception:
        return frappe.db.get_single_value("Telegram Bot Settings", "bot_token")
