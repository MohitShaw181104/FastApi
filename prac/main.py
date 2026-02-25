from enum import IntEnum
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Priority(IntEnum):
    low = 3
    medium = 2
    high = 1   

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=50 , description="The name of the todo item")
    todo_description: str = Field(..., description="The description of the todo item")
    priority: Priority = Field(default=Priority.low , description="The priority level of the todo item")
    

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="The unique identifier of the todo item")
    

class TodoUpdate(TodoBase):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=50 , description="The name of the todo item")
    todo_description: Optional[str] = Field(None, description="The description of the todo item")
    priority: Optional[Priority] = Field(None , description="The priority level of the todo item")


all_todos = [
    Todo(todo_id=1, todo_name='Sports', todo_description='go to the gym', priority=Priority.medium),
    Todo(todo_id=2, todo_name='cooking', todo_description='cook', priority=Priority.medium),
    Todo(todo_id=3, todo_name='Bathing', todo_description='bath', priority=Priority.low),
    Todo(todo_id=4, todo_name='Playing', todo_description='play', priority=Priority.medium),
    Todo(todo_id=5, todo_name='Chatting', todo_description='chat', priority=Priority.low),
]

#GET,POST,PUT,DELETE
@app.get('/')
def index():
    return {"message": "Hello World"}

@app.get('/todos/{todo_id}', response_model=Todo) #path parameters -- 8000/todos  query parameters -- 8000/todos?first_name
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
        
    raise HTTPException(status_code=404, detail="Todo not found")
        
@app.get('/todos', response_model=List[Todo])
def get_todos(first_n:int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
@app.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    
    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    
    all_todos.append(new_todo)
    
    return new_tod

@app.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name or todo.todo_name
            todo.todo_description = updated_todo.todo_description or todo.todo_description
            todo.priority = updated_todo.priority or todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")