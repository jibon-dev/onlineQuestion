from django.contrib.auth import get_user_model
from django import forms
from datetime import date

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # dob = forms.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            ]

    def clean_email(self):
        # print('cleaning mail')
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        # print('cleaning password')
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # def clean_dob(self):
    #     born = self.cleaned_data.get("dob")
    #     # print(born)
    #     today = date.today()
    #     age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    #     # print(age)
    #     if age < 13:
    #         raise forms.ValidationError("You Must be 13!")
    #     return born

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.is_active = False
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

