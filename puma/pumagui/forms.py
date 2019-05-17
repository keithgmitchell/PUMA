from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, ModelFormMixin
from .models import *
from django import forms
from django.forms import ModelForm, Textarea
from django.db.models.fields import PositiveIntegerField


class AnacapaForm(forms.Form):
    metadata = forms.FileField(required=True)
    otu_table = forms.FileField(required=True)
    forward_seqs = forms.FileField(required=True)
    reverse_seqs = forms.FileField(required=True)
    merged_seqs = forms.FileField(required=True)
    rarefaction_depth = forms.IntegerField(required=False)
    rarefaction_iterations = forms.IntegerField(required=False)


class QIIME2Form(forms.Form):
    metadata = forms.FileField(required=True)
    otu_table = forms.FileField(required=True)
    all_seqs = forms.FileField(required=True)
    taxonomy = forms.FileField(required=True)
    rarefaction_depth = forms.IntegerField(required=False)
    rarefaction_iterations = forms.IntegerField(required=False)


class MrDNAForm(forms.Form):
    metadata = forms.FileField(required=True)
    otu_table = forms.FileField(required=True)
    all_seqs = forms.FileField(required=True)
    rarefaction_depth = forms.IntegerField(required=False)
    rarefaction_iterations = forms.IntegerField(required=False)


class PiphillinForm(forms.Form):
    verified_metadata = forms.FileField(required=True)

    def __init__(self, number_forms, *args, **kwargs):
        super(PiphillinForm, self).__init__(*args, **kwargs)
        for i in range(0, number_forms):
            self.fields['zip_file_%s' % (i+1)] = forms.FileField(required=True)








