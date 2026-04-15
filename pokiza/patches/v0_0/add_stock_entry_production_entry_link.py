from pokiza.setup import get_custom_fields


def execute():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    create_custom_fields(get_custom_fields(), ignore_validate=True, update=True)
