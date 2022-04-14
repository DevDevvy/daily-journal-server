class Entry():

    # Class initializer.
    # needs self as the first parameter.
    def __init__(self, id, concept, entry, mood_id, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.date = date
        self.mood = None