from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel


app = FastAPI()


#화면에 {"ping": "pong"} 띄우기
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


#todo data를 dictionary 형태로 저장하기
todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    },
    2: {
        "id": 2,
        "contents": "DB 입문 수강",
        "is_done": True,
    },
    3: {
        "id": 3,
        "contents": "ERD 그려보기",
        "is_done": False,
    },
}

"""
#GET API: 전체 조회
@app.get("/todos")   #api의 path 지정
def get_todos_handler() :
    return list(todo_data.values())   #todo의 iten들 가져오기
"""

#query parameter: 특정 값을 이용해 추가적인 작업 가능
@app.get("/todos", status_code=200)
def get_todos_handler(order: str | None = None) :   #None = None: request시에 order값을 넣지 않아도 되도록 해주는 것
    ret = list(todo_data.values())
    if order and order == "DESC":   #order가 DESC일 경우, 내림차순으로 반환
        return ret[::-1]
    return ret


#GET API: 단일 조회
@app.get("/todos/{todo_id}", status_code=200)   #중괄호 안에 적으면 path로 이용 가능(subpath)
def get_todo_handler(todo_id: int):   #중괄호 안에 넣었던 걸 인자로 전달받을 수 있음
    todo = todo_data.get(todo_id)
    if todo:
        return todo   #todo가 있는 경우, todo 반환
    raise HTTPException(status_code=404, detail="ToDo Not Found")   #todo가 없는 경우, 404 에러 메시지 반환


#POST API: todo 생성
class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()   #request는 class 객체이고, todo_data는 dictionary 형태이기 때문에 형태 변환 필요함
    return todo_data[request.id]


#PATCH API: todo 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),   #fastapi에서 하나의 컬럼 값은 request body를 읽어서 사용할 수 있음.
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")


#DELETE API: todo 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")
