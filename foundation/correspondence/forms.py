from django import forms
from braces.forms import UserKwargModelFormMixin
from .models import Letter, Contact, Attachment
from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.forms import AuthorMixin


class LetterForm(UserKwargModelFormMixin, SingleButtonMixin, AuthorMixin,
                 forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['outgoing', 'contact', 'transfer_on', 'description']


class ContactForm(UserKwargModelFormMixin, SingleButtonMixin, AuthorMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'street', 'city', 'postcode', 'comment']


class AttachmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['protected'].help_text = None

    class Meta:
        model = Attachment
        fields = ['file', 'protected']
