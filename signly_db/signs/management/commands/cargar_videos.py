# miapp/management/commands/cargar_videos.py
import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from signs.models import Etiqueta, SignVideos

class Command(BaseCommand):
    help = 'Sube videos desde carpetas locales a Cloudinary y guarda la URL en la base de datos.'

    def add_arguments(self, parser):
        parser.add_argument('directorio', type=str, help='Ruta a la carpeta raíz donde están las carpetas de etiquetas.')

    def handle(self, *args, **kwargs):
        directorio = kwargs['directorio']

        if not os.path.isdir(directorio):
            self.stdout.write(self.style.ERROR(f"❌ Directorio no encontrado: {directorio}"))
            return

        for nombre_etiqueta in os.listdir(directorio):
            carpeta_etiqueta = os.path.join(directorio, nombre_etiqueta)
            if not os.path.isdir(carpeta_etiqueta):
                continue

            try:
                etiqueta = Etiqueta.objects.get(etiqueta=nombre_etiqueta)
            except Etiqueta.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️ Etiqueta no encontrada en BD: {nombre_etiqueta}'))
                continue

            for archivo in os.listdir(carpeta_etiqueta):
                ruta_archivo = os.path.join(carpeta_etiqueta, archivo)

                if not os.path.isfile(ruta_archivo):
                    continue

                # Verificar si ya existe
                if SignVideos.objects.filter(nombre=archivo, etiqueta=etiqueta).exists():
                    self.stdout.write(f'🟡 Video ya cargado: {archivo} ({etiqueta.etiqueta})')
                    continue

                try:
                    self.stdout.write(f'⬆️ Subiendo: {archivo} -> {etiqueta.etiqueta}...')
                    resultado = cloudinary.uploader.upload(
                        ruta_archivo,
                        resource_type="video",
                        folder=f"LSPy/{nombre_etiqueta}"  # opcional: organiza en carpetas por etiqueta en Cloudinary
                    )

                    url_video = resultado.get('secure_url')

                    SignVideos.objects.create(
                        etiqueta=etiqueta,
                        nombre=archivo,
                        video=url_video
                    )

                    self.stdout.write(self.style.SUCCESS(f'✅ Subido: {archivo} -> {url_video}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error subiendo {archivo}: {e}'))

        self.stdout.write(self.style.SUCCESS('🚀 Carga masiva completada.'))
