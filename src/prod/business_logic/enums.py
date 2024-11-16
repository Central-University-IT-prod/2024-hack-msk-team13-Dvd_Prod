from enum import StrEnum


class TripType(StrEnum):
    AIRPLANE = 'airplane'
    TRAIN = 'train'
    OTHER = 'other'


class TripStatus(StrEnum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    UPCOMING = 'upcoming'
    DETAINED = 'detained'
