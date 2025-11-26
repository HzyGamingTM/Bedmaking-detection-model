from ultralytics import YOLO
from statistics import median
import cv2
import torch

crumple_model = YOLO("crumple.pt")
stain_model = YOLO("stain.pt")
bed_model = YOLO("yolov8m.pt")
placement_model = YOLO("placement.pt")

image_path = input('img file name?') 

crumple_results = crumple_model(image_path, save=True)
stain_results = stain_model(image_path, save=True)
bed_results = bed_model(image_path, save=True)
placement_results = placement_model(image_path, save=True)

results = [crumple_results, stain_results, bed_results, placement_results]

# detection_results: [bed presence, crumple ,stain count, pillow, blanket, foriegnobj count]
detection_results = [False, False, 0, False, False, 0]

stain_list = [
  "broken-end", "coffee-stain", "double-ends", "double-picks", "hole", 
  "ink-stain", "kn", "knot", "missing-picks", "oil-stain", "pin-marks", 
  "slip-knot", "stain", "thread-out", "tiny-hole"
]

others_list = [
    "pillow", "blanket", "bolster", "uncrumpled", "pillow incorrect", "blanket incorrect"
]

bed_box = {"x1": None, "y1": None, "x2": None, "y2": None}


stain_boxes = []
foriegnobj_boxes = []
crumple_detected = False
pillow_placement = False
blanket_placement = False

for result in results:
    for r in result:
        boxes = r.boxes
        names = r.names

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy.int().tolist()[0]
            class_id = int(box.cls)
            confidence = float(box.conf)
            class_name = names[class_id].lower()

            print(f"Object: {class_name}, Coordinates: ({x1}, {y1}, {x2}, {y2}), Confidence: {confidence:.2f}")

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
                
            elif class_name == "pillow correct":
                pillow_placement = True
            
            elif class_name == "blanket correct":
                blanket_placement = True
             
            elif class_name in others_list:
                pass
                
            else:
                foriegnobj_boxes.append((x1, y1, x2, y2))
                

def is_inside(inner, outer):
    """Return True if inner box lies fully inside outer box."""
    ix1, iy1, ix2, iy2 = inner
    ox1, oy1, ox2, oy2 = outer
    return ix1 >= ox1 and iy1 >= oy1 and ix2 <= ox2 and iy2 <= oy2

if detection_results[0]:
    for sbox in stain_boxes:
        if is_inside(sbox, (bed_box["x1"], bed_box["y1"], bed_box["x2"], bed_box["y2"])):
            detection_results[2] += 1
            break
    for fbox in foriegnobj_boxes:
        if is_inside(fbox, (bed_box["x1"], bed_box["y1"], bed_box["x2"], bed_box["y2"])):
            detection_results[5] += 1

detection_results[1] = crumple_detected
detection_results[3] = pillow_placement
detection_results[4] = blanket_placement

print("Final detection results:", detection_results)


def count_to_score(count, max):
    if count >= max:
        return 0
    else:
        return (max - count)


if detection_results[0] == False:
    print("Overall score: 0/10")
else:
    score = 1
    if not detection_results[1]:
        score += 3
    if detection_results[3]:
        score += 1
    if detection_results[4]:
        score += 1
    stain_score = count_to_score(detection_results[2], 2)
    foriegnobj_score = count_to_score(detection_results[5], 2)
    score += (stain_score + foriegnobj_score)
    print(f"Overall score: {score}/10")
