# User Form Fields Fix - Username and Extension Editable in Add Mode

## Issue Description
When trying to add a new user, the username (نام کاربری) and extension (داخلی) fields were not editable, appearing as readonly or disabled fields.

## Root Cause
The issue was caused by JavaScript form mode handling that wasn't properly distinguishing between "Add" and "Edit" modes for certain form fields. The form validation and state management code wasn't explicitly ensuring these critical fields remained editable when creating new users.

## Solution Applied

### 1. JavaScript Enhancements (`static/js/user-profile-fix.js`)

#### Enhanced `updateUserFormUI()` Function
- Added explicit field state management for username and extension fields
- Ensures fields are editable in "add" mode and properly managed in "edit" mode
- Clears any readonly/disabled states and styling when in add mode

#### Updated Form Initialization
- Added multiple checks on page load to ensure proper field states
- Implemented `fixFieldStates()` function that runs at intervals to catch any state issues
- Enhanced the `clearForm()` function to explicitly reset field properties

#### Improved Mode Change Handling
- Modified the editOrAdd change handler to immediately fix field states
- Added immediate field enabling when switching to "add" mode
- Preserved file uploads during mode changes

### 2. CSS Improvements (`Alvand/templates/userprofile.html`)

#### Field State Styling
- Added CSS rules to ensure fields appear editable when not readonly
- Implemented proper styling for readonly states in edit mode
- Added dark mode support for readonly field styling

### 3. Key Changes Made

#### Field State Management
```javascript
// Ensure username and extension fields are editable in add mode
$('#id_username, #id_extension').prop('readonly', false).prop('disabled', false);
$('#id_username, #id_extension').css({
    'background-color': '',
    'cursor': '',
    'pointer-events': '',
    'opacity': ''
});
```

#### CSS Enhancements
```css
/* Ensure username and extension are always editable unless explicitly readonly */
#id_username:not([readonly]), #id_extension:not([readonly]) {
    background-color: var(--input-bg) !important;
    cursor: text !important;
    pointer-events: auto !important;
    opacity: 1 !important;
}
```

## Expected Behavior After Fix

1. **Add Mode**: Both username and extension fields are fully editable
2. **Edit Mode**: Username becomes readonly (for data integrity), extension remains editable
3. **None Mode**: All fields are editable
4. **Form Switching**: Fields maintain proper state when switching between modes

## Testing Steps

1. Navigate to the user management page
2. Set the "ویرایش/اضافه" dropdown to "اضافه" (Add)
3. Verify that both "نام کاربری" (username) and "داخلی" (extension) fields are editable
4. Switch to "ویرایش" (Edit) mode and enter a username
5. Verify that username becomes readonly but extension remains editable
6. Switch back to "اضافه" (Add) mode
7. Verify that both fields become editable again

## Files Modified

- `static/js/user-profile-fix.js` - Enhanced form state management
- `Alvand/templates/userprofile.html` - Added CSS styling fixes

## Notes

- The fix preserves existing functionality while ensuring proper field states
- All changes are backward compatible
- The solution handles edge cases like page reload and dynamic form updates
- Proper error handling and logging have been maintained