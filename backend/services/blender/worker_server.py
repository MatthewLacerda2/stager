import os
import sys
import json
import http.server

# Add current dir to path to import our modules
sys.path.append(os.path.dirname(__file__))

import photoshoot
import extract_obj
import render_camera

class BlenderWorkerHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))
        
        try:
            if self.path == "/extract":
                input_file = payload["input_file"]
                output_file = payload["output_file"]
                bounds = extract_obj.process(input_file, output_file)
                self._send_success({"bounds": bounds})
                
            elif self.path == "/photoshoot":
                input_obj = payload["input_obj"]
                output_dir = payload["output_dir"]
                images = photoshoot.process(input_obj, output_dir)
                self._send_success({"images": images})
                
            elif self.path == "/render":
                scene_data = payload["scene_data"]
                output_path = payload["output_path"]
                is_sketch = payload.get("is_sketch", False)
                image = render_camera.process(scene_data, output_path, is_sketch)
                self._send_success({"image": image})
                
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Endpoint not found"}')
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _send_success(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "success"}
        response.update(data)
        self.wfile.write(json.dumps(response).encode())

def run(port=50051):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, BlenderWorkerHandler)
    print(f"Blender Persistent Worker running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
