import sys
from paithon.utils.core import AbstractMethodError


class ProgressBroadcaster(object):
    def trigger_task_start(self, length, task, params):
        pass

    def trigger_task_progress(self, progress, task):
        pass

    def trigger_task_end(self, task):
        pass


class ProgressEventListener(object):
    def on_start(self, length, task, params):
        raise AbstractMethodError()

    def on_progress(self, progress, task):
        raise AbstractMethodError()

    def on_end(self, task):
        raise AbstractMethodError()


class TaskProgress(object):
    def __init__(self, task, length, params):
        self._task = task
        self._length = length
        self._params = params
        self._progress = 0

    def set_progress(self, progress):
        self._progress = progress


class BaseProgressor(ProgressEventListener):
    def __init__(self):
        self._events = []

    def on_start(self, length, task, params):
        self._events.append(TaskProgress(task, length, params))

    def on_progress(self, progress, task):
        self._events[-1].set_progress(progress)

    def on_end(self, task):
        assert(self._events[-1]._task == task)
        self.on_progress(self._events[-1]._length, task)
        self._events.pop()

    def log(self, task, params=None):
        self.on_start(1, task, params)
        self.on_end(task)


class DummyProgressor(BaseProgressor):
    def on_start(self, length, name, params):
        pass

    def on_progress(self, progress):
        pass

    def on_end(self, progress):
        pass


class StdoutProgressor(BaseProgressor):
    def on_start(self, length, task, params):
        super(StdoutProgressor, self).on_start(length, task, params)
        sys.stdout.write('%s... ' % self.get_name())
        sys.stdout.flush()

    def on_progress(self, progress, task):
        event = self._events[-1]
        old_percent_progress = int(event._progress * 100.0 / event._length)
        new_percent_progress = int(progress * 100.0 / event._length)

        if (old_percent_progress < new_percent_progress
                    or new_percent_progress == 0):
            sys.stdout.write(self.get_progressbar_str(new_percent_progress))
            sys.stdout.flush()
        super(StdoutProgressor, self).on_progress(progress, task)

    def get_name(self):
        event = self._events[-1]
        if event._params is not None:
            return '%s(%s)' % (event._task, event._params)
        else:
            return '%s' % (event._task)

    def get_progressbar_str(self, percent):
        if percent == 100:
            return 'done\n'
        else:
            return '%3d%%\b\b\b\b' % percent
