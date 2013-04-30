from bitdeli.model import model

def get_names(events, name):
    for tstamp, group, ip, event in events:
        if name in event:
            yield event[name]

@model
def build(profiles):
    for profile in profiles:
        events = set(get_names(profile.get('events', []),
                               '$event_name'))
        events.update(get_names(profile.get('$dom_event', []),
                                '$event_label'))
        uid = profile.uid
        for event in events:
            yield event, uid