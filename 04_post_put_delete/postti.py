from pydantic import BaseModel ,Field,computed_field
from fastapi import FastAPI , HTTPException , Path , Query
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse

class cretate_patient(BaseModel):

    id : Annotated[str,Field(...,description="fill the valid patient id",examples=["P001"])]
    name : Annotated[str , Field(...,description="fill the name")]
    city : Annotated[str,Field(...,description="enter the city of the patient")]
    age : Annotated[int,Field(...,gt=0,description="enter the age of the patient")]
    gender: Annotated[Literal['male','female','others'],Field(...,description="fill gender")]
    weight : Annotated[float,Field(...,description="enter the weight in kilos")] 
    height : Annotated[float,Field(...,description="enter the height in cm")]

    @computed_field
    @property
    def bmi(self) -> int:
        bmi = self.weight / ((self.height / 100) ** 2)
        return bmi 
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "under weight"
        elif self.bmi<25:
            return "normal"
        elif self.bmi<30:
            return "normal"
        else :
            return "obesse"



class Update(BaseModel):
    
    id : Annotated[Optional[str],Field(default=None,description="fill the valid patient id",examples=["P001"])]
    name : Annotated[Optional[str] , Field(default=None,description="fill the name")]
    city : Annotated[Optional[str],Field(default=None,description="enter the city of the patient")]
    age : Annotated[Optional[int],Field(gt=0,default=None,description="enter the age of the patient")]
    gender: Annotated[Optional[Literal['male','female','others']],Field(default=None,description="fill gender")]
    weight : Annotated[Optional[float],Field(default=None,description="enter the weight in kilos")] 
    height : Annotated[Optional[float],Field(default = None,description="enter the height in cm")]


import json
def load_data():
    with open("data.json","r") as f :
        data = json.load(f)
        return data 

def dumb(data):
    with open("data.json","w") as f :
        json.dump(data,f)

def patient(patient:cretate_patient):
    print(patient.id)
    print(patient.name)
    print(patient.city)
    print(patient.age)
    print(patient.gender)
    print(patient.weight)
    print(patient.height)


patient_dict = {"id":"P006","name":"sumit","city":"indore","age":30,"gender":"male","weight":100.3,"height":180.00}


original = cretate_patient(**patient_dict)
patient(original)


# ab ham log do or field expet kar re he client se jo ki hame client nahi dega ham khud caluclate karenge using the computed field

app = FastAPI()
@app.get("/")
def home():
    return "hy ye chalu ho gyi he yrr"


@app.get("/view")
def view():
    data = load_data()
    return data 


# ab ham to ye karenge ki create end point banege 
# @app.post("/create")
# def create(pat:cretate_patient):

#     # load data 
#     data = load_data()

#     # check if patient is already exists
#     if pat.id in data:
#         raise HTTPException(status_code=404,detail="patient already exists")

#     # save patient into the db 
#     # or usse pehele abpne ko Basemodel ko convert karna padega na dictionary me 
#     data[pat.id] = pat.model_dump(exclude="id")

#     # ab apan ko change karna padega json me then dump 
#     # sav into json file 
#     # uske liye hame firse ek function banana hoga 

#     dumb(data)

#     # response bejhenge use ko 
#     return JSONResponse(status_code=201,content={"message":"patient cretaed sucessfully"})


@app.post("/create")
def create(pateient: cretate_patient):

    data = load_data()

    # Check if patient already exists
    if pateient.id in data:
        raise HTTPException(
            status_code=409,
            detail="Patient already exists"
        )

    # Convert Pydantic model into dictionary
    data[pateient.id] = pateient.model_dump(exclude={"id"})

    # Save data
    dumb(data)

    return JSONResponse(status_code=201,content={"message": "Patient created successfully"})


@app.put("/edit/{patient_id}")
def updatee(patient_id:str,patient_update:Update):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="pls enter teh correct patient id")

    existing_patient_info = data[patient_id]


    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key]= value
        # ab yha agara man lo ki ap ne weights ko update kiya to automatically bmi or verdict badlna chahiye par 
        # iske liye ye code abhi tak ka taiyar nahi he then fir ab ham ye karenge ki pehle wale model se help leneg 
        # existing)patient_info-> patient_object ->bmi+vedict
        existing_patient_info["id"] = patient_id
        old_model = cretate_patient(**existing_patient_info)
        # model-> dict
        existing_patient_info = old_model.model_dump(exclude="id")

        data[patient_id] = existing_patient_info

        dumb(data)


        return JSONResponse(status_code=201,content= {"message":"updated sucessfully"})
    

    


# now ab # delete ka use karenge 

@app.delete("/delete/{patient_id}")

def delete(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code= 404,detail="not found patient_id")

    del data[patient_id]

    dumb(data)

    return JSONResponse(status_code=201,content="delete ho gya he")