from flask import Flask, request, render_template_string
import sqlite3
from datetime import date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    current_date = date.today().strftime('%Y%m%d')
    message = ""

    if request.method == 'POST':
        option = request.form.get('option')
        id = request.form.get('id', '')

        if option == '1':
            name = request.form.get('name', '')
            if id == '':
                c.execute('''SELECT MAX(id) FROM member''')
                max_id = c.fetchone()[0] + 1
                c.execute('INSERT INTO member VALUES (?, ?, ?)', (max_id, name, current_date))
                message = "Member added successfully."
            else:
                max_id = int(id)
                # If found same id, quit. else, continue
                member = c.execute(f'''SELECT * FROM member WHERE id = {max_id}''')
                member = member.fetchone()
                if member:
                    message = "ID "
                else:
                    c.execute('INSERT INTO member VALUES (?, ?, ?)', (max_id, name, current_date))
                    message = "Member added successfully."

        elif option == '2':
            c.execute('DELETE FROM member WHERE id = ?', (id,))
            message = "Member deleted successfully."

        elif option == '3':
            # This option is handled below in the template
            pass

        elif option == '4':
            # This option is handled below in the template
            pass

        conn.commit()

    members_today = c.execute('SELECT * FROM member WHERE date = ?', (current_date,)).fetchall()
    all_members = c.execute('SELECT * FROM member').fetchall()
    conn.close()

    # HTML content with embedded Python code for Flask and Bootstrap styling
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Member Database Management</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h2>Member Database Management</h2>
            <p>{{ message }}</p>
            <form method="post">
                <div class="form-group">
                    <label for="option">Select an option:</label>
                    <select class="form-control" id="option" name="option">
                        <option value="1">Add a member</option>
                        <option value="2">Delete a member</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="id">ID:</label>
                    <input type="text" class="form-control" id="id" name="id">
                </div>
                <div class="form-group">
                    <label for="name">Name (for adding):</label>
                    <input type="text" class="form-control" id="name" name="name">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            <hr>
            <h3>Members Attended Today</h3>
            {% for member in members_today %}
                <p>{{ member }}</p>
            {% endfor %}
            <hr>
            <h3>All Members</h3>
            {% for member in all_members %}
                <p>{{ member }}</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """, message=message, members_today=members_today, all_members=all_members)

if __name__ == '__main__':
    app.run(debug=True)
