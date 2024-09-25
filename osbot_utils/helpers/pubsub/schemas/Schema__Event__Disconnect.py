from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event

class Schema__Event__Disconnect(Schema__Event):
    event_type : str  = 'disconnect'