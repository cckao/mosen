from collections import deque

MIN_MAX_SIZE = 2


class FrameQueue:
    def __init__(self, maxSize, cap):
        if maxSize < MIN_MAX_SIZE:
            raise
        self.d = deque(maxlen=maxSize)
        self.cap = cap

    def update(self):
        while len(self.d) <= self.d.maxlen:
            r1, r2 = self.cap.read()
            if not r1:
                raise
            self.d.append(r2)

            if len(self.d) == self.d.maxlen:
                return list(self.d)

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.update()
        except:
            raise StopIteration
