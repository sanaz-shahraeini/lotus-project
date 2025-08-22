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
    setTimeout(function() {
        console.log("Performing initial UI setup.");
        const initialMode = $('#id_editOrAdd').val() ? $('#id_editOrAdd').val().toLowerCase() : 'edit';
        updateUserFormUI(initialMode);
    }, 500); // A small delay to ensure other scripts have finished

    // Basic form validation
    $('#form').on('submit', function(e) {
        console.log("Form submitted");
        
        const mode = $('#id_editOrAdd').val().toLowerCase();
        
        // Only validate required fields in add mode
        if (mode === 'add') {
            let hasErrors = false;
            let errorMessages = [];
            
            // 1. Validate username
            const username = $('#id_username').val();
            if (!username || username.trim() === '') {
                $('#id_username').css('border', '2px solid red');
                hasErrors = true;
                errorMessages.push('نام کاربری');
            } else {
                $('#id_username').css('border', '');
            }
            
            // 2. Validate extension
            const extension = $('#id_extension').val();
            if (!extension || extension.trim() === '') {
                $('#id_extension').css('border', '2px solid red');
                hasErrors = true;
                errorMessages.push('داخلی');
            } else {
                $('#id_extension').css('border', '');
            }
            
            // 3. Validate role/groupname
            const role = $('#id_groupname').val();
            if (!role || role === 'none') {
                $('#id_groupname').css('border', '2px solid red');
                hasErrors = true;
                errorMessages.push('نقش');
            } else {
                $('#id_groupname').css('border', '');
            }
            
            // 4. Validate access to extensions
            const extCount = $('#accessToExtsDp input[type="checkbox"]:checked').length;
            if (extCount === 0) {
                $('#accessToExtsBtn').css('border', '2px solid red');
                hasErrors = true;
                errorMessages.push('دسترسی به داخلی');
            } else {
                $('#accessToExtsBtn').css('border', '');
            }
            
            // 5. Validate access level permissions
            const permCount = $('#accessLevelDp input[type="checkbox"]:checked').length;
            if (permCount === 0) {
                $('#accessLevelBtn').css('border', '2px solid red');
                hasErrors = true;
                errorMessages.push('سطح دسترسی');
            } else {
                $('#accessLevelBtn').css('border', '');
            }
            
            // Show error message if validation fails
            if (hasErrors) {
                e.preventDefault();
                alert('لطفا فیلدهای اجباری را پر کنید: ' + errorMessages.join('، '));
                return false;
            }
        }
        
        // Log form data for debugging
        var formData = new FormData(this);
        console.log("Form submission data:");
        for (var pair of formData.entries()) {
            console.log(pair[0] + ": " + pair[1]);
        }
        
        // Always return true to allow form submission if validation passes
        return true;
    });

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
    
    // Handle select user button for password reset requests
    $('.select-user-btn').click(function() {
        const username = $(this).data('username');
        
        // Set the form to edit mode
        $('#id_editOrAdd').val('edit');
        $('#id_editOrAdd').trigger('change');
        
        // Fill in the username field
        $('#id_username').val(username);
        
        // Trigger the username change to load user data
        $('#id_username').trigger('change');
        
        // Scroll to the username field
        $('html, body').animate({
            scrollTop: $('#id_username').offset().top - 100
        }, 500);
        
        // Highlight the fields
        $('#id_username').css('border', '2px solid #00BCD4');
        
        // After a delay, automatically trigger password reset
        setTimeout(function() {
            $('#id_username').css('border', '');
            
            // Get the button for password reset
            const resetButton = $('button[name="ChangePassword"]');
            
            // Add visual feedback
            resetButton.css('background-color', '#00BCD4');
            resetButton.css('transform', 'scale(1.05)');
            
            // Trigger the password reset
            resetButton.trigger('click');
            
            // Show success message
            $('<div class="alert alert-success" style="margin-top: 15px;">')
                .html('<strong>موفق:</strong> رمز عبور کاربر ' + username + ' با موفقیت به 12345678 بازنشانی شد.')
                .insertBefore($('.password-reset-requests'));
        }, 1000);
    });

    // Handle view user details button for password reset requests
    $('.view-user-details-btn').click(function() {
        const username = $(this).data('username');
        const name = $(this).data('name');
        const lastname = $(this).data('lastname');
        const extension = $(this).data('extension');
        const email = $(this).data('email');
        const created = $(this).data('created');
        const groupname = $(this).data('groupname');
        
        // Create HTML structure for modal with avatar
        const modalHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                <div class="user-avatar" style="width: 80px; height: 80px; border-radius: 50%; overflow: hidden; border: 3px solid #00BCD4; margin-bottom: 15px;">
                    <img src="static/pic/avatar.jpg" alt="User Avatar" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 5px;">${name} ${lastname}</div>
                <div style="padding: 3px 10px; border-radius: 20px; background: #e3f2fd; color: #0d47a1; font-size: 0.85rem; margin-bottom: 15px;">${groupname}</div>
            </div>
            
            <div class="user-info-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                <div class="info-item">
                    <div style="font-weight: 600; margin-bottom: 5px; color: #666;">شماره داخلی:</div>
                    <div style="padding: 8px; background: #f5f5f5; border-radius: 4px;">${extension}</div>
                </div>
                <div class="info-item">
                    <div style="font-weight: 600; margin-bottom: 5px; color: #666;">ایمیل:</div>
                    <div style="padding: 8px; background: #f5f5f5; border-radius: 4px;">${email}</div>
                </div>
                <div class="info-item" style="grid-column: span 2;">
                    <div style="font-weight: 600; margin-bottom: 5px; color: #666;">تاریخ درخواست بازنشانی:</div>
                    <div style="padding: 8px; background: #f5f5f5; border-radius: 4px;">${created}</div>
                </div>
            </div>
            
            <div class="info-alert" style="padding: 10px 15px; background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; border-radius: 4px; margin-bottom: 15px;">
                <i class="fa-solid fa-triangle-exclamation"></i> 
                <strong>توجه:</strong> با کلیک روی دکمه «بازنشانی رمز عبور»، رمز عبور کاربر به «12345678» تغییر خواهد کرد.
            </div>
        `;
        
        // Populate modal with user data
        $('#modal-username').text(username);
        $('#modal-body').html(modalHTML);
        
        // Store username in the reset button for later use
        $('#reset-password-modal').data('username', username);
        
        // Show the modal
        $('#user-details-modal').fadeIn(300);
        $('#user-details-modal').removeClass('hidden');
    });
    
    // Close modal when clicking the close button
    $('#close-modal, #cancel-view-details').click(function() {
        $('#user-details-modal').fadeOut(300);
        setTimeout(function() {
            $('#user-details-modal').addClass('hidden');
        }, 300);
    });
    
    // Handle password reset from modal
    $('#reset-password-modal').click(function() {
        const username = $(this).data('username');
        
        // Close the modal
        $('#user-details-modal').fadeOut(300);
        setTimeout(function() {
            $('#user-details-modal').addClass('hidden');
        
            // Set the form to edit mode
            $('#id_editOrAdd').val('edit');
            $('#id_editOrAdd').trigger('change');
            
            // Fill in the username field
            $('#id_username').val(username);
            
            // Trigger the username change to load user data
            $('#id_username').trigger('change');
            
            // After a delay, automatically trigger password reset
            setTimeout(function() {
                // Get the button for password reset
                const resetButton = $('button[name="ChangePassword"]');
                
                // Add visual feedback
                resetButton.css('background-color', '#00BCD4');
                resetButton.css('transform', 'scale(1.05)');
                
                // Trigger the password reset
                resetButton.trigger('click');
            }, 1000);
        }, 300);
    });
    
    // Close modal when clicking outside of it
    $(window).click(function(e) {
        if ($(e.target).is('#user-details-modal')) {
            $('#user-details-modal').fadeOut(300);
            setTimeout(function() {
                $('#user-details-modal').addClass('hidden');
            }, 300);
        }
    });
}); 