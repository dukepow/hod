from http.server import HTTPServer
from mod.manage import myHandler

# handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(('', 8070), myHandler) as httpd:
#     print('Server listening on port 8070...')
#     httpd.serve_forever()


if __name__ == "__main__":

    with HTTPServer(('', 8070), myHandler) as httpd:
        print('Server listening on port 8070...')
        httpd.serve_forever()
# http server를 생성한다.
# httpd = HTTPServer(('', 8070), myHandler)
# 서버 중지(Ctrl + Break)가 나올때까지 message 루프를 돌린다.
# httpd.serve_forever()
