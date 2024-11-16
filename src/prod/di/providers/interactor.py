from dishka import provide_all, Provider, Scope

from prod.business_logic.interactors.trip.add import AddTripInteractor
from prod.business_logic.interactors.trip.edit import EditTripInteractor
from prod.business_logic.interactors.trip.soft_delete import \
    SoftDeleteTripInteractor
from prod.business_logic.interactors.user.add import AddUserInteractor


class InteractorProvider(Provider):
    scope = Scope.REQUEST
    
    provides = provide_all(
        AddUserInteractor,
        AddTripInteractor,
        SoftDeleteTripInteractor,
        EditTripInteractor,
    )