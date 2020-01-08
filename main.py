from app import app
import os

if __name__ == "__main__":
    if os.environ.get("DRAGNET_DEPLOYMENT", None) == "local":
        app.run(host="0.0.0.0")
    else:
        app.run()