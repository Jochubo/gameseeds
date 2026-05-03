# Gameseeds

## Application features
- Users can create an account and log in.
- Users can add, edit and delete posts.
- Users can add new games.
- Posts require a unique seed and the game the seed is for.
- Post creation checks if the seed matches the conditionals for the game it's for.
- Posts can have a description.
- Users can search and see added games.
- Users can search and see posts once they have selected a game.
- Users can comment on posts.
- Application has a public user page that includes total posts and total comments.

## Installation

Install the `flask`-library:

```
$ pip install flask
```

Initialize tables:

```
$ sqlite3 database.db < schema.sql
```

For startup run:

```
$ flask run
```
