from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from ExpenseTracker.auth_app.models import AppUser, Profile

UserModel = get_user_model()


class AppUserViewForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
        exclude = ('password',)
        field_classes = {'email': forms.EmailField}


class AppUserCreationForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
        exclude = ('password',)
        field_classes = {'email': forms.EmailField}

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SignUpForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2',)
        USERNAME_FIELD = 'email'

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            user=user,
        )
        if commit:
            profile.save()

        return user
