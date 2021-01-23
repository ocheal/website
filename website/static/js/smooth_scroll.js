function getTopScroll(e) {
    /* Return the top scroll of element `e` */
    if (e.scrollTop !== undefined) return e.scrollTop;
    return e.scrollY;
}

function getScrollParent(element, includeHidden=false, fallback=window) {
    /* pretty much JQuery getScrollParent */
    var style = getComputedStyle(element);
    var excludeStaticParent = style.position === "absolute";
    var overflowRegex = includeHidden ? /(auto|scroll|hidden)/ : /(auto|scroll)/;

    if (style.position === "fixed") return fallback;
    for (var parent = element; (parent = parent.parentElement);) {
        style = getComputedStyle(parent);
        if (excludeStaticParent && style.position === "static") {
            continue;
        }
        if (overflowRegex.test(style.overflow + style.overflowY + style.overflowX)) return parent;
    }
    return fallback;
}


function scrollSmoothly(amount, element, time=500) {
    /* Scroll the element (default window) by a specified amount.
    the element to be scrolled can be specified by element. */
    element = element || window;
    amount = Math.ceil(amount);
    var scroll_init = getTopScroll(element);
    var time_start = null;
    window.requestAnimationFrame(function step(time_now){
        time_start = !time_start ? time_now : time_start;
        
        var scrolled = (getTopScroll(element) - scroll_init);
        var progress = (time_now - time_start)/time;
        var target_scroll = (progress < 1) ? progress*amount : amount;

        var d_scroll = Math.round(target_scroll - scrolled);
        element.scrollBy(0, d_scroll);

        if (progress < 1) window.requestAnimationFrame(step)
    });
}

(function smoothScrollAll(tag="a") {
    /* Adds smooth scrolling for all document elements
        with with the requested tag (default "a"). */
    var links = document.getElementsByTagName(tag);
    for (let link of links) {
        if (link.hash == "") return;

        let target = document.getElementById(link.hash.substring(1));
        link.addEventListener("click", (event) => {
            event.preventDefault();
            let scrollable = getScrollParent(target);
            let amount = target.getBoundingClientRect().top;
            scrollSmoothly(amount, scrollable);
        });
    }
})();