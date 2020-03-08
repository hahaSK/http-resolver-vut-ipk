import ipaddress
import socket
import sys
import re

from IPKExceptions import *
from Response import Response

HOST = 'localhost'
ENCODING = "utf-8"


def normalize_line_endings(request_data):
    """ Normalizes line endings into '\n' as they can be '\r\n' etc. """
    return ''.join((line + '\n') for line in request_data.splitlines())


def parse_post_request_data(request):
    request_head, request_body = request.split('\n\n', 1)

    # First line is request headline and others are headers
    request_head = request_head.splitlines()
    # Headline is smt "POST some/request HTTP/1.1
    request_headline = request_head[0]
    # Headers have their name and value separated by ': '. They can be duplicates
    # but dict drops duplicates.
    request_headers = dict(x.split(': ', 1) for x in request_head[1:])

    return request_body.splitlines()


def parse_request_data(request):
    """ Parses request data into groups. """
    # DEBUG
    # print(request)
    op_code_pattern = r"^(GET|POST)\s"

    match = re.match(op_code_pattern, request)
    if match is None:
        raise MethodNotAllowedException405()

    http_request = match[0]

    if http_request.strip() == 'GET':
        parameter_pattern = op_code_pattern + r"\/resolve\?name=(.*)\\?&type=(A|PTR)\s+(HTTP\/\d\.\d)"
    else:
        parameter_pattern = op_code_pattern + r"\/dns-query\s+(HTTP\/\d\.\d)"

    match = re.match(parameter_pattern, request)

    if match is None:
        raise BadRequestException400()

    dns = dns_type = request_body = None
    if http_request.strip() == 'GET':
        dns = match[2].rstrip('\\').strip()
        dns_type = match[3]
        proto = match[4]
    else:
        proto = match[2]
        request_body = parse_post_request_data(request)

    return http_request.strip(), dns, dns_type, proto, request_body


def resolve_dns(dns, dns_type):
    """ Resolves dns address. Creates body response. """
    try:
        address_name_ip = socket.gethostbyaddr(dns)
    except Exception:
        raise NotFoundException404()

    if dns_type == 'A':
        # domain name:A = ip address
        body = f"{dns}:{dns_type}={address_name_ip[2][0]}\r\n"
    else:
        # ip address:PTR = domain name
        body = f"{dns}:{dns_type}={address_name_ip[0]}\r\n"

    return body


def parse_post_dns_entry(dns_entry):
    """ Parses dns entry. """

    # pattern is something like "www.google.com:A" or "147.229.14.131:PTR"
    pattern = r"^\s*(.*)\s*:\s*(A|PTR)\s*$"

    match = re.match(pattern, dns_entry)

    if match is None:
        raise BadRequestException400()

    return match[1].strip(), match[2]


def check_dns_type_call(dns, dns_type):
    """ Checks if the dns matches the dns_type"""
    try:
        ipaddress.ip_address(dns)
        if dns_type == 'A':
            raise BadRequestException400()
    except ValueError:
        if dns_type == 'PTR':
            raise BadRequestException400()


def run_socket(s):
    """ Runs the socket and resolve POST and GET methods. """
    s.listen()
    conn, address = s.accept()
    response = Response(conn, ENCODING)
    with conn:
        # print("Connected by ", address[0])
        while True:
            data = conn.recv(1024)
            if not data:
                # DEBUG
                # print("No data received")
                conn.close()
                return

            try:
                http_request, dns, dns_type, proto, request_body = parse_request_data(
                    normalize_line_endings(data.decode()))
                # DEBUG
                # print(http_request)
                # print(dns)
                # print(dns_type)
                response.protocol = proto
            except BadRequestException400:
                response.http_400_bad_request_reply()
                continue
            except MethodNotAllowedException405:
                response.http_405_method_not_allowed_reply()
                continue

            body = ''
            if http_request == 'GET':
                try:
                    check_dns_type_call(dns, dns_type)
                    body = resolve_dns(dns, dns_type)
                except NotFoundException404:
                    response.http_404_not_found_reply()
                    continue
                except BadRequestException400:
                    response.http_400_bad_request_reply()
                    continue
            else:
                entry_ok = False
                for dns_entry in request_body:
                    try:
                        dns, dns_type = parse_post_dns_entry(dns_entry)
                        check_dns_type_call(dns, dns_type)
                        body += (resolve_dns(dns, dns_type))
                        entry_ok = True
                    except NotFoundException404:
                        continue
                    except BadRequestException400:
                        continue

                if not entry_ok:
                    response.http_400_bad_request_reply()

            # DEBUG
            # print(body)
            response.http_200_ok_reply(body)


def run_server():
    # Check parameters
    if len(sys.argv) < 2:
        print(sys.stderr, "PORT not set!")
        exit(-1)

    port = int(sys.argv[1])
    # Check if port is uint16
    if port > 65535 or port <= 0:
        print(sys.stderr, "Wrong PORT number!")
        exit(-2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        while True:
            run_socket(s)


run_server()
