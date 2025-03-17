import sys
sys.path.insert(0, '/home/ivan/hexlet-flask-example')
print('sys.path', sys.path)
from app import app

__all__ = (app,)