from http.server import BaseHTTPRequestHandler
import io
import urllib.parse as urlparse
import mod.common as mcom
import mod.UJlib as ujlib


class myHandler(BaseHTTPRequestHandler):

    stop_server = 0
    base_directory = "./www"   # not add /
    stop_command = "/shutdown"
    reboot_command = "/reboot"

    # GET형식의 파라미터를 파싱한다.(url의 물음표(?) 이후의 값을 딕셔너리로 파싱한다.
    def __get_Parameter(self, key):
        # 해당 클래스에 __param변수가 선언되었는지 확인한다.
        if hasattr(self, "_myHandler__param") == False:
            if "?" in self.path:
                # url의 ?이후의 값을 파싱한다.
                self.__param = dict(urlparse.parse_qsl(self.path.split("?")[1], True))
            else:
                # url의 ?가 없으면 빈 딕셔너리를 넣는다.
                self.__param = {}
        if key in self.__param:
            return self.__param[key]
        return None

    # POST형식의 form 데이터를 파싱한다.
    def __get_Post_Parameter(self, key):
        # 해당 클래스에 __post_param변수가 선언되었는지 확인한다.
        if hasattr(self, "_myHandler__post_param") == False:
            # 해더로 부터 formdata를 가져온다.
            data = self.rfile.read(int(self.headers['Content-Length']))
            if data is not None:
                self.__post_param = dict(urlparse.parse_qs(data.decode()))
            else:
                self.__post_param = {}
        if key in self.__post_param:
            return self.__post_param[key][0]
        return None

    # http 프로토콜의 header 내용을 넣는다.
    def __set_Header(self, code, content_type="text/html"):
        # 응답 코드를 파라미터로 받아 응답한다.
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    # http 프로토콜의 body내용을 넣는다.
    def __set_Body(self, data: str):
        # body 응답은 byte형식으로 넣어야 한다.(필요에 의해 주석 해제)
        #response = io.BytesIO()
        #response.write(b"<html><body><form method='post'><input type='text' name='test' value='hello'><input type='submit'></form></body></html>");
        # self.wfile.write(response.getvalue());
        # data(string)를 byte형식으로 변환해서 응답한다.
        self.wfile.write(data.encode('utf-8'))

    # POST 형식의 request일 때 호출된다.
    def do_GET(self):
        if self.path == "/":
            response = io.FileIO(myHandler.base_directory + '/index.sod', mode='r')
            # response = io.BytesIO(f)
            self.__set_Header(200)
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            self.wfile.write(response.read())
        elif self.path == myHandler.stop_command:
            # 서버 죽이기
            self.__set_Header(200)
            body = "서버를 종료합니다"
            self.__set_Body(body)
            myHandler.stop_server = 4
        elif self.path == myHandler.reboot_command:
            # 서버 죽이기
            self.__set_Header(200)
            body = "서버를 종료합니다"
            self.__set_Body(body)
            myHandler.stop_server = 2
        else:
            if ujlib.FileExists(myHandler.base_directory + self.path):
                if self.path.find(".sod") > 0:
                    # hod 의 처리
                    response = io.FileIO(myHandler.base_directory + self.path)
                else:
                    # 일반 파일들
                    response = io.FileIO(myHandler.base_directory + self.path)

                self.__set_Header(200, mcom.get_mimetype(self.path))

                self.wfile.write(response.read())
            else:
                self.__set_Header(403)

            # GET 방식의 파라미터의 data 값을 취득한다.
            # data = self.__get_Parameter('data')
            # response(응답)할 body내용이다.

    # POST 형식의 request일 때 호출된다.

    def do_POST(self):
        # response header code는 200(정상)으로 응답한다.
        self.__set_Header(200)
        # response body는 form으로 받은 test의 값으로 응답한다.
        self.__set_Body(self.__get_Post_Parameter('test'))
