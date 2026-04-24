const PURCHASE_ITEM_GROUPS = ["Сырё", "Упаковка"];

frappe.ui.form.on("Purchase Invoice", {
    setup(frm) {
        setPurchaseItemQuery(frm);
    },

    refresh(frm) {
        setPurchaseItemQuery(frm);
    },
});

function setPurchaseItemQuery(frm) {
    frm.set_query("item_code", "items", () => {
        return {
            filters: {
                disabled: 0,
                is_purchase_item: 1,
                item_group: ["in", PURCHASE_ITEM_GROUPS],
            },
        };
    });
}
