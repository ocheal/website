function class_toggle(element, klass, is_active=false, from_id=true) {
    /**
    * Toggle the addition/removal of a class from an element
    *
    * @param {string/element} element - The element on which to add/remove the class.
    * @param {string} klass - The class to be added/removed.
    * @param {bool} is_active - Wether the class is already active. If true, the class will be first removed.
    * @param {bool} from_id - Wether the element is given as string id or not
    */
    if (from_id) element = document.getElementById(element);
    return () => {
        if (is_active) {
            element.classList.remove(klass)
        }
        else {
            element.classList.add(klass)
        }
        is_active = !is_active;
    }
}