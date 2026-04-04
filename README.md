# Gameseeds

## Application features
- Users can create an account and log in.
- Users can add, edit and delete posts.
- Posts require a unique seed and the game the seed is for.
- Posts can have a description and a list of tags.
- Users can search and see created posts.
- Users can search for posts with specific tags.
- Users can like posts.
- Users can comment on posts.
- Original poster can highlite comments on their post.
- Application has a public user page that includes, total post likes and created posts.

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
