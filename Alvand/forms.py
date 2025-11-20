from django import forms
from .models import *
from django.template.defaultfilters import truncatewords

class userProfileForm(forms.ModelForm):
    EDIT_OR_ADD = (
        ('none', "------"),
        ("edit", "ویرایش"),
        ("add", "اضافه"),
    )

    def __init__(self, *args, **kwargs):
        super(userProfileForm, self).__init__(*args, **kwargs)
        
        # Set required fields to match frontend validation (red stars)
        self.fields['name'].required = False
        self.fields['lastname'].required = False
        self.fields['extension'].required = False
        self.fields['email'].required = False
        self.fields['username'].required = True  # نام کاربری - required
        # Note: groupname and usersextension are set as required in their field definitions below
        
        # Ensure editOrAdd has a default value
        if 'editOrAdd' in self.fields:
            self.fields['editOrAdd'].initial = 'none'
            
        user_choices = [(user.extension, user.extension) for user in Users.objects.all()]
        recs = [(int(rec.extension), int(rec.extension)) for rec in Records.objects.all()]
        exts = list({val[0]: val for val in (user_choices + recs)}.values())

        exts = sorted(exts, key=lambda x: x[0])
        CHOICES = exts
        self.fields['usersextension'] = forms.MultipleChoiceField(choices=CHOICES, required=False,  # دسترسی به دفاتر - backend validates this
                                                widget=forms.CheckboxSelectMultiple(attrs={
                                                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}))
        
        self.fields['groupname'] = forms.ChoiceField(
            choices=[("none", "------")] + [(group.enname, group.pename) for group in Groups.objects.exclude(enname__in=["superadmin", "supporter"])],
            required=False,  # نقش - backend validates this
            widget=forms.Select(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs py-[2px] appearance-none'}))

    usersextension = forms.MultipleChoiceField(choices=[], required=False)
    editOrAdd = forms.ChoiceField(choices=EDIT_OR_ADD, required=False, initial='none', widget=forms.Select(
        attrs={'class': 'w-[140px] h-6  text-gray-600 py-[2px] text-xs appearance-none', 'data-default': 'none'}))
    groupname = forms.ChoiceField(choices=[("", "------")], required=False, widget=forms.Select(
            attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs py-[2px] appearance-none'}))

    class Meta:
        model = Users
        fields = ["username", "name", "lastname", "extension", "usersextension", "groupname", "email",
                  "email_verified_at", "active"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs'}),
            'name': forms.TextInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs'}),
            'lastname': forms.TextInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs'}),
            'extension': forms.NumberInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs ltr'}),
            'email': forms.EmailInput(attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs ltr'}),
            'active': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),

        }


class InfosForm(forms.ModelForm):
    class Meta:
        model = Infos
        fields = ('nationalcode', 'birthdate', 'telephone', 'phonenumber', 'gender', 'maritalstatus', 'military',
                  'educationfield', 'educationdegree', 'province', 'city', 'accountnumbershaba',
                  'cardnumber', 'groupname',
                  'accountnumber', 'address')

        widgets = {

            'nationalcode': forms.TextInput(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'birthdate': forms.TextInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs', 'data-jdp': None}),
            'telephone': forms.TextInput(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'phonenumber': forms.TextInput(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'gender': forms.Select(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
            'maritalstatus': forms.Select(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
            'military': forms.Select(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
            'educationfield': forms.TextInput(attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs'}),
            'educationdegree': forms.Select(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
            'province': forms.Select(attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
            'city': forms.TextInput(attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs'}),
            'accountnumbershaba': forms.TextInput(attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs ltr'}),
            'cardnumber': forms.TextInput(
                attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'accountnumber': forms.TextInput(
                attrs={'class': 'w-[190px] h-6 text-gray-600 text-xs ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'address': forms.Textarea(
                attrs={'class': 'w-[220px] h-[155px] text-gray-600 text-xs align-top text-start'}),
            'groupname': forms.Select(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs appearance-none py-[2px]'}),
        }


class SelfInfosProfileForm(forms.ModelForm):
    class Meta:
        model = Infos
        fields = ('nationalcode', 'birthdate', 'telephone', 'phonenumber', 'gender', 'maritalstatus', 'military',
                  'educationfield', 'educationdegree', 'province', 'city', 'accountnumbershaba',
                  'cardnumber', 'groupname', 'accountnumber', 'address')

        widgets = {
            'nationalcode': forms.TextInput(
                attrs={'class': 'field-value ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'birthdate': forms.TextInput(attrs={'class': 'field-value', 'data-jdp': None}),
            'telephone': forms.TextInput(
                attrs={'class': 'field-value ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'phonenumber': forms.TextInput(
                attrs={'class': 'field-value ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'gender': forms.Select(attrs={'class': 'field-value appearance-none'}),
            'maritalstatus': forms.Select(
                attrs={'class': 'field-value appearance-none'}),
            'military': forms.Select(attrs={'class': 'field-value appearance-none'}),
            'educationfield': forms.TextInput(attrs={'class': 'field-value'}),
            'educationdegree': forms.Select(
                attrs={'class': 'field-value appearance-none'}),
            'province': forms.Select(attrs={'class': 'field-value appearance-none'}),
            'city': forms.TextInput(attrs={'class': 'field-value'}),
            'accountnumbershaba': forms.TextInput(attrs={'class': 'field-value ltr'}),
            'cardnumber': forms.TextInput(
                attrs={'class': 'field-value ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'accountnumber': forms.TextInput(
                attrs={'class': 'field-value ltr', 'type': 'tel', 'inputmode': 'numeric'}),
            'address': forms.Textarea(
                attrs={'class': 'field-value align-top text-start', 'rows': 2}),
            'groupname': forms.Select(
                attrs={'class': 'field-value appearance-none'}),
        }


class SelfUserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("name", "lastname")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field-value'}),
            'lastname': forms.TextInput(attrs={'class': 'field-value'}),
        }


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permissions
        fields = ("can_view", "can_write", "can_modify", "can_delete")
        widgets = {
            "can_view": forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 onChangeCheckBox'}),
            "can_write": forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 onChangeCheckBox'}),
            "can_modify": forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 onChangeCheckBox'}),
            "can_delete": forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 onChangeCheckBox'}),
        }


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        # Make all device fields required
        self.fields['device'].required = True
        self.fields['number_of_lines'].required = True
        self.fields['cable_type'].required = True
        
        # Always show all cable type options regardless of device model
        self.fields['cable_type'].choices = [('', '------')] + list(CABLE_TYPES)
        
        # Set default cable type to RS232C
        if not self.instance.pk:  # Only set default for new instances
            self.fields['cable_type'].initial = 'rs-232c'
            # Set default values for RS232C fields
            self.fields['baudrate'].initial = 9600
            self.fields['parity'].initial = 'None'
            self.fields['flow'].initial = 'None'
            self.fields['stopbits'].initial = 1
            self.fields['databits'].initial = 8
            # Set default values for Ethernet fields
            self.fields['smdrip'].initial = '192.168.0.101'
            self.fields['smdrport'].initial = 23
            self.fields['smdrpassword'].initial = 'PCCSMDR'

    class Meta:
        model = Device
        fields = ("device", "flow", "stopbits", "baudrate", "parity", "databits", "number_of_lines", "smdrip", "smdrport", "smdrpassword", "cable_type")
        widgets = {
            'device': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr appearance-none py-0', 'required': 'required'}),
            'flow': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'stopbits': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'baudrate': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'parity': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'databits': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'number_of_lines': forms.NumberInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr', 'required': 'required'}),
            'smdrip': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'smdrport': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'smdrpassword': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0', 'required': 'required'}),
            'cable_type': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr py-0 my-2', 'required': 'required'}),

        }


class ContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactInfoForm, self).__init__(*args, **kwargs)
        self.fields['province'].required = False
        self.fields['phone_number'].required = False

    class Meta:
        model = ContactInfo
        fields = ("province", "phone_number")
        widgets = {
            'province': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs rtl py-[2px]'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr inputToNumber', 'placeholder': '09000000000', 'type': 'tel', 'inputmode': 'numeric'})
        }


class costsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(costsForm, self).__init__(*args, **kwargs)
        
        # Set default values if no instance exists
        if not self.instance.pk:
            self.initial['provincial'] = 45
            self.initial['outofprovincial'] = 330
            self.initial['international'] = 3400
            self.initial['irancell'] = 625
            self.initial['hamrahaval'] = 625
            self.initial['rightel'] = 625
        
        for field in self.fields.keys():
            self.fields[field].required = False
            # Set placeholder based on field
            placeholder = '45' if field == 'provincial' else '330' if field == 'outofprovincial' else '65'
            self.fields[field].widget.attrs.update(
                {'class': 'w-full h-5  text-gray-600 text-xs text-center ltr', 'step': '0.1', 'placeholder': placeholder})

    class Meta:
        model = Costs
        fields = ("hamrahaval", "irancell", "rightel", "provincial", "international", "outofprovincial")
        widgets = {
            "provincial": forms.NumberInput(),
            "outofprovincial": forms.NumberInput(),
            "international": forms.NumberInput(),
            "irancell": forms.NumberInput(),
            "hamrahaval": forms.NumberInput(),
            "rightel": forms.NumberInput()
        }


class emailSendingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(emailSendingForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False
            
        errs = [(int(err.errorcodenum), f"{err.errorcodenum} - {truncatewords(err.errormessage, 5)}") for err in Errors.objects.all()]
        errs = list({val[0]: val for val in errs}.values())
        errs = sorted(errs, key=lambda x: x[0])
        self.fields['errors'] = forms.MultipleChoiceField(choices=errs, required=False,
                                         widget=forms.CheckboxSelectMultiple(attrs={
                                             'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}))

    errors = forms.MultipleChoiceField(choices=[], required=False)

    class Meta:
        model = Emailsending
        fields = ("emailtosend", "collectionusername", "collectionpassword", "lines", "errors")
        widgets = {
            'collectionusername': forms.EmailInput(attrs={'class': 'w-full h-5 text-gray-600 text-xs ltr'}),
            'collectionpassword': forms.PasswordInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs'}),
            'emailtosend': forms.EmailInput(attrs={'class': 'w-full h-5 text-gray-600 text-xs ltr'}),
            'lines': forms.Select(attrs={'class': 'w-full h-5 text-gray-600 text-xs rtl appearance-none py-0'})
        }


class extGroups(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(extGroups, self).__init__(*args, **kwargs)
        # Disable auto-generated IDs to avoid duplicate DOM ids if rendered multiple times
        self.auto_id = False
        self.fields['label'].required = False
        
        user_choices = [(user.extension, user.extension) for user in Users.objects.all()]
        recs = [(int(rec.extension), int(rec.extension)) for rec in Records.objects.all()]
        ext = list({val[0]: val for val in (user_choices + recs)}.values())

        ext = sorted(ext, key=lambda x: x[0])
        self.fields['exts'] = forms.MultipleChoiceField(
            choices=ext,
            required=False,
            widget=forms.CheckboxSelectMultiple(
                attrs={'class': 'ext-check w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}
            )
        )
        # Ensure no 'id' attribute is present on the widget; without IDs, Chrome won't warn about duplicates
        self.fields['exts'].widget.attrs.pop('id', None)

    exts = forms.MultipleChoiceField(choices=[], required=False)

    class Meta:
        model = Extensionsgroups
        fields = ("exts", "label")
        widgets = {
            'label': forms.TextInput(attrs={'class': 'w-full h-5 text-gray-600 text-xs appearance-none py-0'})
        }


class userAccessToErrorsPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(userAccessToErrorsPageForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'w-full h-5 text-gray-600 text-xs appearance-none py-0'}),
            choices=[('none', '--------')] + [(user.username, user.username) for user in Users.objects.all()])

    users = forms.ChoiceField(choices=[('none', '--------')], widget=forms.Select(attrs={'class': 'w-full h-5 text-gray-600 text-xs appearance-none py-0'}))

    class Meta:
        model = Permissions
        fields = ("errorsreport", 'users')
        widgets = {
            "errorsreport": forms.CheckboxInput(attrs={'class': 'sr-only peer'})
        }


class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ('name', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'name',
                'placeholder': 'نام و نام خانوادگی خود را وارد کنید'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'message',
                'placeholder': 'پیام خود را بنویسید...',
                'rows': 4
            })
        }