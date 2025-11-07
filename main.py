import cv2
from ultralytics import YOLO
import cvzone
from counter import FootfallCounter


def process_video(video_path, output_path, line_pos, orientation):

    # Process video and save output using YOLOv8 footfall counter.

    model = YOLO("yolov8n.pt")
    names = model.names
    counter = FootfallCounter(line_pos=line_pos, orientation=orientation)

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'H264')  
    out = cv2.VideoWriter(output_path, fourcc, 20, (1020, 600))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1020, 600))
        results = model.track(frame, persist=True, classes=[0])

        if results[0].boxes.id is not None:
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

            for track_id, box, class_id in zip(ids, boxes, class_ids):
                x1, y1, x2, y2 = box
                name = names[class_id]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                if orientation == "horizontal":
                    counter.update_horizontal(track_id, cx, cy)
                else:
                    counter.update_vertical(track_id, cx, cy)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cvzone.putTextRect(frame, f'ID {track_id}', (x1, y1), 1, 1)
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

        # Draw overlays
        in_count, out_count = counter.get_counts()
        cvzone.putTextRect(frame, f'In: {in_count}', (40, 60), scale=2, thickness=2,
                           colorT=(255, 255, 255), colorR=(0, 128, 0))
        cvzone.putTextRect(frame, f'Out: {out_count}', (40, 100), scale=2, thickness=2,
                           colorT=(255, 255, 255), colorR=(0, 0, 255))

        if orientation == "horizontal":
            cv2.line(frame, (0, line_pos), (frame.shape[1], line_pos), (255, 0, 255), 2)
        else:
            cv2.line(frame, (line_pos, 0), (line_pos, frame.shape[0]), (255, 0, 255), 2)

        out.write(frame)

    cap.release()
    out.release()

    entry_count, exit_count = counter.get_counts()

    print(f"Processing complete. Saved to {output_path}")
    print(f"Entry count: {entry_count}, Exit count: {exit_count}")

    return entry_count, exit_count
