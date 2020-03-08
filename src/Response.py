class Response:
    """ Class that sends responses to the client. """

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        if value is None:
            self._protocol = "HTTP/1.1"
        else:
            self._protocol = value

    def __init__(self, conn, encoding):
        self._protocol = "HTTP/1.1"
        self.conn = conn
        self.encoding = encoding

    def http_200_ok_reply(self, body):
        response_status = '200'
        response_status_text = 'OK'
        self.__reply__(body, response_status=response_status, response_status_text=response_status_text)

    def http_400_bad_request_reply(self):
        response_status = '400'
        response_status_text = 'Bad Request'
        self.__reply__('', response_status=response_status, response_status_text=response_status_text)

    def http_405_method_not_allowed_reply(self):
        response_status = '405'
        response_status_text = 'Method Not Allowed'
        self.__reply__('', response_status=response_status, response_status_text=response_status_text)

    def http_404_not_found_reply(self):
        response_status = '404'
        response_status_text = 'Not Found'
        self.__reply__('', response_status=response_status, response_status_text=response_status_text)

    def __get_response_headers__(self, body):
        return {
            'Content-Type': f'text/html; encoding={self.encoding}',
            'Content-Length': len(body),
            'Connection': 'keep-alive',
        }

    def __reply__(self, body, **kwargs):
        response_headers_raw = bytes(''.join('%s: %s\r\n' % (k, v) for k, v in self.__get_response_headers__(body).items()
                                             ), self.encoding)

        # Reply as HTTP / 1.1 server, saying for example "HTTP/1.1 OK"(code200).
        response_status = bytes(
            f'{self.protocol} {kwargs.get("response_status")} {kwargs.get("response_status_text")}\r\n',
            self.encoding)

        self.__send__(response_status, response_headers_raw, body)

    def __send__(self, status, response_headers, body):
        self.conn.send(status)

        self.conn.send(response_headers)
        self.conn.send(bytes('\r\n', self.encoding))  # to separate headers from body
        self.conn.send(bytes(body, self.encoding))
