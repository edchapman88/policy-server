import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class MVar:
    """
    Class to allow a single element pipeline between producer and consumer.
    """

    def __init__(self, init_val):
        self.message = init_val
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def recv(self):
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        return message

    def send(self, message):
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()


def make_handler_class(to_policy: MVar, from_policy: MVar):
    class Server(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            obs_reward = self.rfile.read(content_length).decode('utf-8')
            to_policy.send(obs_reward)
            action = from_policy.recv()
            self._set_response()
            self.wfile.write(action.encode('utf-8'))

    return Server


class PolicyServer:
    def __init__(self, hostname: str, port: int):
        self.to_server = MVar('')
        self.from_server = MVar('')

        def thread_fn():
            """
            Function to run in a seperate thread (a http server daemon thread).

            Start a web server listening on `hostname`:`port`. Observations and Rewards are received by the server, and sent along an MVar channel back to the main thread. Actions are sent along a second MVar channel, from the main thread to the http server daemon thread.
            """
            handler_class = make_handler_class(
                to_policy=self.from_server, from_policy=self.to_server
            )
            server = HTTPServer((hostname, port), handler_class)
            server.serve_forever()

        self.server = threading.Thread(target=thread_fn, daemon=True)
        self.server.start()

    def get_obs(self) -> str:
        return self.from_server.recv()

    def post_action(self, action: str):
        self.to_server.send(action)
