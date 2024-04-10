from typing import Annotated
from fastapi import Depends

from utils.unit_of_work import IUnitOfWork, UnitOfWork

UowDep: Annotated[IUnitOfWork, Depends(UnitOfWork)]