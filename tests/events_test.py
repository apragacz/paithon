from unittest import TestCase

from paithon.core.events import EventDispatcherMixin, EventListener


class EventListenerSample(EventListener):

    def __init__(self):
        self._observed_events = []

    def on_event(self, event, source, params):
        self._observed_events.append((event, source, params))

    def get_observed_events(self):
        return self._observed_events


class EventDispatcherSample(EventDispatcherMixin):
    def __init__(self):
        pass


class EventsTestCase(TestCase):

    def test_simple(self):
        a = EventDispatcherSample()
        b = EventListenerSample()
        c = EventListenerSample()

        a.trigger_ev('event1', param1='a')
        a.trigger_ev('event2', param1='b')

        self.assertRaises(ValueError, lambda: a.remove_event_listener('event1',
                                                                        b))
        del a.__dict__['_event_listeners']

        self.assertRaises(ValueError, lambda: a.remove_event_listener('event1',
                                                                        b))

        del a.__dict__['_event_listeners']

        a.add_event_listener('event1', b)
        a.add_event_listener('event2', c)

        a.trigger_ev('event1', param1='c')
        a.trigger_ev('event2', param1='d')
        a.trigger_ev('event1', param1='c', param2='q')
        a.trigger_ev('event2', param1='d', param2='w')
        a.trigger_event('event1', {'param1': 'e'})
        a.trigger_event('event2', {'param1': 'f'})

        a.remove_event_listener('event1', b)

        a.trigger_event('event1', {'param1': 'g'})
        a.trigger_event('event2', {'param1': 'h'})

        self.assertRaises(ValueError, lambda: a.remove_event_listener('event1',
                                                                        c))
        a.remove_event_listener('event2', c)

        self.assertListEqual(b.get_observed_events(), [
            ('event1', a, {'param1': 'c'}),
            ('event1', a, {'param1': 'c', 'param2': 'q'}),
            ('event1', a, {'param1': 'e'}),
        ])
        self.assertListEqual(c.get_observed_events(), [
            ('event2', a, {'param1': 'd'}),
            ('event2', a, {'param1': 'd', 'param2': 'w'}),
            ('event2', a, {'param1': 'f'}),
            ('event2', a, {'param1': 'h'}),
        ])
