function fixedDismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
    objId = html_unescape(objId);
    newRepr = html_unescape(newRepr);
    var id = windowname_to_id(win.name).replace(/^edit_/, '');
    var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
    var selects = grp.jQuery(selectsSelector);
    selects.find('option').each(function() {
        if (this.value === objId) {
            this.innerHTML = newRepr;
            this.value = newId;
        }
    });

    win.close();
}

window.dismissChangeRelatedObjectPopup = fixedDismissChangeRelatedObjectPopup;
