
Hungry? https://fave-recipes.herokuapp.com/

# The Recipe Collection 🥘
This website has a collection of delicious recipes created by various users. All users can post/share a new recipe for everyone to enjoy. Users can post a comment to a recipe to ask question, provide input and or simply show appreciation. 

## Thought Process

I like to start by thinking about what information needs to be stored in the database.
The database holds valuable data and acts as the brain for the entire application which will lead the direction for the
rest of the code.

I know that I want different users stored in the database so that they can keep track of their own recipes. 
Therefore, I need a `User` table.

I want to be able to store all the data of the recipes such as the title, ingredients, instruction, img_url, date and user_id (foreign key). So I knew I need a `Recipe` table.

I want to be able to store the user's comments for each specific recipe and the date it was posted. So I knew I need a `Comment` table.

The tables are related to each other. Each recipe row is tied to a specific `user_id` from the `User` table. 
Each comment row is tied to a specific `user_id` from the `User` table and specific `recipe_id` in the `Recipe` table. All recipe posts are display on the main page for everyone to view. All users are able to make a comment to any recipes. 

## Code Structure
Created a `CreatePostForm` class which is a `FlaskForm` that displays a template for user to easily input their recipes including the title, ingredients, img_url, and instruction. 

### Created RESTFUL API routes in the server

* `GET` `/` --> show all recipes posts 
* `GET` `/recipes/<int:post_id>` --> show the recipe with the specific post_id 
* `POST` `/recipes/<int:post_id>/comment` --> create a comment on a recipe with the specific post_id
* `POST` `/recipes/new` --> create a new recipe post 
* `GET` `POST` `/recipes/<int:post_id>/edit` --> retrieve a recipe with a specific post_id and edit the post  
* `GET` `/recipes/<int:post_id>/delete` --> delete the recipe with a specific post_id and then displays updated recipe posts 
* `GET` `/about` --> display a brief story about me (the creator) and the website 
* `POST` `/register` --> register user
* `GET` `/login` --> login user
* `DELETE` `/logout` --> logout user 

After most http requests from the frontend, the database gets updated and stores the new data in the respective tables.
The server then returns a response of all data needed to display in the frontend.

## How to run the code.

### 1. Database

Create a database that includes three different tables: User, Recipe and Comment. 

![Brainstorm Image](/docs/database_brainstorm.jpg)

### 2. Environment Variables

The `.env` file stores the secret key and database url to protect the database and any other important information.

Place environment variables inside a file named `.env`

```
RECIPES_SECRET_KEY=8BYkEfBA6O6donzWlSihBXox7C0sKR6b
RECIPES_DATABASE_URL=postgresql://melanie:melanie@localhost/recipes
```

### 3. Install all necessary requirements.

I used the `flask` framework to develop the web application along with `sqlachemy` to communicate with the database.
I used `flask_login_manager` to help with user authentication.

Install the python dependencies

```sh
pip3 intall -r requirements.txt
```

### 4. Start the server

```sh
python3 main.py
```

### 5. Run the app

Open [http://127.0.0.1:5002](http://127.0.0.1:5002) in your browser

## TODO
* Categorize recipes either by type of cuisine or meal type of the day (breakfast, lunch, dinner, dessert, appetizer). 
