from app import app
import os
import logging

logging.basicConfig(filename='access.log', level=logging.DEBUG)
app.run('0.0.0.0')
app.debug = True
