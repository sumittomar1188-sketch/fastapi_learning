# pydantic use kiya jata he data valudation and type vvalidation ke liye 
# noramally python me kya hota he ki  ek valriable me kisis type ke data ko store kiya jata he par production me nahi chltya he vo 
# agar apan maually type validation karne jae to bhot time lag sakta he 
# then isi problemm ko hataane ke liye ham use karte he pydantic \
#setp 1 ki uska model banaenege means ki class baneneg pydantic use hoga usme fir object me 
# dictionary pass karenge then fir use karenge 
# or pydantic hame bhot sare features deta he not only the 
from pydantic import BaseModel

class Patient(BaseModel):
    name:str
    age:int
# hamare function ko patient name ka object mil rha he jo ki he patent type ka 
def patienti (patient:Patient):
    print(patient.name)
    print(patient.age)

patient_info = {"name":"sumit","age":20}
patient = Patient(**patient_info)


patienti(patient)