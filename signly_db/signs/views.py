from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignForm, SignVideosForm, TrainingModelForm, EtiquetaForm
from .models import Sign, SignVideos, TrainingModel, Etiqueta
from django.core.files import File
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
import tempfile
import cv2
import mediapipe as mp
import csv
'''
@login_required
def panel_privado(request):
    return render(request, 'privado.html')

def inicio(request):
    return render(request, 'inicio.html')
'''

def etiqueta_list(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'signly_db/etiqueta_list.html', {'etiquetas': etiquetas})

def etiqueta_detail(request, pk):
    etiquetas = get_object_or_404(Etiqueta, pk=pk)
    return render(request, 'signly_db/etiqueta_detail.html', {'etiquetas': etiquetas})

def etiqueta_edit(request, pk):
    etiquetas = get_object_or_404(Etiqueta, pk=pk)
    if request.method == "POST":
        form = EtiquetaForm(request.POST, instance=etiquetas)
        if form.is_valid():
            etiquetas = form.save(commit=False)
            etiquetas.save()
            return redirect('etiqueta_list')
        else:
            return redirect('etiqueta_edit', pk=etiquetas.pk)
    else: 
        form = EtiquetaForm(instance=etiquetas)
    return render(request, 'signly_db/etiqueta_edit.html', {'form': form, 'etiquetas': etiquetas})

def etiqueta_new(request):
    if request.method == "POST":
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            etiquetas = form.save(commit=False)
            etiquetas.save()
            return redirect('etiqueta_list')
        else:
            return redirect('etiqueta_new')
    else:
        form = EtiquetaForm()
    return render(request, 'signly_db/etiqueta_edit.html', {'form': form})


#SIGN
def sign_list(request):
    signs = Sign.objects.all()
    return render(request, 'signly_db/sign_list.html', {'signs': signs})

def sign_detail(request, pk):
    signs = get_object_or_404(Sign, pk=pk)
    return render(request, 'signly_db/sign_detail.html', {'signs': signs})

def sign_edit(request, pk):
    signs = get_object_or_404(Sign, pk=pk)
    if request.method == "POST":
        form = SignForm(request.POST, instance=signs)
        if form.is_valid():
            signs = form.save(commit=False)
            signs.save()
            return redirect('sign_list')
        else:
            return redirect('sign_edit', pk=signs.pk)
    else: 
        form = SignForm(instance=signs)
    return render(request, 'signly_db/sign_edit.html', {'form': form, 'signs': signs})

def sign_new(request):
    if request.method == "POST":
        form = SignForm(request.POST)
        if form.is_valid():
            signs = form.save(commit=False)
            signs.save()
            return redirect('sign_list')
        else:
            return redirect('sign_new')
    else:
        form = SignForm()
    return render(request, 'signly_db/sign_edit.html', {'form': form})


#SIGN VIDEOS
def signVideo_list(request):
    videos = SignVideos.objects.all()
    return render(request, 'signly_db/signVideo_list.html', {'videos': videos})

def signVideo_detail(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    return render(request, 'signly_db/signVideo_detail.html', {'videos': videos})

def signVideo_edit(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    if request.method == "POST":
        form = SignVideosForm(request.POST, instance=videos)
        if form.is_valid():
            videos = form.save(commit=False)
            videos.save()
            return redirect('signVideo_list')
        else:
            return redirect('signVideo_edit', pk=videos.pk)
    else:
        form = SignVideosForm(instance=videos)
    return render(request, 'signly_db/signVideo_edit.html', {'form': form, 'videos': videos})

def signVideo_new(request):
    if request.method == "POST":
        form = SignVideosForm(request.POST)
        if form.is_valid():
            videos = form.save(commit=False)
            videos.save()
            return redirect('signVideo_list')
        else: 
            return redirect('signVideo_new')
    else:
        form = SignVideosForm()
    return render(request, 'signly_db/signVideo_edit.html', {'form': form})

def signVideo_estadoF(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    SignVideos.objects.filter(id=pk).update(estado=False)
    return redirect('signVideo_list')

def signVideo_estadoT(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    SignVideos.objects.filter(id=pk).update(estado=True)
    return redirect('signVideo_llst')

def signVideo_ap_reF(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    SignVideos.obects.filter(id=pk).update(ap_re=False)
    return redirect('signVideo_list')

def signVideo_ap_reT(request, pk):
    videos = get_object_or_404(SignVideos, pk=pk)
    SignVideos.objects.filter(id=pk).update(ap_re=True)
    return redirect('signVideo_list')

def procesar_videos(request):
    videos_aprobados = SignVideos.objects.filter(estado=True, ap_re=True, processed=False)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

    data_por_etiqueta = {}  # {etiqueta: list of rows with sequence_id, frame, landmarks}

    for video in videos_aprobados:
        etiqueta = video.etiqueta.etiqueta
        if etiqueta not in data_por_etiqueta:
            data_por_etiqueta[etiqueta] = []

        cap = cv2.VideoCapture(video.video.url)
        frame_num = 0  # frame counter

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_num += 1

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            left_hand = [0] * 63
            right_hand = [0] * 63

            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    base = hand_landmarks.landmark[0]
                    coords = []
                    for lm in hand_landmarks.landmark:
                        coords += [lm.x - base.x, lm.y - base.y, lm.z - base.z]
                    handedness = results.multi_handedness[i].classification[0].label
                    if handedness == 'Left':
                        left_hand = coords
                    else:
                        right_hand = coords

            # Add sequence_id (video.id) and frame number for TensorFlow
            row = [video.id, frame_num] + left_hand + right_hand
            data_por_etiqueta[etiqueta].append(row)

        cap.release()
        video.processed = True
        video.save()

    # Save CSVs
    for etiqueta, secuencia in data_por_etiqueta.items():
        etiqueta_obj, _ = Etiqueta.objects.get_or_create(etiqueta=etiqueta)
        csv_path = os.path.join(tempfile.gettempdir(), f"{etiqueta}.csv")

        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            header = ['sequence_id', 'frame']
            for h in ('left', 'right'):
                for i in range(21):
                    header += [f'{h}_hand_{i}_x', f'{h}_hand_{i}_y', f'{h}_hand_{i}_z']
            writer.writerow(header)
            for row_data in secuencia:
                writer.writerow(row_data)

        with open(csv_path, 'rb') as f:
            sign, created = Sign.objects.get_or_create(nombre=etiqueta_obj)
            sign.csv_file.save(f"{etiqueta}.csv", File(f))
            sign.save()

    return redirect('signVideo_list')


#TRAINING MODEL
def trainingMod_list(request):
    model = TrainingModel.objects.all()
    return render(request, 'signly_db/trainingMod_list.html', {'model': model})

def trainingMod_detail(request, pk):
    model = get_object_or_404(TrainingModel, pk=pk)
    return render(request, 'signly_db/trainingMod_detail.html', {'model': model})

def trainingMod_edit(request, pk):
    model = get_object_or_404(TrainingModel, pk=pk)
    if request.method == "POST":
        form = TrainingModelForm(request.POST, instance=model)
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            return redirect('trainingMod_list')
        else:
            return redirect('trainingMod_edit', pk=model.pk)
    else: 
        form = TrainingModelForm(instance=model)
    return render(request, 'signly_db/trainingMod_edit.html', {'form': form, 'model': model})

def trainingMod_new(request):
    if request.method == "POST":
        form = TrainingModelForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            return redirect('trainingMod_list')
        else:
            return redirect('trainingMod_new')
    else:
        form = TrainingModelForm()
    return render(request, 'signly_db/trainingMod_edit.html', {'form': form})