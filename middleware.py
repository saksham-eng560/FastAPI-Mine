from fastapi import FastAPI, Request
import time
app = FastAPI()

@app.middleware("http")
async def process_time(req : Request, call_next):
    start_time = time.time()
    res = await call_next(req)
    end_time = time.time()
    total_time = end_time-start_time
    res.headers["ProcessTime"] = str(total_time)
    return res

@app.get("/home/")
async def home():
    return {
        "message" : "hello"
    }

# Definition: Functions that intercept every incoming request before it reaches your endpoints and every outgoing response before it reaches the client.
# Key Uses: Adding security headers, logging requests, measuring execution time, handling CORS, or compressing data.
# How It Works: Wraps your app, modifies Request → runs endpoint via call_next() → modifies Response
