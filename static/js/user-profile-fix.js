document.addEventListener('DOMContentLoaded', function() {
    console.log("User profile fix script loaded.");
    console.log('DOM Elements Check:');
    console.log('- jQuery loaded:', typeof $ !== 'undefined');
    console.log('- Document ready state:', document.readyState);
    
    // Forward declaration of updateEditOrAddVisualState function
    let updateEditOrAddVisualState;
    
    // Wait a bit for all elements to load
    setTimeout(function() {
        console.log('=== DELAYED ELEMENT CHECK ===');
        console.log('editOrAdd element:', $('#id_editOrAdd').length, $('#id_editOrAdd')[0]);
        console.log('username element:', $('#id_username').length, $('#id_username')[0]);
        console.log('form element:', $('#form').length, $('#form')[0]);
        
        // Fix null editOrAdd value immediately
        if ($('#id_editOrAdd').length > 0) {
            const currentValue = $('#id_editOrAdd').val();
            console.log('Current editOrAdd value:', currentValue);
            
            // Ensure the field has a proper name attribute
            if (!$('#id_editOrAdd').attr('name')) {
                console.log('Adding name attribute to editOrAdd field');
                $('#id_editOrAdd').attr('name', 'editOrAdd');
            }
            
            if (currentValue === null || currentValue === undefined || currentValue === '') {
                console.log('Setting default value for editOrAdd field...');
                $('#id_editOrAdd').val('none').trigger('change');
                console.log('Value after setting default:', $('#id_editOrAdd').val());
            }
            
            // Force visual update of dropdown
            const mode = $('#id_editOrAdd').val();
            console.log('Forcing visual update for mode:', mode);
            updateEditOrAddVisualState(mode);
            
            // Add event listener for manual changes
            $('#id_editOrAdd').on('change', function() {
                const newMode = $(this).val();
                console.log('editOrAdd manually changed to:', newMode);
                updateEditOrAddVisualState(newMode);
            });
        }
        
        // Add test function
        window.testEditOrAdd = function() {
            console.log('=== TESTING EDITORADD FIELD ===');
            
            // Check field state
            window.debugFormState();
            
            // Test setting different values
            console.log('Testing value changes...');
            $('#id_editOrAdd').val('edit');
            console.log('After setting to edit:', $('#id_editOrAdd').val());
            
            $('#id_editOrAdd').val('add');
            console.log('After setting to add:', $('#id_editOrAdd').val());
            
            $('#id_editOrAdd').val('none');
            console.log('After setting to none:', $('#id_editOrAdd').val());
            
            // Test form data
            const formData = new FormData($('#form')[0]);
            console.log('Form data with editOrAdd:');
            for (let pair of formData.entries()) {
                if (pair[0].includes('edit') || pair[0].includes('Edit')) {
                    console.log(`  ${pair[0]}: ${pair[1]}`);
                }
            }
            
            console.log('===========================');
        };
        console.log('=============================');
    }, 2000);

    // Function to handle showing/hiding required indicators
    function updateUserFormUI(mode) {
        // Always remove indicators first to prevent duplicates
        $('.required-indicator').remove();
        
        // Update visual appearance of editOrAdd dropdown
        updateEditOrAddVisualState(mode);

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
    
    // Function to update visual state of editOrAdd dropdown
    updateEditOrAddVisualState = function(mode) {
        const $editOrAdd = $('#id_editOrAdd');
        
        if (!$editOrAdd.length) {
            console.log('editOrAdd field not found, skipping visual update');
            return;
        }
        
        // Normalize mode value - handle null/undefined
        const normalizedMode = mode ? mode.toString().toLowerCase() : 'none';
        console.log('Updating visual state for mode:', normalizedMode);
        
        // Reset styles
        $editOrAdd.removeClass('edit-mode add-mode none-mode');
        
        // Apply mode-specific styling
        switch(normalizedMode) {
            case 'edit':
                $editOrAdd.addClass('edit-mode');
                $editOrAdd.css({
                    'border-color': '#28a745',
                    'color': '#28a745',
                    'font-weight': 'bold',
                    'background-color': '#f8fff9'
                });
                console.log('Dropdown styled for EDIT mode');
                break;
            case 'add':
                $editOrAdd.addClass('add-mode');
                $editOrAdd.css({
                    'border-color': '#007bff',
                    'color': '#007bff',
                    'font-weight': 'bold',
                    'background-color': '#f8f9ff'
                });
                console.log('Dropdown styled for ADD mode');
                break;
            default: // 'none' or any other value
                $editOrAdd.addClass('none-mode');
                $editOrAdd.css({
                    'border-color': '#6c757d',
                    'color': '#6c757d',
                    'font-weight': 'normal',
                    'background-color': '#ffffff'
                });
                console.log('Dropdown styled for NONE mode');
                break;
        }
        
        // Force a repaint to ensure visual changes are applied
        if ($editOrAdd[0]) {
            $editOrAdd[0].offsetHeight;
        }
    };

    // Attach listener to a stable parent element (#form) and delegate to #id_editOrAdd
    $('#form').on('change', '#id_editOrAdd', function () {
        const selectedValue = $(this).val();
        const selectedMode = selectedValue ? selectedValue.toLowerCase() : 'none';
        console.log('editOrAdd changed - Raw value:', selectedValue, 'Normalized mode:', selectedMode);
        updateUserFormUI(selectedMode);
    });

    // Initial check when the page loads
    setTimeout(function() {
        console.log("Performing initial UI setup.");
        const editOrAddValue = $('#id_editOrAdd').val();
        const initialMode = editOrAddValue ? editOrAddValue.toLowerCase() : 'none';
        console.log('Initial setup - Raw value:', editOrAddValue, 'Normalized mode:', initialMode);
        updateUserFormUI(initialMode);
    }, 500); // A small delay to ensure other scripts have finished

    // Function to load user data for editing
    function loadUserData(username) {
        if (!username || username.trim() === '') {
            console.log('No username provided, clearing form');
            clearForm();
            return;
        }

        console.log('Loading user data for:', username);
        
        // Show loading indicator
        $('#id_username').css('border', '2px solid #00BCD4');
        
        // Make AJAX request to fetch user data
        $.ajax({
            url: '/get-user-data/',
            method: 'GET',
            data: { username: username },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                console.log('User data loaded successfully:', response);
                
                if (response.success) {
                    populateForm(response.user_data);
                    $('#id_username').css('border', '2px solid #28a745'); // Green border for success
                    
                    // Remove success border after 2 seconds
                    setTimeout(function() {
                        $('#id_username').css('border', '');
                    }, 2000);
                } else {
                    console.error('Failed to load user data:', response.error);
                    $('#id_username').css('border', '2px solid #dc3545'); // Red border for error
                    alert('کاربر یافت نشد: ' + response.error);
                    clearForm();
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', error);
                $('#id_username').css('border', '2px solid #dc3545'); // Red border for error
                alert('خطا در بارگذاری اطلاعات کاربر');
                clearForm();
            }
        });
    }

    // Function to populate form with user data
    function populateForm(userData) {
        console.log('Populating form with user data:', userData);
        
        // Basic user info
        $('#id_name').val(userData.name || '');
        $('#id_lastname').val(userData.lastname || '');
        $('#id_extension').val(userData.extension || '');
        $('#id_email').val(userData.email || '');
        $('#id_groupname').val(userData.groupname || 'none');
        $('#id_active').prop('checked', userData.active);
        
        // Contact info
        $('#id_nationalcode').val(userData.nationalcode || '');
        $('#id_birthdate').val(userData.birthdate || '');
        $('#id_telephone').val(userData.telephone || '');
        $('#id_phonenumber').val(userData.phonenumber || '');
        $('#id_gender').val(userData.gender || '');
        $('#id_maritalstatus').val(userData.maritalstatus || '');
        $('#id_military').val(userData.military || '');
        $('#id_educationfield').val(userData.educationfield || '');
        $('#id_educationdegree').val(userData.educationdegree || '');
        $('#id_province').val(userData.province || '');
        $('#id_city').val(userData.city || '');
        $('#id_accountnumbershaba').val(userData.accountnumbershaba || '');
        $('#id_cardnumber').val(userData.cardnumber || '');
        $('#id_accountnumber').val(userData.accountnumber || '');
        $('#id_address').val(userData.address || '');
        
        // Update profile image
        if (userData.picurl && userData.picurl !== 'avatar.png') {
            $('#id_picurl').attr('src', '/static/upload/' + userData.picurl);
        } else {
            $('#id_picurl').attr('src', '/static/pic/avatar.jpg');
        }
        
        // Update profile name display
        const fullName = (userData.name || '') + ' ' + (userData.lastname || '');
        $('#profileNameDisplay').text(fullName.trim() || 'انتخاب کاربر');
        $('#profileUsernameDisplay').text(userData.username || 'نام کاربری');
        
        // Handle user extensions
        $('#accessToExtsDp input[type="checkbox"]').prop('checked', false);
        if (userData.usersextension && Array.isArray(userData.usersextension)) {
            userData.usersextension.forEach(function(ext) {
                $(`#accessToExtsDp input[value="${ext}"]`).prop('checked', true);
            });
        }
        
        // Handle permissions
        $('#accessLevelDp input[type="checkbox"]').prop('checked', false);
        if (userData.can_view) $('#id_can_view').prop('checked', true);
        if (userData.can_write) $('#id_can_write').prop('checked', true);
        if (userData.can_modify) $('#id_can_modify').prop('checked', true);
        if (userData.can_delete) $('#id_can_delete').prop('checked', true);
        
        console.log('Form populated successfully');
    }

    // Function to clear form
    function clearForm() {
        console.log('Clearing form');
        
        // Store current editOrAdd value to preserve it
        const currentMode = $('#id_editOrAdd').val();
        
        // Clear all input fields except editOrAdd
        $('#form input[type="text"], #form input[type="email"], #form input[type="number"], #form textarea').val('');
        $('#form select:not(#id_editOrAdd)').val('');
        $('#form input[type="checkbox"]').prop('checked', false);
        
        // Restore editOrAdd value and update visual state
        if (currentMode) {
            $('#id_editOrAdd').val(currentMode);
            updateEditOrAddVisualState(currentMode);
        }
        
        // Reset profile image
        $('#id_picurl').attr('src', '/static/pic/avatar.jpg');
        $('#profileNameDisplay').text('انتخاب کاربر');
        $('#profileUsernameDisplay').text('نام کاربری');
        
        console.log('Form cleared successfully, editOrAdd mode preserved:', currentMode);
    }

    // Listen for username changes in edit mode
    console.log('Setting up username change listeners...');
    
    // Function to check if elements exist
    function checkElements() {
        const editOrAddExists = $('#id_editOrAdd').length > 0;
        const usernameExists = $('#id_username').length > 0;
        console.log('Element check - editOrAdd exists:', editOrAddExists, 'username exists:', usernameExists);
        return editOrAddExists && usernameExists;
    }
    
    // Wait for elements to be ready and then setup listeners
    function setupUsernameListeners() {
        if (!checkElements()) {
            console.log('Elements not ready, retrying in 100ms...');
            setTimeout(setupUsernameListeners, 100);
            return;
        }
        
        console.log('Elements ready, setting up listeners...');
        
        // Direct event listener on username field
        $(document).on('change keyup input blur', '#id_username', function() {
            const mode = $('#id_editOrAdd').val();
            const username = $(this).val();
            
            console.log('Username field event triggered:', {
                event: 'username_change',
                username: username,
                mode: mode,
                timestamp: new Date().toISOString()
            });
            
            if (mode === 'edit' && username && username.trim() !== '') {
                console.log('Will load user data for:', username);
                // Debounce the loading to avoid too many requests
                clearTimeout(window.userLoadTimeout);
                window.userLoadTimeout = setTimeout(function() {
                    loadUserData(username);
                }, 500);
            } else if (mode === 'add') {
                // In add mode, just clear the form when username changes
                console.log('In add mode, clearing form');
                clearForm();
            }
        });

        // Listen for mode changes
        $(document).on('change', '#id_editOrAdd', function() {
            const mode = $(this).val();
            const username = $('#id_username').val();
            
            console.log('Mode change event triggered:', {
                event: 'mode_change',
                mode: mode,
                username: username,
                timestamp: new Date().toISOString()
            });
            
            if (mode === 'edit' && username && username.trim() !== '') {
                console.log('Mode changed to edit, loading user data for:', username);
                loadUserData(username);
            } else {
                console.log('Mode changed, clearing form');
                clearForm();
            }
        });
        
        console.log('Username change listeners set up successfully');
    }
    
    // SIMPLIFIED APPROACH: Direct setup after DOM is ready
    function setupEditFunctionality() {
        console.log('=== SETTING UP EDIT FUNCTIONALITY ===');
        
        // Verify elements exist
        if ($('#id_editOrAdd').length === 0) {
            console.error('editOrAdd field not found!');
            return;
        }
        
        if ($('#id_username').length === 0) {
            console.error('username field not found!');
            return;
        }
        
        console.log('Elements found successfully');
        
        // Simple, direct event binding
        $('#id_username').on('input change keyup blur', function() {
            const mode = $('#id_editOrAdd').val();
            const username = $(this).val();
            
            console.log('USERNAME EVENT - Mode:', mode, 'Username:', username);
            
            if (mode === 'edit' && username && username.trim() !== '') {
                console.log('Triggering user data load...');
                loadUserData(username);
            }
        });
        
        $('#id_editOrAdd').on('change', function() {
            const mode = $(this).val();
            const username = $('#id_username').val();
            
            console.log('MODE CHANGE EVENT - Mode:', mode, 'Username:', username);
            
            if (mode === 'edit' && username && username.trim() !== '') {
                console.log('Mode changed to edit, loading user data...');
                loadUserData(username);
            } else {
                console.log('Clearing form due to mode change');
                clearForm();
            }
        });
        
        console.log('Event listeners attached successfully');
    }
    
    // Call setup function after a delay to ensure DOM is ready
    setTimeout(setupEditFunctionality, 1000);
    
    // Test function to verify AJAX is working
    window.testUserLoad = function(username) {
        console.log('Testing user load for:', username || 'yek_nafar');
        loadUserData(username || 'yek_nafar');
    };
    
    // Test dropdown visual changes
    window.testDropdownVisuals = function() {
        console.log('=== TESTING DROPDOWN VISUAL CHANGES ===');
        
        // Test each mode with delay to see visual changes
        setTimeout(() => {
            console.log('Setting to NONE mode...');
            $('#id_editOrAdd').val('none').trigger('change');
        }, 1000);
        
        setTimeout(() => {
            console.log('Setting to EDIT mode...');
            $('#id_editOrAdd').val('edit').trigger('change');
        }, 3000);
        
        setTimeout(() => {
            console.log('Setting to ADD mode...');
            $('#id_editOrAdd').val('add').trigger('change');
        }, 5000);
        
        setTimeout(() => {
            console.log('Back to NONE mode...');
            $('#id_editOrAdd').val('none').trigger('change');
        }, 7000);
        
        console.log('Visual test started. Watch the dropdown change colors and styles.');
    };
    
    // Enhanced debugging function
    window.debugFormState = function() {
        console.log('=== FORM DEBUG STATE ===');
        console.log('editOrAdd field exists:', $('#id_editOrAdd').length > 0);
        console.log('editOrAdd value:', $('#id_editOrAdd').val());
        console.log('editOrAdd HTML:', $('#id_editOrAdd')[0] ? $('#id_editOrAdd')[0].outerHTML : 'Element not found');
        console.log('username field exists:', $('#id_username').length > 0);
        console.log('username value:', $('#id_username').val());
        
        // Check if the field has options
        if ($('#id_editOrAdd').length > 0) {
            console.log('editOrAdd options:');
            $('#id_editOrAdd option').each(function(index) {
                console.log(`  ${index}: value="${$(this).val()}" text="${$(this).text()}" selected=${$(this).prop('selected')}`);
            });
            
            // Check form attributes
            console.log('editOrAdd field name attribute:', $('#id_editOrAdd').attr('name'));
            console.log('editOrAdd field id attribute:', $('#id_editOrAdd').attr('id'));
            console.log('editOrAdd field form attribute:', $('#id_editOrAdd').attr('form'));
            console.log('editOrAdd field disabled:', $('#id_editOrAdd').prop('disabled'));
        }
        
        // Check if field is inside form
        console.log('editOrAdd field is inside form:', $('#form #id_editOrAdd').length > 0);
        
        // Test form data creation
        if ($('#form').length > 0) {
            const formData = new FormData($('#form')[0]);
            console.log('Current form data entries:');
            for (let pair of formData.entries()) {
                console.log(`  ${pair[0]}: ${pair[1]}`);
            }
        }
        console.log('========================');
    };
    
    // Auto-test if in edit mode and username exists
    setTimeout(function() {
        console.log('=== AUTO DEBUG CHECK ===');
        window.debugFormState();
        const mode = $('#id_editOrAdd').val();
        const username = $('#id_username').val();
        console.log('Auto-test check - Mode:', mode, 'Username:', username);
        
        // Try to set a default value if the field is null
        if (mode === null || mode === undefined || mode === '') {
            console.log('Field value is null/empty, trying to set default value...');
            $('#id_editOrAdd').val('none');
            const newMode = $('#id_editOrAdd').val();
            console.log('After setting default, mode is now:', newMode);
        }
        
        if (mode === 'edit' && username && username.trim() !== '') {
            console.log('Auto-testing user load...');
            loadUserData(username);
        }
    }, 1500);

    // Basic form validation
    $('#form').on('submit', function(e) {
        console.log("Form submitted");
        
        const modeValue = $('#id_editOrAdd').val();
        const mode = modeValue ? modeValue.toLowerCase() : 'none';
        console.log('Form submission - Raw mode value:', modeValue, 'Normalized mode:', mode);
        
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