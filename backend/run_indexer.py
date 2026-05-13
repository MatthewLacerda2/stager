import asyncio
import os
import sys

# Ensure we can import backend packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.database import AsyncSessionLocal
from backend.services.AssetIndexerService.indexer_job import index_asset

async def main():
    if len(sys.argv) < 2:
        print("Usage: python backend/run_indexer.py <path_to_3d_file>")
        return

    input_path = sys.argv[1]
    async with AsyncSessionLocal() as db:
        if os.path.isdir(input_path):
            print(f"Starting batch indexing for folder: {input_path}...")
            valid_extensions = {".obj", ".blend"}
            files_to_index = []
            for root, _, files in os.walk(input_path):
                for f in files:
                    if os.path.splitext(f)[1].lower() in valid_extensions:
                        files_to_index.append(os.path.join(root, f))
            
            if not files_to_index:
                print("No .obj or .blend files found in directory.")
                return
                
            print(f"Found {len(files_to_index)} files to index.")
            for idx, file_path in enumerate(files_to_index, 1):
                print(f"\n[{idx}/{len(files_to_index)}] Indexing: {file_path}...")
                try:
                    object_ids = await index_asset(db, file_path)
                    print(f"  🎉 Successfully indexed! Database IDs: {object_ids}")
                except Exception as e:
                    print(f"  ❌ Indexing failed with error: {e}")
        else:
            print(f"Starting indexing for: {input_path}...")
            try:
                object_ids = await index_asset(db, input_path)
                print(f"🎉 Successfully indexed asset! Database IDs: {object_ids}")
            except Exception as e:
                print(f"❌ Indexing failed with error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
