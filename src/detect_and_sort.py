#!/usr/bin/env python3
"""Run YOLO waste detection and send sorting commands to an ESP32 controller."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import cv2
import requests
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weights', required=True, help='Path to custom YOLO weights (.pt)')
    parser.add_argument('--esp32-url', required=True, help='ESP32 base URL, e.g. http://192.168.1.50:8080')
    parser.add_argument('--class-map', default='config/class_map.json', help='JSON mapping model labels to sorting categories')
    parser.add_argument('--camera', type=int, default=0, help='OpenCV camera index (default: 0)')
    parser.add_argument('--confidence', type=float, default=0.55, help='Minimum detection confidence (default: 0.55)')
    parser.add_argument('--cooldown', type=float, default=3.0, help='Minimum seconds between servo commands')
    return parser.parse_args()


def load_class_map(path: Path) -> tuple[set[str], set[str]]:
    if not path.is_file():
        raise FileNotFoundError(
            f'Class map not found: {path}. Copy config/class_map.example.json to config/class_map.json.'
        )
    data = json.loads(path.read_text(encoding='utf-8'))
    recyclable = {str(label).strip().lower() for label in data.get('recyclable', [])}
    non_recyclable = {str(label).strip().lower() for label in data.get('non_recyclable', [])}
    overlap = recyclable & non_recyclable
    if overlap:
        raise ValueError(f'Labels cannot belong to both groups: {sorted(overlap)}')
    if not recyclable and not non_recyclable:
        raise ValueError('Add your model class names to the class map before running.')
    return recyclable, non_recyclable


def category_for(label: str, recyclable: set[str], non_recyclable: set[str]) -> str | None:
    normalized = label.strip().lower()
    if normalized in recyclable:
        return 'recyclable'
    if normalized in non_recyclable:
        return 'not-recyclable'
    return None


def send_sort_command(base_url: str, category: str) -> None:
    endpoint = f"{base_url.rstrip('/')}/{category}"
    response = requests.get(endpoint, timeout=3)
    response.raise_for_status()
    print(f'ESP32 response: {response.text.strip()}')


def get_label(names: Any, class_id: int) -> str:
    if isinstance(names, dict):
        return str(names.get(class_id, class_id))
    return str(names[class_id])


def main() -> int:
    args = parse_args()
    if not 0.0 <= args.confidence <= 1.0:
        print('Error: --confidence must be between 0 and 1.', file=sys.stderr)
        return 2
    if args.cooldown < 0:
        print('Error: --cooldown cannot be negative.', file=sys.stderr)
        return 2

    try:
        recyclable, non_recyclable = load_class_map(Path(args.class_map))
        model = YOLO(args.weights)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f'Could not load configuration or model: {exc}', file=sys.stderr)
        return 1

    camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened():
        print(f'Could not open camera index {args.camera}.', file=sys.stderr)
        return 1

    last_command_at = 0.0
    print("Camera running. Press 'q' in the video window to quit.")
    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print('Could not read a frame from the camera.', file=sys.stderr)
                break

            result = model.predict(frame, conf=args.confidence, verbose=False)[0]
            best: tuple[float, str, str] | None = None

            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    label = get_label(result.names, class_id)
                    category = category_for(label, recyclable, non_recyclable)
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    caption = f'{label} {confidence:.2f}'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (40, 180, 90), 2)
                    cv2.putText(frame, caption, (x1, max(20, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 180, 90), 2)
                    if category and (best is None or confidence > best[0]):
                        best = (confidence, label, category)

            if best:
                confidence, label, category = best
                cv2.putText(frame, f'Sort: {category} ({label})', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 220), 2)
                now = time.monotonic()
                if now - last_command_at >= args.cooldown:
                    try:
                        send_sort_command(args.esp32_url, category)
                        last_command_at = now
                    except requests.RequestException as exc:
                        print(f'Could not reach ESP32: {exc}', file=sys.stderr)
            else:
                cv2.putText(frame, 'No mapped waste class detected', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 165, 255), 2)

            cv2.imshow('Smart Waste Segregation', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())