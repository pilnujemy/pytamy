from django import forms
from braces.forms import UserKwargModelFormMixin
import autocomplete_light
from .models import Letter, Contact, Attachment
from multiupload.fields import MultiFileField
from atom.ext.crispy_forms import SingleButtonMixin
from atom.forms import AuthorMixin


class LetterForm(UserKwargModelFormMixin, SingleButtonMixin, AuthorMixin,
                 autocomplete_light.ModelForm):
    attachments = MultiFileField(required=False, label="Add attachments")

    def save(self, commit=True, *args, **kwargs):
        obj = super(LetterForm, self).save(commit=False, *args, **kwargs)
        Attachment.objects.bulk_create(Attachment(file=each, letter=obj)
                                       for each in self.cleaned_data['attachments'])
        return obj

    class Meta:
        model = Letter
        fields = ['outgoing', 'contact', 'transfer_on', 'description']


class ContactForm(UserKwargModelFormMixin, SingleButtonMixin, AuthorMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'street', 'city', 'postcode', 'comment']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', ]
