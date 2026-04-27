import os

import frappe
from frappe.utils import add_days, add_months, flt, getdate, today

from pokiza.telegram.messages import AKT_SVERKA_EMPTY, AKT_SVERKA_ERROR, AKT_SVERKA_GENERATING, PERIOD_LABELS
from pokiza.telegram.sender import answer_callback_query, send_document, send_message


def _date_range(period_code: str) -> tuple[str, str]:
    t = getdate(today())
    if period_code == "2w":
        return str(add_days(t, -14)), str(t)
    elif period_code == "1m":
        return str(add_months(t, -1)), str(t)
    elif period_code == "3m":
        return str(add_months(t, -3)), str(t)
    else:
        return "2000-01-01", str(t)


def generate_akt_sverka_pdf(
    party_type: str,
    party_name: str,
    from_date: str,
    to_date: str,
) -> bytes | None:
    """Akt Sverka PDF bytes qaytaradi. Ma'lumot bo'lmasa None."""
    from weasyprint import HTML as WeasyHTML
    from pokiza.pokiza_for_business.report.akt_sverka.akt_sverka import execute

    filters = {
        "party_type": party_type,
        "party": party_name,
        "from_date": from_date,
        "to_date": to_date,
    }

    result = execute(filters)
    data = result[1] if len(result) > 1 else []

    if not data:
        return None

    # Faqat sarlavha va jami qatorlarini chiqarib, asl ma'lumotlarni olib qolish
    data_rows = [r for r in data if not r.get("is_total")]
    if not data_rows:
        return None

    opening_row = next((r for r in data if r.get("voucher_type") == "Opening"), None)
    total_row = next((r for r in data if r.get("is_total")), None)

    opening_balance = flt(opening_row.get("balance", 0)) if opening_row else 0
    closing_balance = flt(total_row.get("balance", 0)) if total_row else flt(data[-1].get("balance", 0))

    company = (
        frappe.defaults.get_user_default("company")
        or frappe.db.get_single_value("Global Defaults", "default_company")
        or ""
    )

    context = {
        "data": data,
        "party": party_name,
        "party_type": party_type,
        "from_date": from_date,
        "to_date": to_date,
        "company": company,
        "opening_credit": opening_balance if opening_balance > 0 else 0,
        "opening_debit": abs(opening_balance) if opening_balance < 0 else 0,
        "goods_credit":    sum(flt(r.get("credit", 0)) for r in data if r.get("voucher_type") == "Purchase Invoice"),
        "goods_debit":     sum(flt(r.get("debit",  0)) for r in data if r.get("voucher_type") == "Sales Invoice"),
        "money_credit":    sum(flt(r.get("credit", 0)) for r in data if r.get("voucher_type") == "Payment Entry"),
        "money_debit":     sum(flt(r.get("debit",  0)) for r in data if r.get("voucher_type") == "Payment Entry"),
        "kassa_credit":    sum(flt(r.get("credit", 0)) for r in data if r.get("voucher_type") == "Kassa"),
        "kassa_debit":     sum(flt(r.get("debit",  0)) for r in data if r.get("voucher_type") == "Kassa"),
        "accruals_credit": sum(flt(r.get("credit", 0)) for r in data if r.get("voucher_type") == "Journal Entry"),
        "accruals_debit":  sum(flt(r.get("debit",  0)) for r in data if r.get("voucher_type") == "Journal Entry"),
        "closing_credit":  closing_balance if closing_balance > 0 else 0,
        "closing_debit":   abs(closing_balance) if closing_balance < 0 else 0,
    }

    template_path = os.path.join(
        frappe.get_app_path("pokiza"),
        "pokiza_for_business", "report", "akt_sverka", "akt_sverka_template.html",
    )
    with open(template_path, "r", encoding="utf-8") as f:
        html = frappe.render_template(f.read(), context)

    return WeasyHTML(string=html).write_pdf()


def handle_akt_sverka(
    chat_id: int,
    callback_query_id: str,
    period_code: str,
    party_type: str,
    party_name: str,
    display_name: str,
) -> None:
    """Background task: Akt Sverka PDF generatsiya va Telegram ga yuborish."""
    answer_callback_query(callback_query_id, "Hisobot tayyorlanmoqda...")
    send_message(chat_id, AKT_SVERKA_GENERATING)

    try:
        from_date, to_date = _date_range(period_code)
        pdf_bytes = generate_akt_sverka_pdf(party_type, party_name, from_date, to_date)

        if not pdf_bytes or len(pdf_bytes) < 1000:
            send_message(chat_id, AKT_SVERKA_EMPTY)
            return

        period_label = PERIOD_LABELS.get(period_code, period_code)
        caption = (
            f"📊 <b>Akt Sverka</b>\n"
            f"👤 {display_name}\n"
            f"📅 {from_date} — {to_date}\n"
            f"⏱ Davr: {period_label}"
        )
        filename = f"Akt_Sverka_{party_name}_{from_date}_{to_date}.pdf"
        send_document(chat_id, pdf_bytes, filename, caption)

    except Exception as e:
        frappe.log_error(str(e), "Pokiza Akt Sverka PDF xatosi")
        send_message(chat_id, AKT_SVERKA_ERROR)
