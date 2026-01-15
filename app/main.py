from fastapi import FastAPI

app = FastAPI(title="GenAI Backend Skeleton")

@app.get("/health")
def health():
    return {"status": "ok"}
