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
        existing_entries = []
        existing_titles = set()  # Keep track of existing titles

        try:
            # Read existing entries from the file
            with open('manga_log.txt', 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines), 3):  # Read three lines at a time (Manga, URL, and a newline)
                    existing_title = lines[i].strip()[len("Manga: "):]
                    existing_url = lines[i + 1].strip()[len("URL: "):]
                    existing_entries.append((existing_title, existing_url))
                    existing_titles.add(existing_title)
        except FileNotFoundError:
            pass

        # Check if the title already exists
        if title in existing_titles:
            print(f"{title} already exists in the log file. Skipping logging.\n")
            return

        # Check if a newer chapter exists in the log
        for i, (existing_title, existing_url) in enumerate(existing_entries):
            # Extract manga name and chapter number from titles
            manga_name_existing, chapter_existing = existing_title.split("Chapter")
            manga_name_title, chapter_title = title.split("Chapter")

            # Remove leading/trailing spaces
            manga_name_existing = manga_name_existing.strip()
            manga_name_title = manga_name_title.strip()
            chapter_existing = float(chapter_existing.strip())
            chapter_title = float(chapter_title.strip())

            # Check if both titles belong to the same manga
            if manga_name_existing == manga_name_title:
                # Check if the existing chapter is newer
                if chapter_title > chapter_existing:
                    print(f"Found older chapter {chapter_existing} for {manga_name_existing}. Removing older entry.")
                    del existing_entries[i]
                    existing_entries.append((title, url))
                    break
                else :
                    print(f"Latest chapter for {manga_name_existing} is already in logs. Skipping logging.")
                    return

        # Write the updated entries to the file
        with open('manga_log.txt', 'w') as file:
            for existing_title, existing_url in existing_entries:
                if existing_title != title:
                    file.write(f"Manga: {existing_title}\nURL: {existing_url}\n\n")
            file.write(f"Manga: {title}\nURL: {url}\n\n")
            print(f"Manga logged: {title}\n")



