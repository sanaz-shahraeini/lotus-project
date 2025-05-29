// Handle dark mode functionality only, no toggle buttons
document.addEventListener('DOMContentLoaded', function() {
    // Get saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme') || 
                      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    // Apply the saved theme
    document.documentElement.className = savedTheme;
    
    // Remove ALL theme toggle buttons from the page
    const toggleButtons = document.querySelectorAll('.theme-toggle, #theme-toggle, [id*="theme"][id*="toggle"], .toggle-theme, .theme-switch');
    toggleButtons.forEach(button => {
        if (button) {
            button.remove();
        }
    });
    
    // Create a style element to hide any other toggle buttons
    const style = document.createElement('style');
    style.textContent = `
        /* Hide all possible theme toggle buttons */
        .theme-toggle, 
        #theme-toggle, 
        [id*="theme"][id*="toggle"],
        .toggle-theme,
        .theme-switch,
        .theme-btn {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: absolute !important;
            top: -9999px !important;
            left: -9999px !important;
            z-index: -1 !important;
        }
    `;
    document.head.appendChild(style);
    
    // Add theme toggle functionality to top header button or create new toggle if needed
    const headerButton = document.querySelector('.print-button');
    if (headerButton) {
        // Create a theme toggle button next to print button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'header-theme-toggle bg-gray-100 dark:bg-gray-700 p-2 rounded-md mx-2';
        toggleBtn.innerHTML = savedTheme === 'dark' ? 
            '<i class="fa-solid fa-moon" style="color: #f8fafc;"></i>' : 
            '<i class="fa-solid fa-sun" style="color: #f59e0b;"></i>';
        
        headerButton.parentNode.insertBefore(toggleBtn, headerButton);
        
        // Add click event to toggle theme
        toggleBtn.addEventListener('click', function() {
            const isDark = document.documentElement.classList.contains('dark');
            document.documentElement.className = isDark ? 'light' : 'dark';
            localStorage.setItem('theme', isDark ? 'light' : 'dark');
            
            // Update icon
            this.innerHTML = isDark ? 
                '<i class="fa-solid fa-sun" style="color: #f59e0b;"></i>' : 
                '<i class="fa-solid fa-moon" style="color: #f8fafc;"></i>';
        });
    }
});