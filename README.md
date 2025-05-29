Self Study Resource System

A Django-based web application to help students manage self-study effectively. 
The platform includes to-do list management with prioritization, homework assignment (individual and group-based), and a user-friendly interface for tracking progress.

Features

- User registration and authentication
- Personalized to-do list with priority levels (High, Medium, Low)
- Admin-assigned homework visible to both group and individual dashboards
- Homework status tracking (completed/pending)
- Group-wise resource and homework allocation
- Clean UI/UX design for intuitive navigation

Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap, Django Templates
- Database: SQLite (default) / MySQL (optional)
- Authentication: Django's built-in user system

Screenshots

1. registration and login page
   
![image](https://github.com/user-attachments/assets/3f3cc4cd-9e51-48f1-a117-99d3c60075c7)

2. dashboard
   
![image](https://github.com/user-attachments/assets/02118c0f-eb3c-4b02-b2b7-0ee718f77b81)

3. homework module
   
![image](https://github.com/user-attachments/assets/5320d649-06a2-4c0b-b042-c3c51a3f2386)

4. ebook module
   
![image](https://github.com/user-attachments/assets/b0ce67ba-cd15-40bf-991e-62c0b2759bd7)

5. to-do module
    
![image](https://github.com/user-attachments/assets/a8632c22-71fa-4ef8-8c46-aef3376223da)

6. notes list module
    
![image](https://github.com/user-attachments/assets/15aa8aa2-fa07-42bc-8865-858f7e0b668d)

7. notes description page
    
![image](https://github.com/user-attachments/assets/c7edcc15-6615-4b78-a4e4-9fa28458fc3b)

8. group dashboard
    
![image](https://github.com/user-attachments/assets/36d7d08c-3482-4d39-9a10-52f1a902eb5e)


=========   How to Run the Project   ==========

=========   Clone the repository   ============

git clone https://github.com/Dipesh2203/myproject.git

cd self-study-resource-system

==========    Create and activate virtual environment    ===============

python -m venv venv

venv\Scripts\activate

===============       Install dependencies       =================

pip install -r requirements.txt

===============        Run migrations           ==================

cd SRS

cd Self-study_Resource_System

python manage.py migrate

==================  Start the server     ====================

python manage.py runserver

=================   Open in browser    ===================

http://127.0.0.1:8000/
