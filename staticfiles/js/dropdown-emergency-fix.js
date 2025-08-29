// Emergency direct fix for settings dropdown
(function() {
    // Wait for DOM to fully load
    document.addEventListener('DOMContentLoaded', function() {
        // Create direct links instead of dropdown
        createDirectLinksForSettings();
    });

    function createDirectLinksForSettings() {
        // 1. Find the settings container elements
        const desktopContainer = document.querySelector('#sidebar .settings-container') || 
                               document.querySelector('#sidebar div:has(#show-settings)');
        
        const mobileContainer = document.querySelector('#mobile-sidebar .settings-container-mb') || 
                              document.querySelector('#mobile-sidebar div:has(#show-settings-mb)');
        
        // 2. Replace containers with direct links in desktop sidebar
        if (desktopContainer) {
            const parentNav = desktopContainer.parentNode;
            
            // Create user settings link - only one entry for user management
            const userSettingsLink = document.createElement('a');
            userSettingsLink.href = "/user/";
            userSettingsLink.className = "py-3 text-xs sm:text-sm flex items-center justify-start";
            userSettingsLink.innerHTML = '<i class="fas fa-user-cog"></i> <span class="ml-2 sidebar-text sm:inline">مدیریت کاربران</span>';
            
            // Create system settings link
            const systemSettingsLink = document.createElement('a');
            systemSettingsLink.href = "/settings/";
            systemSettingsLink.className = "py-3 text-xs sm:text-sm flex items-center justify-start";
            systemSettingsLink.innerHTML = '<i class="fas fa-cogs"></i> <span class="ml-2 sidebar-text sm:inline">مدیریت سیستم</span>';
            
            // Replace the original settings dropdown with direct links
            parentNav.replaceChild(userSettingsLink, desktopContainer);
            parentNav.insertBefore(systemSettingsLink, userSettingsLink.nextSibling);
        }
        
        // 3. Replace containers with direct links in mobile sidebar
        if (mobileContainer) {
            const parentNav = mobileContainer.parentNode;
            
            // Create user settings link - only one entry for user management
            const userSettingsLink = document.createElement('a');
            userSettingsLink.href = "/user/";
            userSettingsLink.className = "py-3 text-xs sm:text-sm flex items-center justify-start";
            userSettingsLink.innerHTML = '<i class="fas fa-user-cog"></i> <span class="ml-2 sidebar-text sm:inline">مدیریت کاربران</span>';
            
            // Create system settings link
            const systemSettingsLink = document.createElement('a');
            systemSettingsLink.href = "/settings/";
            systemSettingsLink.className = "py-3 text-xs sm:text-sm flex items-center justify-start";
            systemSettingsLink.innerHTML = '<i class="fas fa-cogs"></i> <span class="ml-2 sidebar-text sm:inline">مدیریت سیستم</span>';
            
            // Replace the original settings dropdown with direct links
            parentNav.replaceChild(userSettingsLink, mobileContainer);
            parentNav.insertBefore(systemSettingsLink, userSettingsLink.nextSibling);
        }
    }
})(); 