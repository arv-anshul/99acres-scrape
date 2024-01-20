class ScrapperError(Exception):
    """Base Exception for all error classes."""


class ResquestsJsonNotFoundError(ScrapperError):
    """Raise when requests.json file not present."""
