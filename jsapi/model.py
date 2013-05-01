from urlparse import urlparse
from itertools import chain
from bitdeli.model import model

MAX_LEN = 64

def event_names(events):
    for tstamp, group, ip, event in events:
        name = event.get('$event_name')
        if name == '$dom_event':
            name = event.get('$event_label')
        elif name == '$pageview':
            name = 'viewed %s' % urlparse(event.get('$page', '')).path
        if name:
            yield name[:MAX_LEN].encode('utf-8')

@model
def build(profiles):
    for profile in profiles:
        source_events = chain(profile.get('events', []),
                              profile.get('$dom_event', []),
                              profile.get('$pageview', []))
        uid = profile.uid
        for event in frozenset(event_names(source_events)):
            yield event, uid