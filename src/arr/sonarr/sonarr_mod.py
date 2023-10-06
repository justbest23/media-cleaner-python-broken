from sonarr_api import get, delete  # Assuming you have a sonarr_api.py file

async def get_sonarr_data(id, is_4k=False):
    path = f"/series/{id}"
    return await get(path, None, is_4k)

async def remove_sonarr_data_and_files(sonarr_id):
    path = f"/series/{sonarr_id}"
    params = [("deleteFiles", "true"), ("addImportListExclusion", "false")]
    return await delete(path, params)
