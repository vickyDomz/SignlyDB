from django.contrib import admin
from .models import Sign, SignVideos, TrainingModel, Etiqueta

admin.site.register(Etiqueta)
admin.site.register(Sign)
admin.site.register(SignVideos)
admin.site.register(TrainingModel)

# Register your models here.
class SignAdmin(admin.ModelAdmin):
    list_display = ('id', 'csv_file', 'nombre', 'fecha_creacion')

class SignVideos(admin.ModelAdmin):
    list_display = ('id', 'etiqueta' 'video', 'fecha_subida')

class TrainingModel(admin.ModelAdmin):
    list_display = ('id', 'id_signs', 'version', 'csv_training', 'notes')