import attr

@attr.attrs(slots=True, auto_attribs=True)
class Mind:
    thought: str = "The mind is a blank canvas."
