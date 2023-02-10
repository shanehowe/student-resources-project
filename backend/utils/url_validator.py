def add_https_to_url(url: str):
    if url.startswith("https://"):
        return url
    
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
        return url
    
    return f"https://{url}"
    
    
    