import time
from fastapi import *
from src.routers.authenticate.views import rooter as authenticate_rooter
from src.routers.user_info.views import rooter as user_profile_rooter
from src.middlewares.middleware_config import RateLimitingMiddleware

app = FastAPI()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
app.add_middleware(RateLimitingMiddleware)
app.include_router(user_profile_rooter)
app.include_router(authenticate_rooter)
