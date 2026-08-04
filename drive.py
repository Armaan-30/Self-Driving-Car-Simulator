import socketio
import eventlet
import numpy as np
from flask import Flask
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2
import sys
import os

# Hide TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize SocketIO server and Flask app
sio = socketio.Server()
app = Flask(__name__)

# Preprocessing function matching training
def preprocess_image(img):
    img = img[60:135, :, :]
    img = cv2.resize(img, (200, 66))
    img = img / 255.0 
    return img

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        speed = float(data["speed"])
        
        # Decode image from simulator
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        
        # Preprocess and shape for model
        image = preprocess_image(image)
        image = np.array([image])
        
        # Predict steering angle cleanly as a float scalar
        prediction = model.predict(image, batch_size=1, verbose=0)
        steering_angle = float(np.squeeze(prediction))
        
        # Target speed set to 30 mph
        target_speed = 40.0
        
        # Cruise control formula (accelerate hard if slow, brake if too fast)
        throttle = (target_speed - speed) * 0.1
        
        # Clamp the throttle between -1.0 (full brake) and 1.0 (full gas)
        throttle = max(-1.0, min(throttle, 1.0))
            
        print(f"Steering: {steering_angle:.3f} | Throttle: {throttle:.3f} | Speed: {speed:.3f}")
        send_control(steering_angle, throttle)
    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("Simulator Connected successfully!", sid)
    send_control(0, 0)

def send_control(steering_angle, throttle):
    sio.emit(
        'steer',
        data={
            'steering_angle': str(steering_angle),
            'throttle': str(throttle)
        },
        skip_sid=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the model file name. Example: python drive.py model.h5")
        sys.exit()
        
    model_path = sys.argv[1]
    
    print(f"Loading model: {model_path}...")
    model = load_model(model_path, compile=False)
    
    app = socketio.WSGIApp(sio, app)
    
    print("Starting server on port 4567... Waiting for simulator connection.")
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)