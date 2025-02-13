import cv2
from ultralytics import YOLO

# Load your custom YOLOv8 model
model_path = r'C:\Users\NIKHIL\Downloads\kaggle\working\runs\detect\custom_yolov8\weights\best.pt'  # Update this to your model's path
model = YOLO(model_path)

# Load an image you know contains detectable objects
sample_image_path = r'D:\360\bedroom\images\00000.jpg'  # Use raw string literal
img = cv2.imread(sample_image_path)

# Check if the image was loaded successfully
if img is None:
    print(f"Error: Could not read the image from {sample_image_path}. Please check the path.")
else:
    # Make predictions
    results = model.predict(source=img)

    # Display results
    for result in results:
        predictions = result.boxes
        print(f'Detected {len(predictions)} objects in the sample image.')

        for box in predictions:
            # Get the bounding box coordinates, confidence, and class ID
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            cls = int(box.cls[0])  # Class ID

            # Draw the bounding box and label on the image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green bounding box
            cv2.putText(img, f'Class: {cls} Conf: {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Label above the box

    # Show the image with detections
    cv2.imshow('Sample Image Detections', img)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()
