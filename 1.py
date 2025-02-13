from ultralytics import YOLO
import cv2
import requests

# Load your custom YOLO model
model_path = 'C:\\Users\\NIKHIL\\Downloads\\kaggle\\working\\runs\\detect\\custom_yolov8\\weights\\best.pt'  # Update this to your model's path
model = YOLO(model_path)

# ThingSpeak server URL and API key
api_key = "K9HUW7WMOD8JLUO1"  # Replace with your actual API key
server_url = f"https://api.thingspeak.com/update?api_key={api_key}"

# Set the source for prediction (can be an image, video, or webcam)
source = 0  # Use 0 for webcam, or replace with a video file path

# Make predictions and visualize results
def detect_and_send(source):
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print("Error: Camera or video source could not be opened.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break
            
            # Make predictions
            results = model.predict(source=frame)  # Predict using the current frame

            for result in results:
                # Access the predictions and visualize them
                predictions = result.boxes  # Get the detected bounding boxes
                detected_count = len(predictions)
                print(f'Detected {detected_count} objects in the frame.')

                for box in predictions:
                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # x1, y1, x2, y2 coordinates
                    conf = box.conf[0]  # Confidence score
                    cls = int(box.cls[0])  # Class ID

                    # Adjust the threshold as needed
                    if conf > 0.3:  # Lowered confidence threshold for testing
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f'Class: {cls} Conf: {conf:.2f}', (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Send detection status to ThingSpeak
                if detected_count > 0:
                    detection_status = "Object detected"
                    request_url = f"{server_url}&field5={detection_status}&field6={detected_count}"
                    print("Sending request to ThingSpeak:", request_url)  # Debugging request URL
                    response = requests.get(request_url)
                    print("Response from ThingSpeak:", response.status_code, response.text)  # Print response for debugging
                else:
                    clear_status = "Clear"
                    request_url = f"{server_url}&field5={clear_status}&field6=0"
                    print("Sending request to ThingSpeak:", request_url)  # Debugging request URL
                    response = requests.get(request_url)
                    print("Response from ThingSpeak:", response.status_code, response.text)  # Print response for debugging

                # Show the image with predictions
                cv2.imshow('Detections', frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close any OpenCV windows
        print("Camera released.")

# Run the detection function
detect_and_send(source)
