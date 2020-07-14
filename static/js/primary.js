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

function updateField(isDoctor) {
    console.log(isDoctor);
    
    var exposureField = document.getElementById("exposureField");
    var conditionsField = document.getElementById("conditionsField");
    var tripsField = document.getElementById("tripsField");

    var exposureStr = '';
    for(var i = 0; i < exposureField.value.length; i++) {
        var char = exposureField.value.charAt(i);

        if(char != "[" && char != "]" && char != '\'') {
            exposureStr += char;
        }
    }
    exposureField.value = exposureStr;

    var conditionsStr = '';
    for(var i = 0; i < conditionsField.value.length; i++) {
        var char = conditionsField.value.charAt(i);
        
        if(char != "[" && char != "]" && char != '\'') {
            conditionsStr += char;
        }
    }
    conditionsField.value = conditionsStr;

    var tripsStr = '';
    for(var i = 0; i < tripsField.value.length; i++) {
        var char = tripsField.value.charAt(i);

        if(char != "[" && char != "]" && char != '\'') {
            tripsStr += char;
        }
    }
    tripsField.value = tripsStr;
    
    if(isDoctor) {
        var vaccinationsField = document.getElementById("vaccinationsField");
        var vaccinationsStr = '';
        for(var i = 0; i < vaccinationsField.value.length; i++) {
            var char = vaccinationsField.value.charAt(i);

            if(char != "[" && char != "]" && char != '\'') {
                vaccinationsStr += char;
            }
        }
        vaccinationsField.value = vaccinationsStr;
    }
}

function inviteMember() {
    var inviteField = document.getElementById("inviteField");
    console.log('/invite:' + inviteField.value);
    
    window.open('/invite:' + inviteField.value, '_blank')

    window.open('/invite:' + document.getElementById("inviteField").value, '_self')
}