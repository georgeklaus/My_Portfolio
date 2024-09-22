from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, label="Subject", widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Your Message", widget=forms.Textarea(attrs={'class': 'form-control'}))
