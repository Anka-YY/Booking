from fastapi import FastAPI

app = FastAPI(title="Booking API")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI in Docker!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}