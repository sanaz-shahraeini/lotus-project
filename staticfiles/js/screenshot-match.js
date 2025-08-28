// JavaScript to ensure styling matches the screenshot
document.addEventListener('DOMContentLoaded', function() {
    // Force dark theme
    document.documentElement.classList.add('dark');
    document.body.classList.add('dark');
    
    // Ensure the toggle switch is properly styled
    const toggleSwitches = document.querySelectorAll('.toggle-switch input[type="checkbox"]');
    toggleSwitches.forEach(toggle => {
        const slider = toggle.nextElementSibling;
        if (slider) {
            slider.style.backgroundColor = toggle.checked ? '#00BCD4' : '#121824';
            
            toggle.addEventListener('change', function() {
                slider.style.backgroundColor = this.checked ? '#00BCD4' : '#121824';
            });
        }
    });
    
    // Ensure radio buttons are properly styled
    const radioButtons = document.querySelectorAll('.radio-item input[type="radio"]');
    radioButtons.forEach(radio => {
        const label = radio.nextElementSibling;
        if (label) {
            if (radio.checked) {
                label.style.backgroundColor = '#00BCD4';
                label.style.color = 'white';
            } else {
                label.style.backgroundColor = 'transparent';
                label.style.color = '#B0BEC5';
            }
            
            radio.addEventListener('change', function() {
                if (this.checked) {
                    // Reset all labels in the group
                    const group = this.closest('.radio-group');
                    if (group) {
                        const labels = group.querySelectorAll('label');
                        labels.forEach(l => {
                            l.style.backgroundColor = 'transparent';
                            l.style.color = '#B0BEC5';
                        });
                    }
                    
                    // Style this label
                    label.style.backgroundColor = '#00BCD4';
                    label.style.color = 'white';
                }
            });
        }
    });
    
    // Ensure dropdown buttons have the right styling
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        // Make sure there's an icon
        if (!toggle.querySelector('i')) {
            const icon = document.createElement('i');
            icon.className = 'fa-regular fa-chevron-down';
            toggle.appendChild(icon);
        }
    });
    
    // Set initial radio button if none selected
    const radioGroups = document.querySelectorAll('.radio-group');
    radioGroups.forEach(group => {
        const radios = group.querySelectorAll('input[type="radio"]');
        let hasChecked = false;
        
        radios.forEach(radio => {
            if (radio.checked) {
                hasChecked = true;
            }
        });
        
        if (!hasChecked && radios.length > 0) {
            radios[0].checked = true;
            const event = new Event('change');
            radios[0].dispatchEvent(event);
        }
    });
}); 