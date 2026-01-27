# Architecture & Implementation Details

## 1. Architecture Decisions

### Thin Client Approach
To satisfy the requirement of "ZERO business logic" on the frontend:
- **Navigation Logic**: Handled by Authentication State (Context).
- **Data Display**: Frontend renders exactly what backend sends.
- **Video Playback**: The frontend does not even know the YouTube ID. It loads a backend-generated HTML page.

### Backend-Driven UI (Partial)
- The dashboard API dictates which videos are shown.
- The backend controls the stream capability via signed tokens.

## 2. JWT Flow
1. **Login/Signup**: Client sends credentials -> Backend validates and returns `access_token` and `user` info.
2. **Storage**: `access_token` stored in `Expo SecureStore` (Encrypted).
3. **Requests**: Axios Interceptor adds `Authorization: Bearer <token>` to every request.
4. **Expiry**: If backend returns 401, client logs out locally.

## 3. Video Security (Hiding YouTube)
We implemented **Option B + HTML Proxy**.
1. **No ID Exposure**: The API `/video/dashboard` returns `_id`, `title`, queryable metadata, but REMOVES `youtube_id`.
2. **Tokenized Access**: To play, client requests a short-lived `playback_token` for that specific video.
3. **HTML Stream**:
   - Client Webview loads: `GET /video/:id/stream?token=...`
   - Backend validates token.
   - Backend returns a full HTML page with an `iframe` embedding the YouTube player.
   - **Benefit**: The user never sees the YouTube ID in the API JSON. It is only verified and injected serverside into the HTML.

## 4. AI Assistance
- **Helped with**: Rapid scaffolding of Flask blueprints, React Native styles, and Expo Router boilerplate.
- **Manual Intervention**: 
  - **PowerShell Commands**: creating directories with `mkdir` failed due to syntax/parsing overlap. Switched to direct file creation.
  - **Expo Router Config**: Tweaked `_layout` logic to ensure Auth Flow works correctly with `replace`.
  - **Network Config**: correctly identifying `10.0.2.2` for Android Emulator vs `localhost`.

## 5. Security Highlights
- **Passwords**: Bcrypt hashing.
- **Tokens**: Short-lived playback tokens (1 hour).
- **YouTube Obfuscation**: Server-side rendering of the player.
