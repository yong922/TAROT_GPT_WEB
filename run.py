import os
from app import create_app, db
os.environ.setdefault("APP_ENV", "dev") 

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)