from django import forms
from django.contrib.auth.models import User

from .models import ParkingSpot, Profile

class ReservationForm(forms.ModelForm):
    # reserved_until = forms.DateTimeField(widget=forms.SplitDateTimeWidget())
    
    class Meta:
        model = ParkingSpot
        fields = ['reserved_until']
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)
        