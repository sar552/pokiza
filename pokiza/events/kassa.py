"""Kassa doc_events: submit bo'lganda party'ga Telegram xabar yuborish."""

import frappe
from frappe.utils import flt

from pokiza.telegram.messages import DIVIDER
from pokiza.telegram.sender import send_message


# Bildirishnoma faqat shu party_type lar uchun ishlaydi
_NOTIFIABLE_PARTY_TYPES = ("Customer", "Supplier", "Employee")


def _get_chat_id(party_type: str, party: str) -> int | None:
    if party_type not in _NOTIFIABLE_PARTY_TYPES:
        return None
    raw = frappe.db.get_value(party_type, party, "telegram_chat_id")
    if not raw:
        return None
    try:
        return int(raw)
    except (ValueError, TypeError):
        return None


def _get_party_balance(party_type: str, party: str, company: str) -> dict:
    """Party ning GL balansini valyuta bo'yicha hisoblash."""
    try:
        rows = frappe.db.sql("""
            SELECT
                account_currency AS currency,
                SUM(debit_in_account_currency) - SUM(credit_in_account_currency) AS balance
            FROM `tabGL Entry`
            WHERE party_type = %s
              AND party = %s
              AND company = %s
              AND is_cancelled = 0
            GROUP BY account_currency
        """, (party_type, party, company), as_dict=True)

        result = {}
        for row in rows:
            if row.balance is None:
                continue
            b = flt(row.balance)
            # Customer uchun: musbat = mijoz bizga qarzdor
            result[row.currency] = -b if party_type == "Customer" else b
        return result
    except Exception as e:
        frappe.log_error(str(e), "Pokiza GL balans xatosi")
        return {}


def _format_amount(amount: float, currency: str) -> str:
    amt = abs(flt(amount))
    if currency == "USD":
        return f"{amt:,.2f} $"
    elif currency == "UZS":
        return f"{amt:,.0f} so'm"
    return f"{amt:,.2f} {currency}"


def _format_balance(balances: dict, party_type: str) -> str:
    if not balances or all(flt(v) == 0 for v in balances.values()):
        return "✅ Hisob-kitob yo'q"
    lines = []
    for currency, balance in balances.items():
        b = flt(balance)
        if b == 0:
            continue
        amt = _format_amount(b, currency)
        if b > 0:
            label = "Sizning qarzingiz" if party_type == "Customer" else "Bizning qarzimiz"
        else:
            label = "Bizning qarzimiz" if party_type == "Customer" else "Sizning qarzingiz"
        lines.append(f"📌 {label}: <b>{amt}</b>")
    return "\n".join(lines) if lines else "✅ Hisob-kitob yo'q"


def on_submit(doc, method=None) -> None:
    """Kassa submit bo'lganda party'ga xabar yuborish."""
    # Faqat Приход va Расход uchun bildirishnoma
    if doc.transaction_type not in ("Приход", "Расход"):
        return

    if not doc.party_type or not doc.party:
        return

    chat_id = _get_chat_id(doc.party_type, doc.party)
    if not chat_id:
        return

    # Miqdor va valyuta
    amount = flt(doc.amount)
    currency = doc.cash_account_currency or "UZS"
    amount_text = _format_amount(amount, currency)

    # To'lov usuli
    mode = doc.mode_of_payment or "—"

    # Tranzaksiya turi bo'yicha xabar matni
    if doc.transaction_type == "Приход":
        if doc.party_type == "Customer":
            emoji, action = "💰", "Sizdan to'lov qabul qilindi"
        elif doc.party_type == "Supplier":
            emoji, action = "💸", "Sizga to'lov qaytarildi"
        else:
            emoji, action = "💵", "Sizga to'lov amalga oshirildi"
    else:  # Расход
        if doc.party_type == "Customer":
            emoji, action = "💸", "Sizga pul qaytarildi"
        elif doc.party_type == "Supplier":
            emoji, action = "💸", "Sizga to'lov amalga oshirildi"
        else:
            emoji, action = "💵", "Sizga to'lov amalga oshirildi"

    balance = _get_party_balance(doc.party_type, doc.party, doc.company)
    balance_text = _format_balance(balance, doc.party_type)

    message = (
        f"{emoji} <b>{action}</b>\n"
        f"{DIVIDER}\n"
        f"🏢 {doc.company}\n"
        f"📄 {doc.name}\n"
        f"📅 {doc.date}\n"
        f"💳 To'lov usuli: {mode}\n"
        f"{DIVIDER}\n"
        f"💵 Miqdor: <b>{amount_text}</b>\n"
        f"{DIVIDER}\n"
        f"{balance_text}"
    )

    frappe.enqueue(
        "pokiza.telegram.sender.send_message",
        chat_id=chat_id,
        text=message,
        queue="short",
        is_async=True,
    )
