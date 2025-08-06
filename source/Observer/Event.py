class Event:
    """ An event, is a piece of information. It is used as a message for a Subscriber (in the Observer pattern) """
    def __init__(self, name: str, infos: dict[str, object]):
        self.name = name
        self.infos = infos

