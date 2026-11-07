from fastapi import FastAPI,Path,HTTPException,Query
import json 
def load_data():
    with open("data.json","r") as f :
        data = json.load(f)
    return data    
app = FastAPI()
@app.get("/")
def first():
    return {"message":"hello bhai"}

@app.get("/view")
def view():
    data = load_data()
    return data



# now we are adding the path paramter in this present code means ki jab bhi koi locahost/8000/patients/patient_d hit 
# karega to vo patients ko dekh paega bro 
# dynamic path ke andar 
# sirf docs ke liye he ye 
@app.get("/patient/{patient_id}")
# yha par ham client ko show bhi kar sakte he path librariy se g discription add example add 
 # esehi or bhi add kar sakte he 
def patient(patient_id:str =Path(...,description="Id of the patient in the DB",example="P001") ):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    # now intsead of returnniing error we are using the httpExeption error jo ki help karta he error batane me 
    raise HTTPException(status_code=404,detail="patient not found")
    # return {"error":"patient id is not present in the database"}


# now ab ham query parameter ko test karenge jo ki end point kje bad ?marks laga ke use ki jati he or 
# agaf multiple query par ho to & ka bhi use kiya jata he 
# ye ... ka matlab he ki ye batan h padega or agar nahi lagaya to optional rahega 
@app.get("/sort")
def sort(sort_by:str = Query(...,description="give the value for which you want to compare"),order:str=Query(description="asc,desc")):
    values = ["weight","height","bmi"]
    if sort_by not in values:
        raise HTTPException(status_code=400,detail=f"pls write the correct value it is wrong {sort_by}")

    # now for order 
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail = "pls enter correct order")

    orders = True if order =="asc" else False
    data = load_data()
    answer = sorted(data.values(),key= lambda x : x.get(sort_by,0),reverse=orders)


    return answer

# this is url for this 
# http://127.0.0.1:8000/sort?sort_by=height&order=asc 