import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers

# Load environment variables from dotenv file
dotenv.load_dotenv()

app = FastAPI(
    root_path=os.environ.get('BASE_URL', ''),
)

origins = [
    "*",
]

# CORS 문제 해결
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # cross-origin request에서 cookie를 포함할 것인지 (default=False)
    allow_credentials=True,
    # cross-origin request에서 허용할 method들을 나타냄 (default=['GET'])
    allow_methods=["*"],
    allow_headers=["*"],     # cross-origin request에서 허용할 HTTP Header 목록
)

# Register all available routers
app.include_router(routers.health.router)
app.include_router(routers.home.router)
app.include_router(routers.dreams.router)
app.include_router(routers.dream_interpret.router)
