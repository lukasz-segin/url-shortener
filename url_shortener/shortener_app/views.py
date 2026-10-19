from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def short_url(request, hash_value=None):
    """
    http://127.0.0.1:8000/short/?url=https://example.com/very-very/long/url/even-longer
    A simple API endpoint that takes a long URL as a query parameter and returns a shortened version of it.
    When a GET request is made to this endpoint with a 'url' query parameter, it will generate a shortened URL and return it in the response.
    And When the 'url' query parameter is provided as hash, it will return the original long URL associated with that hash.
    But for already hashed URL, it will return a placeholder response indicating the original URL for that hash.
    Url would look like this: http://127.0.0.1:8000/short/3825658415458351892
    In url patterns, we have defined a URL pattern for the short_url view, which will handle requests to the /short/ endpoint.
    Add url mappint into txt file, so that it can be used for future reference. This will help in maintaining the mapping between shortened URLs and their corresponding long URLs.
    """
   
    url_mapping = {}
    long_url = request.GET.get('url')
    hash_value = request.parser_context.get('kwargs', {}).get('hash_value')

    #here check if the long_url is a hash or a long URL
    if long_url is None and hash_value is None:
        return Response({"error": "Missing 'url' query parameter or 'hash_value' in URL"}, status=400)
    if long_url:
        short_url_value = hash(long_url)
        with open('url_mapping.txt', 'a') as f:
            f.write(f"{short_url_value}:{long_url}\n")
        # url_mapping[short_url_value] = long_url
        print(f"URL Mapping: {url_mapping}")  # Debugging line to print the URL mapping
        return Response({"shortened_url": f"http://127.0.0.1:8000/short/{short_url_value}"})
    if hash_value:
        print(f"URL Mapping: {url_mapping}")  # Debugging line to print the URL mapping
        # Here you would implement the logic to retrieve the original long URL associated with the hash
        # For demonstration purposes, we'll just return a placeholder response
        with open('url_mapping.txt', 'r') as f:
            for line in f:
                short_url_value, original_url = line.strip().split(':', 1)
                url_mapping[short_url_value] = original_url
        original_url = url_mapping.get(hash_value)
        if original_url:
            return Response({"original_url": original_url})
        else:
            return Response({"error": f"No original URL found for hash {hash_value}"}, status=404)



    # # Now check if in url there is a hash
    # # if long_url.startswith("http://127.0.0.1:8000/short/"):
    # #     # Extract the hash from the URL
    # #     hash_value = long_url.split('/')[-1]
    # #     # Here you would implement the logic to retrieve the original long URL associated with the hash
    # #     # For demonstration purposes, we'll just return a placeholder response
    # #     return Response({"original_url": f"Original URL for hash {hash_value}"})
    # # Here you would implement the URL shortening logic



    # return Response({"shortened_url": f"http://127.0.0.1:8000/short/{hash(long_url)}"})