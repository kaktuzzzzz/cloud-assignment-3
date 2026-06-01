import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from src.core.config import settings
from src.api.routes import router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.mount("/public", StaticFiles(directory=settings.PUBLIC_DIR), name="public")

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc):
        return FileResponse(settings.ERRORS_DIR / "404.html", status_code=404)

    app.include_router(router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
