from flask import Flask, render_template

# Create app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register/', methods=['POST'])
def register_post():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
