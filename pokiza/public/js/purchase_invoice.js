const PURCHASE_RAW_ITEM_GROUP = "Сырё";

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
                item_group: PURCHASE_RAW_ITEM_GROUP,
            },
        };
    });
}
