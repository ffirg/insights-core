import sys
from threading import Thread
import socket

if (sys.version_info > (3, 0)):
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


def get_free_port():
    """
    Retrieves a free port for the mock service to use

    :return (int): free port
    """
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


SERVER_PORT = get_free_port()


class RequestHandler(BaseHTTPRequestHandler):
    """
    BaseHTTPRequestHandler subclass configured to handle GET requests for the TestMockServer.

    Functions:
        do_GET(): Handles the get fall from the HTTPServer
    """
    def do_GET(self):

        print(self.path)
        value = ''
        send_reply = False
        if self.path.endswith("/mock/"):
            send_reply = True

        value = "text/json"

        if send_reply:
            self.send_response(200)
            self.send_header('Content-type', value)
            self.end_headers()
            output = ""
            output += '{"data":{"id": "001", "name": "Successful return from Mock Service"}}'
            self.wfile.write(output.encode('utf_8'))
            self.wfile.write(output)
            print(output)
            return output
        else:
            self.send_response(404)
            self.send_header('Content-type', value)
            self.end_headers()
            output = ""
            output += '{"error":{"code": "404", "message": "Not Found"}}'
            self.wfile.write(output.encode('utf_8'))
            print(output)
            return
        return


class TestMockServer(object):
    """
    TestMockServer subclass for accessing external Web resources using caching.

    Functions:
        setup_class(): Class mathod that creates the Test Service daemon
        get_server_port: Helper function to get the port that was used to start the service.

    Examples:

        >>> from insights.tests.mock_web_server import TestMockServer, RequestHandler

        >>> crr = CachedRemoteResource()
        >>> sv = TestMockServer()
        >>> sv.setup_class()
        >>> sv.get_server_port()
        35917
        >>> curl -X GET http://localhost:40713/mock/
        {"data":{"id": "001", "name": "Successful return from Mock Service"}}
    """

    @classmethod
    def setup_class(cls):
        cls.server_port = get_free_port()
        cls.mock_server_port = get_free_port()
        cls.mock_server = HTTPServer(('localhost', cls.server_port), RequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

    def get_server_port(self):

        return self.server_port
