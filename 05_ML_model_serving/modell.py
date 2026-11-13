import pandas as pd 
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse


import pickle
with open ("model.pkl","rb") as model:
    model = pickle.load(model)

tier_1 = ['Delhi','Bangalore','Mumbai','Pune']
tier_2 = ["Jaipur","Indore"]

class pydmodel(BaseModel):


    age:Annotated[int,Field(...,description="enter your age")]
    weight:Annotated[float,Field(...,description="enter your height")]
    height: Annotated[float, Field(gt=0, description="Height in cm")]
    income_lpa:Annotated[float,Field(...,description="enter your salary")]
    smoker:Annotated[bool,Field(...,description="are you smoker")]
    city:Annotated[str,Field(...,description="the city from which user belongs")]
    occupation:Annotated[Literal['unemployed','retired','private_job','business_owner','government_job','self_employed'],Field(...,description="enter you occupation")]
# ab ham log computed field bnanege kyuki user thodi calculate karenga isko 
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height / 100) ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker==True and self.bmi >30:
            return "high"
        elif self.smoker==True and self.bmi >27:
            return "medium"
        else :
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age<25:
            return "younng"
        elif self.age<45:
            return "adult"
        elif self.age<60:
            return "middle age"
        else :
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1:
            return 1
        elif self.city in tier_2:
            return 2
        else :
            return 3    

from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
def prediction(data:pydmodel):
    input_data = pd.DataFrame([{
    "bmi": data.bmi,
    # "lifestyle_risk": data.lifestyle_risk,
    "lifstyle_risk": data.lifestyle_risk,
    "age_group": data.age_group,
    "city": data.city_tier,
    "income_lpa": data.income_lpa,
    "occupation": data.occupation
}])

    prediction = model.predict(input_data)[0]


    return JSONResponse(status_code=201,content={"response":prediction})

# iske liye hamne dusra python dowload kiya tha 
