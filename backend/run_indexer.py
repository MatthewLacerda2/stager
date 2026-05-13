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

    file_path = sys.argv[1]
    async with AsyncSessionLocal() as db:
        print(f"Starting indexing for: {file_path}...")
        try:
            object_ids = await index_asset(db, file_path)
            print(f"🎉 Successfully indexed assets! Database IDs: {object_ids}")
        except Exception as e:
            print(f"❌ Indexing failed with error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
