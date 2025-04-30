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
                    otherArrow.innerHTML = '<i class="fa-solid fa-angle-down"></i>';
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

        console.log(dropdownToggle);

        const checkedItems = dropdownMenu.querySelectorAll('input[type="checkbox"]:checked');

        const dropdownText = dropdownToggle.querySelector("span.dropdown-text");
        console.log(dropdownToggle.childNodes);

        if(checkedItems.length === 0) {
            dropdownText.innerHTML = originalText;
        } else if (checkedItems[0].value == "all"){
            const selectedLabel = checkedItems[0].parentElement.textContent.trim();
            dropdownText.innerHTML = selectedLabel;
        } else if(checkedItems.length === 1) {
            var selectedLabel = checkedItems[0].parentElement.textContent.trim();
            dropdownText.innerHTML = selectedLabel;
        } else {
            dropdownText.innerHTML = checkedItems.length + " selected";
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
        } 
        else if(individualCheckboxes.includes(checkbox) && checkbox.checked) {
            if(allCheckbox) allCheckbox.checked = false;
        }

    }

    //prevent dropdown menu clicks from closing the dropdown
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log("click");
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //search button functionality
    const searchBtn = document.querySelector('.search-btn');
    
    searchBtn.addEventListener('click', function() {
        //find all visible filter containers
        const visibleFilters = document.querySelector('.user-filters:not([style*="display: none"])');
        
        if (!visibleFilters) {
            console.error('No visible filters found');
            return;
        }
                
        //find all checked checkboxes in visible filters
        const checkedBoxes = visibleFilters.querySelectorAll('input[type="checkbox"]:checked');
        
        if (checkedBoxes.length <= 1) {
            const resultError = document.getElementById('resultsError');
            const normalMessage = document.getElementById('resultsMessage');

            resultError.style = "display: block;";
            normalMessage.style = "display: none;";
            return;
        }

        //initialize an object to store selected values
        const selectedFilters = {
            type: [],
            department: [],
            team: [],
            healthCheckCard: [],
            progressOverTime: []
        };

        checkedBoxes.forEach(function(checkbox) {
            const checkboxLabel = checkbox.closest('.checkbox-label');
            const dropdownContainer = checkbox.closest('.dropdown-container');
            const dropdownToggle = dropdownContainer.querySelector('.dropdown-toggle');
            const type = dropdownToggle.attributes.getNamedItem('data-original-text').nodeValue.trim();
            const value = checkboxLabel.childNodes[2].nodeValue.trim();


            //determine which filter category this belongs to
            if (type == 'Type' || type == 'Types') {
                selectedFilters.type.push(value);
            } else if (type == 'Department') {
                selectedFilters.department.push(value);
            } else if (type == 'Team') {
                selectedFilters.team.push(value);
            } else if (type == 'Health Check Card') {
                selectedFilters.healthCheckCard.push(value);
            } else if (type == 'Progress Over Time') {
                selectedFilters.progressOverTime.push(value.match(/\d+/)[0]);
            }
        })

        fetch('/results/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(selectedFilters)
        }).then(response => response.json())
        .then(data => {

            console.log(data['img']);

            const searchResultsArea = document.getElementById('searchResults');
            const resultsMessage = document.getElementById('resultsMessage');

            const resultImage = document.getElementById('resultImage');

            resultsMessage.style = "display: none;"
            searchResultsArea.style = "display: block;"

            resultImage.src = '../static/img/'+ data['img'];
        }).catch(error => {
            console.log(error);
        })
    });


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