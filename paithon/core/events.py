from abc import ABCMeta, abstractmethod


class EventListener(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def on_event(self, event, source, params):
        pass


class EventDispatcherMixin(object):
    def __init__(self):
        self._event_listeners = {}

    def add_event_listener(self, event, listener):
        if not hasattr(self, '_event_listeners'):
            self._event_listeners = {}
        self._event_listeners.setdefault(event, []).append(listener)

    def remove_event_listener(self, event, listener):
        if not hasattr(self, '_event_listeners'):
            self._event_listeners = {}
        listeners = self._event_listeners.get(event, [])
        try:
            listeners.remove(listener)
        except ValueError:
            raise ValueError('EventDispatcher.remove_listener: listener not on list')

    def trigger_event(self, event, params):
        if not hasattr(self, '_event_listeners'):
            self._event_listeners = {}
        for listener in self._event_listeners.get(event, []):
            listener.on_event(event, self, params)

    def trigger_ev(self, event, **params):
        self.trigger_event(event, params)
