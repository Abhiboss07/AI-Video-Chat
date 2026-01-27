# Setup Instructions

## Prerequisites
- Python 3.8+
- Node.js & npm
- MongoDB running locally (default 27017)
- Android Studio / Emulator (for App)

## 1. Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. Setup Environment:
Values are already in `.env`.
To change secrets:
```
JWT_SECRET=your_new_secret
MONGO_URI=mongodb://localhost:27017/videoapp
```

4. Seed Database (Optional but recommended):
```bash
python seed_data.py
```

5. Run Server:
```bash
python -m app.main
```
Server runs on `0.0.0.0:5000`.

## 2. Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure API URL:
Open `constants/Config.ts`.
- If using Android Emulator: `http://10.0.2.2:5000` (Default)
- If using Physical Device: Replace with your PC's Local IP (e.g. `192.168.1.X`).

4. Run App:
```bash
npx expo start
```
- Press `a` for Android Emulator.
- Scan QR code with Expo Go app on device.

## Troubleshooting
- **Network Error**: Ensure Backend is running and IP in `Config.ts` is correct.
- **Video not playing**: Ensure Internet access is available (YouTube embed requires it).
- **Login fails**: Check MongoDB connection.
