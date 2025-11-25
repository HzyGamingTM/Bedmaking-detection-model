from ultralytics import YOLO
from statistics import median
import cv2
import torch

crumple_model = YOLO("crumple.pt")
stain_model = YOLO("stain.pt")
bed_model = YOLO("yolov8m.pt")

image_path = "test_img_1.jpg"

crumple_results = crumple_model(image_path, save=True)
stain_results = stain_model(image_path, save=True)
bed_results = bed_model(image_path, save=True)

results = [crumple_results, stain_results, bed_results]

# detection_results: [Bed present, Crumple present, Stain present]
detection_results = [False, False, False]

stain_list = [
    "broken-end",
    "coffee-stain",
    "double-ends",
    "double-picks",
    "hole",
    "ink-stain",
    "kn",
    "knot",
    "missing-picks",
    "oil-stain",
    "pin-marks",
    "slip-knot",
    "stain",
    "thread-out",
    "tiny-hole",
]

bed_box = {"x1": None, "y1": None, "x2": None, "y2": None}


stain_boxes = []
crumple_detected = False

for result in results:
    for r in result:
        boxes = r.boxes
        names = r.names

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy.int().tolist()[0]
            class_id = int(box.cls)
            confidence = float(box.conf)
            class_name = names[class_id].lower()

            print(
                f"Object: {class_name}, Coordinates: ({x1}, {y1}, {x2}, {y2}), Confidence: {confidence:.2f}"
            )

            # Bed detected
            if class_name == "bed":
                detection_results[0] = True
                bed_box = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

            # Crumple detected
            elif class_name == "crumpled":
                crumple_detected = True

            # Save stain boxes for later checking
            elif class_name in stain_list:
                stain_boxes.append((x1, y1, x2, y2))


def is_inside(inner, outer):
    """Return True if inner box lies fully inside outer box."""
    ix1, iy1, ix2, iy2 = inner
    ox1, oy1, ox2, oy2 = outer
    return ix1 >= ox1 and iy1 >= oy1 and ix2 <= ox2 and iy2 <= oy2


if detection_results[0]:
    for sbox in stain_boxes:
        if is_inside(
            sbox, (bed_box["x1"], bed_box["y1"], bed_box["x2"], bed_box["y2"])
        ):
            detection_results[2] = True
            break

detection_results[1] = crumple_detected

print("Final detection results:", detection_results)

bed_ready_status = False

if detection_results[0] and (not detection_results[1]) and (not detection_results[1]):
    bed_ready_status = True

print(f"Bed Ready Status {bed_ready_status}")
