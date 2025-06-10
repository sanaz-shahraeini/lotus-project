// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.querySelector('.fa-sun');
    const moonIcon = document.querySelector('.fa-moon');
    
    // Check for saved theme preference or use default
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.className = currentTheme;
    
    // Set initial icon visibility
    if (currentTheme === 'dark') {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
    } else {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
        // Make sure moon icon is visible in light mode
        if (moonIcon) moonIcon.style.color = '#3b82f6';
    }
    
    // Add click event listener
    themeToggle.addEventListener('click', function() {
        console.log('Theme toggle clicked');
        
        // Toggle theme
        if (document.documentElement.classList.contains('light')) {
            // Switch to dark mode
            document.documentElement.classList.replace('light', 'dark');
            localStorage.setItem('theme', 'dark');
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
            console.log('Switched to dark mode');
        } else {
            // Switch to light mode
            document.documentElement.classList.replace('dark', 'light');
            localStorage.setItem('theme', 'light');
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
            // Make sure moon icon is visible in light mode
            if (moonIcon) moonIcon.style.color = '#3b82f6';
            console.log('Switched to light mode');
        }
    });
});
