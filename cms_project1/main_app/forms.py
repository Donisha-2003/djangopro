import re
from django import forms
from django.forms.widgets import DateInput, TextInput
from .models import *
from django.core.exceptions import ValidationError


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class WalkinForm(forms.ModelForm):
    class Meta:
        model=Walkin
        fields="__all__"

class CollectionReportForm(forms.ModelForm):
    class Meta:
        model=CollectionReport
        fields="__all__"  
class WalkinReportForm(forms.ModelForm):
    class Meta:
        model=WalkinReport
        fields="__all__"  
class RegistrationReportForm(forms.ModelForm):
    class Meta:
        model=RegistrationReport
        fields="__all__" 

class ReferenceReportForm(forms.ModelForm):
    class Meta:
        model=ReferenceReport
        fields="__all__"   

class PendingPaymentReportForm(forms.ModelForm):
    class Meta:
        model=PendingPaymentReport
        fields="__all__" 
# class FollowReportForm(forms.ModelForm):
#     class Meta:
#         model=FollowReport
#         fields="__all__"   

class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"


    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else: 
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail: 
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail
    
    def clean_first_name(self):
        form_first_name = self.cleaned_data.get('first_name')
        if not form_first_name:
            raise forms.ValidationError("First name cannot be empty")

        # Add regex pattern validation
        if not re.match(r'^[A-Za-z]*$', form_first_name):
            raise forms.ValidationError("First name must contain only letters")

        return form_first_name
    
    def clean_last_name(self):
        form_last_name = self.cleaned_data.get('last_name')
        if not form_last_name:
            raise forms.ValidationError("Last name cannot be empty")

        # Add regex pattern validation
        if not re.match(r'^[A-Za-z]*$', form_last_name):
            raise forms.ValidationError("Last name must contain only letters")

        return form_last_name
    
    def clean(self):
        cleaned_data = super().clean()  # Call the parent class's clean method to ensure other validations are performed

        for field_name, field in self.fields.items():
            form_field = cleaned_data.get(field_name)

            if field.required and (form_field is None or form_field == ''):
                self.add_error(field_name, "This field is required")
                self.fields[field_name].widget.attrs.update({'class': 'form-control is-invalid'})  # Add CSS class for validation error

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class CroForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(CroForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Cro
        fields = CustomUserForm.Meta.fields + \
            ['course', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
            ['course' ]
class StuForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StuForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Stu
        fields = CustomUserForm.Meta.fields + \
            ['course' ]


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Course


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'staff', 'course']



class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']

class AreaofimprovementForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(AreaofimprovementForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Areaofimprovement
        fields = ['remarks']


class LeaveReportCroForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportCroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportCro
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackCroForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackCroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackCro
        fields = ['feedback']


class CroEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(CroEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Cro
        fields = CustomUserForm.Meta.fields 
class CroEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(CroEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Cro
        fields = CustomUserForm.Meta.fields


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CroResult
        fields = ['session_year', 'subject', 'cro', 'test', 'exam']
