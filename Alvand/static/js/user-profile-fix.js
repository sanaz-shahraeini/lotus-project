// User Profile Image Upload and Preview Handler
$(document).ready(function() {
    const uploadInput = document.getElementById('upload');
    const profileImage = document.getElementById('id_picurl');
    const uploadZone = document.getElementById('photoUploadZone');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFileBtn = document.getElementById('removeFile');
    
    // Handle file selection
    if (uploadInput) {
        uploadInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                handleFileUpload(file);
            }
        });
    }
    
    // Handle drag and drop
    if (uploadZone) {
        uploadZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.add('drag-over');
        });
        
        uploadZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.remove('drag-over');
        });
        
        uploadZone.addEventListener('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.remove('drag-over');
            
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                uploadInput.files = e.dataTransfer.files;
                handleFileUpload(file);
            }
        });
    }
    
    // Handle file upload
    function handleFileUpload(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            alert('لطفا یک فایل تصویری معتبر انتخاب کنید (JPG, PNG, GIF, WEBP)');
            return;
        }
        
        // Validate file size (5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (file.size > maxSize) {
            alert('حجم فایل نباید بیشتر از 5 مگابایت باشد');
            return;
        }
        
        // Read and display the image
        const reader = new FileReader();
        reader.onload = function(e) {
            // Update the profile image
            profileImage.src = e.target.result;
            profileImage.classList.remove('placeholder');
            
            // Ensure the image fills the container properly
            profileImage.style.objectFit = 'cover';
            profileImage.style.objectPosition = 'center';
            profileImage.style.width = '100%';
            profileImage.style.height = '100%';
            profileImage.style.display = 'block';
            profileImage.style.borderRadius = '50%';
            
            // Show file preview info
            if (fileName) fileName.textContent = file.name;
            if (fileSize) fileSize.textContent = formatFileSize(file.size);
            if (filePreview) filePreview.classList.add('show');
        };
        reader.readAsDataURL(file);
    }
    
    // Remove file handler
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Clear the file input
            uploadInput.value = '';
            
            // Reset the profile image to placeholder
            profileImage.src = '';
            profileImage.classList.add('placeholder');
            
            // Hide file preview
            filePreview.classList.remove('show');
        });
    }
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 بایت';
        const k = 1024;
        const sizes = ['بایت', 'کیلوبایت', 'مگابایت'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
});
