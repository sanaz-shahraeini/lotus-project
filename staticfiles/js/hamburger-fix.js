// Fix for hamburger menu clickability
document.addEventListener('DOMContentLoaded', function() {
    // Get the hamburger menu button
    const toggleMenu = document.getElementById('toggle-menu');
    
    if (toggleMenu) {
        // Remove any existing event listeners
        toggleMenu.replaceWith(toggleMenu.cloneNode(true));
        
        // Get the fresh reference
        const newToggleMenu = document.getElementById('toggle-menu');
        
        // Add a fresh click event listener
        newToggleMenu.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Get the mobile sidebar
            const sidebar = document.getElementById('mobile-sidebar');
            const menuIcon = document.getElementById('menu-icon');
            
            if (sidebar) {
                // Toggle the sidebar
                const isOpen = sidebar.style.transform === 'translateX(0px)';
                
                if (isOpen) {
                    // Sidebar is currently open, so we're closing it
                    sidebar.style.transform = 'translateX(100%)';
                    // Change icon to hamburger when sidebar is closed
                    if (menuIcon) menuIcon.classList.replace('fa-times', 'fa-bars');
                    document.body.classList.remove('overflow-hidden');
                    newToggleMenu.classList.remove('right-32');
                    newToggleMenu.classList.add('right-4');
                } else {
                    // Sidebar is currently closed, so we're opening it
                    sidebar.style.transform = 'translateX(0)';
                    // Change icon to close (X) when sidebar is open
                    if (menuIcon) menuIcon.classList.replace('fa-bars', 'fa-times');
                    document.body.classList.add('overflow-hidden');
                    newToggleMenu.classList.remove('right-4');
                    newToggleMenu.classList.add('right-32');
                }
            }
        });
        
        // Make sure it's visible and clickable
        newToggleMenu.style.pointerEvents = 'auto';
        newToggleMenu.style.cursor = 'pointer';
        newToggleMenu.style.zIndex = '1000000';
        
        // Initialize with correct icon (hamburger/bars when closed)
        const menuIcon = document.getElementById('menu-icon');
        if (menuIcon) {
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    }
});
