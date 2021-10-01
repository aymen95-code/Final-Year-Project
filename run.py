"""
    This is the entry file,
"""
from Mood import create_app

__author__ = 'AymenHitta'

app = create_app()

if __name__ == "__main__":
    # Launch the flask server
    app.run(debug=True)
