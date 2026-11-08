import uvicorn





def main_api_test():
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)



