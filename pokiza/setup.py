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
        ]
    }


def after_install():
    create_custom_fields(get_custom_fields(), ignore_validate=True, update=True)
