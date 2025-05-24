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
                    sidebar.style.transform = 'translateX(100%)';
                    if (menuIcon) menuIcon.classList.replace('fa-times', 'fa-bars');
                    document.body.classList.remove('overflow-hidden');
                    newToggleMenu.classList.remove('right-32');
                    newToggleMenu.classList.add('right-4');
                } else {
                    sidebar.style.transform = 'translateX(0)';
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
        newToggleMenu.style.zIndex = '9999';
    }
});
