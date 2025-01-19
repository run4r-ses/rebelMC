from datetime import datetime
class MethodLogger:
    def __init__(self, log_file_path, name=""):
        self.log_file_path = log_file_path
        self.log_file = open(log_file_path, "r+")
        self.name = name

    def log(self, type, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        branding = f" <{self.name}>" if self.name else ""
        self.log_file.write(f"[{timestamp}]{branding} [{type}] {msg}\n")
        self.log_file.flush()
    
    def debug(self, msg):
        self.log("DEBUG", msg)
    
    def info(self, msg):
        self.log("INFO", msg)
    
    def warning(self, msg):
        self.log("WARNING", msg)
    
    def error(self, msg):
        self.log("ERROR", msg)
    
    def close(self):
        self.log_file.close()
