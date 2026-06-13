"""Video input/output helpers.

Todo:
- open a video file,
- iterate over frames,
- expose frame number and timestamp,
- read basic video metadata.
"""

import os
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from traffic_analyzer.schemas import VideoMeta


@dataclass(frozen=True)
class VideoFrame:
    """Single frame read from a video file.

    Attributes:
        frame_id: Zero-based index of the frame within the video.
        timestamp_seconds: Presentation timestamp of the frame in seconds.
        image: Frame image in BGR format as returned by OpenCV.
    """

    frame_id: int
    timestamp_seconds: float
    image: np.ndarray


def get_video_meta(video_path: str | Path) -> VideoMeta:
    """Extract basic metadata from a video file.

    Args:
        video_path: Path to the video file.

    Raises:
        FileNotFoundError: If the file does not exist or cannot be opened.

    Returns:
        Video metadata populated from OpenCV properties.
    """
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError("Video file not found!")

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise FileNotFoundError("Video file not opened properly")

    fps = video.get(cv2.CAP_PROP_FPS)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    creation_time = os.path.getctime(video_path)
    duration_seconds = (frame_count / fps) if fps > 0 else 0

    meta = VideoMeta(
        video_name=video_path.stem,
        fps=fps,
        width=int(width),
        height=int(height),
        frame_count=int(frame_count),
        creation_time=creation_time,
        duration_seconds=duration_seconds,
        gps=None,
    )
    video.release()
    return meta


def iterate_video_frames(video_path: str | Path, max_frames: int | None = None):
    """Iterate over frames in a video file.

    Args:
        video_path: Path to the video file.
        max_frames: Optional maximum number of frames to yield.

    Raises:
        FileNotFoundError: If the file does not exist or cannot be opened.

    Yields:
        VideoFrame objects in sequential order.
    """
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError("Video file not found!")

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise FileNotFoundError("Video file not opened properly")

    frame_id = 0
    try:
        while True:
            success, frame = video.read()
            if not success:
                break
            if max_frames is not None and frame_id >= max_frames:
                break
            timestamp_ms = video.get(cv2.CAP_PROP_POS_MSEC)
            timestamp_seconds = timestamp_ms / 1000.0

            yield VideoFrame(
                frame_id=frame_id, timestamp_seconds=timestamp_seconds, image=frame
            )
            frame_id += 1
    finally:
        video.release()
