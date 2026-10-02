# Computer vision: face detection notebooks

[Repository](https://github.com/jeet-biswas/face_detection) |
[Reviewed notebook](https://github.com/jeet-biswas/face_detection/blob/218646ba687f99618af297b8671a6c41e817c2c7/face_detection.ipynb)

This notebook explores image loading, color conversion, face detection, and
bounding-box visualization with OpenCV and Matplotlib.

## What the notebook demonstrates

The progression starts with a manually drawn bounding box and then uses an
OpenCV Haar cascade on individual and group photographs. A pretrained detector
provides candidate face regions, which are drawn over the image for inspection.

```text
Image -> color conversion -> pretrained detector -> boxes -> visualization
```

Detecting a face means locating a region of an image. It does not identify who
the person is. The notebook is a detection exercise, not a face-recognition system
or a custom-trained neural network.

## Reproducibility and evaluation

The reviewed notebook references local image files and an absolute cascade path.
Those inputs must be supplied or made portable before another machine can rerun
the examples. The repository does not establish precision, recall, or robustness
across lighting, pose, occlusion, or camera conditions.

Useful next checks are to replace machine-specific paths, record permitted test
images, compare predicted boxes with labeled examples, and inspect missed and
incorrect detections separately.

The repository also contains an Iris clustering notebook; that is a separate
exercise and should not be interpreted as part of the face detector.

[Back to profile](../../README.md)
