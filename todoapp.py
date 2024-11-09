import pickle
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__,  template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Necessary for flash() functionality

# File where todo items will be saved
TODO_FILE = 'todo_items.pkl'

# Load the todo items from the file
def load_todo_items():
    try:
        with open(TODO_FILE, 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return []

# Save the todo items to the file
def save_todo_items():
    with open(TODO_FILE, 'wb') as file:
        pickle.dump(todo_items, file)

# Starting with loading the list from file (if it exists)
todo_items = load_todo_items()

@app.route('/')
def index():
    return render_template('index.html', todo_items=todo_items)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    # Data validation
    if "@" not in email or "." not in email:  # rudimentary email check
        flash('Invalid email address. Please enter a valid email.', 'error')
        return redirect(url_for('index'))  # redirect if invalid email

    if priority not in ['Low', 'Medium', 'High']:
        flash('Invalid priority. Please select a valid priority.', 'error')
        return redirect(url_for('index'))  # redirect if invalid priority

    # Add item to the list if validation passed
    todo_items.append({'task': task, 'email': email, 'priority': priority})
    save_todo_items()  # Save updated list to file
    flash('Task added successfully!', 'success')

    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    global todo_items
    todo_items = []  # clear the list
    save_todo_items()  # Save empty list to file
    flash('To-Do list has been cleared.', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_item(index):
    global todo_items
    if 0 <= index < len(todo_items):
        del todo_items[index]  # Delete the item at the given index
        save_todo_items()  # Save updated list
        flash('Item deleted successfully!', 'success')
    else:
        flash('Invalid index for deletion.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
