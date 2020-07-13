function getPixelValue(property) {
    return parseInt(property.substring(0, property.indexOf("px")));
}

function dropdownHover(src, cond) {
    var dropdown = document.getElementsByClassName('dropdown-menu')[0];
    var profile = document.getElementsByClassName('profile')[0];

    if(src === dropdown) {
        hoverOnDropdown = cond;
    } else {
        hoverOnProfile = cond;
    }

    if(dropdown.style.visibility == 'visible' && !hoverOnDropdown && !hoverOnProfile) {
        dropdown.style.visibility = 'hidden';
        profile.style.filter = "brightness(100%)"

    } else if(hoverOnDropdown || hoverOnProfile) {
        dropdown.style.visibility = 'visible';
        profile.style.filter = "brightness(92.5%)"
    }
}