const todoListElements = document.getElementById('todo-list')
const inputElement = document.querySelector('input')

const renderToDoList = async () => {
    try {
        // Fetch the todo list from the backend
        const response = await fetch('/api/todos/');
        if (!response.ok) {
            console.error('Failed to fetch todos:', response.statusText);
            return;
        }

        const todos = await response.json();
        let todosComponents = '';

        // Generate HTML for each todo item
        todos.forEach(todo => {
            todosComponents += createTodoCompenent(todo);
        });

        // Render the list to the DOM
        todoListElements.innerHTML = todosComponents;
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
}

const createTodoCompenent = (todo) => {
    return `
        <figure>
            <h3 ${todo.completed ? 'class="completed"' : ''}'>${todo.task}</h3>
            <p ${todo.completed ? 'class="completed"' : ''}'>${formatDate(todo.date)} ${todo.time}</p>
            <button onclick="toggleTodoItem(${todo.id})" class="toggle-todo">${todo.completed ? 'Completed' : 'Check'}</button>
            <div onclick="removeTodoById(${todo.id})" class="remove-todo">X</div>
        </figure>
        `
}

const removeTodoById = async (id) => {
    try {
        // Send a DELETE request to the Django API
        const response = await fetch(`/api/todos/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            console.log(`Todo item with ID ${id} deleted successfully.`);
            renderToDoList();  // Refresh the list to show the updated tasks
        } else {
            console.error('Failed to delete todo:', response.statusText);
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

const formatDate = (dateString) => {
    const [year, month, day] = dateString.split('-');
    return `${day}-${month}-${year}`;
};


const toggleTodoItem = async (id) => {
    try {
        // Fetch the current task from the database
        const response = await fetch(`/api/todos/${id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Failed to fetch the todo item:', response.statusText);
            return;
        }
        const todo = await response.json();

        // Toggle the completion status
        const updatedStatus = !todo.completed;
        
        // Send the PUT request to update the status in the database
        const updateResponse = await fetch(`/api/todos/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: todo.task,
                completed: updatedStatus,
                date: formatDate(todo.date), 
                time: todo.time  
            })
        });

        if (updateResponse.ok) {
            console.log('Todo item updated successfully.');
            renderToDoList();  // Refresh the list after updating
        } else {
            console.error('Failed to update todo:', updateResponse.statusText);
        }
    } catch (error) {
        console.error('Error updating todo:', error);
    }
}


const createTodoItem = async () => {
    const text = inputElement.value;
    if(!text){
        return;
    }

    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');  // Months are zero-based
    const year = today.getFullYear();
    const formattedDate = `${day}-${month}-${year}`;

    // Get current time in HH:MM:SS format
    const formattedTime = today.toLocaleTimeString('en-GB'); 

    todoItem = {
        task: text,
        completed:false,
        date: formattedDate,
        time: formattedTime
    };
    try {
        // Send POST request to Django API
        const response = await fetch('/api/todos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(todoItem)
        });
        console.log('Todo item added successfully.')

        if(!response.ok){
            console.error('Failed to create todo:', response.statusText);
        }
    }
    catch (error) {
        console.error('Error creating todo:', error);
    }
    renderToDoList();
    inputElement.value = "";
}

renderToDoList();
