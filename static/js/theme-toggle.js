/**
 * Theme Toggle Functionality for Lotus Application
 * Provides consistent dark/light mode toggle across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle button with forceful override
    const initThemeToggle = function() {
        const themeToggleBtn = document.getElementById('theme-toggle');
        
        if (!themeToggleBtn) return;
        
        // Remove any existing event listeners
        const newButton = themeToggleBtn.cloneNode(true);
        themeToggleBtn.parentNode.replaceChild(newButton, themeToggleBtn);
        
        // Get saved theme or use system preference
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Set initial theme
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.documentElement.classList.add('dark');
            document.documentElement.classList.remove('light');
        } else {
            document.documentElement.classList.add('light');
            document.documentElement.classList.remove('dark');
        }
        
        // Add toggle event
        newButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.add('light');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.classList.remove('light');
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
        });
    };
    
    // Initialize theme toggle
    initThemeToggle();
    
    // Add a backup initialization for any race conditions
    setTimeout(initThemeToggle, 500);
});
