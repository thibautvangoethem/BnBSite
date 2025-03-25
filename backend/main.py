import uvicorn
from app import app


if __name__ == "__main__":
    uvicorn.run(app, host=None, port=8000)
