from django import forms


class UserForm(forms.Form):
    username1 = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                                required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                required=True)


class RegistrationForm(forms.Form):
    username2 = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                                required=True)
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                required=True)
    password_2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'}),required=True)
