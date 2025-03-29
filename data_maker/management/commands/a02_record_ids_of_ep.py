from data_maker.models import S1_Endpoint
from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = "Count the number of endpoints in the database"
    
    def handle(self, *args, **kwargs):
        ep_urls = S1_Endpoint.objects.iterator()
        for ep_url in ep_urls:
            url = ep_url.url + "/?limit=999999"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            total_ids = data["count"]
            ep_url.total_ids = total_ids
            ep_url.save()
            
            results = data["results"]
            exist_ids = [result["url"].split("/")[-2] for result in results]
            ep_url.exist_ids = exist_ids
            ep_url.save()