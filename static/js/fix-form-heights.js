// Fix form element heights to be consistent
document.addEventListener('DOMContentLoaded', function() {
    // Get reference height from تعداد خطوط شهری field
    let referenceField = document.querySelector('input[name="urbanlines"]');
    let referenceHeight = '38px'; // Default height if reference not found
    
    if (referenceField) {
        // Get computed style to find actual height
        const computedStyle = window.getComputedStyle(referenceField);
        referenceHeight = computedStyle.height || '38px';
        console.log('Reference height:', referenceHeight);
    }
    
    // Apply the height to all select elements
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach(select => {
        select.style.height = referenceHeight;
        select.style.lineHeight = referenceHeight;
        
        // Force the parent element if it's controlling the height
        if (select.parentElement) {
            const parentComputed = window.getComputedStyle(select.parentElement);
            if (parentComputed.position === 'relative' || 
                parentComputed.position === 'absolute') {
                select.parentElement.style.height = referenceHeight;
            }
        }
    });
    
    // Special handling for styled/custom dropdowns
    const customDropdowns = document.querySelectorAll('.dropdown-toggle, .custom-select, .form-select');
    customDropdowns.forEach(dropdown => {
        dropdown.style.height = referenceHeight;
        dropdown.style.lineHeight = referenceHeight;
    });
    
    // Monitor for dynamically added elements
    observeDynamicElements();
});

// Use a MutationObserver to catch dynamically added form elements
function observeDynamicElements() {
    const targetNode = document.body;
    const config = { childList: true, subtree: true };
    
    const callback = function(mutationsList, observer) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    // Check if the added node is an element
                    if (node.nodeType === 1) {
                        // Apply styles to new select elements
                        if (node.tagName === 'SELECT') {
                            node.style.height = '38px';
                            node.style.lineHeight = '38px';
                        }
                        
                        // Check for select elements within the added node
                        const selects = node.querySelectorAll('select');
                        selects.forEach(select => {
                            select.style.height = '38px';
                            select.style.lineHeight = '38px';
                        });
                    }
                });
            }
        }
    };
    
    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
} 