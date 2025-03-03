const todoListElements = document.getElementById('todo-list');
const inputElement = document.querySelector('input');
const token = localStorage.getItem("token");

document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('username') || 'Guest';
    document.querySelector('.username').innerText = username;
});
const getAuthHeaders = () => {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
    };
}

const goBackHome = async () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
}

const renderToDoList = async () => {
    try {
        const response = await fetch('/api/todos/', {
            headers: getAuthHeaders()
        });
        if (!response.ok) {
            console.error('Failed to fetch todos:', response.statusText);
            return;
        }

        const todos = await response.json();
        let todosComponents = '';

        todos.forEach(todo => {
            todosComponents += createTodoCompenent(todo);
        });

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
        const response = await fetch(`/api/todos/${id}/`, {
            method: 'DELETE',
            headers: getAuthHeaders() 
        });

        if (response.ok) {
            console.log(`Todo item with ID ${id} deleted successfully.`);
            renderToDoList();  
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
        const response = await fetch(`/api/todos/${id}/`, {
            method: 'GET',
            headers: getAuthHeaders() 
        });

        if (!response.ok) {
            console.error('Failed to fetch the todo item:', response.statusText);
            return;
        }
        const todo = await response.json();

        const updatedStatus = !todo.completed;
        
        const updateResponse = await fetch(`/api/todos/${id}/`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                task: todo.task,
                completed: updatedStatus,
                date: formatDate(todo.date), 
                time: todo.time  
            })
        });

        if (updateResponse.ok) {
            console.log('Todo item updated successfully.');
            renderToDoList();  
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
    const month = String(today.getMonth() + 1).padStart(2, '0'); 
    const year = today.getFullYear();
    const formattedDate = `${day}-${month}-${year}`;

    const formattedTime = today.toLocaleTimeString('en-GB'); 

    todoItem = {
        task: text,
        completed:false,
        date: formattedDate,
        time: formattedTime
    };
    try {
        const response = await fetch('/api/todos/', {
            method: 'POST',
            headers: getAuthHeaders(),
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

//TODO לא סידרתי כתובת ופנוקציה למחיקת משתמש
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('delete-account-button').addEventListener('click', deleteAccountButton);
});

function deleteAccountButton() {
    const password = prompt("Please enter your password to confirm account deletion:");
    if (!password) {
        alert("Account deletion cancelled.");
        return;
    }

    const token = localStorage.getItem("token");

    fetch("/api/users/delete-account/", {
        method: "DELETE",
        headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password }) 
    })
    .then(response => {
        if (response.ok) {
            alert("Your account and all your tasks have been deleted successfully.");
            localStorage.clear(); 
            window.location.href = "/login/"; 
        } else {
            return response.json().then(data => {
                alert(data.error || "Failed to delete account. Please check your password.");
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Sorry but yet, no one allowd to leave us (עוד לא עשיתי את המחיקה).");
    });
}

renderToDoList();
