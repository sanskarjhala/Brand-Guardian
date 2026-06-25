"""
Connector : Python and Azure Video indexer
"""

import os
import time
import logging
import requests
import yt_dlp
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("video_indexer")


class VideoIndexerService:
    def __init__(self):
        self.account_id = os.getenv("")
        self.location = os.getenv("")
        self.subscription_id = os.getenv("")
        self.resource_group = os.getenv("")
        self.vi_name = os.getenv("")
        self.credentials = DefaultAzureCredential()

    def get_access_token(self):
        """
        Generates an ARM Access Token
        """
        try:
            token_object = self.credentials.get_token("AZURE_VI_AUTHORIZATION_URL")
            return token_object.token
        except Exception as e:
            logger.error(f"Fadiled to get Azure token : {str(e)}")
            raise

    def get_account_token(self, arm_access_token):
        """
        Exchanges the ARM token for video INdexer account team
        """
        url = (
            f"https://management.azure.com/subscription/{self.subscription_id}",
            f"/resourceGroups/{self.resource_group}",
            f"/providers/Microsoft.VideoIndexer/accounts/{self.vi_name}",
            f"/generateAccessToken?api-version=2024-01-01",
        )
        headers = {"Authorization": f"Bearer {arm_access_token}"}
        payload = {"permissionType": "Contributor", "scope": "Account"}
        response = requests.post(url=url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Faield to get the VI account token : {response.text}")

        return response.json().get("accessToken")

    # Funtion to download the youtube Video
    def download_youtube_video(self, url, output_path="temp_video.mp4"):
        """Downloads the youtube  video to a local file

        Args:
            url (_type_): youtube url
            output_path (str, optional): it dowloaded to thi temprory path Defaults to "temp_video.mp4".
        """

        logger.info(f"Downloading Youtube Video : {url}")

        ydl_opts = {
            "format": "best",
            "outtmpl": output_path,
            "quiet": False,
            "no_warnings": False,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Window NT 10.0; Win64; 64) AppleWebKit/537.36"
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info("Download Complete")
            return output_path
        except Exception as e:
            raise Exception(f"Youtube video Download Failed : {str(e)}")

    # Function for uploading to azure Video indexer
    def upload_video(self, video_path, video_name):
        arm_token = self.get_access_token()
        vi_token = self.get_account_token(arm_token)

        api_url = f"https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}/Videos"

        params = {
            "accessToken": vi_token,
            "name": video_name,
            "privacy": "Private",
            "indexingPreset": "Default",
        }

        logger.info(f"uplading file {video_path} to Azure...........")

        # Open the file in binary and streams it on the azure
        with open(video_path, "rb") as video_file:
            file = {"file": video_file}
            response = requests.post(api_url, params=params, files=file)

        if response.status_code != 200:
            raise Exception(f"Azure Upload Failed  : {response.text}")

    # Function for wait for processing
    def wait_for_processing(self, video_id):
        logger.info(f"Waiting for the video {video_id} to process.....")
        while True:
            arm_token = self.get_access_token()
            vi_token = self.get_account_token(arm_token)

            api_url = f"https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}/Videos"
            params = {"access_token": vi_token}
            response = requests.get(url=api_url, params=params)
            data = response.json()

            state = data.get("state")
            if state == "Processed":
                return data
            elif state == "Failed":
                raise Exception("Video Indexing Failed in Azure")
            elif state == "Quarantine":
                raise Exception(
                    "Video Quarantine (Copyright / Content Policy Violation)"
                )
            logger.info(f"Status {state} .................. waiting 30 seconds")
            time.sleep(30)

    def extract_data(self, vi_json):
        """
        Parses the JSON into out State Format
        """

        logger.info(
            f"---- [EXTRACT-DATA FUNCTION FROM VIDEO - INDEXER] ---- data received {vi_json} ----"
        )

        transcipt_lines = []
        for v in vi_json.get("videos", []):
            for insight in v.get("insights", {}).get("transcript", []):
                transcipt_lines.append(insight.get("text"))

        ocr_lines = []
        for v in vi_json.get("videos", []):
            for insight in v.get("insights", {}).get("ocr", []):
                ocr_lines.append(insight.get("text"))

        return {
            "transcript": " ".join(transcipt_lines),
            "ocr_text": ocr_lines,
            "video_metadata": {
                "duration": vi_json.get("summarizedInsights", {}).get("duration"),
                "platform": "youtube",
            },
        }
