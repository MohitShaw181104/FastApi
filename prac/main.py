from fastapi import FastAPI

app = FastAPI()

all_todos = [
    {'todo_id': 1, 'todo_name': 'Sports', 'todo_description': 'go to the gym'},
    {'todo_id': 2, 'todo_name': 'cooking', 'todo_description': 'cook'},
    {'todo_id': 3, 'todo_name': 'Bathing', 'todo_description': 'bath'},
    {'todo_id': 4, 'todo_name': 'Playing', 'todo_description': 'play'},
    {'todo_id': 5, 'todo_name': 'Chatting', 'todo_description': 'chat'},
]

#GET,POST,PUT,DELETE
@app.get('/')
def index():
    return {"message": "Hello World"}

@app.get('/todos/{todo_id}') #path parameters -- 8000/todos  query parameters -- 8000/todos?first_name
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result': todo}
        
@app.get('/todos')
def get_todos(first_n:int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
