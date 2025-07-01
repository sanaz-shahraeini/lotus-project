// Enhanced Mobile Sidebar Functionality
document.addEventListener('DOMContentLoaded', function() {
    // References to DOM elements
    const toggleButton = document.getElementById('toggle-menu');
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const menuIcon = document.getElementById('menu-icon');
    const body = document.body;
    
    // Track sidebar state
    let isSidebarOpen = false;
    
    // Add animation classes if missing
    if (mobileSidebar && !mobileSidebar.classList.contains('slide-in') && 
        !mobileSidebar.classList.contains('slide-out')) {
        mobileSidebar.classList.add('slide-out');
    }
    
    // Toggle sidebar function
    function toggleSidebar() {
        if (!mobileSidebar) return;
        
        isSidebarOpen = !isSidebarOpen;
        
        if (isSidebarOpen) {
            // Open sidebar
            mobileSidebar.classList.remove('slide-out');
            mobileSidebar.classList.add('slide-in');
            mobileSidebar.style.transform = 'translateX(0)';
            
            // Change icon to X
            if (menuIcon) {
                menuIcon.classList.remove('fa-bars');
                menuIcon.classList.add('fa-times');
            }
            
            // Move toggle button
            if (toggleButton) {
                toggleButton.classList.remove('right-4');
                toggleButton.classList.add('right-36'); // Position near sidebar
            }
            
            // Prevent body scrolling
            body.style.overflow = 'hidden';
            
        } else {
            // Close sidebar
            mobileSidebar.classList.remove('slide-in');
            mobileSidebar.classList.add('slide-out');
            mobileSidebar.style.transform = 'translateX(100%)';
            
            // Change icon back to bars
            if (menuIcon) {
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
            }
            
            // Reset toggle button position
            if (toggleButton) {
                toggleButton.classList.remove('right-36');
                toggleButton.classList.add('right-4');
            }
            
            // Re-enable body scrolling
            body.style.overflow = '';
        }
    }
    
    // Setup event listeners
    if (toggleButton) {
        // Remove any existing listeners
        const newToggleBtn = toggleButton.cloneNode(true);
        toggleButton.parentNode.replaceChild(newToggleBtn, toggleButton);
        
        // Add fresh event listener
        newToggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSidebar();
        });
    }
    
    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
        if (isSidebarOpen && 
            mobileSidebar && 
            !mobileSidebar.contains(e.target) && 
            toggleButton && 
            !toggleButton.contains(e.target)) {
            toggleSidebar();
        }
    });
    
    // Highlight current page link
    highlightCurrentPage();
    
    // Function to highlight current page in sidebar
    function highlightCurrentPage() {
        const currentPath = window.location.pathname;
        
        if (mobileSidebar) {
            const links = mobileSidebar.querySelectorAll('nav a');
            
            links.forEach(link => {
                // Remove any existing active class
                link.classList.remove('active');
                
                // Compare href with current path
                const href = link.getAttribute('href');
                
                // Add active class if matches current path
                if (href === currentPath || 
                    (currentPath.includes(href) && href !== '/')) {
                    link.classList.add('active');
                }
            });
        }
    }
}); 