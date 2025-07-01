// Fix form elements specifically for settings page
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the settings page
    const isSettingsPage = window.location.pathname.includes('settings') ||
                          document.title.includes('تنظیمات');
    
    if (!isSettingsPage) return;
    
    console.log('Applying settings page form fixes');
    
    // Fix select elements height
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach(select => {
        makeConsistentHeight(select);
        
        // Also attach a listener for any styling changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'style' || 
                    mutation.attributeName === 'class') {
                    makeConsistentHeight(select);
                }
            });
        });
        
        observer.observe(select, { 
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    });
    
    // Force all inputs to consistent height
    const inputElements = document.querySelectorAll('input:not([type="checkbox"]):not([type="radio"])');
    inputElements.forEach(input => {
        makeConsistentHeight(input);
    });
    
    // Apply select specific fixes
    selectElements.forEach(select => {
        // Ensure native appearance
        select.style.webkitAppearance = 'menulist';
        select.style.mozAppearance = 'menulist';
        select.style.appearance = 'menulist';
        
        // Remove any custom background images
        select.style.backgroundImage = 'none';
    });
    
    // Create a stylesheet with higher specificity
    createHighSpecificityStyles();
});

function makeConsistentHeight(element) {
    element.style.height = '38px';
    element.style.minHeight = '38px';
    element.style.maxHeight = '38px';
    
    // Fix padding to ensure text is vertically centered
    element.style.paddingTop = '0';
    element.style.paddingBottom = '0';
    element.style.boxSizing = 'border-box';
}

function createHighSpecificityStyles() {
    // Create style element
    const style = document.createElement('style');
    
    // Add rules with high specificity
    style.textContent = `
        body[dir="rtl"] .content-wrapper select,
        body[dir="rtl"] form select,
        body[dir="rtl"] .settings-form select,
        body[dir="rtl"] #device-form select,
        html body form select.form-control,
        html body select[name],
        html body select {
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            appearance: menulist !important;
            -webkit-appearance: menulist !important;
            -moz-appearance: menulist !important;
            background-image: none !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 0.375rem !important;
        }
    `;
    
    // Add to head
    document.head.appendChild(style);
} 