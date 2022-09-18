from server import app
import uvicorn

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["default"]["fmt"] = "[%(levelname)s] Uvicorn - %(message)s"

HOST = "localhost"
PORT = 8080

if __name__ == "__main__":
    uvicorn.run(app.fastapi, host=HOST, port=PORT, log_config=log_config)
