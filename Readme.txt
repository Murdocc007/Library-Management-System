This project is made in django.
In order to run it,python,MySQL and django needs to be installed on your computer.

It can be run on any OS, Windows,Mac OS and linux.

After you have installed django and pyhton to your computer.

1. Go to the LMS directory in the terminal

2. Then execute command 'python manage.py makemigrations polls'
3. Then execuet command 'python manage.py migrate'( It makes the relevant tables in the database)
4. Then execute the command 'python manage.py runserver'(runs the server)
5. Open browser and type '127.0.0.1:8000'
6. You'll see the application running.

Note: I don't have an update button that updates the value of the fine in the database.Instead after the fine and the book has been returned I store it's final value in the fine table. 
