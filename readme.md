PyQt5-based GUY app, built for TBC Academy course, greets an user with registration screen, where the user can enter email and password to register.
The credentials are validated and if passed, stored to SQLite database called "users.db".
Passwords are encrypted before saving.

If an user is already registered, it's possible to go to login page via bottom "Log in" button.
Here the user input is taken and checked against DB data. If validated, then the user is allowed to login.

In "ui" folder the Two .ui files are generated from Qt Designer and they are imported in "app.py" to handle UI.
"resources" folder stores images for GUI background and window icon.