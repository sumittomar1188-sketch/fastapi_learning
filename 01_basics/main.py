from fastapi import FastAPI
import json
app = FastAPI()

def loaddata():
    with open("data.json","r") as f :
        data = json.load(f)

    return data    
@app.get("/")
def hellow():
    return {"message":"hellow sumit"}

@app.get("/about")
def about():
    return {"message":"sumit is a good boy"}

@app.get("/input")


@app.get("/input")
def inputx(de):
    return {"message": de}

@app.get("/view")
def view():
    data = loaddata()
    return data