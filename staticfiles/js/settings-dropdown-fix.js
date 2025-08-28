// Complete replacement for settings dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log("New settings dropdown implementation loaded");
    
    // Get references to all elements
    const settingsBtn = document.getElementById('show-settings');
    const settingsBtnMobile = document.getElementById('show-settings-mb');
    const dropdown = document.getElementById('dropdownmenu');
    const dropdownMobile = document.getElementById('dropdownmenu-mb');
    
    // Log element existence for debugging
    console.log("Desktop settings button exists:", !!settingsBtn);
    console.log("Mobile settings button exists:", !!settingsBtnMobile);
    console.log("Desktop dropdown exists:", !!dropdown);
    console.log("Mobile dropdown exists:", !!dropdownMobile);

    // Remove any existing event listeners by cloning and replacing elements
    if (settingsBtn) {
        const newSettingsBtn = settingsBtn.cloneNode(true);
        settingsBtn.parentNode.replaceChild(newSettingsBtn, settingsBtn);
        
        // Add click handler to the new button
        newSettingsBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Force show dropdown
            if (dropdown) {
                // Hide all other dropdowns first
                if (dropdownMobile && dropdownMobile.style.display === 'block') {
                    dropdownMobile.style.display = 'none';
                }
                
                // Toggle current dropdown
                if (dropdown.style.display === 'block') {
                    dropdown.style.display = 'none';
                } else {
                    dropdown.style.display = 'block';
                    
                    // Force proper positioning
                    dropdown.style.position = 'absolute';
                    dropdown.style.zIndex = '10000';
                    dropdown.style.top = '100%';
                    dropdown.style.right = '0';
                }
                
                console.log("Toggled desktop dropdown, display:", dropdown.style.display);
            }
        });
    }
    
    // Same for mobile
    if (settingsBtnMobile) {
        const newSettingsBtnMobile = settingsBtnMobile.cloneNode(true);
        settingsBtnMobile.parentNode.replaceChild(newSettingsBtnMobile, settingsBtnMobile);
        
        // Add click handler to the new button
        newSettingsBtnMobile.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Force show dropdown
            if (dropdownMobile) {
                // Hide all other dropdowns first
                if (dropdown && dropdown.style.display === 'block') {
                    dropdown.style.display = 'none';
                }
                
                // Toggle current dropdown
                if (dropdownMobile.style.display === 'block') {
                    dropdownMobile.style.display = 'none';
                } else {
                    dropdownMobile.style.display = 'block';
                    
                    // Force proper positioning
                    dropdownMobile.style.position = 'absolute';
                    dropdownMobile.style.zIndex = '10000';
                    dropdownMobile.style.top = '100%';
                    dropdownMobile.style.right = '0';
                }
                
                console.log("Toggled mobile dropdown, display:", dropdownMobile.style.display);
            }
        });
    }
    
    // Initialize dropdown styles
    if (dropdown) {
        dropdown.classList.add('settings-dropdown');
        dropdown.style.display = 'none';
        dropdown.style.position = 'absolute';
        dropdown.style.zIndex = '10000';
        dropdown.style.backgroundColor = 'white';
        dropdown.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        dropdown.style.borderRadius = '4px';
        dropdown.style.width = '200px';
        dropdown.style.top = '100%';
        dropdown.style.right = '0';
    }
    
    if (dropdownMobile) {
        dropdownMobile.classList.add('settings-dropdown');
        dropdownMobile.style.display = 'none';
        dropdownMobile.style.position = 'absolute';
        dropdownMobile.style.zIndex = '10000';
        dropdownMobile.style.backgroundColor = 'white';
        dropdownMobile.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        dropdownMobile.style.borderRadius = '4px';
        dropdownMobile.style.width = '200px';
        dropdownMobile.style.top = '100%';
        dropdownMobile.style.right = '0';
    }
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (dropdown && dropdown.style.display === 'block' && 
            !e.target.closest('#show-settings') && 
            !e.target.closest('#dropdownmenu')) {
            
            dropdown.style.display = 'none';
            console.log("Closed desktop dropdown by outside click");
        }
        
        if (dropdownMobile && dropdownMobile.style.display === 'block' && 
            !e.target.closest('#show-settings-mb') && 
            !e.target.closest('#dropdownmenu-mb')) {
            
            dropdownMobile.style.display = 'none';
            console.log("Closed mobile dropdown by outside click");
        }
    });
    
    // Remove the 'hidden' class from dropdowns completely
    if (dropdown) dropdown.classList.remove('hidden');
    if (dropdownMobile) dropdownMobile.classList.remove('hidden');
}); 