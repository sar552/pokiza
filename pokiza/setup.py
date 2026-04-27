from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


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
