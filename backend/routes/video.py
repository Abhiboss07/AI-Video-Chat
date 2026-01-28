from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.video import Video
from middleware.auth import jwt_required_custom
import requests

video_bp = Blueprint('video', __name__, url_prefix='/video')

@video_bp.route('/dashboard', methods=['GET'])
@jwt_required_custom
def dashboard():
    """Get active videos for dashboard"""
    try:
        videos = Video.get_active_videos(limit=2)
        
        return jsonify({
            'videos': videos
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch videos'}), 500

@video_bp.route('/<video_id>/stream', methods=['GET'])
def get_video_stream(video_id):
    """Get secure video stream with token validation"""
    try:
        # Get playback token from query params
        playback_token = request.args.get('token')
        if not playback_token:
            return jsonify({'error': 'Missing playback token'}), 400
            
        # Verify playback token
        token_data = Video.verify_playback_token(playback_token)
        if not token_data:
            return jsonify({'error': 'Invalid or expired playback token'}), 401
            
        # Verify token matches requested video
        if token_data['video_id'] != video_id:
            return jsonify({'error': 'Token mismatch'}), 401
            
        # Get video data from database
        video_data = Video.find_by_id(video_id)
        if not video_data or not video_data.get('is_active'):
            return jsonify({'error': 'Video not found or inactive'}), 404
            
        # Generate secure playback HTML
        # The client NEVER sees the YouTube URL, effectively hiding the source
        # The WebView loads THIS endpoint, which renders the player
        youtube_id = video_data['youtube_id']
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                body {{ margin: 0; padding: 0; background: black; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}
                iframe {{ width: 100%; height: 100%; border: none; }}
            </style>
        </head>
        <body>
            <iframe 
                src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&modestbranding=1&rel=0&playsinline=1" 
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </body>
        </html>
        """
        
        return html_content, 200, {
            'Content-Type': 'text/html',
            'X-Frame-Options': 'ALLOWALL',  # Allow embedding
            'Content-Security-Policy': "frame-ancestors *;" # For modern browsers
        }
        
    except Exception as e:
        return jsonify({'error': 'Failed to get video stream'}), 500

@video_bp.route('/<video_id>/token', methods=['POST'])
@jwt_required_custom
def generate_playback_token(video_id):
    """Generate a playback token for a specific video"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify video exists and is active
        video_data = Video.find_by_id(video_id)
        if not video_data or not video_data.get('is_active'):
            return jsonify({'error': 'Video not found or inactive'}), 404
            
        # Generate playback token
        playback_token = Video.generate_playback_token(video_id, current_user_id)
        
        return jsonify({
            'video_id': video_id,
            'playback_token': playback_token,
            'expires_in': 3600  # 1 hour in seconds
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate playback token'}), 500
