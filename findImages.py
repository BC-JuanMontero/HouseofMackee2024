import requests

def get_image_file_size(image_url):
    # Send a HEAD request to the image URL to get only headers
    response = requests.head(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the 'Content-Length' header which gives the size of the image in bytes
        size_in_bytes = response.headers.get('Content-Length', None)
        
        if size_in_bytes:
            # Convert size to integer
            size_in_bytes = int(size_in_bytes)
            
            # Convert bytes to kilobytes (optional)
            size_in_kb = size_in_bytes / 1024
            
            return size_in_bytes, size_in_kb
        else:
            return None, None
    else:
        return None, None

# Example usage
url = "https://cf-images.us-east-1.prod.boltdns.net/v1/jit/5680571037001/e9f43e0d-63d0-483b-9502-30939fe2cbd6/main/1280x720/4m11s754ms/match/image.jpg"
size_in_bytes, size_in_kb = get_image_file_size(url)

if size_in_bytes:
    print(f"The image size is {size_in_bytes} bytes ({size_in_kb:.2f} KB).")
else:
    print("Failed to retrieve the image size.")
