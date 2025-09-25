from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

class Etiqueta(models.Model):
    etiqueta = models.CharField(max_length=30)

    def __str__(self):
        return self.etiqueta

class Sign(models.Model):
    csv_file = models.FileField(upload_to="csv_files/")
    nombre = models.OneToOneField(Etiqueta, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre.etiqueta

class SignVideos(models.Model):
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    video = CloudinaryField('video',
                            resource_type = 'video',
                            transformation={
                                'quality': 'auto',
                                'fetch_format': 'mp4'
                            }
    ) #espacio de almacenamiento :b
    estado = models.BooleanField(default=False)
    ap_re = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)


class TrainingModel(models.Model):
    id_signs = models.ForeignKey(Sign, on_delete=models.CASCADE)
    version = models.CharField(max_length=25)
    csv_training = models.FileField(upload_to="csv_training_file/")
    notes = models.CharField(max_length=250)
    fecha_creacion = models.DateTimeField(default=timezone.now)
