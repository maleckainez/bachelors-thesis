"""Object detection helpers."""

from __future__ import annotations

from pathlib import Path

from traffic_analyzer.schemas import BoundingBox, DetectionRecord, VideoFrame

DEFAULT_VEHICLE_CLASSES = frozenset({"car", "motorcycle", "bus", "truck"})


class YoloDetector:
    """YOLO-based detector returning normalized detection records.

    Args:
        model_name: YOLO model name or path to model weights.
        confidence_threshold: Minimum confidence required to keep a detection.
        vehicle_classes: Class names accepted by the detector.
    """

    def __init__(
        self,
        model_name: str = "yolo26s.pt",
        confidence_threshold: float = 0.5,
        vehicle_classes: set[str] | frozenset[str] = DEFAULT_VEHICLE_CLASSES,
        device: str = "mps",
    ) -> None:
        """Initialize a YOLO model wrapper."""
        from ultralytics import YOLO

        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold
        self.vehicle_classes = vehicle_classes
        self.device = device

    def detect_from_image(
        self,
        frame: VideoFrame,
        video_name: str | Path,
    ) -> list[DetectionRecord]:
        """Detect vehicles in a single video frame.

        Args:
            frame: Video frame with image data and frame metadata.
            video_name: Name or path identifying the processed video.

        Returns:
            Detection records for accepted vehicle classes.
        """
        detections: list[DetectionRecord] = []
        results = self.model.predict(frame.image, verbose=False, device=self.device)

        for result in results:
            class_names = result.names
            if result.boxes is None:
                continue

            for box in result.boxes:
                confidence = float(box.conf[0])
                if confidence < self.confidence_threshold:
                    continue

                class_id = int(box.cls[0])
                class_name = class_names[class_id]
                if class_name not in self.vehicle_classes:
                    continue

                x1, y1, x2, y2 = [float(value) for value in box.xyxy[0].tolist()]
                detections.append(
                    DetectionRecord(
                        video_name=Path(video_name).stem,
                        frame_id=frame.frame_id,
                        timestamp_seconds=frame.timestamp_seconds,
                        bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                        confidence=confidence,
                        class_name=class_name,
                    )
                )

        return detections
