// Disable theme toggle and force light mode
document.addEventListener('DOMContentLoaded', function() {
    // Force light theme
    document.documentElement.className = 'light';
    localStorage.setItem('theme', 'light');
    
    // Remove the theme toggle button from DOM
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.remove();
    }
    
    // Override the theme toggle functionality
    if (window.jQuery) {
        jQuery("#theme-toggle").off('click');
    }
    
    // Create a style element to hide the toggle button
    const style = document.createElement('style');
    style.textContent = `
        .theme-toggle, #theme-toggle {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
    `;
    document.head.appendChild(style);
}); 