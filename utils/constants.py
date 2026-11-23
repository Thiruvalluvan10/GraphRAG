import configparser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPERTIES_FILE = os.environ.get(
    "APP_CONFIG_FILE",
    os.path.join(BASE_DIR, "resources", "application.properties"),
)

config = configparser.ConfigParser(interpolation=None)
config.optionxform = str  # keep keys in CAPS as written
if not config.read(PROPERTIES_FILE, encoding="utf-8"):
    raise FileNotFoundError(f"Could not read {PROPERTIES_FILE}")

# [WEAVIATE_CLUSTER]
WEAVIATE_HOST = config.get("WEAVIATE_CLUSTER", "HOST")
WEAVIATE_HTTP_PORT = config.getint("WEAVIATE_CLUSTER", "HTTP_PORT")
WEAVIATE_GRPC_PORT = config.getint("WEAVIATE_CLUSTER", "GRPC_PORT")
WEAVIATE_SECURE = config.getboolean("WEAVIATE_CLUSTER", "SECURE")
WEAVIATE_API_KEY = config.get("WEAVIATE_CLUSTER", "API_KEY")