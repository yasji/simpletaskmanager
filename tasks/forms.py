from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task

class BaseFormMixin:
    """
    Mixin that adds common styling and functionality to all forms.
    Can be used with both ModelForm and Form classes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})
            
            # Add a placeholder based on field label if not set
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = field.label or field_name.title()


class BaseForm(BaseFormMixin, forms.ModelForm):
    """
    Base model form class that adds common styling and functionality.
    """
    pass


class BaseNonModelForm(BaseFormMixin, forms.Form):
    """
    Base non-model form class that adds common styling and functionality.
    """
    pass


class TaskForm(BaseForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        

class CustomUserCreationForm(BaseFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class CustomAuthenticationForm(BaseFormMixin, AuthenticationForm):
    """
    Custom authentication form with bootstrap styling
    """
    pass
