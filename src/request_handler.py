from http.server import BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            url = data.get('url')
            title = data.get('title')
            
            if title.endswith(" - Mangakakalot.com"):
                title = title.replace("- Mangakakalot.com", "").strip()

            if url and title:
                self.log_data(url, title)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write("Data logged successfully".encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')  # Add CORS header
                self.end_headers()
                self.wfile.write("Bad Request".encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')  # Add CORS header
            self.end_headers()
            self.wfile.write("Internal Server Error".encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_data(self, url, title):
        existing_titles = set()
        
        try:
            with open('manga_log.txt', 'r') as file:
                for line in file:
                    if line.startswith("Manga:"):
                        existing_titles.add(line[len("Manga:"):].strip())
        except FileNotFoundError:
            pass

        # check if title is already in file
        if title.strip() not in existing_titles:
            # if not present, append to file
            with open('manga_log.txt', 'a') as file:
                file.write(f"Manga: {title}\nURL: {url}\n\n")
                print(f"Data logged: {title}\n")
        else:
            print(f"{title} already exists in the log file. Skipping logging.\n")
