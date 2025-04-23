//THIS SECTION MIGHT CHANGE AFTER THE BACKEND IMPLEMENTATION
document.addEventListener('DOMContentLoaded', function() {
    //initialize all dropdowns
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // add event listeners to all dropdown toggles
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleDropdown(this);
        });
    });

    function toggleDropdown(toggle) {
        //close any other open dropdowns
        dropdownToggles.forEach(otherToggle => {
            if(otherToggle !== toggle && otherToggle.getAttribute('aria-expanded') === 'true') {
                otherToggle.setAttribute('aria-expanded', 'false');
                otherToggle.nextElementSibling.classList.remove('show');

                //rest arrow icon for other toggles
                const otherArrow = otherToggle.querySelector('.arrow-down');
                if(otherArrow) {
                    otherArrow.innerHTML = '<i class="fa-solid fa-angle-down></i>';
                }
            }
        });

        //toggle current dropdown
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !isExpanded);
        const dropdownMenu = toggle.nextElementSibling;
        dropdownMenu.classList.toggle('show');

        //toggle arrow direction
        const arrowIcon = toggle.querySelector('.arrow-down');
        if(arrowIcon) {
            arrowIcon.innerHTML = !isExpanded
                ? '<i class="fa-solid fa-angle-up"></i>'
                : '<i class="fa-solid fa-angle-down"></i>';
        }
    }

    //close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if(!e.target.closest('.dropdown-container')) {
            dropdownToggles.forEach(toggle => {
                toggle.setAttribute('aria-expanded', 'false');
                toggle.nextElementSibling.classList.remove('show');

                const arrowIcon = toggle.querySelector('.arrow-down');
                if(arrowIcon) {
                    arrowIcon.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
                }
            });
        }
    });

    //handle checkbox changes
    document.querySelectorAll('.dropdown-menu input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateDropdownText(this);
            handleMutuallyExclusiveCheckboxes(this);
        });
    });

    function updateDropdownText(checkbox) {
        const dropdownMenu = checkbox.closest('.dropdown-menu');
        const dropdownToggle = document.querySelector(`[id="${dropdownMenu.getAttribute('aria-labelledby')}"]`);

        if(!dropdownToggle) return;

        const originalText = dropdownToggle.getAttribute('data-original-text') || dropdownToggle.textContent.trim().split('\n')[0].trim();

        //store original text if not ready stored
        if(!dropdownToggle.getAttribute('data-original-text')) {
            dropdownToggle.setAttribute('data-original-text', originalText);
        }

        const checkedItems = dropdownMenu.querySelectorAll('input[type="checkbox"]:checked');

        if(checkedItems.length === 0) {
            dropdownToggle.innerHTML = originalText + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        } else if(checkedItems.length === 1) {
            const selectedLabel = checkedItems[0].parentElement.textContent.trim();
            dropdownToggle.innerHTML = selectedLabel + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        } else {
            dropdownToggle.innerHTML = checkedItems.length + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        }
    }

    function handleMutuallyExclusiveCheckboxes(checkbox) {
        const dropdownMenu = checkbox.closest('.dropdown-menu');
        const allCheckbox = dropdownMenu.querySelector('input[value="all"]');

        if(!allCheckbox) return;

        const individualCheckboxes = Array.from(
            dropdownMenu.querySelectorAll('input[type ="checkbox"]:not([value="all"])')
        );

        if(checkbox === allCheckbox && checkbox.checked) {
            individualCheckboxes.forEach(cb => {
                cb.checked = false;
            });
        } else if(individualCheckboxes.includes(checkbox) && checkbox.checked) {
            if(allCheckbox) allCheckbox.checked = false;
        }
    }

    //prevent dropdown menu clicks from closing the dropdown
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });

    //search button functionality - IT CAN BE FIXED ONLY WHEN THE BACKEND FUNCTIONALITY IS SET
    const searchBtn = document.querySelector('.search-btn');
    

    //clear button functionality 
    const clearBtn = document.querySelector('.clear-btn');
    if(clearBtn) {
        clearBtn.addEventListener('click', function() {
            document.querySelectorAll('.dropdown-menu input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });

            //reset the dropdowns text to original 
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                const originalText = toggle.getAttribute('data-original-text') || toggle.textContent.trim().split('\n')[0].trim();
                toggle.innerHTML = originalText + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
            });
        });
    }

    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        const originalText = toggle.textContent.trim().split('\n')[0].trim();
        toggle.setAttribute('data-original-text', originalText);
    });

});