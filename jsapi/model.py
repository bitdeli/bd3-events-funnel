from itertools import chain
from bitdeli.model import model

MAX_URL = 64

# Customize to hide domain from page views
# Example: "bitdeli.com"
URL_DOMAIN = ""

def event_names(events):
    for tstamp, group, ip, event in events:
        name = event.get('$event_name', None)
        if name == '$dom_event':
            name = event.get('$event_label', None)
        elif name == '$pageview':
            if not event.get('$page', ''):
                return
            url = event['$page']
            splitter = URL_DOMAIN if URL_DOMAIN else 'http://'
            if splitter in url:
                url = url.split(splitter, 1)[1]
            url = ('...' + url[-MAX_URL:]) if len(url) > MAX_URL else url
            name = 'Page: %s' % url
        if name:
            yield name

def get_names(events, name):
    for tstamp, group, ip, event in events:
        if name in event:
            yield event[name]

@model
def build(profiles):
    for profile in profiles:
        source_events = chain(profile.get('events', []),
                              profile.get('$dom_event', []),
                              profile.get('$pageview', []))
        uid = profile.uid
        for event in frozenset(event_names(source_events)):
            yield event, uid