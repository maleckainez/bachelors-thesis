"""Tests for object detection helpers."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from traffic_analyzer.detection import YoloDetector
from traffic_analyzer.schemas import VideoFrame


class FakeYoloModel:
    """Fake YOLO model with deterministic prediction output."""

    def __init__(self, model_name: str) -> None:
        """Store the model name passed by the detector wrapper."""
        self.model_name = model_name

    def predict(
        self,
        image: np.ndarray,
        verbose: bool = False,
        device: str | None = None,
    ) -> list[SimpleNamespace]:
        """Return fake detections matching the shape used by Ultralytics."""
        del image, verbose, device
        return [
            SimpleNamespace(
                names={0: "person", 2: "car", 5: "bus"},
                boxes=[
                    SimpleNamespace(
                        conf=np.array([0.90]),
                        cls=np.array([2]),
                        xyxy=np.array([[10, 20, 110, 220]]),
                    ),
                    SimpleNamespace(
                        conf=np.array([0.95]),
                        cls=np.array([0]),
                        xyxy=np.array([[30, 40, 130, 240]]),
                    ),
                    SimpleNamespace(
                        conf=np.array([0.10]),
                        cls=np.array([5]),
                        xyxy=np.array([[50, 60, 150, 260]]),
                    ),
                ],
            )
        ]


def test_yolo_detector_returns_vehicle_detection(monkeypatch) -> None:
    """Detector keeps confident vehicle detections and skips the rest."""
    monkeypatch.setitem(
        __import__("sys").modules,
        "ultralytics",
        SimpleNamespace(YOLO=FakeYoloModel),
    )
    detector = YoloDetector("fake-model.pt", confidence_threshold=0.5)
    frame = VideoFrame(
        frame_id=7,
        timestamp_seconds=0.28,
        image=np.zeros((100, 100, 3), dtype=np.uint8),
    )

    detections = detector.detect_from_image(frame, "data/raw/intersection.mp4")

    assert len(detections) == 1
    detection = detections[0]
    assert detection.video_name == "intersection"
    assert detection.frame_id == 7
    assert detection.timestamp_seconds == 0.28
    assert detection.class_name == "car"
    assert detection.confidence == 0.90
    assert detection.bbox.x1 == 10
    assert detection.bbox.y1 == 20
    assert detection.bbox.x2 == 110
    assert detection.bbox.y2 == 220
