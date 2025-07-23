// Fix sidebar text truncation issues
document.addEventListener('DOMContentLoaded', function() {
    // Find all sidebar text elements and remove any truncation
    fixSidebarTextTruncation();
    
    // Remove any ellipsis from sidebar text
    removeAllEllipsis();
    
    // Check if there are any elements with ellipsis and fix them
    setTimeout(checkForEllipsis, 500);
});

function fixSidebarTextTruncation() {
    // Target all elements in both sidebars that might contain text
    const sidebarTextElements = document.querySelectorAll('#sidebar span, #mobile-sidebar span, .sidebar-text');
    
    sidebarTextElements.forEach(element => {
        // Remove any CSS properties that might cause truncation
        element.style.textOverflow = 'clip';
        element.style.overflow = 'visible';
        element.style.whiteSpace = 'nowrap'; // Ensure text is on a single line
        element.style.width = 'auto';
        element.style.maxWidth = 'none';
        
        // Force-fix any link text if it contains dots (ellipsis)
        if (element.textContent.includes('...')) {
            // Try to get the full text from title attribute or data attribute
            const fullText = element.getAttribute('title') || 
                             element.getAttribute('data-full-text') || 
                             element.textContent.replace('...', '');
            
            if (fullText && fullText !== element.textContent) {
                element.textContent = fullText;
            }
        }
    });
    
    // Fix for specific menu items we know exist
    fixSpecificMenuItems();
}

// New function to remove all ellipsis
function removeAllEllipsis() {
    // Find all elements in the sidebar
    const allElements = document.querySelectorAll('#sidebar *, #mobile-sidebar *');
    
    allElements.forEach(element => {
        if (element.nodeType === Node.TEXT_NODE || typeof element.textContent === 'string') {
            // Replace any occurrence of ellipsis with empty string
            if (element.textContent) {
                element.textContent = element.textContent.replace(/\.\.\./g, '');
            }
        }
    });
}

function fixSpecificMenuItems() {
    // Known menu item texts to fix - without ellipsis
    const knownMenuItems = {
        'پروفایل کاربری': 'پروفایل کاربری',
        'مدیریت سیستم': 'مدیریت سیستم',
        'مدیریت کاربران': 'مدیریت کاربران',
        'راهنما': 'راهنما',
        'گزارش خطا': 'گزارش خطا'
    };
    
    // Find all span elements
    const spans = document.querySelectorAll('span');
    
    spans.forEach(span => {
        const text = span.textContent.trim();
        
        // Check if this text needs fixing - use direct matching without ellipsis
        for (const [key, full] of Object.entries(knownMenuItems)) {
            if (text.includes(key.substring(0, 4))) {
                span.textContent = full;
                break;
            }
        }
    });
}

function checkForEllipsis() {
    // Find any text containing ellipsis in the sidebar
    const elements = document.querySelectorAll('#sidebar *, #mobile-sidebar *');
    let foundEllipsis = false;
    
    elements.forEach(el => {
        if (el.textContent && el.textContent.includes('...')) {
            foundEllipsis = true;
            console.log('Found ellipsis in:', el);
            
            // Remove ellipsis
            el.textContent = el.textContent.replace(/\.\.\./g, '');
            
            // Try to fix this specific element
            el.style.textOverflow = 'clip';
            el.style.overflow = 'visible';
            el.style.whiteSpace = 'nowrap';
            el.style.width = 'auto';
        }
    });
    
    if (foundEllipsis) {
        // If we found ellipsis, apply more aggressive fixes
        applyAggressiveFixes();
    }
}

function applyAggressiveFixes() {
    // Apply style directly to the document
    const style = document.createElement('style');
    style.textContent = `
        #sidebar *, #mobile-sidebar * {
            text-overflow: clip !important;
            overflow: visible !important;
            white-space: nowrap !important;
            width: auto !important;
        }
        
        /* Specifically target span elements */
        #sidebar span, #mobile-sidebar span {
            display: inline !important;
            max-width: none !important;
        }
        
        /* Fix sidebar width */
        #sidebar, #mobile-sidebar {
            width: 260px !important; /* Increased from 240px to fit text better */
        }
        
        /* Fix sidebar menu links visibility */
        #sidebar a, #mobile-sidebar a,
        #sidebar button, #mobile-sidebar button {
            opacity: 1 !important;
            visibility: visible !important;
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }
    `;
    
    document.head.appendChild(style);
} 