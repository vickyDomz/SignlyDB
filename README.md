# 📖 Signly Database

## 🚀 Overview

Signly Database is a Django-based application for managing and organizing datasets related to sign language recognition.

It stores structured information such as CSV files (with hand and face landmarks) and video recordings (.mp4), making it easier to prepare data for AI models.

This project represents my second experience designing and deploying a Django-based database, building upon earlier work with relational data management.

## ✨ Features

- 📂 Upload and organize sign language datasets (CSV + video)
- 🗄️ SQLite by default (easily switchable to MySQL)

## 🛠 Technologies

- **Python 3.x** – main programming language  
- **Django** – backend framework used to manage datasets and project structure  
- **SQLite** (default) / **MySQL** (planned) – database system  
- **MediaPipe** – extraction of hand and facial landmarks for gesture recognition  
- **OpenCV (cv2)** – video processing and frame handling  
- **NumPy** – numerical operations and array manipulation  
- **Cloudinary** – media storage and URL management for uploaded videos
