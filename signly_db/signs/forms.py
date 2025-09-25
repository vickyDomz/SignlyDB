from .models import Sign, SignVideos, TrainingModel, Etiqueta
from django import forms

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ('etiqueta',)

class SignForm(forms.ModelForm):
    class Meta:
        model = Sign
        fields = ('csv_file', 'nombre')

class SignVideosForm(forms.ModelForm):
    class Meta:
        model = SignVideos
        fields = ('etiqueta', 'video',)

class TrainingModelForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        fields = ('id_signs', 'csv_training', 'notes')