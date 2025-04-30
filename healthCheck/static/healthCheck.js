// Make these functions globally accessible
function toggleTeamDropdown() {
    document.getElementById("teamDropdown").classList.toggle("show");
    const selectedOption = document.getElementById('choose-arrow-down');

    const sessionBox = document.getElementById('team');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function toggleSessionDropdown() {
    document.getElementById("sessionDropdown").classList.toggle("show");

    const sessionBox = document.getElementById('session');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    console.log(sessionBox.style.border);

    const selectedOption = document.getElementById('choose-arrow-down');
    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function toggleVoteColorDropdown() {

    const sessionBox = document.getElementById('voteColorSelected');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.getElementById("voteColorDropdown").classList.toggle("show");
    const selectedOption = document.getElementById('vote-color-arrow');
    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function toggleProgressIndicatorDropdown() {

    const sessionBox = document.getElementById('progressIndicatorSelected');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.getElementById("progressIndicatorDropdown").classList.toggle("show");
    const selectedOption = document.getElementById('progress-indicator-arrow');
    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function selectTeam(id, name) {

    const sessionBox = document.getElementById('team');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.querySelector(".selected-option").innerHTML = name + '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("team-select").value = id;
    document.getElementById("teamDropdown").classList.remove("show");
}

function selectSession(id, date) {

    const sessionBox = document.getElementById('session');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.getElementById("session").innerHTML = date + '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("session-select").value = id;
    document.getElementById("sessionDropdown").classList.remove("show");
}

function selectVoteColor(value, text) {

    const sessionBox = document.getElementById('voteColorSelected');

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.getElementById("voteColorSelected").innerHTML = text + '<span id="vote-color-arrow" class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("id_voteColour").value = value;
    document.getElementById("voteColorDropdown").classList.remove("show");
}

function selectProgressIndicator(value, text) {

    const sessionBox = document.getElementById('progressIndicatorSelected');

    console.log(sessionBox);

    sessionBox.style.border = sessionBox.style.border == "2px solid var(--sky-primary-blue)" ? 
                                            "1px solid var(--container-outline)":  "2px solid var(--sky-primary-blue)";

    document.getElementById("progressIndicatorSelected").innerHTML = text + '<span id="progress-indicator-arrow" class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("id_progressIndicator").value = value;
    document.getElementById("progressIndicatorDropdown").classList.remove("show");
}

// Run this when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle dropdown arrow animation for session select
    const sessionSelect = document.getElementById('session-select');
    if (sessionSelect) {
        const sessionArrow = sessionSelect.parentElement.querySelector('.choose-arrow-down');
        
        sessionSelect.addEventListener('focus', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-up"></i></span>';
                this.classList.add('active');
            }
        });
        
        sessionSelect.addEventListener('blur', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
                this.classList.remove('active');
            }
        });
        
        sessionSelect.addEventListener('change', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
                this.blur();
            }
        });
    }
    
    // Handle dropdown arrow animation for team select
    const teamSelect = document.getElementById('team-select');
    if (teamSelect) {
        const teamArrow = teamSelect.parentElement.querySelector('.choose-arrow-down');
        

        // teamSelect.addEventListener('focus', function() {
        //     if (teamArrow) {
        //         teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-up"></i></span>';
        //         this.classList.add('active');
        //     }
        // });
        
    //     teamSelect.addEventListener('blur', function() {
    //         console.log('fos');
    //         if (teamArrow) {
    //             teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    //             this.classList.remove('active');
    //         }
    //     });
        
    //     teamSelect.addEventListener('change', function() {
    //         if (teamArrow) {
    //             teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    //             this.blur();
    //         }
    //     });
    }

    document.addEventListener("click", function(event) {
        // For vote color dropdown
        const voteColorDropdown = document.getElementById("voteColorDropdown");
        const voteColorTrigger = document.getElementById("voteColorSelected");
        
        if (voteColorDropdown && voteColorTrigger && 
            !voteColorDropdown.contains(event.target) && 
            !voteColorTrigger.contains(event.target)) {
            voteColorDropdown.classList.remove("show");
        }
        
        // For progress indicator dropdown
        const progressDropdown = document.getElementById("progressIndicatorDropdown");
        const progressTrigger = document.getElementById("progressIndicatorSelected");
        
        if (progressDropdown && progressTrigger && 
            !progressDropdown.contains(event.target) && 
            !progressTrigger.contains(event.target)) {
            progressDropdown.classList.remove("show");
        }
    });

    // Global click listener to close dropdown when clicking outside
    document.addEventListener("click", function(event) {
        const dropdown = document.getElementById("teamDropdown");
        const trigger = document.querySelector(".selected-option");
        if (dropdown && trigger && !dropdown.contains(event.target) && !trigger.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });

    document.addEventListener("click", function(event) {
        const dropdown = document.getElementById("sessionDropdown");
        const trigger = document.querySelector(".selected-option");
        if (dropdown && trigger && !dropdown.contains(event.target) && !trigger.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });

    document.addEventListener("click", function(event) {
        const dropdown = document.getElementById("voteColorSelected");
        const trigger = document.querySelector(".selected-option");
        if (dropdown && trigger && !dropdown.contains(event.target) && !trigger.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });

    document.addEventListener("click", function(event) {
        const dropdown = document.getElementById("progressIndicatorSelected");
        const trigger = document.querySelector(".selected-option");
        if (dropdown && trigger && !dropdown.contains(event.target) && !trigger.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });

});