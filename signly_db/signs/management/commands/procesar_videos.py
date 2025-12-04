from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from signs.models import SignVideos, Sign, Etiqueta
import cv2
import numpy as np
import os
import tempfile
import requests
import csv
import mediapipe as mp
from cloudinary.utils import cloudinary_url

class Command(BaseCommand):
    help = "Processes all approved videos and generates CSV files with hand landmarks."

    def handle(self, *args, **kwargs):
        videos_aprobados = SignVideos.objects.filter(estado=True, ap_re=True, processed=False)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

        NUM_FRAMES = 45
        TARGET_FPS = 30
        csv_folder = "E:/sign_csvs"
        os.makedirs(csv_folder, exist_ok=True)

        for video in videos_aprobados:
            etiqueta = video.etiqueta.etiqueta
            etiqueta_obj, _ = Etiqueta.objects.get_or_create(etiqueta=etiqueta)
            csv_path = os.path.join(csv_folder, f"{etiqueta}.csv")

            # --- Prepare CSV file (create if missing, append otherwise)
            file_exists = os.path.exists(csv_path)
            f = open(csv_path, mode='a', newline='')
            writer = csv.writer(f)
            if not file_exists:
                header = ['sequence_id', 'frame']
                for h in ('left', 'right'):
                    for i in range(21):
                        header += [f'{h}_hand_{i}_x', f'{h}_hand_{i}_y', f'{h}_hand_{i}_z']
                writer.writerow(header)

            try:
                # --- Download video
                url = video.video.url
                public_id = "/".join(url.split("/")[7:])
                cloud_url, _ = cloudinary_url(public_id, resource_type="video", transformation=[{"fps": TARGET_FPS}])
                response = requests.get(cloud_url, stream=True)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", dir="E:/sign_temp")

                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp.close()

                cap = cv2.VideoCapture(tmp.name)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                active_frames = []

                for idx in range(total_frames):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)
                    if results.multi_hand_landmarks:
                        active_frames.append(idx)
                cap.release()

                if not active_frames:
                    os.remove(tmp.name)
                    video.processed = True
                    video.save()
                    continue

                start = active_frames[0]
                end = active_frames[-1]
                if end - start + 1 < NUM_FRAMES:
                    frame_indices = list(range(start, end + 1))
                else:
                    frame_indices = np.linspace(start, end, NUM_FRAMES, dtype=int)

                cap = cv2.VideoCapture(tmp.name)
                frame_num = 0
                for idx in range(total_frames):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    if idx not in frame_indices:
                        continue
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

                    row = [video.id, frame_num] + left_hand + right_hand
                    writer.writerow(row)

                cap.release()
                os.remove(tmp.name)

                # Save progress
                video.processed = True
                video.save()
                print(f"Processed and saved video: {video.id} under '{etiqueta}' ✅")

            except Exception as e:
                print(f"Error processing video {video.id}: {e}")

            finally:
                f.close()

        print("All available videos processed and CSVs updated!")
