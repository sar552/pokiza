def execute():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    custom_fields = {
        "Customer": [
            {
                "fieldname": "contact_number",
                "label": "Telefon raqam",
                "fieldtype": "Data",
                "options": "Phone",
                "insert_after": "customer_name",
                "in_standard_filter": 1,
            },
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "contact_number",
                "read_only": 1,
            },
        ],
        "Supplier": [
            {
                "fieldname": "contact_number",
                "label": "Telefon raqam",
                "fieldtype": "Data",
                "options": "Phone",
                "insert_after": "supplier_name",
                "in_standard_filter": 1,
            },
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "contact_number",
                "read_only": 1,
            },
        ],
        "Employee": [
            {
                "fieldname": "telegram_chat_id",
                "label": "Telegram Chat ID",
                "fieldtype": "Data",
                "insert_after": "employee_name",
                "read_only": 1,
            },
        ],
    }

    create_custom_fields(custom_fields, ignore_validate=True, update=True)
