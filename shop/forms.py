
from django import forms
from .models import ContactTicket, Order

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactTicket
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваша электронная почта'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение'}),
        }
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'message': 'Сообщение',
        }

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)

    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment_method', 'delivery_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
        }