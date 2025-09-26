from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(label="Full name", required=True)
    phone = forms.CharField(required=False)
    vehicle_no = forms.CharField(label="Vehicle number", required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'phone', 'vehicle_no')

    def save(self, commit=True):
        user = super().save(commit=False)
        # split full name
        full_name = self.cleaned_data.get('full_name', '').strip()
        parts = full_name.split()
        if parts:
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # create profile
            from .models import Profile
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                vehicle_no=self.cleaned_data.get('vehicle_no', '')
            )
        return user

class ProfileForm(forms.Form):
    phone = forms.CharField(required=False)
    vehicle_no = forms.CharField(required=False)
