#!/usr/bin/env python

import argparse
import cv2
import captures
import errno
import FrameQueue
import os


def absDiff(frames, thr):
    rets = []
    nextFrames = frames[1:]
    for i, j in zip(frames, nextFrames):
        rets.append(cv2.threshold(cv2.absdiff(i, j), thr, 1,
                                  cv2.THRESH_BINARY)[-1])
    return rets


def changeRate(diffs):
    ret = diffs[0]
    for diff in diffs:
        ret = cv2.bitwise_and(ret, diff)
    return ret.sum() / (float)(ret.size)


def imPath(dirPath, i):
    return os.path.join(dirPath, str(i).zfill(5) + '.jpg')


def saveMid(frames, imPath):
    cv2.imwrite(imPath, frames[len(frames) / 2])


if '__main__' == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument('--vid', help='path to the video file')
    ap.add_argument('--imdir', help='path to the image directory')
    ap.add_argument('--step', type=int, default=3, help='''
                    number of consecutive frames used to detect differences
                    ''')
    ap.add_argument('--diffthr', type=int, default=30, help='''
                    label a pixel changed if the absolute difference exceeds
                    this threshold
                    ''')
    ap.add_argument('--cr', type=float, default=0.00001, help='''
                    motion detected if the ratio of changed pixels in the
                    frame exceeds this threshold
                    ''')
    ap.add_argument('--out', default='out', help='output directory')
    ap.add_argument('--cid', type=int, default=0, help='camera id')
    ap.add_argument('--keepFileName', action='store_true', help='''
                    if the source is image squence, using originmal file name.
                    ''')
    args = ap.parse_args()

    # use video stream first
    cap = cv2.VideoCapture(args.vid)
    if not cap.isOpened():
        cap.open(args.cid)

    # use image sequence
    if not cap.isOpened():
        cap = captures.FileCapture(args.imdir)

    try:
        os.makedirs(args.out)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if isinstance(cap, captures.FileCapture) and args.keepFileName:
        # this section should be refectored
        if args.step < 2:
            raise

        from collections import deque
        names = deque(maxlen=args.step)
        fs = deque(maxlen=args.step)

        while len(fs) <= fs.maxlen:
            if len(cap._imgs) > 0:
                name = cap._imgs[0]

            r1, r2 = cap.read()
            if not r1:
                break
            names.append(name)
            fs.append(r2)

            if len(fs) == fs.maxlen:
                if changeRate(absDiff(list(fs), args.diffthr)) > args.cr:
                    saveMid(fs, os.path.join(args.out, names[len(fs) / 2]))
    else:
        i = 0
        for fs in FrameQueue.FrameQueue(args.step, cap):
            if changeRate(absDiff(fs, args.diffthr)) > args.cr:
                saveMid(fs, imPath(args.out, i))
                i = i + 1
