import logging
import sys

def setup_logging():
    """
    Configures a professional logging format for the entire application.
    In production, this could be extended to send logs to a file or a JSON formatter.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s (%(lineno)d): %(message)s",
        stream=sys.stdout,
    )

    # Prevent 'uvicorn.access' from flooding the terminal with every request
    # but keep errors visible.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Optional: Silence SQLAlchemy logs unless you are debugging SQL
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)