from enum import Enum

class SeleniumCode(Enum):
    DRIVER_INIT_ERROR = 0
    INVALID_LOGIN = 1
    NO_CLASS = 2
    PRESENCE_NOT_OPENED_YET = 3
    SUCCESS = 4
    PRESENCE_ALREADY_FILLED = 5

    message = {
        DRIVER_INIT_ERROR: "Failed to init driver",
        INVALID_LOGIN: "Invalid password",
        NO_CLASS: "There's currently no class",
        PRESENCE_NOT_OPENED_YET: "Presence form not opened yet",
        SUCCESS: "Presence form filled successfully",
        PRESENCE_ALREADY_FILLED: "Presence form already filled",
    }

class RequestCode():
    INVALID_LOGIN = 1
    PRESENCE_NOT_OPEN = 2
    PRESENCE_FILLED = 3
    SUCCESS = 4
    NO_CLASS = 5

class RequestCodeMessage():
    INVALID_LOGIN = "Invalid credentials"
    PRESENCE_NOT_OPEN = "Presence form not open for this class"
    PRESENCE_FILLED = "Presence form already filled"
    SUCCESS = "Presence form filled successfully"
    NO_CLASS = "There's currently no class"

