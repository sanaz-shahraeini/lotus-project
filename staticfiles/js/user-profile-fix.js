document.addEventListener('DOMContentLoaded', function() {
    console.log("User profile fix script loaded.");

    // Function to handle showing/hiding required indicators
    function updateUserFormUI(mode) {
        // Always remove indicators first to prevent duplicates
        $('.required-indicator').remove();

        if (mode === 'add') {
            console.log("Setting up Add Mode UI.");
            const requiredIndicator = '<span class="required-indicator" style="color: red; font-weight: bold; font-size: 1.2rem; margin-left: 5px;">*</span>';

            // Add indicators to labels
            $('label[for="id_username"]').append(requiredIndicator);
            $('label[for="id_extension"]').append(requiredIndicator);
            $('#id_label_groupname').append(requiredIndicator);
            $('#accessToExtsLabel').append(requiredIndicator);
            $('#accessLevelLabel').append(requiredIndicator);
            
            // Set required attributes on inputs
            $('#id_username, #id_extension, #id_groupname').prop('required', true);
            
            // Show the notice
            $('#required-fields-notice').show();

        } else { // 'edit' mode
            console.log("Setting up Edit Mode UI.");
            // Remove required attributes
            $('form input, form select').prop('required', false);
            
            // Hide the notice
            $('#required-fields-notice').hide();
        }
    }

    // Attach listener to a stable parent element (#form) and delegate to #id_editOrAdd
    $('#form').on('change', '#id_editOrAdd', function () {
        const selectedMode = $(this).val().toLowerCase();
        updateUserFormUI(selectedMode);
    });

    // Initial check when the page loads
    // We need to make sure this runs after the interfering script has done its job
    setTimeout(function() {
        console.log("Performing initial UI setup.");
        const initialMode = $('#id_editOrAdd').val() ? $('#id_editOrAdd').val().toLowerCase() : 'edit';
        updateUserFormUI(initialMode);
    }, 500); // A small delay to ensure other scripts have finished

}); 

// User Profile Dropdown functionality with jQuery
$(document).ready(function() {
    console.log("User profile script loaded with jQuery");
    
    // Add styling for dropdown content
    $("<style>")
        .prop("type", "text/css")
        .html(`
            .dropdown-content {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                max-height: 200px;
                overflow-y: auto;
                width: 100%;
                z-index: 100;
            }
            
            .dropdown-item {
                padding: 8px 12px;
                border-bottom: 1px solid #eee;
            }
            
            .dropdown-item:hover {
                background-color: #f5f5f5;
            }
            
            .dropdown-item:last-child {
                border-bottom: none;
            }
        `)
        .appendTo("head");
    
    // Simplified dropdown functionality
    $("#accessLevelBtn").click(function(e) {
        e.preventDefault();
        $("#accessLevelDp").toggle();
    });
    
    $("#accessToExtsBtn").click(function(e) {
        e.preventDefault();
        $("#accessToExtsDp").toggle();
    });
    
    // Close dropdowns when clicking outside
    $(document).click(function(e) {
        if (!$(e.target).closest("#accessLevelBtn, #accessLevelDp").length) {
            $("#accessLevelDp").hide();
        }
        
        if (!$(e.target).closest("#accessToExtsBtn, #accessToExtsDp").length) {
            $("#accessToExtsDp").hide();
        }
    });
    
    // Handle dropdown item clicks
    $(".dropdown-item").click(function(e) {
        const checkbox = $(this).find('input[type="checkbox"]');
        if (checkbox.length && !$(e.target).is(checkbox) && !$(e.target).is('label')) {
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });
    
    // Select all permissions checkbox
    $("#allPerm").change(function() {
        const isChecked = $(this).prop('checked');
        $('#accessLevelDp input[type="checkbox"]:not(#allPerm)').prop('checked', isChecked);
    });
    
    // Update button text when checkboxes are changed
    function updateButtonText() {
        const levelCount = $('#accessLevelDp input[type="checkbox"]:checked:not(#allPerm)').length;
        const extCount = $('#accessToExtsDp input[type="checkbox"]:checked').length;
        
        if (levelCount > 0) {
            $("#accessLevelBtn span").text(`${levelCount} مورد انتخاب شده`);
        } else {
            $("#accessLevelBtn span").text("انتخاب سطح دسترسی");
        }
        
        if (extCount > 0) {
            $("#accessToExtsBtn span").text(`${extCount} مورد انتخاب شده`);
        } else {
            $("#accessToExtsBtn span").text("انتخاب دسترسی");
        }
    }
    
    // Listen for checkbox changes
    $('input[type="checkbox"]').change(updateButtonText);
}); 