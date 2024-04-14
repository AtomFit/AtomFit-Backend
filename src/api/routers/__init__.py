from api.routers.auth import router as auth_router
from api.routers.users import router as users_router

routers = [auth_router, users_router]