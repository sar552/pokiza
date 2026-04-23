frappe.ui.form.on("Sales Invoice", {
    setup(frm) {
        setSalesItemQuery(frm);
    },

    refresh(frm) {
        setSalesItemQuery(frm);
    },
});

function setSalesItemQuery(frm) {
    frm.set_query("item_code", "items", () => {
        return {
            filters: {
                disabled: 0,
                is_sales_item: 1,
                item_group: "Сотув махсулотлари",
            },
        };
    });
}
