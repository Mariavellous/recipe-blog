Hungry? https://fave-recipes.herokuapp.com/


# The Recipe Blog 🥘

## How to run the code.

### 1. Database


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

### 5. Play the game

Open [http://127.0.0.1:5008](http://127.0.0.1:5008) in your browser


## Thought Process


## Code Structure


### Created RESTFUL API routes in the server


### TODO
