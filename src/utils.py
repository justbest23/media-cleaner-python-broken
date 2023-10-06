from urllib.parse import urlencode

def create_param_string(params=None):
    if params is None:
        return ""
    return urlencode(params)

def create_api_error_message(code, path, service):
    if code == 400:
        return f"Got 400 Bad Request from {service} at {path}. The api may have changed, please report this on Github."
    elif code == 401:
        return f"Got 401 Unauthorized from {service}, please check the appropriate API key."
    elif code == 403:
        return f"Got 403 Forbidden from {service}, please check the appropriate API key."
    elif code == 404:
        return f"Got 404 Not Found from {service} at path {path}. Please make sure the URL is correct."
    elif code == 505:
        return f"Got 505 internal server error from {service}. Please try again later."
    else:
        return f"Error {code} returned from {service}. Code unknown, please create issue on Github."

def human_file_size(size):
    gig_size = 1000000000.0
    gigs = size / gig_size
    return f"{gigs:.2f}GB"
