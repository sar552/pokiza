const BOM_FINISHED_GOODS_ITEM_GROUP = "Готовый продукт";

frappe.ui.form.on("BOM", {
    setup(frm) {
        setBomItemQuery(frm);
    },

    refresh(frm) {
        setBomItemQuery(frm);
    },
});

function setBomItemQuery(frm) {
    frm.set_query("item", () => {
        return {
            filters: {
                disabled: 0,
                item_group: BOM_FINISHED_GOODS_ITEM_GROUP,
            },
        };
    });
}
