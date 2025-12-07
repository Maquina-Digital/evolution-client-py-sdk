import unittest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient, EvolutionApiClient
from evolution_client.utils import get_media_type

class TestMimeDetection(unittest.IsolatedAsyncioTestCase): # Using IsolatedAsyncioTestCase for async
    
    def test_utils_get_media_type(self):
        # Test the utility function directly
        self.assertEqual(get_media_type("http://example.com/image.png"), "image")
        self.assertEqual(get_media_type("http://example.com/image.jpg"), "image")
        self.assertEqual(get_media_type("http://example.com/video.mp4"), "video")
        self.assertEqual(get_media_type("http://example.com/audio.mp3"), "audio")
        self.assertEqual(get_media_type("http://example.com/file.pdf"), "document")
        self.assertEqual(get_media_type("http://example.com/unknown"), "document")

    async def test_async_client_auto_detection(self):
        async with respx.mock:
            route = respx.post("https://api.example.com/message/sendMedia/default").mock(
                return_value=Response(200, json={"status": "success"})
            )
            
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                # 1. Send PNG -> expect "image"
                await client.send_media(number="123", url_media="http://site.com/img.png")
                last_request = route.calls.last.request
                import json
                payload = json.loads(last_request.content)
                self.assertEqual(payload["mediatype"], "image")

                # 2. Send MP4 -> expect "video"
                await client.send_media(number="123", url_media="http://site.com/vid.mp4")
                payload = json.loads(route.calls.last.request.content)
                self.assertEqual(payload["mediatype"], "video")
                
                # 3. Send MP3 -> expect "audio"
                await client.send_media(number="123", url_media="http://site.com/song.mp3")
                payload = json.loads(route.calls.last.request.content)
                self.assertEqual(payload["mediatype"], "audio")

                # 4. Explicit override -> expect "document" even if jpg
                await client.send_media(number="123", url_media="http://site.com/img.jpg", mime_type="document")
                payload = json.loads(route.calls.last.request.content)
                self.assertEqual(payload["mediatype"], "document")

class TestSyncClientMimeDetection(unittest.TestCase):
    def test_sync_client_auto_detection(self):
        with respx.mock:
            route = respx.post("https://api.example.com/message/sendMedia/default").mock(
                return_value=Response(200, json={"status": "success"})
            )
            
            client = EvolutionApiClient("https://api.example.com", "default", "key")
            
            # 1. Send PNG -> expect "image"
            client.send_media(number="123", url_media="http://site.com/img.png")
            last_request = route.calls.last.request
            import json
            payload = json.loads(last_request.content)
            self.assertEqual(payload["mediatype"], "image")
