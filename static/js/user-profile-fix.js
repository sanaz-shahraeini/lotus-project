document.addEventListener('DOMContentLoaded', function() {
    // Forward declaration of updateEditOrAddVisualState function
    let updateEditOrAddVisualState;
    
    // Enhanced Photo Upload Functionality
    function initializePhotoUpload() {
        const uploadInput = document.getElementById('upload');
        const uploadZone = document.getElementById('photoUploadZone');
        const filePreview = document.getElementById('filePreview');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const removeFile = document.getElementById('removeFile');
        const userImage = document.getElementById('id_picurl');
        
        console.log('Initializing photo upload...');
        console.log('Upload input found:', !!uploadInput);
        console.log('Upload zone found:', !!uploadZone);
        console.log('Form element:', document.getElementById('form'));
        
        if (!uploadInput) {
            console.error('Upload input not found!');
            return;
        }
        
        if (!uploadZone) {
            console.error('Upload zone not found!');
            return;
        }
        
        // Verify form association
        console.log('Upload input name:', uploadInput.name);
        console.log('Upload input form:', uploadInput.form);
        console.log('Upload input parent form:', uploadInput.closest('form'));
        
        // Add test function for file selection with global storage check
        window.testFileSelection = function() {
            const fileInput = document.getElementById('upload');
            console.log('=== ENHANCED FILE SELECTION TEST ===');
            console.log('File input element:', fileInput);
            console.log('File input name:', fileInput ? fileInput.name : 'N/A');
            console.log('File input form:', fileInput ? fileInput.form : 'N/A');
            console.log('Files in input:', fileInput ? fileInput.files.length : 'N/A');
            console.log('Global file available:', !!window.selectedUploadFile);
            console.log('Backup file available:', fileInput ? !!fileInput._selectedFile : 'N/A');
            
            // Check all possible file sources
            const inputFile = fileInput && fileInput.files.length > 0 ? fileInput.files[0] : null;
            const globalFile = window.selectedUploadFile;
            const backupFile = fileInput ? fileInput._selectedFile : null;
            
            console.log('File sources:');
            if (inputFile) {
                console.log('  Input file:', { name: inputFile.name, size: inputFile.size });
            }
            if (globalFile) {
                console.log('  Global file:', { name: globalFile.name, size: globalFile.size });
            }
            if (backupFile) {
                console.log('  Backup file:', { name: backupFile.name, size: backupFile.size });
            }
            
            // Test FormData creation
            const form = document.getElementById('form');
            if (form) {
                const formData = new FormData(form);
                const formFile = formData.get('uploadPhoto');
                console.log('Form file:', formFile);
                
                if (globalFile) {
                    console.log('Testing manual file injection...');
                    formData.set('uploadPhoto', globalFile);
                    const injectedFile = formData.get('uploadPhoto');
                    console.log('Injected file:', {
                        name: injectedFile.name,
                        size: injectedFile.size,
                        type: injectedFile.type
                    });
                }
            }
            
            console.log('=== END ENHANCED TEST ===');
        };
        
        // Manual file upload trigger for testing
        window.triggerFileUpload = function() {
            const fileInput = document.getElementById('upload');
            if (fileInput) {
                fileInput.click();
            } else {
                console.error('File input not found');
            }
        };
        
        // Call test function after initialization
        setTimeout(() => {
            console.log('Auto-running enhanced file selection test...');
            window.testFileSelection();
        }, 2000);
        
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
        
        // Enhanced file input monitoring with mutation observer
        function setupFileInputMonitoring() {
            if (!uploadInput) return;
            
            // Monitor file input changes with MutationObserver
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'value') {
                        console.log('File input value changed via attribute');
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
                        console.log('Invalid file detected during monitoring, clearing:', {
                            name: file.name,
                            size: file.size
                        });
                        uploadInput.value = '';
                        window.selectedUploadFile = null;
                        uploadInput._selectedFile = null;
                        hideFilePreview();
                    }
                }
            }
            
            // Run validation every 2 seconds
            setInterval(validateCurrentFiles, 2000);
            
            console.log('File input monitoring setup complete');
        }
        
        // Initialize monitoring
        setupFileInputMonitoring();
        
        // Global file storage for reliable access
        window.selectedUploadFile = null;
        
        // Clean any existing empty files from input
        if (uploadInput && uploadInput.files.length > 0) {
            const existingFile = uploadInput.files[0];
            if (!isValidFile(existingFile)) {
                console.log('Found invalid/empty file in input, clearing it');
                uploadInput.value = '';
            }
        }
        
        // Function to clean FormData of invalid files
        function cleanFormData(formData) {
            const uploadPhotoFile = formData.get('uploadPhoto');
            if (uploadPhotoFile && uploadPhotoFile instanceof File) {
                if (!isValidFile(uploadPhotoFile)) {
                    console.log('Removing invalid file from FormData:', {
                        name: uploadPhotoFile.name,
                        size: uploadPhotoFile.size
                    });
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
            console.log('File input change event triggered');
            console.log('Event target:', e.target);
            console.log('Files selected:', e.target.files.length);
            
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                console.log('File details:', {
                    name: file.name,
                    size: file.size,
                    type: file.type,
                    valid: isValidFile(file)
                });
                
                if (isValidFile(file)) {
                    console.log('Valid file selected, processing...');
                    
                    // Store file globally for reliable access
                    window.selectedUploadFile = file;
                    uploadInput._selectedFile = file;
                    
                    console.log('File stored globally and in input backup');
                    handleFileSelect(file);
                    
                    // Verify file is still accessible
                    setTimeout(() => {
                        console.log('File accessibility check:');
                        console.log('  Input files:', e.target.files.length);
                        console.log('  Input file valid:', e.target.files.length > 0 ? isValidFile(e.target.files[0]) : false);
                        console.log('  Global file:', !!window.selectedUploadFile);
                        console.log('  Backup file:', !!uploadInput._selectedFile);
                    }, 100);
                } else {
                    console.log('Invalid file detected (empty or corrupted), clearing selection');
                    e.target.value = '';
                    window.selectedUploadFile = null;
                    uploadInput._selectedFile = null;
                    hideFilePreview();
                }
            } else {
                console.log('No file selected');
                window.selectedUploadFile = null;
                uploadInput._selectedFile = null;
                hideFilePreview();
            }
        });
        
        // Remove file functionality with complete cleanup
        if (removeFile) {
            removeFile.addEventListener('click', function() {
                console.log('Remove file clicked');
                uploadInput.value = '';
                uploadInput._selectedFile = null;
                window.selectedUploadFile = null;
                hideFilePreview();
                console.log('File removed and all references cleared');
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
                console.log('File dropped:', file.name, 'Size:', file.size);
                
                if (isValidFile(file)) {
                    console.log('Valid file dropped, processing...');
                    
                    // Store file globally and in input
                    window.selectedUploadFile = file;
                    uploadInput._selectedFile = file;
                    
                    // Create a new DataTransfer object to properly set files
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    uploadInput.files = dt.files;
                    
                    console.log('File set to input via drag and drop');
                    handleFileSelect(file);
                    
                    // Verify the file is properly set
                    setTimeout(() => {
                        console.log('Drag drop file verification:');
                        console.log('  Input files:', uploadInput.files.length);
                        console.log('  Input file valid:', uploadInput.files.length > 0 ? isValidFile(uploadInput.files[0]) : false);
                        console.log('  Global file:', !!window.selectedUploadFile);
                    }, 100);
                } else {
                    console.log('Invalid file dropped, ignoring');
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
        
        // Form submission interceptor with enhanced file validation
        const form = document.getElementById('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                console.log('=== FORM SUBMISSION INTERCEPTED ===');
                
                const fileInput = document.getElementById('upload');
                
                // Get all possible file sources and validate them
                let validFile = null;
                
                // Check input files first
                if (fileInput && fileInput.files.length > 0) {
                    const inputFile = fileInput.files[0];
                    if (isValidFile(inputFile)) {
                        validFile = inputFile;
                        console.log('Valid file found in input:', { name: inputFile.name, size: inputFile.size });
                    } else {
                        console.log('Invalid file in input, ignoring:', { name: inputFile.name, size: inputFile.size });
                    }
                }
                
                // Check global file if no valid input file
                if (!validFile && window.selectedUploadFile) {
                    if (isValidFile(window.selectedUploadFile)) {
                        validFile = window.selectedUploadFile;
                        console.log('Valid file found in global storage:', { name: validFile.name, size: validFile.size });
                    } else {
                        console.log('Invalid file in global storage, ignoring');
                        window.selectedUploadFile = null;
                    }
                }
                
                // Check backup file if no valid file found yet
                if (!validFile && fileInput && fileInput._selectedFile) {
                    if (isValidFile(fileInput._selectedFile)) {
                        validFile = fileInput._selectedFile;
                        console.log('Valid file found in backup storage:', { name: validFile.name, size: validFile.size });
                    } else {
                        console.log('Invalid file in backup storage, ignoring');
                        fileInput._selectedFile = null;
                    }
                }
                
                console.log('File validation summary:');
                console.log('  Input files count:', fileInput ? fileInput.files.length : 0);
                console.log('  Global file available:', !!window.selectedUploadFile);
                console.log('  Backup file available:', fileInput ? !!fileInput._selectedFile : false);
                console.log('  Valid file selected:', !!validFile);
                
                // If we have a valid file, handle upload
                if (validFile) {
                    // Prevent default submission
                    e.preventDefault();
                    
                    console.log('Processing file upload for:', {
                        name: validFile.name,
                        size: validFile.size,
                        type: validFile.type
                    });
                    
                    // Validate file before submission
                    const errors = validateFile(validFile);
                    if (errors.length > 0) {
                        console.error('File validation errors:', errors);
                        showError(errors.join(' '));
                        return false;
                    }
                    
                    // Create FormData manually
                    const formData = new FormData(form);
                    
                    // Remove any existing invalid files from FormData
                    formData.delete('uploadPhoto');
                    
                    // Add our valid file
                    formData.set('uploadPhoto', validFile);
                    
                    // Final validation of FormData
                    const finalFile = formData.get('uploadPhoto');
                    if (!finalFile || !isValidFile(finalFile)) {
                        console.error('Final validation failed - invalid file in FormData');
                        showError('خطا در بارگذاری فایل. لطفا دوباره تلاش کنید.');
                        return false;
                    }
                    
                    console.log('FormData created with validated file:');
                    for (let [key, value] of formData.entries()) {
                        if (value instanceof File) {
                            console.log(`  ${key}: File(${value.name}, ${value.size} bytes, ${value.type})`);
                        } else {
                            console.log(`  ${key}:`, value);
                        }
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
                        console.log('Form submitted successfully');
                        // Reload the page to show results
                        window.location.reload();
                    }).catch(error => {
                        console.error('Form submission error:', error);
                        // Re-enable buttons on error
                        submitButtons.forEach(btn => {
                            btn.disabled = false;
                            btn.classList.remove('upload-loading');
                        });
                        alert('خطا در ارسال فرم');
                    });
                    
                    return false;
                } else {
                    console.log('No valid file to upload, proceeding with normal submission');
                    
                    // Clean up any invalid files in the form data to prevent empty file submissions
                    if (fileInput && fileInput.files.length > 0) {
                        const inputFile = fileInput.files[0];
                        if (!isValidFile(inputFile)) {
                            console.log('Clearing invalid file from input before submission');
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
            
            // Show the notice
            $('#required-fields-notice').show();

        } else { // 'edit' mode or other
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
        console.log('populateForm called with:', userData);
        
        // Preserve any currently selected file during form population
        const uploadInput = document.getElementById('upload');
        const preservedFile = uploadInput && uploadInput._selectedFile;
        
        if (preservedFile) {
            console.log('Preserving selected file during form population:', preservedFile.name);
        }
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
            console.log('Restoring preserved file after form population');
            try {
                const dt = new DataTransfer();
                dt.items.add(preservedFile);
                uploadInput.files = dt.files;
                uploadInput._selectedFile = preservedFile;
                console.log('File restored successfully');
            } catch (error) {
                console.error('Failed to restore preserved file:', error);
            }
        }
        
        console.log('Form population completed');
    }

    // Function to clear form
    function clearForm() {
        console.log('clearForm called');
        
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
            console.log('Clearing file input (not in edit mode)');
            uploadInput.value = '';
            uploadInput._selectedFile = null;
            window.selectedUploadFile = null;
        } else {
            console.log('Preserving file input (in edit mode)');
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
        
        console.log('Form cleared, mode preserved:', currentMode);
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
        
        // Direct event listener on username field
        $(document).on('change keyup input blur', '#id_username', function() {
            const mode = $('#id_editOrAdd').val();
            const username = $(this).val();
            
            if (mode === 'edit' && username && username.trim() !== '') {
                // Debounce the loading to avoid too many requests
                clearTimeout(window.userLoadTimeout);
                window.userLoadTimeout = setTimeout(function() {
                    loadUserData(username);
                }, 500);
            } else if (mode === 'add') {
                // In add mode, just clear the form when username changes
                clearForm();
            }
        });

        // Listen for mode changes
        $(document).on('change', '#id_editOrAdd', function() {
            const mode = $(this).val();
            const username = $('#id_username').val();
            
            console.log('Mode changed to:', mode, 'for username:', username);
            
            // Preserve file selection during mode changes
            const uploadInput = document.getElementById('upload');
            const preservedFile = uploadInput && uploadInput._selectedFile;
            
            if (mode === 'edit' && username && username.trim() !== '') {
                loadUserData(username);
            } else {
                clearForm();
                
                // Restore file if we're switching to add mode and had a file
                if (mode === 'add' && preservedFile) {
                    console.log('Restoring file after mode change to add');
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
                        console.log('File and preview restored after mode change');
                    } catch (error) {
                        console.error('Failed to restore file after mode change:', error);
                    }
                }
            }
        });
    }
    
    // Call setup function after a delay to ensure DOM is ready
    setTimeout(setupUsernameListeners, 1000);

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