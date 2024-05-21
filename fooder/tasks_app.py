from fastapi import FastAPI
from .view.tasks import router
from .settings import Settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Fooder Tasks admininstrative API")
app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings().ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
