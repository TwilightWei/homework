from app import app # read and setup configurations of the server and import flask app instance

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
