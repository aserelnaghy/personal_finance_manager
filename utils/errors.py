class UserNotFoundError(Exception):
    """Raised when a user cannot be found in the database."""
    pass

class InvalidTransactionError(Exception):
    """Raised when a transaction has invalid or missing data."""
    pass

class DataPersistenceError(Exception):
    """Raised when saving or loading data fails."""
    pass

class AuthenticationError(Exception):
    """Raised when login or password verification fails."""
    pass

class InvalidDateError(Exception):
    """Raised when a date is in an incorrect format or out of range."""
    pass

class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user that already exists."""
    pass
