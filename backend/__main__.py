import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", port=8000, host="0.0.0.0", reload=False)
