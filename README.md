# 📌 Project Overview
This project presents a Smart Wearable Assistive Device designed to help visually impaired people (VIPs) navigate safely and independently in both indoor and outdoor environments.
The system integrates IoT hardware with deep learning–based object detection (YOLOv8) to provide real-time obstacle detection and alerts.
The device uses ESP32, ultrasonic sensors, and a buzzer for obstacle detection, while YOLOv8 enables intelligent object detection with 360° awareness.

# 🧠 Motivation
According to the World Health Organization (WHO):

Over 2.2 billion people globally suffer from vision impairment.
Nearly 1 billion cases could have been prevented or remain unaddressed.
More than 90% of blind people live in developing countries.
Most existing assistive solutions lack real-time safety, object-level awareness, and reliability.
This project aims to address these challenges using AI + IoT technologies.

# Key Features

🔍 Real-time Object Detection using YOLOv8
🔄 360° Obstacle Detection
📢 Audio Alerts using Buzzer
🌐 IoT-based Monitoring
☁️ Cloud Integration with ThingSpeak
⚡ Low Latency & Fast Response

# 🛠️ Technologies Used
Hardware

ESP32
Ultrasonic Sensors (Front, Back, Left, Right)
Buzzer
Wi-Fi (ESP32 built-in)

Software & Tools
Python 3
YOLOv8 (Ultralytics)
PyTorch
Kaggle (Model Training)
Albumentations (Data Augmentation)
ThingSpeak
Wokwi (ESP32 Simulation)

# 🧩 System Architecture

Four ultrasonic sensors detect obstacles in all directions
ESP32 processes sensor inputs
Buzzer provides audio alerts based on obstacle distance
YOLOv8 detects objects in real time
Sensor data is sent to ThingSpeak via Wi-Fi

# 🤖 Object Detection Model (YOLOv8)
Why YOLO?

Single-pass detection (high speed)
Detects multiple objects simultaneously
Suitable for real-time applications
High efficiency and accuracy

Dataset
Total Images: 2300
Training: 85%
Validation: 8%
Testing: 7%


# ⚙️ Training & Implementation Details
| Parameter        | Value   |
| ---------------- | ------- |
| Epochs           | 200     |
| Batch Size       | 16      |
| Patience         | 180     |
| YOLO Version     | YOLOv8n |
| Framework        | PyTorch |
| Python Version   | 3.10.12 |
| GPU Acceleration | CUDA    |


# 📊 Experimental Results
| Metric       | Value   |
| ------------ | ------- |
| Precision    | 0.83    |
| Recall       | 0.65    |
| mAP@50       | 0.74    |
| mAP@50–95    | 0.55    |
| Accuracy     | 77%     |


# 📉 Performance Analysis
Confusion Matrix used for evaluation
Metrics such as Precision, Recall, F1-score analyzed
Training graphs show stable convergence and learning behavior


# 🚀 Future Scope

🎧 Voice-based object description (hearing-aid style output)
🧠 Improved object classification accuracy
🧭 GPS-based navigation support
🔋 Power optimization and miniaturization
🌍 Real-world testing in diverse environments


