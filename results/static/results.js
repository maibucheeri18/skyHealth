//THIS SECTION MIGHT CHANGE AFTER THE BACKEND IMPLEMENTATION
document.addEventListener('DOMContentLoaded', function() {
    //initialize all dropdowns
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    //add event listeners to all dropdown toggles
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation;

            //close any other open dropdowns
            dropdownToggles.forEach(otherToggle => {
                if (otherToggle !== toggle && otherToggle.classList.contains('active')) {
                    otherToggle.classList.remove('active');
                    otherToggle.nextElementSibling.classList.remove('show');
                }
            });

            //toggle current dropdown
            this.classList.toggle('active');
            const dropdownMenu = this.nextElementSibling;
            dropdownMenu.classList.toggle('show');

            //toggle arrow direction
            const arrowIcon = this.querySelector('.arrow-down');
            if(arrowIcon) {
                if(this.classList.contains('active')) {
                    arrowIcon.innerHTML = '<i class="fa-solid fa-angle-up"></i>';
                } else {
                    arrowIcon.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
                }
            }
        });
    });

    //close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if(!e.target.closest('.dropdown-container')) {
            dropdownToggles.forEach(toggle => {
                toggle.classList.remove('active');
                toggle.nextElementSibling.classList.remove('show');

                const arrowIcon = toggle.querySelector('.arrow-down');
                if(arrowIcon) {
                    arrowIcon.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
                }
            });
        }
    });

    //prevent dropdown meny clicks from closing the dropdown
    document.querySelectorAll.apply('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });

})