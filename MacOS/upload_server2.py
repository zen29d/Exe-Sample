from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import uuid

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            upload_dir = "./uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            unique_filename = f"uploaded_file_{uuid.uuid4().hex}.zip"
            file_path = os.path.join(upload_dir, unique_filename)
            
            with open(file_path, "wb") as f:
                f.write(post_data)
            
            # Send a response
            self.send_response(200)
            self.end_headers()
            response_message = f"File uploaded successfully! {unique_filename}"
            self.wfile.write(response_message.encode())
            print(f"File received and saved to {file_path}")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            err = f"Error: {str(e)}"
            self.wfile.write(err.encode())
            print(err)

# Start the server
server_add = ('', 80)
httpd = HTTPServer(server_add, SimpleHTTPRequestHandler)
print("Starting server on port 80...")
httpd.serve_forever()
