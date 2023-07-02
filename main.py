from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_data():
    return {"message": "Data Fetched Successfully", "success": True}