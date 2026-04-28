from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "ToBeDetect"
OUTPUT_DIR = ROOT / "EdgeResults"

IMAGES = {
    "windmill": {
        "path": INPUT_DIR / "windmill.webp",
        "kind": "general",
    },
    "brain": {
        "path": INPUT_DIR / "brain.webp",
        "kind": "medical",
    },
}


def read_image(path: Path) -> np.ndarray:
    data = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Failed to decode image: {path}")
    return image


def preprocess_general(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (5, 5), 1.0)


def preprocess_medical(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    denoise = cv2.medianBlur(gray, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoise)
    return cv2.GaussianBlur(enhanced, (5, 5), 1.0)


def normalize_uint8(image: np.ndarray) -> np.ndarray:
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def sobel_edges(gray: np.ndarray) -> np.ndarray:
    sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = cv2.magnitude(sx, sy)
    return normalize_uint8(mag)


def laplacian_edges(gray: np.ndarray) -> np.ndarray:
    lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
    return normalize_uint8(np.abs(lap))


def canny_edges(gray: np.ndarray) -> np.ndarray:
    med = float(np.median(gray))
    lower = int(max(0, 0.66 * med))
    upper = int(min(255, 1.33 * med))
    return cv2.Canny(gray, lower, upper)


def log_edges(gray: np.ndarray) -> np.ndarray:
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    lap = cv2.Laplacian(blur, cv2.CV_64F, ksize=3)
    abs_lap = normalize_uint8(np.abs(lap))
    _, binary = cv2.threshold(abs_lap, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def save_image(path: Path, img: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    ok, encoded = cv2.imencode(ext if ext else ".png", img)
    if not ok:
        raise ValueError(f"Failed to encode image: {path}")
    path.write_bytes(encoded.tobytes())


def make_panel(original_bgr: np.ndarray, preprocessed: np.ndarray, results: dict[str, np.ndarray]) -> np.ndarray:
    h, w = preprocessed.shape[:2]

    original = cv2.resize(original_bgr, (w, h), interpolation=cv2.INTER_AREA)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    tiles = [
        ("Original", original),
        ("Preprocessed", preprocessed),
        ("Sobel", results["sobel"]),
        ("Laplacian", results["laplacian"]),
        ("Canny", results["canny"]),
        ("LoG", results["log"]),
    ]

    canvases: list[np.ndarray] = []
    for title, img in tiles:
        canvas = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.putText(canvas, title, (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
        canvases.append(canvas)

    row1 = np.hstack(canvases[:3])
    row2 = np.hstack(canvases[3:])
    return np.vstack([row1, row2])


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, meta in IMAGES.items():
        bgr = read_image(meta["path"])

        if meta["kind"] == "medical":
            gray = preprocess_medical(bgr)
        else:
            gray = preprocess_general(bgr)

        results = {
            "sobel": sobel_edges(gray),
            "laplacian": laplacian_edges(gray),
            "canny": canny_edges(gray),
            "log": log_edges(gray),
        }

        image_out_dir = OUTPUT_DIR / name
        image_out_dir.mkdir(parents=True, exist_ok=True)

        save_image(image_out_dir / "00_original_gray.png", cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY))
        save_image(image_out_dir / "01_preprocessed.png", gray)
        save_image(image_out_dir / "02_sobel.png", results["sobel"])
        save_image(image_out_dir / "03_laplacian.png", results["laplacian"])
        save_image(image_out_dir / "04_canny.png", results["canny"])
        save_image(image_out_dir / "05_log.png", results["log"])

        panel = make_panel(bgr, gray, results)
        save_image(image_out_dir / "comparison_panel.png", panel)

    print(f"Edge detection completed. Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run()
