# ObjectOrientedProgramming-BlackJack

GUI for playing Blackjack - complete with animations.

## Play single player
Run using `python singleplayer.py` . 

Card images from Byron Knoll: http://code.google.com/p/vector-playing-cards/

Please use `pip install pillow` for installing the `ImageTK` module from the Pillow library.

## Play multiplayer
Please use `pip install flask flask-socketio` and `pip install python-socketio` for WebSocket support. 

It's recommended to use a `SECRET_KEY`. 

The SECRET_KEY is a security measure used in Flask to protect against cross-site request forgery (CSRF) attacks and other security vulnerabilities. It is recommended to generate a random secret key and keep it confidential.

Generate one in Python like this:

```
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)
```

And replace `YOUR_SECRET_KEY` this line in `multiplayer.py`:

```
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
```

Make sure to keep the secret key private and avoid sharing it publicly or committing it to version control repositories.

Then run using `python multiplayer.py`.

The server will be accessible at http://localhost:5000.
