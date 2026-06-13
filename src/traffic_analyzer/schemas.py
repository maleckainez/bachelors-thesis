"""Pydantic models for detections, tracks, and video metadata."""

from __future__ import annotations

from pydantic import BaseModel, model_validator


class BoundingBox(BaseModel):
    """Axis-aligned bounding box in pixel coordinates.

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
        """Validate coordinate order and non-negative bounds.

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
            raise ValueError("x2 must be greater than x1")
        if self.y2 <= self.y1:
            raise ValueError("y2 must be greater than y1")
        return self


class DetectionRecord(BaseModel):
    """Single detection produced by an object detection model.

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
    """Tracked object observation for a single frame.

    Attributes:
        video_name: Name of the processed video.
        track_id: Index of the track in the video.
        frame_id: Index of the video frame.
        timestamp_seconds: Timestamp of the frame in seconds.
        bbox: Tracked object bounding box.
        confidence: Confidence score associated with the observation.
        class_name: Predicted object class name.
    """

    video_name: str
    track_id: int
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
        duration_frames: Number of frames covered by the track.
        final_class: Final class assigned to the track.
        mean_confidence: Mean confidence score across track observations.
    """

    video_name: str
    track_id: int
    start_frame: int
    end_frame: int
    duration_frames: int
    final_class: str
    mean_confidence: float


class GpsMeta(BaseModel):
    """GPS metadata associated with a video recording.

    Attributes:
        gps_time: GPS timestamp in seconds.
        gps_lat: Latitude in decimal degrees.
        gps_lon: Longitude in decimal degrees.
    """

    gps_time: float
    gps_lat: float
    gps_lon: float


class VideoMeta(BaseModel):
    """Metadata describing a processed video file.

    Attributes:
        video_name: Name or identifier of the video.
        fps: Frames per second.
        width: Frame width in pixels.
        height: Frame height in pixels.
        frame_count: Total number of frames.
        creation_time: Video creation timestamp, when available.
        duration_seconds: Duration of the video in seconds.
        gps: Optional GPS metadata associated with the recording.
    """

    video_name: str
    fps: float
    width: int
    height: int
    frame_count: int
    creation_time: float | None
    duration_seconds: float
    gps: GpsMeta | None
