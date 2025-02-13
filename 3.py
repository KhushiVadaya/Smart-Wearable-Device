import cv2
import requests
from ultralytics import YOLO

# Load your custom YOLO model
model_path = r'C:\Users\NIKHIL\Downloads\kaggle\working\runs\detect\custom_yolov8\weights\best.pt'  # Update this to your model's path
model = YOLO(model_path)

# Define your ThingSpeak server URL and API key
api_key = "K9HUW7WMOD8JLUO1"  # Replace with your actual API key
server_url =  f"https://api.thingspeak.com/update?api_key={api_key}"

# Load an image you know contains detectable objects
sample_image_path = 'D:\\360\\bedroom\\images\\00000.jpg'  # Update this path
img = cv2.imread(sample_image_path)

if img is None:
    print("Error: Image not found.")
else:
    print("Image loaded successfully.")

# Make predictions
results = model.predict(source=img)
print("Predictions made successfully.")  # Debugging statement

# Initialize detection count
detected_count = 0

# Display results
for result in results:
    predictions = result.boxes
    detected_count = len(predictions)
    print(f'Detected {detected_count} objects in the sample image.')

    if detected_count > 0:
        for box in predictions:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            print(f"Detected box: [{x1}, {y1}, {x2}, {y2}] Class: {cls} Confidence: {conf:.2f}")  # Debugging each box

            # Draw bounding box on the image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'Class: {cls} Conf: {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the image with predictions
    cv2.imshow('Sample Image Detections', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Send detection status to ThingSpeak
    if detected_count > 0:  # Check if any objects are detected
        detection_status = "Object detected"
        request_url = f"{server_url}&field5={detection_status}&field6={detected_count}"
        print("Sending request to ThingSpeak:", request_url)  # Debugging request URL
        response = requests.get(request_url)

        # Debugging response
        print("Response from ThingSpeak:", response.status_code, response.text)  # Print response for debugging

    else:
        clear_status = "Clear"
        request_url = f"{server_url}&field5={clear_status}&field6=0"
        print("Sending clear status to ThingSpeak:", request_url)  # Debugging request URL
        response = requests.get(request_url)

        # Debugging response
        print("Response from ThingSpeak:", response.status_code, response.text)  # Print response for debugging

# Test sending a request with static values
test_response = requests.get(f"{server_url}&field5=TestStatus&field6=1")
print("Test response from ThingSpeak:", test_response.status_code, test_response.text)
