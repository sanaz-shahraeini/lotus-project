// Enhanced theme toggle functionality - works with base.html's theme toggle
document.addEventListener('DOMContentLoaded', function() {
    // We'll let base.html handle the theme preference loading and initial setup
    
    // Find the main theme toggle button (it's already being handled by jQuery in base.html)
    const mainThemeToggle = document.querySelector('#theme-toggle');
    
    // Just ensure the icons display correctly based on current theme
    if (mainThemeToggle) {
        // Update visual state only, without attaching new event handlers
        const isDark = document.documentElement.classList.contains('dark');
        const sunIcon = mainThemeToggle.querySelector('.fa-sun');
        const moonIcon = mainThemeToggle.querySelector('.fa-moon');
        
        if (sunIcon && moonIcon) {
            if (isDark) {
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            } else {
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            }
        }
        
        // Make sure the toggle is visible and properly styled
        mainThemeToggle.style.display = 'inline-flex';
        mainThemeToggle.style.opacity = '1';
        mainThemeToggle.style.visibility = 'visible';
        mainThemeToggle.style.position = 'relative';
        mainThemeToggle.style.zIndex = '100';
    }
});