from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# 生肖列表（以2000年为鼠年）
zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 如果是根路径，返回 HTML 页面
        if self.path == '/':
            with open('index.html', 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        
        # 如果是 /calc?year=1990，处理计算并返回结果
        elif self.path.startswith('/calc'):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            year_str = query.get('year', [''])[0]
            
            if not year_str:
                self.send_error(400, "年份未提供")
                return

            try:
                year = int(year_str)
                offset = (year - 2000) % 12
                zodiac = zodiacs[offset]
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(zodiac.encode('utf-8'))
            except Exception as e:
                self.send_error(500, "计算错误")
                print(e)

    def log_message(self, format, *args):
        # 美化控制台输出
        pass

# 启动服务器
if __name__ == '__main__':
    print("🚀 正在启动网页服务器...")
    print("👉 打开浏览器，访问：http://localhost:8000")
    print("🛑 按 Ctrl+C 停止服务")

    server = HTTPServer(('localhost', 8000), MyHandler)
    server.serve_forever()
