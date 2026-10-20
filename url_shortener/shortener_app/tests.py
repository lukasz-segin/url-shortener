from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ShortUrlTests(APITestCase):
    def test_shorten_url(self):
        """
        Ensure we can shorten a new URL.
        """
        url = reverse('short_url')
        data = {'url': 'https://example.com/very-very/long/url/even-longer'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if the response contains the shortened URL
        self.assertIn('shortened_url', response.data)


    def test_e2e_retrieve_original_url(self):
        """
        Ensure we can shorten a URL and retrieve the original URL from a shortened URL.
        """
        # First, shorten a URL to get a hash value
        url = reverse('short_url')
        data = {'url': 'https://example.com/very-very/long/url/even-longer'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shortened_url = response.data['shortened_url']
        hash_value = shortened_url.split('/')[-1]

        # Retrieve the original URL using the hash value
        url_with_hash = reverse('short_url_with_hash', args=[hash_value])
        response = self.client.get(url_with_hash, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('original_url', response.data)
        self.assertEqual(response.data['original_url'], 'https://example.com/very-very/long/url/even-longer')