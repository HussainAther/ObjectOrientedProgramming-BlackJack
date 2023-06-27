# ObjectOrientedProgramming-BlackJack

GUI for playing Blackjack - complete with animations.

Card images from Byron Knoll: http://code.google.com/p/vector-playing-cards/ and https://opengameart.org/content/colorful-poker-card-back

## Play single player
Please use `pip install pillow` for installing the Pillow library.

Run using `python singleplayer.py` . 

## Play multiplayer
Please use `pip install flask flask-socketio`, `pip install eventlet`, and `pip install python-socketio` for WebSocket support. 

For compatibility reasons, it's recommended to use the following versions:

```
pip install --upgrade python-socketio==4.6.0

pip install --upgrade python-engineio==3.13.2

pip install --upgrade Flask-SocketIO==4.3.1
```

It's recommended to use a secret key.  

The SECRET_KEY is a security measure used in Flask to protect against cross-site request forgery (CSRF) attacks and other security vulnerabilities. It is recommended to generate a random secret key and keep it confidential.

Generate one in Python like this:

```
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)
```

And replace `your_secret_key` this line in `multiplayer.py`:

```
app.secret_key = "your_secret_key"
```

Make sure to keep the secret key private and avoid sharing it publicly or committing it to version control repositories.

Then run using `python multiplayer.py`.

The server will be accessible to one player at http://localhost:5000 or the URL output by the Flask. The second player must visit the IP address of the first player followed by the port (e.g., xxx.xxx.x.xxx:5000). 
