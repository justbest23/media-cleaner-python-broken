import asyncio
from config import Config  # Replace with your actual config module
from media_item import CompleteMediaItem, MediaItem  # Replace with your actual media_item module
from overseerr.overseerr_responses import MediaRequest, ServerItem  # Replace with your actual overseerr module
from utils import human_file_size  # Replace with your actual utils module
from itertools import groupby
from operator import itemgetter
import os

async def main():
    read_and_validate_config()
    deletion_items = await get_deletion_items()
    show_requests_result(deletion_items)
    clear_screen()
    chosen = choose_items_to_delete(deletion_items)
    await delete_chosen_items(deletion_items, chosen)

def read_and_validate_config():
    try:
        Config.read_conf()
    except Exception as e:
        raise Exception(f"Failed to read the config, with the following error: {e}.\nPlease make sure all fields are filled.")
    
    config = Config.global_config()
    if config.radarr is None and config.sonarr is None:
        raise Exception("You have not configured Sonarr or Radarr. Application can't continue without at least one of these.")

async def get_deletion_items():
    print("Gathering all required data from your services.\nDepending on the amount of data and your connection speed, this could take a while...")
    all_items = True  # Replace with actual logic to get this value
    
    media_items = [MediaItem.from_request(req) for req in await MediaRequest.get_all()]
    
    if all_items:
        not_requested_media_items = [MediaItem.from_server_item(item) for item in await ServerItem.get_all()]
        media_items += not_requested_media_items
    
    # Remove duplicates and sort by title
    media_items.sort(key=lambda x: (x.rating_key, not x.request))
    media_items = [next(g) for k, g in groupby(media_items, key=itemgetter('rating_key'))]
    
    complete_items = []
    errors = []
    for item in media_items:
        if item.is_available() and item.has_manager_active() and not item.user_ignored():
            try:
                complete_item = await item.into_complete_media()
                complete_items.append(complete_item)
            except Exception as e:
                errors.append(e)
    
    if errors:
        show_potential_request_errors(errors)
    
    return complete_items

def show_potential_request_errors(errors):
    print(f"You got {len(errors)} errors while gathering data. Press y to show them, or any other input to continue with the errored items ignored.")
    user_input = input().strip().lower()
    if user_input.startswith('y'):
        for i, error in enumerate(errors):
            print(f"Error {i+1} was {error}")

def show_requests_result(requests):
    if len(requests) == 0:
        print("You do not seem to have any valid requests, with data available.")
        exit(0)

def choose_items_to_delete(requests):
    print("Choose what media to delete:")
    for i, item in enumerate(requests):
        print(f"{i+1}. {item.title}")
    chosen_indices = input("Enter the numbers of the items to delete, separated by commas: ")
    chosen_indices = list(map(int, chosen_indices.split(',')))
    return [requests[i-1] for i in chosen_indices]

async def delete_chosen_items(requests, chosen):
    errors = []
    for item in chosen:
        try:
            await item.remove_from_server()
        except Exception as e:
            errors.append((item.title, e))
    
    if errors:
        print("Had some errors deleting items:")
        for title, error in errors:
            print(f"Got the following error while deleting {title}: {error}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    asyncio.run(main())
