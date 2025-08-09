from fastapi import FastAPI
from api.routes import router as api_router
from container import Container
from config import settings

app = FastAPI(title=settings.PROJECT_NAME)
container = Container()
app.container = container

app.include_router(api_router, prefix=settings.API_PREFIX)
