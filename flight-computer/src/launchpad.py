import time
import json
import websocket
import threading

class Client:
    def __init__(self, rocket):
        self.rocket = rocket
        self.client = None
        self.on_pair_handler = None
        self.on_arm_handler = None
        self.on_disarm_handler = None

    def connect(self):
        self.client = websocket.WebSocketApp("ws://launchpad.local/api")
        self.client.on_message = lambda socket, message: self.on_message(socket, message)
        self.client.on_open = lambda socket: self.on_open(socket)
        self.client.on_error = lambda socket, error: self.on_error(socket, error)
        threading.Thread(target=self.client.run_forever).start()

    def on_error(self, socket, error):
        time.sleep(5)
        threading.Thread(target=self.connect).start()

    def on_message(self, socket, message):
        message = json.loads(message)
        if message['command'] == 'pair':
            self.on_pair(message['launcher'])
        elif message['command'] == 'arm':
            self.on_arm(socket)
        elif message['command'] == 'disarm':
            self.on_disarm(socket)

    def on_open(self, socket):
        socket.send(json.dumps({'command': 'pair', 'type': 'rocket', 'rocket': {'name': self.rocket}}))

    def on_pair(self, launchpad):
        self.on_pair_handler(launchpad)
        return

    def on_arm(self, socket):
        if self.on_arm_handler() == True:
            socket.send(json.dumps({'command': 'update', 'type': 'armed'}))
        return

    def on_disarm(self):
        if self.on_disarm_handler() == True:
            socket.send(json.dumps({'command': 'update', 'type:': 'disarmed'}))
        return
