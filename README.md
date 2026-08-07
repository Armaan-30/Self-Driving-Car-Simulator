# Autonomous Run

This project is a lightweight autonomous driving agent for a simulator. It uses a trained Keras/TensorFlow model to predict steering angles from camera images and sends control commands back to the simulator over a Socket.IO connection.

## What the project does

The system works like this:

1. The simulator sends telemetry data including the current vehicle speed and a camera image.
2. The server decodes the image and preprocesses it to match the training format used by the model.
3. A loaded neural network predicts a steering angle.
4. The script computes a throttle value based on the target speed and sends both steering and throttle commands back to the simulator.

## Project files

- `Udacity Car Sim` - https://github.com/udacity/self-driving-car-sim
- `drive.py` - Main server script that loads the model, receives simulator telemetry, predicts steering, and sends driving commands.
- `model.h5` - Pretrained Keras model used for inference.
- `requirements.txt` - Python dependencies required to run the project.
- `Training Data Drive Link` - https://drive.google.com/file/d/1RjGounrgGelA2gwDLPSdO-lz11vN8pOx/view?usp=sharing

## How it works

The main logic is implemented in `drive.py`:

- A Flask app and a Socket.IO server are initialized.
- The `telemetry` event receives incoming data from the simulator.
- The image is decoded from base64 and converted to a NumPy array.
- The image is cropped, resized, and normalized to the same format expected during training.
- The model predicts a steering angle.
- A simple cruise-control-style throttle controller adjusts the throttle based on the current speed.
- The server emits steering and throttle values back to the simulator.

## Requirements

This project depends on:

- Python 3
- TensorFlow / Keras
- Flask
- Flask-SocketIO
- Eventlet
- NumPy
- OpenCV
- Pillow
- h5py

## Setup

1. Create and activate a Python environment if desired.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server with your model file:

```bash
python drive.py model.h5
```

## Usage

After starting the server:

- Open the simulator.
- Connect it to the local server on port `4567`.
- The script will begin receiving camera data and sending steering and throttle commands.

## Notes

- The image preprocessing in this project is intentionally simple and should match the preprocessing used during model training.
- The model file must be compatible with the Keras loading code used in `drive.py`.
- The server prints steering and throttle values in real time so you can monitor behavior while driving.

## Example

A typical run looks like this:

```bash
python drive.py model.h5
```

You should see output indicating that the model is loading and that the server is waiting for simulator connections.
