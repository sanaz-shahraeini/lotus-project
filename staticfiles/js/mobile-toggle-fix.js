// Fix for hamburger menu visibility and functionality in mobile view
document.addEventListener('DOMContentLoaded', function() {
    // Ensure the hamburger menu toggle is visible on all screens
    function fixToggleButton() {
        const toggleMenu = document.getElementById('toggle-menu');
        const isMobile = window.innerWidth < 1024;
        
        if (toggleMenu) {
            // First, set up the toggle visibility based on screen size
            if (isMobile) {
                // Show toggle in mobile view
                toggleMenu.style.display = 'flex';
                toggleMenu.style.visibility = 'visible';
                toggleMenu.style.opacity = '1';
                toggleMenu.style.pointerEvents = 'auto';
            } else {
                // Hide toggle in desktop view
                toggleMenu.style.display = 'none';
                toggleMenu.style.visibility = 'hidden';
                toggleMenu.style.opacity = '0';
                toggleMenu.style.pointerEvents = 'none';
                return; // Don't apply other styles if hidden
            }
            
            // Only continue with styling if we're in mobile view
            if (isMobile) {
                // Ensure proper positioning and styling
                toggleMenu.style.position = 'fixed';
                toggleMenu.style.zIndex = '10000';
                toggleMenu.style.top = '1rem';
                toggleMenu.style.right = '1rem';
                toggleMenu.style.alignItems = 'center';
                toggleMenu.style.justifyContent = 'center';
                toggleMenu.style.cursor = 'pointer';
                
                // Add styling for better visibility
                if (window.innerWidth <= 768) {
                    // Specific styles for mobile
                    toggleMenu.style.width = '40px';
                    toggleMenu.style.height = '40px';
                    toggleMenu.style.borderRadius = '50%';
                    
                    // Set background based on theme
                    if (document.documentElement.classList.contains('dark')) {
                        toggleMenu.style.backgroundColor = 'rgba(13, 27, 42, 0.9)';
                        toggleMenu.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.5)';
                    } else {
                        toggleMenu.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
                        toggleMenu.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.2)';
                    }
                }
                
                // Check sidebar visibility to set correct icon
                checkSidebarState();
            }
        }
    }
    
    // Function to check sidebar state and update icon accordingly
    function checkSidebarState() {
        const menuIcon = document.getElementById('menu-icon');
        const sidebar = document.getElementById('mobile-sidebar');
        
        if (menuIcon && sidebar) {
            const sidebarStyle = window.getComputedStyle(sidebar);
            const transformValue = sidebarStyle.transform || sidebarStyle.webkitTransform || '';
            
            // If sidebar is visible (right at 0 position)
            if (sidebar.classList.contains('translate-x-0') || 
                (transformValue && !transformValue.includes('translateX(100%)') && 
                !transformValue.includes('translate3d(100%'))) {
                
                // Make sure we show the close icon
                menuIcon.classList.remove('fa-bars');
                menuIcon.classList.add('fa-times');
            } else {
                // Make sure we show the hamburger icon
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
            }
        }
    }
    
    // Fix toggle button styling initially
    fixToggleButton();
    
    // Also run a separate check after a short delay to catch any race conditions
    setTimeout(checkSidebarState, 300);
    
    // Fix toggle button when window is resized
    window.addEventListener('resize', fixToggleButton);
    
    // Fix toggle button when theme changes
    document.addEventListener('themeChanged', fixToggleButton);
    
    // Watch for theme changes through a mutation observer
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                fixToggleButton();
            }
        });
    });
    
    observer.observe(document.documentElement, { attributes: true });
}); 