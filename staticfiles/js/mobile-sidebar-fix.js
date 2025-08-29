// Fix for mobile sidebar toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('mobile-sidebar');
    const toggleButton = document.getElementById('toggle-menu');
    const menuIcon = document.getElementById('menu-icon');
    
    if (!sidebar || !toggleButton || !menuIcon) {
        console.error('Mobile sidebar elements not found');
        return;
    }
    
    // Toggle sidebar when menu button is clicked
    toggleButton.addEventListener('click', function() {
        const isOpen = sidebar.classList.contains('translate-x-0');
        
        if (isOpen) {
            // Close sidebar
            sidebar.classList.remove('translate-x-0');
            sidebar.classList.add('translate-x-full');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        } else {
            // Open sidebar
            sidebar.classList.remove('translate-x-full');
            sidebar.classList.add('translate-x-0');
            menuIcon.classList.remove('fa-bars');
            menuIcon.classList.add('fa-times');
        }
    });
    
    // Close sidebar when clicking outside
    document.addEventListener('click', function(event) {
        const isOpen = sidebar.classList.contains('translate-x-0');
        const clickedOnToggle = toggleButton.contains(event.target);
        const clickedInsideSidebar = sidebar.contains(event.target);
        
        if (isOpen && !clickedOnToggle && !clickedInsideSidebar) {
            sidebar.classList.remove('translate-x-0');
            sidebar.classList.add('translate-x-full');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    });
    
    // Handle exit button clicks for mobile
    const exitBtnMobile = document.getElementById('exit-mb');
    const exitModalMobile = document.getElementById('exitmodal-mb');
    
    if (exitBtnMobile && exitModalMobile) {
        exitBtnMobile.addEventListener('click', function() {
            exitModalMobile.classList.remove('hidden');
            exitModalMobile.style.opacity = '1';
            
            const modalContent = exitModalMobile.querySelector('.modal-content');
            if (modalContent) {
                modalContent.style.transform = 'scale(1)';
            }
        });
    }
});
