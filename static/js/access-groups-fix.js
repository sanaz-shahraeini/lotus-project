// Access Groups Section Enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Create dropdown backdrop if it doesn't exist
    if (!document.querySelector('.dropdown-backdrop')) {
        const backdrop = document.createElement('div');
        backdrop.className = 'dropdown-backdrop';
        document.body.appendChild(backdrop);
    }
    
    const dropdownBackdrop = document.querySelector('.dropdown-backdrop');
    // Fix dropdown functionality
    const dropdownToggle = document.querySelector('#dropdownCheckboxButton2');
    const dropdownMenu = document.querySelector('#dropdownDefaultCheckbox2');
    
    if (dropdownToggle && dropdownMenu) {
        // Add arrow icon if missing
        if (!dropdownToggle.querySelector('i')) {
            const arrowIcon = document.createElement('i');
            arrowIcon.className = 'fa-regular fa-chevron-down';
            dropdownToggle.appendChild(arrowIcon);
        }
        
        // Update dropdown text based on selected items
        function updateDropdownText() {
            const checkedBoxes = dropdownMenu.querySelectorAll('input[type="checkbox"]:checked');
            if (checkedBoxes.length > 0) {
                dropdownToggle.innerHTML = `${checkedBoxes.length} داخلی انتخاب شده <i class="fa-regular fa-chevron-down"></i>`;
            } else {
                dropdownToggle.innerHTML = `انتخاب داخلی <i class="fa-regular fa-chevron-down"></i>`;
            }
        }
        
        // Initialize dropdown text
        updateDropdownText();
        
        // Toggle dropdown on button click
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Close all other open dropdowns first
            document.querySelectorAll('.dropdown-menu:not(.hidden)').forEach(menu => {
                if (menu !== dropdownMenu) {
                    menu.classList.add('hidden');
                }
            });
            
            // Toggle dropdown visibility
            const isHidden = dropdownMenu.classList.toggle('hidden');
            
            // Toggle arrow direction
            const arrow = this.querySelector('i');
            if (arrow) {
                if (isHidden) {
                    arrow.className = 'fa-regular fa-chevron-down';
                    dropdownBackdrop.classList.remove('show');
                } else {
                    arrow.className = 'fa-regular fa-chevron-up';
                    dropdownBackdrop.classList.add('show');
                }
            }
            
            // Position dropdown properly
            if (!isHidden) {
                const toggleRect = this.getBoundingClientRect();
                dropdownMenu.style.width = `${toggleRect.width}px`;
                dropdownMenu.style.top = `${toggleRect.bottom + window.scrollY}px`;
                dropdownMenu.style.left = `${toggleRect.left}px`;
                
                // Ensure dropdown is visible
                dropdownMenu.style.display = 'block';
                dropdownMenu.style.opacity = '1';
                dropdownMenu.style.visibility = 'visible';
                dropdownMenu.style.pointerEvents = 'auto';
                
                // Add click handler to backdrop
                dropdownBackdrop.onclick = function() {
                    dropdownMenu.classList.add('hidden');
                    dropdownBackdrop.classList.remove('show');
                    if (arrow) {
                        arrow.className = 'fa-regular fa-chevron-down';
                    }
                };
            }
        });
        
        // Handle checkbox clicks
        const checkboxes = dropdownMenu.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function(e) {
                e.stopPropagation();
                updateDropdownText();
            });
        });
        
        // Prevent dropdown from closing when clicking inside
        dropdownMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('#dropdownCheckboxButton2') && !e.target.closest('#dropdownDefaultCheckbox2') && !e.target.closest('.dropdown-backdrop')) {
                dropdownMenu.classList.add('hidden');
                dropdownBackdrop.classList.remove('show');
                
                // Reset arrow direction
                const arrow = dropdownToggle.querySelector('i');
                if (arrow) {
                    arrow.className = 'fa-regular fa-chevron-down';
                }
            }
        });
    }
    
    // Enhance radio buttons for better UX
    const radioButtons = document.querySelectorAll('input[type="radio"][name="operation"]');
    
    // Initialize with first radio button selected if none are checked
    let hasCheckedRadio = false;
    radioButtons.forEach(radio => {
        if (radio.checked) {
            hasCheckedRadio = true;
        }
    });
    
    if (!hasCheckedRadio && radioButtons.length > 0) {
        radioButtons[0].checked = true;
        
        // Trigger the change event for the first radio button
        const event = new Event('change');
        radioButtons[0].dispatchEvent(event);
    }
    
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Uncheck other radio buttons in the group
            if (this.checked) {
                radioButtons.forEach(otherRadio => {
                    if (otherRadio !== this && otherRadio.name !== this.name) {
                        otherRadio.checked = false;
                    }
                });
                
                // Handle specific actions based on selected radio
                if (this.id === 'add') {
                    // Convert label select to text input for adding new group
                    const labelSelect = document.querySelector('#id_label');
                    if (labelSelect && labelSelect.tagName.toLowerCase() === 'select') {
                        const labelContainer = labelSelect.parentElement;
                        const newInput = document.createElement('input');
                        newInput.type = 'text';
                        newInput.id = 'id_label';
                        newInput.name = 'label';
                        newInput.className = labelSelect.className;
                        newInput.placeholder = 'نام گروه جدید';
                        labelContainer.replaceChild(newInput, labelSelect);
                    }
                } else {
                    // Ensure label is a select element for edit/delete operations
                    const labelInput = document.querySelector('#id_label');
                    if (labelInput && labelInput.tagName.toLowerCase() === 'input') {
                        updateLabelSelectOptions();
                    }
                }
                
                // Update visual state for all radio items
                updateRadioButtonsVisualState();
            }
        });
    });
    
    // Function to update visual state of radio buttons
    function updateRadioButtonsVisualState() {
        radioButtons.forEach(radio => {
            const radioItem = radio.closest('.radio-item');
            if (radioItem) {
                if (radio.checked) {
                    radioItem.setAttribute('aria-checked', 'true');
                    radioItem.classList.add('active');
                } else {
                    radioItem.setAttribute('aria-checked', 'false');
                    radioItem.classList.remove('active');
                }
            }
        });
    }
    
    // Initialize visual state
    updateRadioButtonsVisualState();
    
    // Add touch-friendly interaction for mobile
    const radioItems = document.querySelectorAll('.radio-item');
    radioItems.forEach(item => {
        item.addEventListener('click', function(e) {
            const radio = this.querySelector('input[type="radio"]');
            if (radio && !radio.checked) {
                radio.checked = true;
                
                // Trigger the change event
                const event = new Event('change');
                radio.dispatchEvent(event);
            }
        });
    });
    
    // Function to update label select options based on available groups
    function updateLabelSelectOptions() {
        // Get groupname data from JSON script
        const groupnameScript = document.getElementById('groupname_json');
        if (!groupnameScript) return;
        
        try {
            const groupnameData = JSON.parse(groupnameScript.textContent);
            const labelInput = document.querySelector('#id_label');
            
            if (labelInput && labelInput.tagName.toLowerCase() === 'input') {
                const labelContainer = labelInput.parentElement;
                const selectElement = document.createElement('select');
                selectElement.id = 'id_label';
                selectElement.name = 'label';
                selectElement.className = labelInput.className;
                
                // Add default option
                let optionsHtml = '<option value="none"> ------ </option>';
                
                // Add options from groupname data
                if (groupnameData && Array.isArray(groupnameData)) {
                    groupnameData.forEach(function(ext) {
                        if (ext.label) {
                            optionsHtml += `<option value="${ext.label}"> ${ext.label} </option>`;
                        }
                    });
                }
                
                selectElement.innerHTML = optionsHtml;
                labelContainer.replaceChild(selectElement, labelInput);
                
                // Add change event to the new select
                selectElement.addEventListener('change', handleLabelChange);
            }
        } catch (error) {
            console.error('Error parsing groupname data:', error);
        }
    }
    
    // Handle label change to update extensions
    function handleLabelChange() {
        const selectedLabel = this.value.toLowerCase();
        if (selectedLabel === 'none') {
            // Clear all checkboxes
            document.querySelectorAll('#dropdownDefaultCheckbox2 input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            return;
        }
        
        // Get groupname data from JSON script
        const groupnameScript = document.getElementById('groupname_json');
        if (!groupnameScript) return;
        
        try {
            const groupnameData = JSON.parse(groupnameScript.textContent);
            
            // Find the selected group
            const selectedGroup = groupnameData.find(group => 
                group.label && group.label.toLowerCase() === selectedLabel
            );
            
            if (selectedGroup && selectedGroup.exts_from_groups) {
                const exts = selectedGroup.exts_from_groups.map(String);
                
                // Update checkboxes
                document.querySelectorAll('#dropdownDefaultCheckbox2 input[type="checkbox"]').forEach(checkbox => {
                    checkbox.checked = exts.includes(checkbox.value);
                });
            }
        } catch (error) {
            console.error('Error updating extensions:', error);
        }
    }
    
    // Add change event to existing label select
    const labelSelect = document.querySelector('#id_label');
    if (labelSelect && labelSelect.tagName.toLowerCase() === 'select') {
        labelSelect.addEventListener('change', handleLabelChange);
    }
    
    // Fix toggle switch for better visibility
    const toggleSwitch = document.querySelector('.toggle-switch');
    if (toggleSwitch) {
        const toggleLabel = toggleSwitch.closest('.form-group');
        if (toggleLabel) {
            toggleLabel.style.display = 'flex';
            toggleLabel.style.justifyContent = 'space-between';
            toggleLabel.style.alignItems = 'center';
        }
    }
    
    // Fix form element heights to be consistent
    const formElements = document.querySelectorAll('select, input[type="text"], .dropdown-toggle');
    formElements.forEach(element => {
        element.style.height = '38px';
    });
}); 