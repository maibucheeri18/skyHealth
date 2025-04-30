// Make these functions globally accessible
function toggleTeamDropdown() {
    document.getElementById("teamDropdown").classList.toggle("show");
    const selectedOption = document.getElementById('choose-arrow-down');
    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function selectTeam(id, name) {
    document.querySelector(".selected-option").innerHTML = name + '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("team-select").value = id;
    document.getElementById("teamDropdown").classList.remove("show");
}

function toggleSessionDropdown() {
    document.getElementById("sessionDropdown").classList.toggle("show");
    const selectedOption = document.getElementById('choose-arrow-down');
    selectedOption.innerHTML = selectedOption.innerHTML == '<i class="fa-solid fa-angle-down"></i>' ? 
                                                     '<i class="fa-solid fa-angle-up"></i>' :
                                                     '<i class="fa-solid fa-angle-down"></i>';
}

function selectSession(id, name) {
    document.querySelector(".selected-option").innerHTML = name + '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    document.getElementById("session-select").value = id;
    document.getElementById("sessionDropdown").classList.remove("show");
}

// Run this when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle dropdown arrow animation for session select
    const sessionSelect = document.getElementById('session-select');
    if (sessionSelect) {
        const sessionArrow = sessionSelect.parentElement.querySelector('.choose-arrow-down');
        
        sessionSelect.addEventListener('focus', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<i class="fa-solid fa-angle-up"></i>';
                this.classList.add('active');
            }
        });
        
        sessionSelect.addEventListener('blur', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
                this.classList.remove('active');
            }
        });
        
        sessionSelect.addEventListener('change', function() {
            if (sessionArrow) {
                sessionArrow.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
                this.blur();
            }
        });
    }
    
    // Handle dropdown arrow animation for team select
    const teamSelect = document.getElementById('team-select');
    if (teamSelect) {
        const teamArrow = teamSelect.parentElement.querySelector('.choose-arrow-down');
        
        teamSelect.addEventListener('click', function() {
            console.log('a')
            if (teamArrow) {
                teamArrow.innerHTML = teamArrow
                this.classList.add('active');
            }
        })

        teamSelect.addEventListener('focus', function() {
            if (teamArrow) {
                teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-up"></i></span>';
                this.classList.add('active');
            }
        });
        
        teamSelect.addEventListener('blur', function() {
            console.log('fos');
            if (teamArrow) {
                teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
                this.classList.remove('active');
            }
        });
        
        teamSelect.addEventListener('change', function() {
            if (teamArrow) {
                teamArrow.innerHTML = '<span class="choose-arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
                this.blur();
            }
        });
    }

    // Global click listener to close dropdown when clicking outside
    document.addEventListener("click", function(event) {
        const dropdown = document.getElementById("teamDropdown");
        const trigger = document.querySelector(".selected-option");
        if (dropdown && trigger && !dropdown.contains(event.target) && !trigger.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });
});