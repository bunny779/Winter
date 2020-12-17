from django import forms
from .models import Register

class loginForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('email','password')
        widgets = {
            'password': forms.TextInput(attrs={'type':'password'}),
            'email': forms.TextInput(attrs={'type':'email','placeholder':'abcd@xyz.com'})
        }
        
class registerForm(forms.ModelForm):
    class Meta:
        model = Register   
        fields = "__all__"
        widgets = {
            'password': forms.TextInput(attrs={'type':'password'}),
            'email': forms.TextInput(attrs={'type':'email','placeholder':'abcd@xyz.com'})
        }