from django import forms
from django.contrib.auth.models import User


class FaqForm(forms.ModelForm):
  answer = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':"password"}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':"username"}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':"email"}))

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email1 = cleaned_data.get("email")
        
        email2 = User.objects.filter(email=email1)
        if User.objects.exclude(pk=self.instance.pk).filter(email=email1).exists():
            raise forms.ValidationError(
                    
                    'Email Aready Exists'+str(email2)
                )
class Login(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':"password"}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':"username"}))
    
    class Meta:
        model = User
        fields = ['username', 'password']
  
