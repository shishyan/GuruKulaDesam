import sys
try:
    import websockets
    print("websockets installed!")
except ImportError:
    print("websockets NOT installed")
