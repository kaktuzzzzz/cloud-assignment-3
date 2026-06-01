from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from src.core.config import settings

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse(settings.PAGES_DIR / "home.html")

@router.get("/research", response_class=HTMLResponse)
async def research():
    return FileResponse(settings.PAGES_DIR / "research.html")

@router.get("/projects", response_class=HTMLResponse)
async def projects():
    return FileResponse(settings.PAGES_DIR / "projects.html")

@router.get("/hpc", response_class=HTMLResponse)
async def hpc():
    return FileResponse(settings.PAGES_DIR / "hpc.html")

@router.get("/gallery", response_class=HTMLResponse)
async def gallery():
    return FileResponse(settings.PAGES_DIR / "gallery.html")

@router.get("/archive", response_class=HTMLResponse)
async def archive():
    return FileResponse(settings.PAGES_DIR / "archive.html")

@router.get("/portal", response_class=HTMLResponse)
async def portal():
    return FileResponse(settings.PAGES_DIR / "portal.html")

@router.get("/about", response_class=HTMLResponse)
async def about():
    about_path = settings.PAGES_DIR / "about.html"
    if about_path.exists():
        return FileResponse(about_path)
    return FileResponse(settings.PAGES_DIR / "home.html")

@router.get("/home", response_class=RedirectResponse)
async def redirected_home():
    return RedirectResponse(url="/", status_code=301)