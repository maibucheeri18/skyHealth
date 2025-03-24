// Get user role from session storage or set default
function getCurrentRole() {
    return sessionStorage.getItem('userRole') || 'Engineer';
}

// Save user role to session storage
function saveUserRole(role) {
    sessionStorage.setItem('userRole', role);
}

// update the navbar based on the user
function updateNavbar(role) {
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.innerHTML = role + '<span class="arrow-down"><i class="fa-solid fa-angle-down"></i></span>';
    }

    // update dropdown options to include all roles EXCEPT the currently selected one
    const roleDropdown = document.getElementById('roleDropdown');
    if (roleDropdown) {
        const allRoles = ['Engineer', 'Team Leader', 'Department Leader', 'Senior Manager'];
        
        const otherRoles = allRoles.filter(r => r !== role);
        
        roleDropdown.innerHTML = '';
        
        otherRoles.forEach(otherRole => {
            const link = document.createElement('a');
            link.className = 'subnav-item';
            link.href = '#';
            link.textContent = otherRole;
            
            link.addEventListener('click', function(event) {
                event.preventDefault();
                saveUserRole(otherRole);
                updateNavbar(otherRole);
                updateNavLinks(otherRole);
                roleDropdown.classList.remove('show');
                const arrowIcon = userDropdown.querySelector('.arrow-down i');
                arrowIcon.classList.remove('fa-angle-up');
                arrowIcon.classList.add('fa-angle-down');
            });
            
            roleDropdown.appendChild(link);
        });
    }

    updateNavLinks(role);
}

// Update the main navigation links based on role
function updateNavLinks(role) {
    const navbarNav = document.getElementById('navbarNav');
    if (!navbarNav) return;

    const navLinks = navbarNav.querySelector('.navbar-nav');
    if (!navLinks) return;

    navLinks.innerHTML = '';

    if (role === 'Engineer' || role === 'Team Leader') {
        navLinks.innerHTML = `
            <li class="navbar-item">
                <a class="nav-link active" href="#">Health Check</a>
            </li>
            <li class="navbar-item">
                <a class="nav-link" href="#">Results</a>
            </li>
            <li class="navbar-item">
                <a class="nav-link" href="#">My Account</a>
            </li>
            <li class="navbar-item">
                <a class="nav-link" href="#">Log Off</a>
            </li>
        `;
    } else {
        navLinks.innerHTML = `
            <li class="navbar-item">
                <a class="nav-link active" href="#">Results</a>
            </li>
            <li class="navbar-item">
                <a class="nav-link" href="#">My Account</a>
            </li>
            <li class="navbar-item">
                <a class="nav-link" href="#">Log Off</a>
            </li>
        `;
    }
    
    setActiveNavLink();
}

// Function to handle setting the active link
function setActiveNavLink() {
    const navLinks = document.querySelectorAll('#navbarNav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            navLinks.forEach(navLink => {
                navLink.classList.remove('active');
            });
            
            this.classList.add('active');
        });
    });
}

// Show appropriate navbar based on page type
function showAppropriateNavbar() {
   
    const isLoggedIn = document.body.classList.contains('logged-in') || 
                       window.location.pathname.includes('/dashboard') ||
                       document.cookie.includes('sessionid=');  
    
    const authNavbar = document.querySelector('.auth-navbar');
    if (!authNavbar) return;
    
    const authNavbarContainer = authNavbar.closest('.navbar-container');
    const mainNavbarContainer = document.querySelectorAll('.navbar-container')[1];
    
    if (isLoggedIn) {
        if (authNavbarContainer) authNavbarContainer.style.display = 'none';
        if (mainNavbarContainer) mainNavbarContainer.style.display = 'block';
        updateNavbar(getCurrentRole());
    } else {
        if (authNavbarContainer) authNavbarContainer.style.display = 'block';
        if (mainNavbarContainer) mainNavbarContainer.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    showAppropriateNavbar();
    
    setActiveNavLink();
    
    const userDropdown = document.getElementById('userDropdown');
    const roleDropdown = document.getElementById('roleDropdown');
    
    // Handle dropdown functionality (keeping original behavior)
    if (userDropdown && roleDropdown) {
        userDropdown.addEventListener('click', function(event) {
            event.stopPropagation();
            roleDropdown.classList.toggle('show');
            const arrowIcon = userDropdown.querySelector('.arrow-down i');
            arrowIcon.classList.toggle('fa-angle-down');
            arrowIcon.classList.toggle('fa-angle-up');
        });
        
        window.addEventListener('click', function() {
            if (roleDropdown.classList.contains('show')) {
                roleDropdown.classList.remove('show');
                const arrowIcon = userDropdown.querySelector('.arrow-down i');
                arrowIcon.classList.remove('fa-angle-up');
                arrowIcon.classList.add('fa-angle-down');
            }
        });
        
        const currentRole = getCurrentRole();
        updateNavbar(currentRole);
        
        roleDropdown.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
});