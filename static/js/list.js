function setAndSubmit(name, value) {
    let form = jQuery("#data");
    form.find("input[name=" + name + "]").val(value);
    form.get(0).submit();
    return false;
}