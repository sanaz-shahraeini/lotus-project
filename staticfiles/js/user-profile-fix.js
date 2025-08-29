document.addEventListener('DOMContentLoaded', function() {
    // Forward declaration of updateEditOrAddVisualState function
    let updateEditOrAddVisualState;
    
    // Photo Upload Functionality
    function initializePhotoUpload() {
        const uploadInput = document.getElementById('upload');
        const uploadZone = document.getElementById('photoUploadZone');
        const filePreview = document.getElementById('filePreview');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const removeFile = document.getElementById('removeFile');
        const userImage = document.getElementById('id_picurl');
        
        if (!uploadInput || !uploadZone) {
            return;
        }
        

        
        // File validation settings
        const maxFileSize = 5 * 1024 * 1024; // 5MB
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        
        // Format file size
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
        
        // Validate file
        function validateFile(file) {
            const errors = [];
            
            if (!allowedTypes.includes(file.type)) {
                errors.push('فرمت فایل مجاز نیست. لطفا JPG، PNG یا GIF انتخاب کنید.');
            }
            
            if (file.size > maxFileSize) {
                errors.push('حجم فایل نباید بیشتر از 5MB باشد.');
            }
            
            return errors;
        }
        
        // Show file preview
        function showFilePreview(file) {
            if (fileName) fileName.textContent = file.name;
            if (fileSize) fileSize.textContent = formatFileSize(file.size);
            if (filePreview) {
                filePreview.classList.add('show');
            }
            
            // Create preview image
            const reader = new FileReader();
            reader.onload = function(e) {
                if (userImage) {
                    userImage.src = e.target.result;
                }
            };
            reader.readAsDataURL(file);
        }
        
        // Hide file preview
        function hideFilePreview() {
            if (filePreview) {
                filePreview.classList.remove('show');
            }
            if (userImage) {
                userImage.src = '/static/pic/avatar.jpg';
            }
        }
        
        // Show error message
        function showError(message) {
            // Remove existing error messages
            document.querySelectorAll('.upload-error').forEach(el => el.remove());
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'upload-error';
            errorDiv.style.cssText = `
                background: rgba(220, 53, 69, 0.1);
                border: 1px solid rgba(220, 53, 69, 0.3);
                color: #dc3545;
                padding: 0.75rem;
                border-radius: 0.5rem;
                margin-top: 0.75rem;
                font-size: 0.875rem;
                text-align: center;
            `;
            errorDiv.innerHTML = `<i class="fa-solid fa-exclamation-triangle"></i> ${message}`;
            
            if (uploadZone) {
                uploadZone.appendChild(errorDiv);
                setTimeout(() => errorDiv.remove(), 5000);
            }
        }
        
        // Handle file selection
        function handleFileSelect(file) {
            const errors = validateFile(file);
            
            if (errors.length > 0) {
                showError(errors.join(' '));
                return;
            }
            
            showFilePreview(file);
        }
        
        // Enhanced file validation function
        function isValidFile(file) {
            return file && 
                   file instanceof File && 
                   file.name && 
                   file.name.trim() !== '' && 
                   file.size > 0;
        }
        
        // File input monitoring with mutation observer
        function setupFileInputMonitoring() {
            if (!uploadInput) return;
            
            // Monitor file input changes with MutationObserver
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'value') {
                        validateCurrentFiles();
                    }
                });
            });
            
            observer.observe(uploadInput, {
                attributes: true,
                attributeFilter: ['value']
            });
            
            // Periodic validation of files
            function validateCurrentFiles() {
                if (uploadInput.files.length > 0) {
                    const file = uploadInput.files[0];
                    if (!isValidFile(file)) {
                        uploadInput.value = '';
                        window.selectedUploadFile = null;
                        uploadInput._selectedFile = null;
                        hideFilePreview();
                    }
                }
            }
            
            // Run validation every 2 seconds
            setInterval(validateCurrentFiles, 2000);
        }
        
        // Initialize monitoring
        setupFileInputMonitoring();
        
        // Global file storage for reliable access
        window.selectedUploadFile = null;
        
        // Clean any existing empty files from input
        if (uploadInput && uploadInput.files.length > 0) {
            const existingFile = uploadInput.files[0];
            if (!isValidFile(existingFile)) {
                uploadInput.value = '';
            }
        }
        
        // Function to clean FormData of invalid files
        function cleanFormData(formData) {
            const uploadPhotoFile = formData.get('uploadPhoto');
            if (uploadPhotoFile && uploadPhotoFile instanceof File) {
                if (!isValidFile(uploadPhotoFile)) {
                    formData.delete('uploadPhoto');
                    return false; // No valid file
                }
            }
            return true; // Valid file or no file
        }
        
        // Monitor FormData creation and clean it
        const originalFormData = window.FormData;
        if (originalFormData) {
            window.FormData = function(form) {
                const formData = new originalFormData(form);
                
                // Only clean FormData for our specific form
                if (form && form.id === 'form') {
                    cleanFormData(formData);
                }
                
                return formData;
            };
            
            // Copy static methods if any
            Object.setPrototypeOf(window.FormData.prototype, originalFormData.prototype);
            Object.setPrototypeOf(window.FormData, originalFormData);
        }
        
        // File input change event with direct file storage
        uploadInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                
                if (isValidFile(file)) {
                    // Store file globally for reliable access
                    window.selectedUploadFile = file;
                    uploadInput._selectedFile = file;
                    
                    handleFileSelect(file);
                } else {
                    e.target.value = '';
                    window.selectedUploadFile = null;
                    uploadInput._selectedFile = null;
                    hideFilePreview();
                }
            } else {
                window.selectedUploadFile = null;
                uploadInput._selectedFile = null;
                hideFilePreview();
            }
        });
        
        // Remove file functionality with complete cleanup
        if (removeFile) {
            removeFile.addEventListener('click', function() {
                uploadInput.value = '';
                uploadInput._selectedFile = null;
                window.selectedUploadFile = null;
                hideFilePreview();
            });
        }
        
        // Drag and drop functionality
        let dragCounter = 0;
        
        uploadZone.addEventListener('dragenter', function(e) {
            e.preventDefault();
            dragCounter++;
            uploadZone.classList.add('drag-over');
        });
        
        uploadZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            dragCounter--;
            if (dragCounter === 0) {
                uploadZone.classList.remove('drag-over');
            }
        });
        
        uploadZone.addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        
        uploadZone.addEventListener('drop', function(e) {
            e.preventDefault();
            dragCounter = 0;
            uploadZone.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                
                if (isValidFile(file)) {
                    // Store file globally and in input
                    window.selectedUploadFile = file;
                    uploadInput._selectedFile = file;
                    
                    // Create a new DataTransfer object to properly set files
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    uploadInput.files = dt.files;
                    
                    handleFileSelect(file);
                } else {
                    showError('فایل نامعتبر است. لطفا یک فایل معتبر انتخاب کنید.');
                }
            }
        });
        
        // Click to upload
        uploadZone.addEventListener('click', function(e) {
            if (!e.target.closest('.upload-button') && !e.target.closest('.file-preview')) {
                uploadInput.click();
            }
        });
        
        // Add hover effects
        const overlay = document.querySelector('.photo-upload-overlay');
        const container = document.querySelector('.profile-image-container');
        
        if (overlay && container) {
            overlay.addEventListener('click', function() {
                uploadInput.click();
            });
        }
        
        // Image load handling
        if (userImage) {
            userImage.addEventListener('load', function() {
                this.classList.add('loaded');
                this.classList.remove('loading');
            });
            
            userImage.addEventListener('error', function() {
                this.src = '/static/pic/avatar.jpg';
                this.classList.remove('loading');
            });
        }
        
        // Form submission interceptor with file validation
        const form = document.getElementById('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                const fileInput = document.getElementById('upload');
                
                // Get all possible file sources and validate them
                let validFile = null;
                
                // Check input files first
                if (fileInput && fileInput.files.length > 0) {
                    const inputFile = fileInput.files[0];
                    if (isValidFile(inputFile)) {
                        validFile = inputFile;
                    }
                }
                
                // Check global file if no valid input file
                if (!validFile && window.selectedUploadFile) {
                    if (isValidFile(window.selectedUploadFile)) {
                        validFile = window.selectedUploadFile;
                    } else {
                        window.selectedUploadFile = null;
                    }
                }
                
                // Check backup file if no valid file found yet
                if (!validFile && fileInput && fileInput._selectedFile) {
                    if (isValidFile(fileInput._selectedFile)) {
                        validFile = fileInput._selectedFile;
                    } else {
                        fileInput._selectedFile = null;
                    }
                }
                
                // If we have a valid file, handle upload
                if (validFile) {
                    // Prevent default submission
                    e.preventDefault();
                    
                    // Validate file before submission
                    const errors = validateFile(validFile);
                    if (errors.length > 0) {
                        showError(errors.join(' '));
                        return false;
                    }
                    
                    // Create FormData manually
                    const formData = new FormData(form);
                    
                    // Remove any existing invalid files from FormData
                    formData.delete('uploadPhoto');
                    
                    // Add our valid file
                    formData.set('uploadPhoto', validFile);
                    
                    // CRITICAL: Add the saveUser field to trigger backend processing
                    formData.set('saveUser', 'save');
                    
                    // Final validation of FormData
                    const finalFile = formData.get('uploadPhoto');
                    if (!finalFile || !isValidFile(finalFile)) {
                        showError('خطا در بارگذاری فایل. لطفا دوباره تلاش کنید.');
                        return false;
                    }
                    
                    // Show loading state
                    const submitButtons = form.querySelectorAll('button[type="submit"]');
                    submitButtons.forEach(btn => {
                        btn.disabled = true;
                        btn.classList.add('upload-loading');
                    });
                    
                    // Submit form manually with fetch
                    fetch(form.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                        }
                    }).then(response => {
                        // Reload the page to show results
                        window.location.reload();
                    }).catch(error => {
                        // Re-enable buttons on error
                        submitButtons.forEach(btn => {
                            btn.disabled = false;
                            btn.classList.remove('upload-loading');
                        });
                        alert('خطا در ارسال فرم');
                    });
                    
                    return false;
                } else {
                    // Clean up any invalid files in the form data to prevent empty file submissions
                    if (fileInput && fileInput.files.length > 0) {
                        const inputFile = fileInput.files[0];
                        if (!isValidFile(inputFile)) {
                            fileInput.value = '';
                        }
                    }
                    
                    // Allow normal form submission
                    return true;
                }
            });
        }
        
        // Keyboard accessibility
        uploadZone.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                uploadInput.click();
            }
        });
        
        // Make upload zone focusable
        uploadZone.setAttribute('tabindex', '0');
        uploadZone.setAttribute('role', 'button');
        uploadZone.setAttribute('aria-label', 'انتخاب عکس پروفایل');
    }
    
    // Initialize photo upload functionality
    setTimeout(initializePhotoUpload, 500);
    
    // Wait a bit for all elements to load
    setTimeout(function() {
        
        // Fix null editOrAdd value immediately
        if ($('#id_editOrAdd').length > 0) {
            const currentValue = $('#id_editOrAdd').val();
            
            // Ensure the field has a proper name attribute
            if (!$('#id_editOrAdd').attr('name')) {
                $('#id_editOrAdd').attr('name', 'editOrAdd');
            }
            
            if (currentValue === null || currentValue === undefined || currentValue === '') {
                $('#id_editOrAdd').val('none').trigger('change');
            }
            
            // Force visual update of dropdown
            const mode = $('#id_editOrAdd').val();
            updateEditOrAddVisualState(mode);
            
            // Add event listener for manual changes
            $('#id_editOrAdd').on('change', function() {
                const newMode = $(this).val();
                updateEditOrAddVisualState(newMode);
            });
        }
        
    }, 2000);

    // Function to handle showing/hiding required indicators
    function updateUserFormUI(mode) {
        // Always remove indicators first to prevent duplicates
        $('.required-indicator').remove();
        
        // Update visual appearance of editOrAdd dropdown
        updateEditOrAddVisualState(mode);

        if (mode === 'add') {
            const requiredIndicator = '<span class="required-indicator" style="color: red; font-weight: bold; font-size: 1.2rem; margin-left: 5px;">*</span>';

            // Add indicators to labels
            $('label[for="id_username"]').append(requiredIndicator);
            $('label[for="id_extension"]').append(requiredIndicator);
            $('#id_label_groupname').append(requiredIndicator);
            $('#accessToExtsLabel').append(requiredIndicator);
            $('#accessLevelLabel').append(requiredIndicator);
            
            // Set required attributes on inputs
            $('#id_username, #id_extension, #id_groupname').prop('required', true);
            
            // Ensure username and extension fields are editable in add mode
            $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
            $('#id_username, #id_extension').css({
                'background-color': '',
                'cursor': '',
                'pointer-events': '',
                'opacity': ''
            });
            
            // Show the notice
            $('#required-fields-notice').show();

        } else { // 'edit' mode or other
            // Remove required attributes
            $('form input, form select').prop('required', false);
            
            // In edit mode, username should be readonly but extension can be editable
            if (mode === 'edit') {
                $('#id_username').prop('readonly', true).css({
                    'background-color': '#f8f9fa',
                    'cursor': 'not-allowed'
                });
                $('#id_extension').prop('readonly', false).prop('disabled', false);
            } else {
                // For 'none' mode, ensure fields are editable
                $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
                $('#id_username, #id_extension').css({
                    'background-color': '',
                    'cursor': '',
                    'pointer-events': '',
                    'opacity': ''
                });
            }
            
            // Hide the notice
            $('#required-fields-notice').hide();
        }
    }
    
    // Function to update visual state of editOrAdd dropdown
    updateEditOrAddVisualState = function(mode) {
        const $editOrAdd = $('#id_editOrAdd');
        
        if (!$editOrAdd.length) {
            return;
        }
        
        // Normalize mode value - handle null/undefined
        const normalizedMode = mode ? mode.toString().toLowerCase() : 'none';
        
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
                break;
            case 'add':
                $editOrAdd.addClass('add-mode');
                $editOrAdd.css({
                    'border-color': '#007bff',
                    'color': '#007bff',
                    'font-weight': 'bold',
                    'background-color': '#f8f9ff'
                });
                break;
            default: // 'none' or any other value
                $editOrAdd.addClass('none-mode');
                $editOrAdd.css({
                    'border-color': '#6c757d',
                    'color': '#6c757d',
                    'font-weight': 'normal',
                    'background-color': '#ffffff'
                });
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
        updateUserFormUI(selectedMode);
    });

    // Initial check when the page loads
    setTimeout(function() {
        const editOrAddValue = $('#id_editOrAdd').val();
        const initialMode = editOrAddValue ? editOrAddValue.toLowerCase() : 'none';
        updateUserFormUI(initialMode);
        
        // Force ensure username and extension are editable if not in edit mode
        if (initialMode !== 'edit') {
            $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
            $('#id_username, #id_extension').css({
                'background-color': '',
                'cursor': '',
                'pointer-events': '',
                'opacity': ''
            });
        }
    }, 500); // A small delay to ensure other scripts have finished

    // Function to load user data for editing
    function loadUserData(username) {
        if (!username || username.trim() === '') {
            clearForm();
            return;
        }
        
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
                if (response.success) {
                    populateForm(response.user_data);
                    $('#id_username').css('border', '2px solid #28a745'); // Green border for success
                    
                    // Remove success border after 2 seconds
                    setTimeout(function() {
                        $('#id_username').css('border', '');
                    }, 2000);
                } else {
                    $('#id_username').css('border', '2px solid #dc3545'); // Red border for error
                    alert('کاربر یافت نشد: ' + response.error);
                    clearForm();
                }
            },
            error: function(xhr, status, error) {
                $('#id_username').css('border', '2px solid #dc3545'); // Red border for error
                alert('خطا در بارگذاری اطلاعات کاربر');
                clearForm();
            }
        });
    }

    // Function to populate form with user data
    function populateForm(userData) {
        // Preserve any currently selected file during form population
        const uploadInput = document.getElementById('upload');
        const preservedFile = uploadInput && uploadInput._selectedFile;
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
        
        // Update profile image with loading state
        const userImage = document.getElementById('id_picurl');
        if (userImage && userData.picurl && userData.picurl !== 'avatar.png') {
            userImage.classList.add('loading');
            userImage.src = '/static/upload/' + userData.picurl;
        } else if (userImage) {
            userImage.classList.add('loading');
            userImage.src = '/static/pic/avatar.jpg';
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
        
        // Restore preserved file if it exists
        if (preservedFile && uploadInput) {
            try {
                const dt = new DataTransfer();
                dt.items.add(preservedFile);
                uploadInput.files = dt.files;
                uploadInput._selectedFile = preservedFile;
            } catch (error) {
                // Silent fail for file restoration
            }
        }
    }

    // Function to clear form
    function clearForm() {
        // Store current editOrAdd value to preserve it
        const currentMode = $('#id_editOrAdd').val();
        
        // Clear all input fields except editOrAdd
        $('#form input[type="text"], #form input[type="email"], #form input[type="number"], #form textarea').val('');
        $('#form select:not(#id_editOrAdd)').val('');
        $('#form input[type="checkbox"]').prop('checked', false);
        
        // Explicitly clear readonly and disabled states on key fields
        $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
        $('#id_username, #id_extension').css({
            'background-color': '',
            'cursor': '',
            'pointer-events': '',
            'opacity': ''
        });
        
        // Restore editOrAdd value and update visual state
        if (currentMode) {
            $('#id_editOrAdd').val(currentMode);
            updateEditOrAddVisualState(currentMode);
        }
        
        // Reset profile image with loading state
        const userImage = document.getElementById('id_picurl');
        if (userImage) {
            userImage.classList.add('loading');
            userImage.src = '/static/pic/avatar.jpg';
        }
        
        // Reset file preview
        const filePreview = document.getElementById('filePreview');
        if (filePreview) {
            filePreview.classList.remove('show');
        }
        
        // Only clear file input if not in edit mode or if explicitly requested
        const uploadInput = document.getElementById('upload');
        if (uploadInput && currentMode !== 'edit') {
            uploadInput.value = '';
            uploadInput._selectedFile = null;
            window.selectedUploadFile = null;
        }
        
        // Remove any error messages
        document.querySelectorAll('.upload-error').forEach(el => el.remove());
        
        // Reset upload zone state
        const uploadZone = document.getElementById('photoUploadZone');
        if (uploadZone) {
            uploadZone.classList.remove('drag-over', 'active', 'error');
        }
        $('#profileNameDisplay').text('انتخاب کاربر');
        $('#profileUsernameDisplay').text('نام کاربری');
    }

    // Listen for username changes in edit mode
    // Function to check if elements exist
    function checkElements() {
        const editOrAddExists = $('#id_editOrAdd').length > 0;
        const usernameExists = $('#id_username').length > 0;
        return editOrAddExists && usernameExists;
    }
    
    // Wait for elements to be ready and then setup listeners
    function setupUsernameListeners() {
        if (!checkElements()) {
            setTimeout(setupUsernameListeners, 100);
            return;
        }
        
        // Direct event listener on username field - only for edit mode
        $(document).on('change blur', '#id_username', function() {
            const mode = $('#id_editOrAdd').val();
            const username = $(this).val();
            
            // Only trigger user loading in edit mode
            if (mode === 'edit' && username && username.trim() !== '') {
                // Debounce the loading to avoid too many requests
                clearTimeout(window.userLoadTimeout);
                window.userLoadTimeout = setTimeout(function() {
                    loadUserData(username);
                }, 500);
            }
            // Removed the clearForm() call for add mode to prevent form clearing on keystroke
        });

        // Listen for mode changes
        $(document).on('change', '#id_editOrAdd', function() {
            const mode = $(this).val();
            const username = $('#id_username').val();
            
            // Preserve file selection during mode changes
            const uploadInput = document.getElementById('upload');
            const preservedFile = uploadInput && uploadInput._selectedFile;
            
            // Only clear form when switching between modes, not when already in add mode
            if (mode === 'add') {
                // Only clear if we have data from edit mode
                if (username && username.trim() !== '') {
                    const shouldClear = confirm('Switching to add mode will clear the current form. Continue?');
                    if (shouldClear) {
                        clearForm();
                    } else {
                        return; // Don't change mode
                    }
                }
                
                // Ensure fields are editable
                $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
                $('#id_username, #id_extension').css({
                    'background-color': '',
                    'cursor': 'text',
                    'pointer-events': 'auto',
                    'opacity': '1'
                });
                
                // Restore file if we're switching to add mode and had a file
                if (preservedFile) {
                    try {
                        const dt = new DataTransfer();
                        dt.items.add(preservedFile);
                        uploadInput.files = dt.files;
                        uploadInput._selectedFile = preservedFile;
                        // Re-show the file preview
                        const filePreview = document.getElementById('filePreview');
                        const fileName = document.getElementById('fileName');
                        const fileSize = document.getElementById('fileSize');
                        if (filePreview && fileName && fileSize) {
                            fileName.textContent = preservedFile.name;
                            fileSize.textContent = formatFileSize(preservedFile.size);
                            filePreview.classList.add('show');
                        }
                    } catch (error) {
                        // Silent fail for file restoration
                    }
                }
            } else if (mode === 'edit' && username && username.trim() !== '') {
                loadUserData(username);
            } else if (mode === 'none') {
                // Clear form when going to none mode
                clearForm();
            }
            
            // Update UI based on new mode
            updateUserFormUI(mode);
        });
    }
    
    // Call setup function after a delay to ensure DOM is ready
    setTimeout(setupUsernameListeners, 1000);
    
    // Add a function to explicitly fix field states
    function fixFieldStates() {
        const mode = $('#id_editOrAdd').val();
        
        if (mode === 'add' || mode === 'none' || !mode) {
            // Ensure username and extension are editable
            $('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
            $('#id_username, #id_extension').css({
                'background-color': '',
                'cursor': '',
                'pointer-events': '',
                'opacity': ''
            });
        } else if (mode === 'edit') {
            // In edit mode, username should be readonly but extension can be editable
            $('#id_username').prop('readonly', true).css({
                'background-color': '#f8f9fa',
                'cursor': 'not-allowed'
            });
            $('#id_extension').prop('readonly', false).prop('disabled', false);
        }
    }
    
    // Run field state fix on page load and periodically
    setTimeout(fixFieldStates, 500);
    setTimeout(fixFieldStates, 1500);
    setTimeout(fixFieldStates, 3000);

    // Basic form validation
    $('#form').on('submit', function(e) {
        const modeValue = $('#id_editOrAdd').val();
        const mode = modeValue ? modeValue.toLowerCase() : 'none';
        
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
        
        // Always return true to allow form submission if validation passes
        return true;
    });

// User Profile Dropdown functionality with jQuery
$(document).ready(function() {
    
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
}); })