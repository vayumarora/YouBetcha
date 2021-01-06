from django import forms
from .models import *


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)

    class Meta:
        model = User
        fields = ('email', 'password')


class RegisterForm(forms.ModelForm):

    name = forms.CharField(required=True, widget=forms.TextInput())
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=6)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password', 'gender')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password:
            raise forms.ValidationError("Confirm your password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords must be same")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            raise forms.ValidationError("User error")
        return email


class ProfileForm(forms.ModelForm):

    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control date-picker'}, format='%Y-%m-%d'))

    class Meta:
        model = User
        fields = ('name', 'gender', 'dob')
