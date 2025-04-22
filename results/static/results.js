//THIS SECTION MIGHT CHANGE AFTER THE BACKEND IMPLEMENTATION
document.addEventListener('DOMContentLoaded', function() {
    //initialize all dropdowns
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    //add event listeners to all dropdown toggles
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();

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

    //checkboxes to update dropdown button text
    document.querySelectorAll('.dropdown-menu input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateDropdownText(this);
        });
    });

    function updateDropdownText(checkbox) {
        const dropdownMenu = checkbox.closest('.dropdown-menu');
        const dropdownToggle = dropdownMenu.previousElementSibling;
        const originalText = dropdownToggle.getAttribute('data-original-text') || dropdownToggle.textContent.trim().split('\n')[0].trim();
        
        // Store original text if not already stored
        if (!dropdownToggle.getAttribute('data-original-text')) {
            dropdownToggle.setAttribute('data-original-text', originalText);
        }

        const checkedItems = dropdownMenu.querySelectorAll('input[type="checkbox"]:checked');
        
        if (checkedItems.length === 0) {
            // Reset to original text if no items are selected
            dropdownToggle.innerHTML = originalText + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        } else if (checkedItems.length === 1) {
            // Show the single selected item
            const selectedLabel = checkedItems[0].parentElement.textContent.trim();
            dropdownToggle.innerHTML = selectedLabel + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        } else {
            // Show count for multiple selections
            dropdownToggle.innerHTML = checkedItems.length + ' selected <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
        }
    }


    //prevent dropdown meny clicks from closing the dropdown
    document.querySelectorAll.apply('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });

    //search button click
    const searchBtn = document.querySelector('.search-btn');
    if(searchBtn) {
        searchBtn.addEventListener('click', function() {
            
            const selectedFilters = {};

            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                const dropdownId = toggle.id;
                const checkedItems = [];

                toggle.nextElementSibling.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
                    checkedItems.push(checkbox.value);
                });

                selectedFilters[dropdownId] = checkedItems;
            });

            //CHECK IF ANY FILTERS ARE SELECTED AND ERROR MESSAGE 
            //i will look into it later when I apply the errors of the page
        });
    }

    //clear button click
    const clearBtn = document.querySelector('.clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            document.querySelectorAll('.dropdown-menu input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });

            // Reset all dropdown button text to original
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                const originalText = toggle.getAttribute('data-original-text') || toggle.textContent.trim().split('\n')[0].trim();
                if (!toggle.getAttribute('data-original-text')) {
                    toggle.setAttribute('data-original-text', originalText);
                }
                toggle.innerHTML = originalText + ' <span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
            });

            document.getElementById('searchResults').style.display = 'none';
            document.querySelector('.results-message').style.display = 'block';
        });
    }

    // Store original dropdown texts on page load
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        const originalText = toggle.textContent.trim().split('\n')[0].trim();
        toggle.setAttribute('data-original-text', originalText);
    });

});