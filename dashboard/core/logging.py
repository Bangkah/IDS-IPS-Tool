import logging

def setup_logging():
    logging.basicConfig(
        filename="dashboard_audit.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
