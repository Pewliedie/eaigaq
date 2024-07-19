from django import forms
from .models import User
from .models import MaterialEvidence
from .models import Case
from .models import Camera
from .models import TableModel


class UserForm(forms.ModelForm):
    photo_data = forms.CharField(widget=forms.HiddenInput(), required=False)  # Добавляем скрытое поле для фотографии

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'rank', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class MaterialEvidenceForm(forms.ModelForm):
    class Meta:
        model = MaterialEvidence
        fields = ['name', 'case', 'created_by', 'description', 'status', 'barcode']


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['name', 'description', 'investigator', 'active']


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['device_id', 'name', 'type', 'active']


class TableModelForm(forms.ModelForm):
    class Meta:
        model = TableModel
        fields = ['name', 'description']


class MaterialEvidenceGroupForm(forms.Form):
    evidence_ids = forms.ModelMultipleChoiceField(
        queryset=MaterialEvidence.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
