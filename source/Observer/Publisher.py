from Subscriber import Subscriber


class Publisher:
    """
    A Publisher will send an event (a piece of information) to his subscribers.
    The main idea is that almost anyone in the code will have access to the publisher, and so, they will be able to
    send information to the subscribers.
    """
    def __init__(self):
        self.subscribers = set()

    def add_subscriber(self, subscriber):
        assert isinstance(subscriber, Subscriber), "subscriber must be a sub-class of Subscriber"
        self.subscribers.add(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)
