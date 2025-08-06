class Model:
    """
    In the architecture MVC (Model View Controller), Model is the Model.
    So it's one of the greatest and more high-level class.

    Model must manage all the in-game elements, and how they interact each other.

    The classes used by Model must have an `update` method and a `draw` method.
    The `update` method must update the values of the object using the inputs of the player.
    The `draw` method must create all the outputs made by the Object. It's important that he MUST NOT change values in
    the Object. We don't want side effects.
    """
