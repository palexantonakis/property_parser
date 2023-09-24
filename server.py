import http.server
import socketserver

from postgres import fetch_data_from_postgres

# Create an HTML page template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Technical assignment</title>
</head>
<body>
    <h1>Technical Assignment - Aikaterini Adam</h1>

    <h2>Sell flats from sreality.cz</h2>
</body>
</html>
"""

# Define a custom request handler to serve the HTML page
class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            data = fetch_data_from_postgres()
            html = html_template.replace("{% for title, image_url in data %}", "")
            for prop in data:
                index = prop['index']
                title = prop['title']
                link = prop['link']
                html += f'<div><h3>{index} - {title}</h3><img src="{link}"</div>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            super().do_GET()
            
            
with socketserver.TCPServer(("", 8080), CustomRequestHandler) as httpd:
    print("Server started on port 8080")
    httpd.serve_forever()