import logging

from app import app

def init_loggers():
    """
    Initializing two app loggers writing to logfile.log:
    root - General logs and incoming requests
    c_logger - Outcoming requests (via requests library)
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    c_logger = logging.getLogger("requests.packages.urllib3")
    c_logger.setLevel(logging.DEBUG)
    c_logger.propagate = True

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s")

    fh = logging.FileHandler("logfile.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    root.addHandler(fh)
    c_logger.addHandler(fh)

def main():
    """
    Main function - Initializes settings and runs the app
    """
    init_loggers()
    app.run()


if __name__ == "__main__":
    main()
