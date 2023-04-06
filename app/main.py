from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers.user_router import user_router

app = FastAPI()

app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(content, ex):
    return JSONResponse(
        status_code=ex.status_code,
        content={"message": ex.detail}
    )
