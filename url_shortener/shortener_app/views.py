from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def short_url(request, hash_value=None):
    """
    A simple API endpoint that takes a long URL as a query parameter and returns a shortened version of it.
    
    Example usage:
    1. To shorten a long URL:
       GET http://127.0.0.1:8000/short/?url=https://example.com/very-very/long/url/even-longer
    2. To retrieve the original URL from a shortened URL:
       GET http://127.0.0.1:8000/short/{hash_value}
    """
   
    url_mapping = {}
    long_url = request.GET.get('url')
    hash_value = request.parser_context.get('kwargs', {}).get('hash_value')

    # Check if the long_url is a hash or a long URL
    if long_url is None and hash_value is None:
        return Response({"error": "Missing 'url' query parameter or 'hash_value' in URL"}, status=400)
    
    if long_url:
        short_url_value = hash(long_url)
        with open('url_mapping.txt', 'a') as f:
            f.write(f"{short_url_value}:{long_url}\n")
        return Response({"shortened_url": f"http://127.0.0.1:8000/short/{short_url_value}"})
    
    if hash_value:
        with open('url_mapping.txt', 'r') as f:
            for line in f:
                short_url_value, original_url = line.strip().split(':', 1)
                url_mapping[short_url_value] = original_url
        original_url = url_mapping.get(hash_value)
        if original_url:
            return Response({"original_url": original_url})
        else:
            return Response({"error": f"No original URL found for hash {hash_value}"}, status=404)