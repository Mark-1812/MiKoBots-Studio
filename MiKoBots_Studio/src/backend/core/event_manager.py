class EventManager:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, listener):
        """Subscribe a listener to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(listener)

    def publish(self, event_type, *args):
        """Publish an event to all listeners."""
        results = []
        if event_type in self.subscribers:
            for listener in self.subscribers[event_type]:
                 result = listener(*args)
                 if result is not None:
                    results.append(result)  # Collect non-None results
        return results  # Return all collected results

# Create a global instance of the EventManager
event_manager = EventManager()