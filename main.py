from fastapi import FastAPI
import random
import time

app = FastAPI()

# Simulate a degrading model
request_count = 0

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: dict):
    global request_count
    request_count += 1

    # Simulate latency
    time.sleep(random.uniform(0.1, 0.5))

    # Every 5th request → model fails completely
    if request_count % 5 == 0:
        return {
            "prediction": "error",
            "confidence": round(random.uniform(0.0, 0.15), 3),
            "status": "degraded"
        }

    # Every 3rd request → low confidence (drift simulation)
    if request_count % 3 == 0:
        return {
            "prediction": random.choice(["spam", "not_spam"]),
            "confidence": round(random.uniform(0.1, 0.35), 3),
            "status": "uncertain"
        }

    # Normal requests → borderline confidence
    return {
        "prediction": random.choice(["spam", "not_spam"]),
        "confidence": round(random.uniform(0.4, 0.65), 3),
        "status": "nominal"
    }