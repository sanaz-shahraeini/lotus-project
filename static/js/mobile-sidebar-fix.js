// Mobile Sidebar Fix

// Wait for document to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Force hide desktop sidebar on mobile devices
    function hideSidebarOnMobile() {
        if (window.innerWidth < 1024) {
            // Hide desktop sidebar
            const desktopSidebar = document.getElementById('sidebar');
            if (desktopSidebar) {
                desktopSidebar.style.display = 'none';
            }
        }
    }
    
    // Run on page load
    hideSidebarOnMobile();
    
    // Run when window is resized
    window.addEventListener('resize', hideSidebarOnMobile);
    
    // Fix hamburger menu toggle functionality
    const toggleButton = document.getElementById('toggle-menu');
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const menuIcon = document.getElementById('menu-icon');
    
    if (toggleButton && mobileSidebar && menuIcon) {
        let isSidebarOpen = false;
        
        toggleButton.addEventListener('click', function() {
            isSidebarOpen = !isSidebarOpen;
            
            if (isSidebarOpen) {
                mobileSidebar.style.transform = 'translateX(0)';
                document.body.classList.add('overflow-hidden');
                menuIcon.classList.remove('fa-bars');
                menuIcon.classList.add('fa-times');
                toggleButton.classList.remove('right-4');
                toggleButton.classList.add('right-32');
            } else {
                mobileSidebar.style.transform = 'translateX(100%)';
                document.body.classList.remove('overflow-hidden');
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
                toggleButton.classList.remove('right-32');
                toggleButton.classList.add('right-4');
            }
        });
        
        // Close sidebar when clicking outside
        document.addEventListener('click', function(e) {
            if (isSidebarOpen && e.target !== mobileSidebar && !mobileSidebar.contains(e.target) && e.target !== toggleButton) {
                isSidebarOpen = false;
                mobileSidebar.style.transform = 'translateX(100%)';
                document.body.classList.remove('overflow-hidden');
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
                toggleButton.classList.remove('right-32');
                toggleButton.classList.add('right-4');
            }
        });
    }
});
