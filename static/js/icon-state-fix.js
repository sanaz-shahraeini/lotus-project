// This script runs at the end to ensure correct icon state
(function() {
    // Function to check sidebar state and update icon
    function fixIconState() {
        const menuIcon = document.getElementById('menu-icon');
        const sidebar = document.getElementById('mobile-sidebar');
        const toggleMenu = document.getElementById('toggle-menu');
        
        if (!menuIcon || !sidebar) return;
        
        // Get computed style
        const sidebarStyle = window.getComputedStyle(sidebar);
        const transform = sidebarStyle.transform || sidebarStyle.webkitTransform || '';
        const right = sidebarStyle.right;
        const visibility = sidebarStyle.visibility;
        const display = sidebarStyle.display;
        const dataState = sidebar.getAttribute('data-sidebar-state');
        
        // Check if sidebar is visibly open
        const isOpen = dataState === 'open' ||
                      sidebar.classList.contains('translate-x-0') || 
                      (transform && !transform.includes('translateX(100%)') && 
                       !transform.includes('translate3d(100%')) ||
                      right === '0px' ||
                      sidebar.style.transform === 'translateX(0px)' ||
                      sidebar.style.transform === 'translateX(0)';
        
        // Force icon to match sidebar state
        if (isOpen) {
            // Make sure we update the data attribute too
            sidebar.setAttribute('data-sidebar-state', 'open');
            
            // Remove fa-bars before adding fa-times to avoid having both
            if (menuIcon.classList.contains('fa-bars')) {
                menuIcon.classList.remove('fa-bars');
            }
            if (!menuIcon.classList.contains('fa-times')) {
                menuIcon.classList.add('fa-times');
            }
            
            // Also fix toggle position
            if (toggleMenu) {
                toggleMenu.classList.remove('right-4');
                if (!toggleMenu.classList.contains('right-32')) {
                    toggleMenu.classList.add('right-32');
                }
            }
        } else {
            // Make sure we update the data attribute too
            sidebar.setAttribute('data-sidebar-state', 'closed');
            
            // Remove fa-times before adding fa-bars to avoid having both
            if (menuIcon.classList.contains('fa-times')) {
                menuIcon.classList.remove('fa-times');
            }
            if (!menuIcon.classList.contains('fa-bars')) {
                menuIcon.classList.add('fa-bars');
            }
            
            // Reset toggle position
            if (toggleMenu) {
                toggleMenu.classList.remove('right-32');
                if (!toggleMenu.classList.contains('right-4')) {
                    toggleMenu.classList.add('right-4');
                }
            }
        }
    }
    
    // Run on load
    if (document.readyState === 'complete') {
        fixIconState();
    } else {
        window.addEventListener('load', fixIconState);
    }
    
    // Also run after a delay to catch any late rendering
    setTimeout(fixIconState, 500);
    setTimeout(fixIconState, 1000);
    
    // Add event listener for sidebar transitions
    const sidebar = document.getElementById('mobile-sidebar');
    if (sidebar) {
        sidebar.addEventListener('transitionend', fixIconState);
    }
})(); 