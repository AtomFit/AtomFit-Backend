from api.routers.auth import router as auth_router
from api.routers.users import router as users_router
from api.routers.meal_nutrients import router as meal_nutrients_router

routers = [auth_router, users_router, meal_nutrients_router]
