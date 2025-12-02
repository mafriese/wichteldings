import os

port = os.environ.get("PORT", "8080")
bind = "0.0.0.0:" + port
workers = 1
threads = 8
timeout = 0
