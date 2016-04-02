__author__ = 'aditya'
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.utils.html import strip_tags
from .models import UserProfile, User,BORROWER
from django.utils.translation import ugettext_lazy as _


class bookSearchForm(forms.Form):
    BookName = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'BookName'}))
    AuthorName = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Author'}))
    ISBN = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'ISBN','style':''}))


    def __init__(self, *args, **kwargs):
        super(bookSearchForm, self).__init__(*args, **kwargs)


class UserCreateForm(UserCreationForm):

    card_no = forms.CharField(required=False,widget=forms.HiddenInput())
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    phone_no = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Phone Number'}))
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Address'}))
    ssn = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'SSN'}))

    error_messages = {
        'mobile_number_not_ten': _("Phone number doesn't have 10 digits"),
        'mobile_number_has_alpha':_("Phone number cannot have alphabets"),
        'incorrect_ssn':_("SSN is incorrect"),
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_ssn(self):
        temp=self.cleaned_data['ssn']
        if(len(temp)!=9 or not(all(x.isdigit() for x in temp))):
            raise forms.ValidationError(
                self.error_messages['incorrect_ssn'],
                code='incorrect_ssn',
            )
        try:
            Users = UserProfile.objects.get(Ssn=self.cleaned_data['ssn'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data['ssn']
        raise forms.ValidationError(_("The ssn already exists in database"))

    def clean_card_no(self):
        try:
            Users = UserProfile.objects.get(Card_no=self.cleaned_data['card_no'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data['card_no']
        raise forms.ValidationError(_("The card already exists."))

    def clean_phone_no(self):
        mobile = self.cleaned_data.get('phone_no')
        if len(mobile)!=10:
            raise forms.ValidationError(
                self.error_messages['mobile_number_not_ten'],
                code='mobile_number_not_ten',
            )
        if(any(c.isalpha() for c in mobile)):
            raise forms.ValidationError(
                self.error_messages['mobile_number_has_alpha'],
                code='mobile_number_has_alpha',
            )
        return self.cleaned_data['phone_no']


    def is_valid(self):

        form = super(UserCreateForm, self).is_valid()
        return form

    def save(self):
        user = super(UserCreateForm, self).save()
        user_profile = UserProfile(User=user,Card_no=self.cleaned_data['card_no'],Fname=self.cleaned_data['first_name'],
                                   Lname=self.cleaned_data['last_name'],Phone_no=self.cleaned_data['phone_no'],
                                   Address=self.cleaned_data['address'],Ssn=self.cleaned_data['ssn']
                                   )

        borrower = BORROWER(Card_no=self.cleaned_data['card_no'],Fname=self.cleaned_data['first_name'],
                                   Lname=self.cleaned_data['last_name'],Phone=self.cleaned_data['phone_no'],
                                   Address=self.cleaned_data['address'],Ssn=self.cleaned_data['ssn']
                                   )
        borrower.save()
        user_profile.save()
        return user_profile

    class Meta:
        fields = ['card_no', 'first_name', 'last_name','ssn', 'password1',
                  'password2','phone_no','address','username']
        model = User


class AuthenticateForm(AuthenticationForm):

    username = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder': 'Card Number'}))
    password = forms.CharField(required=True,widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        # for f, error in self.errors.iteritems():
        #     if f != '__all__':
        #         self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
