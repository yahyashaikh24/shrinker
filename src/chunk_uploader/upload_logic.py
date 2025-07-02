import os
import aiofiles
import shutil

CHUNK_DIR = "uploaded_chunks"
FINAL_DIR = "final_files"

os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

async def save_chunk(file, chunk_index, file_id):
    file_path = os.path.join(CHUNK_DIR, file_id)
    os.makedirs(file_path, exist_ok=True)

    chunk_name = os.path.join(file_path, f"chunk_{chunk_index:05d}.part")

    async with aiofiles.open(chunk_name, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)


def check_upload_status(file_id: str, total_chunks: int):
    file_path = os.path.join(CHUNK_DIR, file_id)
    if not os.path.exists(file_path):
        return "missing"

    uploaded_chunks = len(os.listdir(file_path))
    if uploaded_chunks == total_chunks:
        return "complete"
    else:
        return "incomplete"


async def assemble_chunks(file_id: str, original_filename: str):
    chunk_dir = os.path.join(CHUNK_DIR, file_id)
    final_path = os.path.join(FINAL_DIR, original_filename)

    with open(final_path, 'wb') as outfile:
        for chunk_file in sorted(os.listdir(chunk_dir)):
            chunk_path = os.path.join(chunk_dir, chunk_file)
            with open(chunk_path, 'rb') as c:
                shutil.copyfileobj(c, outfile)

    return final_path
