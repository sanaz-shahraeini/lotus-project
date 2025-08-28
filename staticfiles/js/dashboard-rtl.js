// Dashboard RTL fixes
document.addEventListener('DOMContentLoaded', function() {
    // Ensure all dashboard header elements have RTL styling
    const dashboardHeader = document.querySelector('.dashboard-header');
    if (dashboardHeader) {
        // Add RTL classes to ensure proper alignment
        dashboardHeader.setAttribute('dir', 'rtl');
        
        // Handle all flex containers inside the dashboard header
        dashboardHeader.querySelectorAll('.flex').forEach(flexContainer => {
            // Ensure flex items are properly aligned for RTL
            if (!flexContainer.classList.contains('flex-col')) {
                flexContainer.style.display = 'flex';
                flexContainer.style.flexDirection = 'row';
                flexContainer.style.alignItems = 'center';
            }
        });
        
        // Fix search input alignment
        const searchInput = dashboardHeader.querySelector('#quickSearch');
        if (searchInput) {
            searchInput.style.textAlign = 'right';
            searchInput.style.paddingRight = '2.5rem';
            searchInput.style.direction = 'rtl';
        }
        
        // Fix search icon position
        const searchIcon = dashboardHeader.querySelector('.absolute');
        if (searchIcon) {
            searchIcon.style.right = '0.75rem';
            searchIcon.style.left = 'auto';
        }
        
        // Fix print button icon
        const printBtnIcon = dashboardHeader.querySelector('#printbtn i');
        if (printBtnIcon) {
            printBtnIcon.style.marginLeft = '0.375rem';
            printBtnIcon.style.marginRight = '0';
        }
    }
    
    // Force RTL for forms and inputs throughout the dashboard
    document.querySelectorAll('.rtl input, .rtl select, .rtl textarea').forEach(element => {
        element.style.direction = 'rtl';
        element.style.textAlign = 'right';
    });
}); 