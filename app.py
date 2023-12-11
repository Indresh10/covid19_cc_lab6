from flask import Flask, render_template, request, redirect
import pymysql
import json

app = Flask(__name__)

# Configure MySQL
db_host = "covid19.c9c3wtijerem.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "root1234"
db_name = "covid19"

# Function to create a connection to the database


def create_connection():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Home Page


@app.route('/')
def home():
    # connection = create_connection()
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM Covid_details ORDER BY No_of_Positive ASC")
    # data = cursor.fetchall()
    # connection.close()
    data = {}
    return render_template('home.html', data=data)

# Add Page


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        state_name = request.form['state_name']
        date_of_record = request.form['date_of_record']
        no_of_samples = int(request.form['no_of_samples'])
        no_of_deaths = int(request.form['no_of_deaths'])
        no_of_positive = int(request.form['no_of_positive'])
        no_of_negative = int(request.form['no_of_negative'])
        no_of_discharge = int(request.form['no_of_discharge'])

        connection = create_connection()
        cursor = connection.cursor()

        # Insert the data into the database
        cursor.execute(
            "INSERT INTO Covid_details (State_Name, Date_of_Record, No_of_Samples, No_of_Deaths, No_of_Positive, No_of_Negative, No_of_Discharge) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (state_name, date_of_record, no_of_samples, no_of_deaths,
             no_of_positive, no_of_negative, no_of_discharge)
        )

        connection.commit()
        connection.close()

        # Redirect to the home page after adding the entry
        return redirect('/')

    return render_template('add.html')

# Analysis Page


@app.route('/analysis')
def analysis():
    # connection = create_connection()
    # cursor = connection.cursor()
    # cursor.execute(
    #     "SELECT State_Name, sum(No_of_Positive) FROM Covid_details group by State_Name")
    # data = cursor.fetchall()
    # connection.close()

    # # Extracting data for chart
    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]

    # Convert data to JSON for JavaScript
    chart_data = json.dumps({
        'labels': ["A", "B", "C"],
        'values': [10, 150, 60]
    })

    return render_template('analysis.html', chart_data=chart_data)


# Pie Chart Page
@app.route('/pie_chart')
def pie_chart():
    # connection = create_connection()
    # cursor = connection.cursor()
    # cursor.execute(
    #     "SELECT State_Name, sum(No_of_Positive) FROM Covid_details group by State_Name")
    # data = cursor.fetchall()
    # connection.close()

    # Extracting data for pie chart
    labels = ["A", "B", "C"]
    values = [300, 150, 100]

    return render_template('pie_chart.html', labels=labels, values=values)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
