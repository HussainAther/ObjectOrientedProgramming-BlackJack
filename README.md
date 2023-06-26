# ObjectOrientedProgramming-BlackJack

GUI for playing Blackjack - complete with animations.

## Play single player
Run using `python singleplayer.py` . 

Card images from Byron Knoll: http://code.google.com/p/vector-playing-cards/

Please use `pip install pillow` for installing the `ImageTK` module from the Pillow library.

## Player multiplayer
Please use `pip install flask flask-socketio` for WebSocket support. 

It's recommended to use a `SECRET_KEY`:

```
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)
```

Then run using `python multiplayer.py`.

The server will be accessible at http://localhost:5000.
