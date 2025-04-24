import os
from flask import Flask

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['DEBUG'] = True