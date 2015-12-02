#!/usr/bin/env python

import argparse
import cv2
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
    ap.add_argument('--step', type=int, default=3,
                    help='number of frames used to detect')
    ap.add_argument('--diffthr', type=int, default=30,
                    help='threshold for diff images')
    ap.add_argument('--cr', type=float, default=0.00001,
                    help='positive if persentage of pixels changed exceeds it')
    ap.add_argument('--out', default='out', help='output directory')
    ap.add_argument('--cid', type=int, default=0, help='camera id')
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.vid)
    if not cap.isOpened():
        cap.open(args.cid)

    try:
        os.makedirs(args.out)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    i = 0
    for fs in FrameQueue.FrameQueue(args.step, cap):
        if changeRate(absDiff(fs, args.diffthr)) > args.cr:
            saveMid(fs, imPath(args.out, i))
            i = i + 1
