from django.contrib.auth.models import User
from django.forms import ModelForm


class ToggleStaffForm(ModelForm):
    class Meta:
        model = User
        fields = ('is_staff',)
        help_texts = {
            'is_staff': 'Designates whether the user can modify staff specific models and non-staff object instances.'
        }
        labels = {
            'is_staff': 'User is Staff Member'
        }