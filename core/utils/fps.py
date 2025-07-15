from core.utils.timer import Timer


class FPS:
    def __init__(self):
        self._cur_time = 0.0
        self._last_time = 0.0
        self._delta_time = 0.0
        self.timer = Timer()


    def update(self):
        self._cur_time = self.timer.elapsed_time()
        
        if self._last_time != 0.0:
            self._delta_time = (self._cur_time - self._last_time)
            self._fps = 1.0 / self._delta_time
        else:
            self._fps = 0.0

        self._last_time = self._cur_time
        
        return self._fps
    
    def reset(self):
        self._last_time = 0.0
        self.timer.reset()



