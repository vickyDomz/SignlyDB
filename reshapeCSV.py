import os
import numpy as np
import pandas as pd

DATA_DIR = "/path/to/your/csvs"  # folder where the processed CSVs are
NUM_FRAMES = 30
NUM_FEATURES = 63*2  # left + right hand

all_sequences = []
all_labels = []

for csv_file in os.listdir(DATA_DIR):
    if not csv_file.endswith(".csv"):
        continue
    
    label = os.path.splitext(csv_file)[0]  # CSV name = label
    df = pd.read_csv(os.path.join(DATA_DIR, csv_file))
    
    # group by video_id
    for video_id, group in df.groupby("sequence_id"):
        group = group.sort_values("frame")  # make sure frames are in order
        
        # extract landmarks only (skip sequence_id and frame columns)
        landmarks = group.iloc[:, 2:].to_numpy()  # shape: (num_frames_video, 126)
        
        # if fewer frames than NUM_FRAMES, pad with zeros at the end
        if landmarks.shape[0] < NUM_FRAMES:
            padding = np.zeros((NUM_FRAMES - landmarks.shape[0], NUM_FEATURES))
            landmarks = np.vstack([landmarks, padding])
        # if more frames, sample evenly NUM_FRAMES
        elif landmarks.shape[0] > NUM_FRAMES:
            indices = np.linspace(0, landmarks.shape[0]-1, NUM_FRAMES, dtype=int)
            landmarks = landmarks[indices]
        
        all_sequences.append(landmarks)
        all_labels.append(label)

# final arrays for LSTM
X = np.array(all_sequences)  # shape: (num_sequences, NUM_FRAMES, 126)
y = np.array(all_labels)     # shape: (num_sequences,)

print("X shape:", X.shape)
print("y shape:", y.shape)