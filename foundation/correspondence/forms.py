from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from braces.forms import UserKwargModelFormMixin
import autocomplete_light
from .models import Letter, Contact, Attachment
from multiupload.fields import MultiFileField


class AuthorMixin(object):
    def save(self, commit=True, *args, **kwargs):
        obj = super(AuthorMixin, self).save(commit=False, *args, **kwargs)
        if obj.pk:  # update
            obj.modified_by = self.user
        else:  # new
            obj.created_by = self.user
        if commit:
            obj.save()
        return obj


class LetterForm(UserKwargModelFormMixin, AuthorMixin, autocomplete_light.ModelForm):
    attachments = MultiFileField(required=False, label="Fast attachment")

    def save(self, commit=True, *args, **kwargs):
        obj = super(LetterForm, self).save(commit=False, *args, **kwargs)
        Attachment.objects.bulk_create(Attachment(file=each, letter=obj)
            for each in self.cleaned_data['attachments'])
        return obj

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'outgoing',
            'contact',
            'transfer_on',
            'description',
            'attachments',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )
        super(LetterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Letter
        fields = ['outgoing', 'contact', 'transfer_on', 'description']


class ContactForm(UserKwargModelFormMixin, AuthorMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'street',
            'city',
            'postcode',
            'comment',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )
        super(ContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
        fields = ['name', 'street', 'city', 'postcode', 'comment']


class AttachmentForm(forms.ModelForm):

    class Meta:
        model = Attachment
        fields = ['file', ]
