from http.server import HTTPServer
from mod.manage import myHandler
import os

# handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(('', 8070), myHandler) as httpd:
#     print('Server listening on port 8070...')
#     httpd.serve_forever()


if __name__ == "__main__":

    # args = parser.parse_args()
    # if args.cgi:
    myHandler.stop_server = 0
    myHandler.base_url = "http://localhost:8070"
    myHandler.base_directory = os.getcwd() + "/www"   # not add /
    myHandler.stop_command = "/shutdown"  # server shutdown command
    myHandler.reboot_command = "/reboot"  # server reboot command (cash refresh)

    while myHandler.stop_server != 4:
        httpd = HTTPServer(('', 8070), myHandler)
        print('Server listening on port 8070...')
        # httpd.serve_forever() # not used
        httpd.timeout = 1
        while myHandler.stop_server == 0:
            # print(myHandler.stop_server)
            httpd.handle_request()

        httpd.handle_request()
        
        print("request server command", myHandler.stop_server)
        if myHandler.stop_server == 2:  # reboot
            myHandler.stop_server = 0
            httpd = 0
        else:
            print("kill")

    print("killed")
