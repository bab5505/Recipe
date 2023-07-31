Recipe App


This is a Flask-based recipe application that allows users to create, view, edit, and delete recipes. Users can sign up, log in, and manage their own recipes. The application also integrates with the Edamam API to fetch additional recipe information.


Features:

- User authentication: Users can sign up and log in to the application using their username and password.
- User profiles: Each user has a profile page that displays their information and a list of their created recipes.
- Recipe management: Users can create, view, edit, and delete their own recipes.
- External API integration: The application uses the Edamam API to fetch additional recipe information based on user queries.



Installation:

To run the application locally, follow these steps:

1. Clone the repository: git clone <repository_url>
2. Navigate to the project directory: cd recipe-app
3. Create a virtual environment: python -m venv venv
4. Activate the virtual environment:
5.Windows: venv\Scripts\activate
6. Unix/Mac: source venv/bin/activate
7. Install the required dependencies: pip install -r requirements.txt
8. Set up the database:
9. Create a PostgreSQL database with the name recipe (or modify the SQLALCHEMY_DATABASE_URI in config.py to use a different database).
10. Apply the database migrations: flask db upgrade
11. Set the Flask app environment variable:
12. Windows: set FLASK_APP=app.py
13. Unix/Mac: export FLASK_APP=app.py
14. Set the secret key environment variable:
15. Windows: set SECRET_KEY=your_secret_key
16. Unix/Mac: export SECRET_KEY=your_secret_key
17. Start the application: flask run
18. Open the application in your browser: http://localhost:5000



Usage:

- Sign Up: Click on the "Sign Up" link to create a new user account.
- Log In: Use your username and password to log in to the application.
- Home: The home page displays a list of recipes, including ones fetched from the Edamam API. Click on a recipe to view its details.
- My Profile: After logging in, click on "My Profile" to view your user profile page, which includes your information and a list of your recipes.
- Add Recipe: To create a new recipe, click on "Add Recipe" and fill out the form with the required details.
- Edit Recipe: If you are the owner of a recipe, you can edit it by clicking on the "Edit" button on the recipe details page.
- Delete Recipe: If you are the owner of a recipe, you can delete it by clicking on the "Delete" button on the recipe details page.
- Log Out: Click on "Log Out" to log out of your user account.



Technologies Used:

- Flask: The web framework used to build the application.
- SQLAlchemy: The ORM (Object-Relational Mapping) library for database management.
- Flask-Login: The extension used for user authentication and session management.
- Alembic: The database migration tool used to manage database schema changes.
- Edamam API: An external API used to fetch recipe information.
- HTML/CSS: The markup and styling languages used for the application's templates.


