"""Shared data structures for detections, tracks and benchmark results."""

from __future__ import annotations

from pydantic import BaseModel, model_validator


class BoundingBox(BaseModel):
    """Bounding box coordinates in pixel space.

    Attributes:
        x1: Left coordinate of the box.
        y1: Top coordinate of the box.
        x2: Right coordinate of the box.
        y2: Bottom coordinate of the box.
    """

    x1: float
    y1: float
    x2: float
    y2: float

    @classmethod
    @model_validator(mode="after")
    def validate_coordinates(self) -> "BoundingBox":
        """Validate bounding box coordinate order and bounds.

        Raises:
            ValueError: If coordinates are negative or do not define a valid box.

        Returns:
            The validated bounding box instance.
        """
        if min(self.x1, self.y1, self.x2, self.y2) < 0:
            raise ValueError(
                "Bounding Box out of bounds! Coordinates can't have negative values"
            )
        if self.x2 <= self.x1:
            raise ValueError("x2 must be grater than x1")
        if self.y2 <= self.y1:
            raise ValueError("y2 must be grater than y1")
        return self


class DetectionRecord(BaseModel):
    """Single detection returned by an object detection model.

    Attributes:
        video_name: Name of the processed video.
        frame_id: Index of the video frame.
        timestamp_seconds: Timestamp of the frame in seconds.
        bbox: Detected object bounding box.
        confidence: Detection confidence score.
        class_name: Predicted object class name.
    """

    video_name: str
    frame_id: int
    timestamp_seconds: float
    bbox: BoundingBox
    confidence: float
    class_name: str


class TrackObservation(BaseModel):
    """Tracked object observation for one frame.

    Attributes:
        video_name: Name of the processed video.
        frame_id: Index of the video frame.
        timestamp_seconds: Timestamp of the frame in seconds.
        bbox: Tracked object bounding box.
        confidence: Confidence score associated with the observation.
        class_name: Predicted object class name.
    """

    video_name: str
    frame_id: int
    timestamp_seconds: float
    bbox: BoundingBox
    confidence: float
    class_name: str


class TrackSummary(BaseModel):
    """Summary of one tracked object across a video segment.

    Attributes:
        video_name: Name of the processed video.
        track_id: Unique identifier assigned by the tracker.
        start_frame: First frame where the track appears.
        end_frame: Last frame where the track appears.
        dutarion_frames: Number of frames covered by the track.
        final_class: Final class assigned to the track.
        mean_confidence: Mean confidence score across track observations.
    """

    video_name: str
    track_id: int
    start_frame: int
    end_frame: int
    dutarion_frames: int
    final_class: str
    mean_confidence: float
