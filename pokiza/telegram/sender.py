import frappe
import requests

from pokiza.telegram.config import get_bot_token

_API = "https://api.telegram.org/bot{token}/{method}"


def _url(method: str) -> str:
    token = get_bot_token()
    if not token:
        frappe.log_error("Telegram bot token kiritilmagan", "Telegram Bot")
        return ""
    return _API.format(token=token, method=method)


def send_message(chat_id: int | str, text: str, reply_markup=None, parse_mode: str = "HTML") -> bool:
    url = _url("sendMessage")
    if not url:
        return False
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        import json
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(url, json=payload, timeout=10)
        if not r.ok:
            frappe.log_error(r.text, f"Telegram sendMessage xatosi (chat_id={chat_id})")
        return r.ok
    except Exception as e:
        frappe.log_error(str(e), "Telegram sendMessage xatosi")
        return False


def send_document(
    chat_id: int | str,
    file_bytes: bytes,
    filename: str,
    caption: str = "",
) -> bool:
    url = _url("sendDocument")
    if not url:
        return False
    try:
        r = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"},
            files={"document": (filename, file_bytes, "application/pdf")},
            timeout=60,
        )
        if not r.ok:
            frappe.log_error(r.text, f"Telegram sendDocument xatosi (chat_id={chat_id})")
        return r.ok
    except Exception as e:
        frappe.log_error(str(e), "Telegram sendDocument xatosi")
        return False


def answer_callback_query(callback_query_id: str, text: str = "") -> None:
    url = _url("answerCallbackQuery")
    if not url:
        return
    try:
        requests.post(
            url,
            json={"callback_query_id": callback_query_id, "text": text},
            timeout=5,
        )
    except Exception:
        pass


def get_me() -> dict:
    url = _url("getMe")
    if not url:
        return {}
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("result", {})
    except Exception:
        return {}


def set_webhook(webhook_url: str) -> dict:
    url = _url("setWebhook")
    if not url:
        return {}
    try:
        r = requests.post(url, json={"url": webhook_url}, timeout=10)
        return r.json()
    except Exception as e:
        frappe.log_error(str(e), "Telegram setWebhook xatosi")
        return {}


def delete_webhook() -> dict:
    url = _url("deleteWebhook")
    if not url:
        return {}
    try:
        r = requests.post(url, timeout=10)
        return r.json()
    except Exception as e:
        frappe.log_error(str(e), "Telegram deleteWebhook xatosi")
        return {}
