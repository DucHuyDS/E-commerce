from dataclasses import fields

from .models import Account,AccountProfile
from django import forms

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Tạo mật khẩu'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Xác nhận mật khẩu'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','password','phone']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
        self.fields['first_name'].widget.attrs['placeholder']='Tên'
        self.fields['last_name'].widget.attrs['placeholder']='Họ'
        self.fields['email'].widget.attrs['placeholder']='Email'
        self.fields['phone'].widget.attrs['placeholder']='Số điện thoại'

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields=['first_name','last_name','phone']
    def __init__(self,*args,**kwargs):
        super(AccountForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
        self.fields['first_name'].widget.attrs['placeholder']='Họ'
        self.fields['last_name'].widget.attrs['placeholder']='Tên'
        self.fields['phone'].widget.attrs['placeholder']='Số điện thoại'
  
    

      



class AccountProfileForm(forms.ModelForm):
    birthday = forms.DateField(required=False,widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',                                                                 
        }))
    profile_picture=forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'class':'btn btn-sm btn-light',
    }))
    class Meta:
        model = AccountProfile
        fields=['profile_picture','address','birthday']
    
    def __init__(self,*args,**kwargs):
        super(AccountProfileForm,self).__init__(*args,**kwargs)
        self.fields['address'].widget.attrs['class']='form-control'
        self.fields['address'].widget.attrs['placeholder']='Địa chỉ'
      

