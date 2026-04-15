frappe.ui.form.on("Payment Entry", {
    refresh(frm) {
        renderKassaOrigin(frm);
    },
});

function renderKassaOrigin(frm) {
    const kassaName = getKassaReference(frm);
    const referenceField = frm.fields_dict.reference_no;
    if (!referenceField || !referenceField.$wrapper) return;

    referenceField.$wrapper.find(".kassa-origin-link").remove();
    referenceField.$wrapper.find(".input-with-feedback, input, .control-value").off(".kassa_link");
    referenceField.$wrapper.find(".input-with-feedback, input, .control-value").css({
        cursor: "",
        color: "",
        "text-decoration": "",
    });

    if (!kassaName) return;

    frm.add_custom_button(__("Open Kassa"), () => {
        frappe.set_route("Form", "Kassa", kassaName);
    }, __("Connections"));

    const clickTargets = referenceField.$wrapper.find(".input-with-feedback, input, .control-value");
    clickTargets.css({
        cursor: "pointer",
        color: "var(--primary-color)",
        "text-decoration": "underline",
    });
    clickTargets.on("click.kassa_link", () => {
        frappe.set_route("Form", "Kassa", kassaName);
    });
}

function getKassaReference(frm) {
    const referenceNo = (frm.doc.reference_no || "").trim();
    if (!referenceNo) return "";
    return referenceNo.startsWith("KASSA-") ? referenceNo : "";
}
