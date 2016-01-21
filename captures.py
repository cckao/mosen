import cv2
import os


class FileCapture:
    def __init__(self, im_dir):
        self.open(im_dir)

    def isOpened(self):
        return self._imgs is not None

    def read(self):
        if not self.isOpened():
            return False, None

        # read files until an image is loaded
        im = None
        while len(self._imgs) > 0 and im is None:
            # not empty image list and no image is read
            im = cv2.imread(os.path.join(self._im_dir, self._imgs[0]), -1)
            del self._imgs[0]

        return im is not None, im

    def open(self, im_dir):
        if os.path.isdir(im_dir):
            self._im_dir = im_dir
            self._imgs = [f for f in os.listdir(self._im_dir)
                          if os.path.isfile(os.path.join(self._im_dir, f))]
            self._imgs.sort()
        else:
            self._imgs = None
