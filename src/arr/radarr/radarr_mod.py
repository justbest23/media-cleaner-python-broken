from radarr_api import get, delete  # Assuming you have a radarr_api.py file

async def get_radarr_data(id, is_4k=False):
    path = f"/movie/{id}"
    return await get(path, None, is_4k)

async def delete_radarr_data_and_files(radarr_id):
    path = f"/movie/{radarr_id}"
    params = [("deleteFiles", "true"), ("addImportExclusion", "false")]
    return await delete(path, params)
