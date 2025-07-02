#!/usr/bin/env python3
"""
Simple HTTP server for AI Prompt Directory
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 AI Prompt Directory Server")
        print(f"📂 Serving directory: {DIRECTORY}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📊 Database contains 3,438 prompts across 10 categories")
        print("\nPress Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("🌍 Browser opened automatically")
        except:
            print("💡 Open your browser and navigate to the URL above")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()