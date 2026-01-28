# 🎥 **API-First Video Streaming App**

> A production-ready, security-focused mobile application built with **React Native (Expo)** and **Flask**. 
> Designed as a **Thin Client** architecture where all business logic resides in the backend.

---

## 🚀 **Project Overview**

This project demonstrates a robust **API-First Architecture**. The mobile app is strictly a "dumb view" layer that renders data provided by the backend. It features a secure video streaming mechanism that **completely hides the YouTube source** from the client, preventing direct URL scraping.

### **Key Features**
*   **🔌 Thin Client Model**: Frontend contains **ZERO** business logic.
*   **🛡️ Video Security**:
    *   YouTube IDs are **never** sent to the client.
    *   Videos are played via a backend-proxied HTML stream.
    *   One-time signed **JWT Playback Tokens** prevent link sharing.
*   **🔐 Authentication**: Secure Signup/Login with bcrypt password hashing and JWT access tokens.
*   **📱 Modern UI**: Built with React Native, Expo Router, and a dark-mode-first aesthetic.

---

## 🛠️ **Tech Stack**

### **Frontend (Mobile)**
*   **Framework**: React Native (via Expo)
*   **Routing**: Expo Router (File-based)
*   **Styling**: StyleSheet (Dark Theme)
*   **Network**: Axios + Interceptors
*   **Storage**: Expo Secure Store (Encrypted Token Storage)

### **Backend (API)**
*   **Framework**: Python Flask
*   **Database**: MongoDB (PyMongo)
*   **Auth**: Flask-JWT-Extended
*   **Security**: Bcrypt, CORS, Signed URL Tokens

---

## 🏗️ **Architecture**

```mermaid
graph LR
    A[Mobile App] -->|1. Login Creds| B[Auth API]
    B -->|2. Returns JWT & User| A
    A -->|3. Get Dashboard| C[Video API]
    C -->|4. Returns Video List (No YouTube IDs)| A
    A -->|5. Request Playback| C
    C -->|6. Signs Token & Returns Secure URL| A
    A -->|7. Load Stream URL in WebView| D[Video Player Endpoint]
    D -->|8. Validates Token & Injects Embed| A
```

---

## ⚡ **Getting Started**

### **Prerequisites**
*   Node.js & npm
*   Python 3.10+
*   MongoDB (Local or Atlas)
*   Expo Go App (on your phone) or Android Emulator

### **1. Backend Setup**
```bash
cd backend

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Seed Database (Critical!)
python clean_and_seed.py

# Run Server
python -m app.main
```
*   Server runs at: `http://127.0.0.1:5000`

### **2. Frontend Setup**
```bash
cd frontend

# Install Dependencies
npm install

# Update Config (Important!)
# Open frontend/constants/Config.ts and set your LAN IP
# export const API_URL = 'http://YOUR_LAN_IP:5000';

# Run App
npx expo start
```
*   Scan the QR code with your phone (Expo Go) or press `a` for Android Emulator.

---

## 🧪 **Testing & Verification**

### **Audit Script**
We have included a full system audit script to verify security rules (e.g., ensuring YouTube IDs are not leaked).
```bash
cd backend
python audit_project.py
```

### **Manual Test Credentials**
*   **Email**: `audit@example.com`
*   **Password**: `password123`

---

## 🔒 **Security Details**

### **1. The "Hidden YouTube" Problem**
Standard apps embed YouTube IDs directly (e.g., `youtube.com/embed/xyz`). This allows anyone to copy the ID and watch it elsewhere.
**Our Solution**: 
1. The API sends `_id: "123"` (Internal Mongo ID).
2. Client requests `POST /video/123/token`.
3. Backend checks specific user permissions and signs a token: `eyJ...`.
4. Client loads `GET /video/123/stream?token=eyJ...`.
5. Backend verifies signature -> Renders HTML with the YouTube iframe server-side.

### **2. Token Storage**
We use `expo-secure-store` to encrypt the JWT on the device, ensuring it cannot be extracted easily like `AsyncStorage`.

---

## 📂 **Project Structure**

```
/
├── backend/
│   ├── app/            # App factory
│   ├── models/         # Database Schemas (User, Video)
│   ├── routes/         # API Endpoints (Auth, Video)
│   ├── seed_data.py    # Database Seeder
│   └── audit_project.py # Security Verification Script
│
├── frontend/
│   ├── app/            # Screens (File-based Routing)
│   ├── components/     # Reusable UI Components
│   ├── services/       # API Integration Layer
│   └── context/        # Auth State Management
```

---

## 👥 **Author**
**Abhi** - *Senior Full Stack Engineer*

---
© 2026 AI Video Project. All rights reserved.
