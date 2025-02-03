const savedTodos = JSON.parse(localStorage.getItem('todos'));
const savedGloablId = JSON.parse(localStorage.getItem('globalId'));

let globalId = savedGloablId || 0;
let todos = savedTodos || [];

const todoListElements = document.getElementById('todo-list')
const inputElement = document.querySelector('input')

const renderToDoList = () => {
    saveTodoList();
    let todosComponents = ''
    todos.forEach(todo => {
        todosComponents += createTodoCompenent(todo);
    })
    todoListElements.innerHTML = todosComponents;
}

const createTodoCompenent = (todo) => {
    const date = new Date(todo.created).toLocaleDateString('he-IL');
    const time = new Date(todo.created).toLocaleTimeString('he-IL');
    return `
        <figure>
            <h3 ${todo.isCompleted ? 'class="completed"' : ''}'>${todo.Text}</h3>
            <p ${todo.isCompleted ? 'class="completed"' : ''}'>${date} ${time}</p>
            <button onclick="toggleTodoItem(${todo.id})" class="toggle-todo">${todo.isCompleted ? 'Completed' : 'Check'}</button>
            <div onclick="removeTodoById(${todo.id})" class="remove-todo">X</div>
        </figure>
        `
}
const removeTodoById = (id) => {
    todos = [...todos.filter(todo => todo.id !== id)]
    renderToDoList()
}

const toggleTodoItem = (id) => {
    const idx = todos.findIndex(todo => todo.id === id);
    todos[idx].isCompleted = !todos[idx].isCompleted;
    renderToDoList();
}

const createTodoItem = () => {
    const text = inputElement.value;
    if(!text){
        return;
    }
    todoItem = { id: genId(), Text: text, created:Date.now(), isCompleted:false };
    todos.push(todoItem);
    renderToDoList();
    inputElement.value = "";
}

const genId = () => {
    return ++globalId;
}

const saveTodoList = () => {
    localStorage.setItem('todos', JSON.stringify(todos));
    localStorage.setItem('globalId', JSON.stringify(globalId));
}

renderToDoList();