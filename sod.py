from http.server import HTTPServer
from mod.manage import myHandler

# handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(('', 8070), myHandler) as httpd:
#     print('Server listening on port 8070...')
#     httpd.serve_forever()


if __name__ == "__main__":

    # args = parser.parse_args()
    # if args.cgi:
    myHandler.stop_server = 0
    myHandler.base_directory = "./www"   # not add /
    myHandler.stop_command = "/shutdown"  # server shutdown command
    myHandler.reboot_command = "/reboot"  # server reboot command (cash refresh)

    while myHandler.stop_server != 4:
        httpd = HTTPServer(('', 8070), myHandler)
        print('Server listening on port 8070...')
        # httpd.serve_forever()
        httpd.timeout = 1
        while myHandler.stop_server == 0:
            # print(myHandler.stop_server)
            httpd.handle_request()

        print("서버 죽었나", myHandler.stop_server)
        if myHandler.stop_server == 2:  # reboot
            myHandler.stop_server = 0
            httpd = 0
        else:
            print("죽어라")

    print("죽었어")
# http server를 생성한다.
# httpd = HTTPServer(('', 8070), myHandler)
# 서버 중지(Ctrl + Break)가 나올때까지 message 루프를 돌린다.
# httpd.serve_forever()
