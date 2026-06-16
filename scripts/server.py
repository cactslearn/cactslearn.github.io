import http.server
import socketserver
import os

PORT = 8000

class CleanURLHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract path without query parameters or fragment anchors
        clean_path = self.path.split('?')[0].split('#')[0]
        
        # If the requested path is not root and does not end with an extension
        if clean_path != '/' and not os.path.splitext(clean_path)[1]:
            # Translate path to local file path
            local_filepath = self.translate_path(clean_path)
            
            # If the exact path doesn't exist, but the .html file does, rewrite path
            if not os.path.exists(local_filepath) and os.path.exists(local_filepath + '.html'):
                self.path = clean_path + '.html'
                
        return super().do_GET()

if __name__ == "__main__":
    # Ensure current working directory is the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    # Allow port reuse to avoid 'Address already in use' errors on quick restarts
    socketserver.TCPServer.allow_reuse_address = True
    print(f"Starting CACTS Local Dev Server on http://localhost:{PORT}")
    print("Supporting Clean SEO URLs (e.g. clicking '/about' loads 'about.html')")
    
    with socketserver.TCPServer(("", PORT), CleanURLHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping CACTS Dev Server.")
