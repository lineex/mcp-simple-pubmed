from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from io import StringIO
from contextlib import redirect_stdout

# 添加mcp_simple_pubmed到Python路径
sys.path.insert(0, '/app')
from mcp_simple_pubmed import server

class StreamableHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # 解析请求
            request = json.loads(post_data.decode('utf-8'))
            
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Transfer-Encoding', 'chunked')
            self.end_headers()
            
            # 捕获标准输出
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            try:
                # 处理请求
                # 这里需要根据MCP协议实现具体的请求处理逻辑
                # 以下是一个示例框架
                
                # 模拟流式输出
                for i in range(10):
                    chunk = json.dumps({
                        "type": "chunk",
                        "data": f"Processing step {i+1}",
                        "progress": (i+1)*10
                    }) + "\n"
                    
                    self.wfile.write(bytes(f"{len(chunk):X}\r\n{chunk}\r\n", "utf-8"))
                    self.wfile.flush()
                
                # 最终结果
                result = json.dumps({
                    "type": "result",
                    "data": "Processing complete"
                }) + "\n"
                
                self.wfile.write(bytes(f"{len(result):X}\r\n{result}\r\n", "utf-8"))
                self.wfile.write(b"0\r\n\r\n")  # 结束chunked传输
                
            finally:
                # 恢复标准输出
                sys.stdout = old_stdout
                
        except Exception as e:
            self.send_error(500, str(e))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StreamableHTTPHandler)
    print(f"Starting streamable HTTP server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
