from fastapi import FastAPI
from .router import router


app = FastAPI(title="Fooder")
app.include_router(router)
