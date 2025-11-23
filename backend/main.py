from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pkgutil
from importlib import import_module
import pathlib

app = FastAPI(title="API Ecomerce")

# 🟢 Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🖼️ Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔁 Cargar automáticamente todos los routers (incluso subcarpetas)
for path in pathlib.Path("routers").rglob("*.py"):
    module_path = path.with_suffix("").as_posix().replace("/", ".")
    module = import_module(module_path)
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend Mascota iniciado correctamente"}
