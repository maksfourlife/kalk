from os import path, makedirs
from fastapi import FastAPI, File, HTTPException, status
import hashlib
import argparse

parser = argparse.ArgumentParser(
    prog="Kalk.", description="Deploy and execute your wasm modules."
)
parser.add_argument(
    "-db", default="./db", help='path to db directory. (default: "./db")'
)
args = parser.parse_args()


app = FastAPI(title="Kalk.", description="Deploy and execute your wasm modules.")


@app.post("/deploy")
def index(bytecode: bytes = File()):
    bytecode_hash = hashlib.sha1(bytecode).hexdigest()

    module_dir = path.join(args.db, bytecode_hash)
    if path.exists(module_dir):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="module already exists."
        )
    makedirs(module_dir)

    module_bin = path.join(module_dir, ".wasm")
    with open(module_bin, "wb") as f:
        f.write(bytecode)

    return {"address": bytecode_hash}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
