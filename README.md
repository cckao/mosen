# mosen
Motion detection algorithms

## diffdet.py
Detect motion by absolute differences of frames. Suitable for a stationary camera.

It finds the input source in the following order: video file (--vid), camera (--cid), image sequence (--imdir).

`./diffdet.py --vid <path/to/vid> --diffthr <threshold> --cr <ratio_of_changed_pixels> --out <path/to/output>`

`./diffdet.py -h` for more information.
