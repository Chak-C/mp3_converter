class Mediator:
    def __init__(self):
        self.item = None
        self.subscriber = []

    def subscribe(self, subscriber):
        self.subscriber.append(subscriber)

    def set_item(self, item):
        self.item = item
        self.notify()

    def notify(self):
        for subscriber in self.subscriber:
            subscriber.update(self.item)