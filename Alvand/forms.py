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
        user_choices = [(user.extension, user.extension) for user in Users.objects.all()]
        extgps = [(extgp.label, extgp.label) for extgp in Extensionsgroups.objects.all()]
        recs = [(int(rec.extension), int(rec.extension)) for rec in Records.objects.all()]
        exts = list({val[0]: val for val in (user_choices + recs)}.values())

        exts = sorted(exts, key=lambda x: x[0])
        CHOICES = extgps + exts
        self.fields['usersextension'] = forms.MultipleChoiceField(choices=CHOICES, required=False,
                                                widget=forms.CheckboxSelectMultiple(attrs={
                                                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}))
        
        self.fields['groupname'] = forms.ChoiceField(
            choices=[("none", "------")] + [(group.enname, group.pename) for group in Groups.objects.exclude(enname__in=["superadmin", "supporter"])],
            widget=forms.Select(
                attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs py-[2px] appearance-none'}))

    usersextension = forms.MultipleChoiceField(choices=[], required=False)
    editOrAdd = forms.ChoiceField(choices=EDIT_OR_ADD, required=True, widget=forms.Select(
        attrs={'required': True, 'class': 'w-[140px] h-6  text-gray-600 py-[2px] text-xs appearance-none'}))
    groupname = forms.ChoiceField(choices=[("none", "------")], widget=forms.Select(
            attrs={'class': 'w-[140px] h-6 text-gray-600 text-xs py-[2px] appearance-none'}))

    class Meta:
        model = Users
        fields = ["editOrAdd", "username", "name", "lastname", "extension", "usersextension", "groupname", "email",
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
                  'cardnumber',
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
        self.fields['device'].required = False

    class Meta:
        model = Device
        fields = ("device", "flow", "stopbits", "baudrate", "parity", "databits", "number_of_lines", "smdrip", "smdrport", "smdrpassword", "cable_type")
        widgets = {
            'device': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr appearance-none py-0'}),
            'flow': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'stopbits': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'baudrate': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'parity': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'databits': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'number_of_lines': forms.NumberInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr'}),
            'smdrip': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'smdrport': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'smdrpassword': forms.TextInput(attrs={'class': 'w-full h-5  text-gray-600 text-xs appearance-none py-0'}),
            'cable_type': forms.Select(attrs={'class': 'w-full h-5  text-gray-600 text-xs ltr py-0 my-2'}),

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
        for field in self.fields.keys():
            self.fields[field].required = False
            self.fields[field].widget.attrs.update(
                {'class': 'w-full h-5  text-gray-600 text-xs text-center ltr', 'step': '0.1', 'placeholder': '0.0'})

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
        self.fields['label'].required = False
        
        user_choices = [(user.extension, user.extension) for user in Users.objects.all()]
        recs = [(int(rec.extension), int(rec.extension)) for rec in Records.objects.all()]
        ext = list({val[0]: val for val in (user_choices + recs)}.values())

        ext = sorted(ext, key=lambda x: x[0])
        self.fields['exts'] = forms.MultipleChoiceField(choices=ext, required=False,
                                       widget=forms.CheckboxSelectMultiple(attrs={'class':
                                                                                      'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}))

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