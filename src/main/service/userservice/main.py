import time
from fastapi import *
from router.user import user
from router.authen import authen

app = FastAPI()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
app.include_router(user)
app.include_router(authen)
