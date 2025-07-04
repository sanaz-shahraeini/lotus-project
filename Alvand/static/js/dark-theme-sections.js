// Dark Theme Sections Enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to form elements
    const formElements = document.querySelectorAll('.settings-card input, .settings-card select, .settings-card .dropdown-toggle');
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.borderColor = '#00BCD4';
            this.style.boxShadow = '0 0 0 2px rgba(0, 188, 212, 0.25)';
        });
        
        element.addEventListener('blur', function() {
            this.style.borderColor = '#1E2A3B';
            this.style.boxShadow = 'none';
        });
    });
    
    // Initialize radio buttons
    const radioButtons = document.querySelectorAll('.radio-item input[type="radio"]');
    radioButtons.forEach(radio => {
        if (radio.checked) {
            const label = radio.nextElementSibling;
            if (label && label.tagName === 'LABEL') {
                label.style.backgroundColor = '#00BCD4';
                label.style.color = '#FFFFFF';
            }
        }
    });
    
    // Enhance toggle switches
    const toggleSwitches = document.querySelectorAll('.toggle-switch input[type="checkbox"]');
    toggleSwitches.forEach(toggle => {
        const slider = toggle.nextElementSibling;
        
        // Add ripple effect on click
        toggle.addEventListener('change', function() {
            if (slider) {
                // Create ripple effect
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.position = 'absolute';
                ripple.style.width = '100%';
                ripple.style.height = '100%';
                ripple.style.backgroundColor = this.checked ? 'rgba(0, 188, 212, 0.2)' : 'rgba(176, 190, 197, 0.2)';
                ripple.style.borderRadius = '24px';
                ripple.style.transform = 'scale(0)';
                ripple.style.opacity = '1';
                ripple.style.transition = 'transform 0.3s, opacity 0.5s';
                
                slider.appendChild(ripple);
                
                // Trigger animation
                setTimeout(() => {
                    ripple.style.transform = 'scale(1)';
                    ripple.style.opacity = '0';
                    
                    // Remove after animation
                    setTimeout(() => {
                        slider.removeChild(ripple);
                    }, 500);
                }, 10);
            }
        });
    });
    
    // Add subtle animations to dropdowns
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('dropdown-menu')) {
                if (dropdown.classList.contains('hidden')) {
                    dropdown.style.opacity = '0';
                    dropdown.style.transform = 'translateY(-10px)';
                    dropdown.classList.remove('hidden');
                    
                    // Trigger animation
                    setTimeout(() => {
                        dropdown.style.transition = 'opacity 0.2s, transform 0.2s';
                        dropdown.style.opacity = '1';
                        dropdown.style.transform = 'translateY(0)';
                    }, 10);
                } else {
                    dropdown.style.transition = 'opacity 0.2s, transform 0.2s';
                    dropdown.style.opacity = '0';
                    dropdown.style.transform = 'translateY(-10px)';
                    
                    // Hide after animation
                    setTimeout(() => {
                        dropdown.classList.add('hidden');
                    }, 200);
                }
            }
        });
    });
}); 