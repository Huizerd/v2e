import argparse
from pathlib import Path

import h5py
from moviepy.editor import ImageSequenceClip, clips_array
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("frame_dir", type=str)
    parser.add_argument("event_file", type=str)
    args = parser.parse_args()

    event_file = Path(args.event_file)
    frame_dir = Path(args.frame_dir)

    with h5py.File(event_file, "r") as f:
        events = f["events"][()]  # N, (ts, x, y, p)
        t0, tk = events[0, 0], events[-1, 0]
        events[:, 0] -= t0
    
    window = 5000  # 5ms in us
    time_window_starts = np.arange(t0, tk, window)
    time_window_ends = time_window_starts + window
    starts = np.searchsorted(events[:, 0], time_window_starts)
    ends = np.searchsorted(events[:, 0], time_window_ends)

    frames = []
    for i, (start, end) in enumerate(zip(starts, ends)):
        # create event count frame
        frame = np.zeros((180, 180, 3))  # rgb, red = neg, green = pos
        np.add.at(frame, (events[start:end, 2], events[start:end, 1], events[start:end, 3]), 1)  # pol in 0, 1

        # scale to [0, 255] per channel
        min_count = 0
        max_count = 1
        # min_count = frame.min(axis=(0, 1))
        # max_count = frame.max(axis=(0, 1))
        frame = ((frame - min_count) / (max_count - min_count) * 255).clip(0, 255).astype(np.uint8)
        frames.append(frame)
    
    # write event frames to video
    event_clip = ImageSequenceClip(frames, fps=200)
    event_clip = event_clip.resize(8)

    # write image frames to video
    image_clip = ImageSequenceClip(frame_dir, fps=20)
    image_clip = image_clip.resize(8)

    # stack clips
    clip = clips_array([[image_clip, event_clip]])
    clip.write_videofile(str(event_file.parent / "event_frame_video.mp4"), codec="libx264", bitrate="30M")
    