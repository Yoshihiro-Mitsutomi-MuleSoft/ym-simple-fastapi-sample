from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
import uvicorn

app = FastAPI(root_path="/api/v1")
app.openapi_version = "3.0.2"

wkItems = []

class Customer_In(BaseModel):
    firstName: str
    lastName: str
    sex: str
    email: str


    '''
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "firstName": "Koji",
                    "lastName": "Yamada",
                    "sex": "male",
                    "email": "kyamada@aaa.com"
                }
            ]
        }
    }
    '''

class Customer_Out(BaseModel):
    id: int
    customer: Customer_In

    '''
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "customer": {"firstName": "Koji",
                        "lastName": "Yamada",
                        "sex": "male",
                        "email": "kyamada@aaa.com"},
                }
            ]
        }
    }
    '''



@app.on_event("startup")
async def startup_event():
    wkItems.append({"firstName": "Koji","lastName": "Yamada","sex": "male","email": "kyamada@aaa.com"})
    wkItems.append({"firstName": "Keiichi","lastName": "Matsumoto","sex": "male","email": "kmatsumoto@bbb.com"})
    wkItems.append({"firstName": "Shinobu","lastName": "Takaiwa","sex": "female","email": "stakaiwa@ccc.com"})
    wkItems.append({"firstName": "Kanji","lastName": "Nagayo","sex": "male","email": "knagayo@ddd.com"})
    wkItems.append({"firstName": "Shohei","lastName": "Kanemoto","sex": "male","email": "kshohei@eee.com"})
    wkItems.append({"firstName": "Akira","lastName": "Inoki","sex": "female","email": "ainoki@fff.com"})
    wkItems.append({"firstName": "Kaoru","lastName": "Baba","sex": "female","email": "kbaba@ggg.com"})
    wkItems.append({"firstName": "Tatsuhito","lastName": "Otani","sex": "male","email": "tonita@hhh.com"})
    wkItems.append({"firstName": "Shinjiro","lastName": "Hokuto","sex": "male","email": "shokuto@iii.com"})
    wkItems.append({"firstName": "Chigusa","lastName": "Kandori","sex": "female","email": "ckandori@jjj.com"})

@app.post("/customers", status_code=201)
async def create_item(wkBody: Customer_In) -> Customer_Out:
    wkItems.append(wkBody)
    wkListSize = len(wkItems)
    resCust = {"id": wkListSize, "customer": wkItems[wkListSize - 1]}
    return resCust


@app.get("/customers")
async def read_items() -> list[Customer_Out]:
    wkList = []
    for idx, item in enumerate(wkItems, 1):
        wkList.append({"id": idx, "customer": item})
    return wkList

@app.put("/customers/{customer_id}")
async def update_item(
    customer_id: Annotated[int,
    Path(title="The ID of the customer to update")],
    wkBody: Customer_In
) -> Customer_Out:
    try:
        wkItems[customer_id - 1] = wkBody
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid ID is specified")


    wkRes = {"id": customer_id, "customer": wkBody}
    return wkRes

@app.get("/customers/{customer_id}")
async def read_item(
    customer_id: Annotated[int, Path(title="The ID of the customer to read")]
) -> Customer_Out:
    try:
        wkCustomer = wkItems[customer_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid ID is specified")

    wkRes = {"id": customer_id, "customer": wkCustomer}
    return wkRes

@app.delete("/customers/{customer_id}")
async def delete_item(
    customer_id: Annotated[int, Path(title="The ID of the customer to delete")]
):
    try:
        wkCustomer = wkItems[customer_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid ID is specified")

    idx2delete = customer_id - 1
    wkItems.pop(idx2delete)
    return {"message": "Data Deletion has been completed. (warning) ID is reorganized"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
