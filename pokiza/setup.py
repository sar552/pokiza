from pathlib import Path

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


NAKLADNAYA_PRINT_FORMAT = "Накладная Pokiza"


def get_custom_fields():
    return {
        "Stock Entry": [
            {
                "fieldname": "custom_production_entry",
                "label": "Production Entry",
                "fieldtype": "Link",
                "options": "Production Entry",
                "insert_after": "work_order",
                "read_only": 1,
            }
        ],
        "Customer": [
            {
                "fieldname": "contact_number",
                "label": "Telefon raqam",
                "fieldtype": "Data",
                "options": "Phone",
                "insert_after": "customer_name",
                "in_list_view": 0,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "contact_number",
                "read_only": 1,
                "in_list_view": 0,
            },
        ],
        "Supplier": [
            {
                "fieldname": "contact_number",
                "label": "Telefon raqam",
                "fieldtype": "Data",
                "options": "Phone",
                "insert_after": "supplier_name",
                "in_list_view": 0,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "contact_number",
                "read_only": 1,
                "in_list_view": 0,
            },
        ],
        "Employee": [
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "employee_name",
                "read_only": 1,
                "in_list_view": 0,
            },
        ],
    }


def after_install():
    create_custom_fields(get_custom_fields(), ignore_validate=True, update=True)
    create_nakladnaya_print_format()


def create_nakladnaya_print_format():
    html = Path(__file__).parent.joinpath(
        "print_formats", "sales_invoice_nakladnaya.html"
    ).read_text(encoding="utf-8")

    values = {
        "doc_type": "Sales Invoice",
        "module": "Pokiza for business",
        "custom_format": 1,
        "standard": "No",
        "print_format_for": "DocType",
        "print_format_type": "Jinja",
        "print_format_builder": 0,
        "print_format_builder_beta": 0,
        "raw_printing": 0,
        "disabled": 0,
        "font": "Calibri",
        "font_size": 12,
        "page_number": "Hide",
        "margin_top": 0,
        "margin_bottom": 0,
        "margin_left": 0,
        "margin_right": 0,
        "html": html,
    }

    if frappe.db.exists("Print Format", NAKLADNAYA_PRINT_FORMAT):
        print_format = frappe.get_doc("Print Format", NAKLADNAYA_PRINT_FORMAT)
        print_format.update(values)
        print_format.save(ignore_permissions=True)
    else:
        print_format = frappe.get_doc(
            {
                "doctype": "Print Format",
                "name": NAKLADNAYA_PRINT_FORMAT,
                **values,
            }
        )
        print_format.insert(ignore_permissions=True)

    property_setter = frappe.db.exists(
        "Property Setter",
        {
            "doctype_or_field": "DocType",
            "doc_type": "Sales Invoice",
            "property": "default_print_format",
        },
    )
    if property_setter:
        frappe.db.set_value(
            "Property Setter", property_setter, "value", NAKLADNAYA_PRINT_FORMAT
        )
    else:
        frappe.make_property_setter(
            {
                "doctype_or_field": "DocType",
                "doctype": "Sales Invoice",
                "property": "default_print_format",
                "property_type": "Data",
                "value": NAKLADNAYA_PRINT_FORMAT,
            }
        )

    frappe.clear_cache(doctype="Sales Invoice")
