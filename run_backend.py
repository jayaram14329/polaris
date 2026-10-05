import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting POLARIS FastAPI Server on port {port} ...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
