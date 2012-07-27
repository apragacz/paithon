from paithon.core.events import EventDispatcherMixin

EVENT_TASK_INFO = 'task_info'

SUBTYPE_START = 'start'
SUBTYPE_PROGRESS = 'progress'
SUBTYPE_END = 'end'


class TaskInfo(EventDispatcherMixin):

    def __init__(self, name, length=1):
        self._name = name
        self._length = max([length, 1])
        self._progress = 0

    def set_length(self, length):
        self._length = max([length, 1])

    def signal_start(self):
        self.trigger_ev(EVENT_TASK_INFO, subtype=SUBTYPE_START)
        self.trigger_ev(EVENT_TASK_INFO, subtype=SUBTYPE_PROGRESS,
                                            progress=self._progress)

    def signal_progress(self, progress):
        self._progress = min([progress, self._length])
        self.trigger_ev(EVENT_TASK_INFO, subtype=SUBTYPE_PROGRESS,
                                            progress=self._progress)

    def signal_end(self, progress):
        self._progress = self._length
        self.trigger_ev(EVENT_TASK_INFO, subtype=SUBTYPE_PROGRESS,
                                            progress=self._progress)
        self.trigger_ev(EVENT_TASK_INFO, subtype=SUBTYPE_END)

    @property
    def length(self):
        return self._length

    @property
    def name(self):
        return self._name

    @property
    def progress(self):
        return self._progress

    @property
    def fraction_progress(self):
        return self._progress / float(self._length)

    @property
    def percent_progress(self):
        return int(100.0 * (self._progress / float(self._length)))
