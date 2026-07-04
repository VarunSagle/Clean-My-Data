
📊 CleanMyData – Data Cleaning & Visualization Dashboard

1. Project Description:- CleanMyData is a Flask-based web application that helps users clean, transform, analyze, and visualize CSV datasets through an interactive dashboard. Users can upload datasets, perform common data-cleaning operations, generate charts, and download the processed data. The application also includes user authentication and activity logging using MySQL.

2. Features:

✔ User Registration & Login
✔ Secure Password Hashing
✔ CSV File Upload
✔ Missing Value Handling
✔ Fill Missing Values
    - Custom Value
    - Mean
    - Numeric Value
✔ Drop Rows
✔ Drop Columns
✔ Rename Columns
✔ Convert Data Types
✔ Filter Dataset
✔ View Dataset Summary
✔ Detect Duplicate Records
✔ Head & Tail Preview
✔ Dataset Information
✔ Descriptive Statistics
✔ Unique Values
✔ Value Counts
✔ GroupBy Operations
✔ Data Visualization
✔ Download Cleaned CSV
✔ Activity Logs using MySQL


3. Technologies Used:

Python
Flask
Pandas
Matplotlib
Seaborn
MySQL
HTML
CSS
Bootstrap
Jinja2


4. Project Structure

CleanMyData/
│
├── app.py
├── Registration.py
├── templates/
├── static/
├── requirements.txt
├── README.md
└── database.sql

5. Installation

1. Clone the repository

git clone <repo>

2. Create virtual environment

python -m venv venv

3. Activate environment

4. Install requirements

pip install -r requirements.txt

5. Create MySQL database

6. Import database.sql

7. Run

python app.py


--------------  if you not understand this the you read the following instraction  ----------------

First create the 'ENVIROMENT' :
HOW TO CREATE THE env OR venv FOLDER 

python -m venv venv
OR (if python not working):

py -m venv venv
This creates a folder called venv (your isolated environment).

For Windows:
Inside the Terminal enter this  : venv\Scripts\activate


If successful, you will see:

(venv) C:\Users\YourName\flask_project>

That (venv) means environment is active ✅


Now Install the Libraries :

pip install Flask
pip install Flask-Bcrypt
pip install pandas
pip install matplotlib
pip install seaborn
pip install mysql-connector-python


## The system cannot find the file specified. ##

solution :-  python -m pip install pandas

In this solution you can write the ' matplotlib ' or any other librery what you want to install


Now RUN the app:  python app.py



5. Database Setup

-----Make sure services is running-----
If theserver is not running you got thia error:  mysql.connector.errors.DatabaseError: 2003 (HY000): Can't connect to MySQL server on 'localhost:3306' (10061)

CREATE DATABASE cleanmydata;

Then

Import database.sql into MySQL.

In mySQL database write this query
create database cleanmydata;
use cleanmydata;

CREATE TABLE uploaded_files(
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_name varchar(100),
    file_name VARCHAR(255),
    total_rows INT,
    total_columns INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS register (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    passwords VARCHAR(255) NOT NULL
);

CREATE TABLE users(id int AUTO_INCREMENT primary key, username varchar(100), email varchar(200) unique, password varchar(255) );

select * from users;

6. You can see the Logs in your browser
http://127.0.0.1:5000/logs





# Register And Login Page                                                                                                                                 
<img width="400" height="600" alt="Create Account" src="https://github.com/user-attachments/assets/443d61f5-3c9b-4b1b-b129-cb31309ad678" />     
<img width="400" height="600" alt="Screenshot 2026-07-04 140656" src="https://github.com/user-attachments/assets/553bef46-4a4d-461a-b8fc-9d2755183aa7" /> </br>

# Dashboard
<img width="1890" height="860" alt="Screenshot 2026-07-04 140752" src="https://github.com/user-attachments/assets/515ff651-506e-4029-a705-778e1a32a859" />
<img width="1871" height="727" alt="Screenshot 2026-07-04 140852" src="https://github.com/user-attachments/assets/e75de709-46f3-4830-ab90-8237c4b1f4fd" />
<img width="1882" height="862" alt="Screenshot 2026-07-04 140930" src="https://github.com/user-attachments/assets/2a6407f1-2ac8-49ca-a27a-aa683269c1bb" />
<img width="1885" height="866" alt="Screenshot 2026-07-04 141350" src="https://github.com/user-attachments/assets/b6284e80-78d9-4ab3-bb36-983ffb45213f" />
<img width="1882" height="722" alt="Screenshot 2026-07-04 141429" src="https://github.com/user-attachments/assets/c2425614-56da-4adb-8fea-7ab289ba0a64" /></br>

# Visualization Page
<img width="1607" height="833" alt="Screenshot 2026-07-04 141415" src="https://github.com/user-attachments/assets/1e61c6fc-7888-4d95-8c34-82df8844134c" /></br>

# Activity Logs

<img width="1626" height="802" alt="Screenshot 2026-07-04 141530" src="https://github.com/user-attachments/assets/bb2334af-6836-42a2-bd0f-4ce8e71c56bb" />






