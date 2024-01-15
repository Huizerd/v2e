import argparse
from pathlib import Path

import h5py
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_file", type=str)
    parser.add_argument("frame_dir", type=str)
    parser.add_argument("output_dir", type=str)
    args = parser.parse_args()

    event_file = Path(args.event_file)
    frame_dir = Path(args.frame_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    with h5py.File(event_file, "r") as f:
        events = f["events"][()]  # N, (ts, x, y, p)
    
    gt = {"position": [], "euler": [], "time": []}
    for i, _ in enumerate(frame_dir.glob("*.hdf5")):
        path = frame_dir / f"{i}.hdf5"
        with h5py.File(path, "r") as f:
            gt["position"].append(f["pos"][()])
            gt["euler"].append(f["euler"][()])
            gt["time"].append(f["time"][()])

    gt["position"] = np.stack(gt["position"])
    gt["euler"] = np.stack(gt["euler"])
    gt["time"] = (np.stack(gt["time"]) / 20 * 1e6).astype(int)  # 20 fps to ms

    seq_name = f"{event_file.parent.parent.stem}_{event_file.parent.stem}".replace("-", "_")
    with h5py.File(output_dir / f"{seq_name}.h5", "w") as f:
        f.create_dataset("events/ts", data=events[:, 0])
        f.create_dataset("events/xs", data=events[:, 1])
        f.create_dataset("events/ys", data=events[:, 2])
        f.create_dataset("events/ps", data=events[:, 3])

        f.create_dataset("position/ts", data=gt["time"])
        f.create_dataset("position/x", data=gt["position"][:, 0])
        f.create_dataset("position/y", data=gt["position"][:, 1])
        f.create_dataset("position/z", data=gt["position"][:, 2])

        f.create_dataset("euler/ts", data=gt["time"])
        f.create_dataset("euler/x", data=gt["euler"][:, 0])
        f.create_dataset("euler/y", data=gt["euler"][:, 1])
        f.create_dataset("euler/z", data=gt["euler"][:, 2])

        f.attrs["t0"] = 0
