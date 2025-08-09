import os
import yt_dlp
import shutil

class MediaDownloader:
    """
    Download TikTok, YouTube, etc. as MP4 (video with sound) or MP3 (audio with thumbnail).
    """

    def __init__(self, save_path: str = "downloads"):
        self.save_path = save_path
        self._ensure_directory()
        self._check_ffmpeg()

    def _ensure_directory(self) -> None:
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            print(f"Directory created at {self.save_path}.")
        else:
            print(f"Directory already exists at {self.save_path}.")

    def _check_ffmpeg(self):
        if not shutil.which("ffmpeg"):
            raise EnvironmentError(
                "ffmpeg is not installed. Install with:\n  sudo apt install ffmpeg"
            )

    def download(self, url: str, media_type: str = "mp4"):
        if media_type.lower() == "mp3":
            # MP3 with thumbnail
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "quiet": False,
                "writethumbnail": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    },
                    {
                        "key": "FFmpegMetadata",
                    },
                    {
                        "key": "EmbedThumbnail",
                    },
                ],
            }
        else:
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "merge_output_format": "mp4",
                "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "quiet": False,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"{media_type.upper()} downloaded successfully.")
        except Exception as e:
            print(f"Error downloading {media_type}: {e}")
            if media_type.lower() == "mp4":
                print("Retrying with fallback format...")
                self._retry_fallback(url)

    def _retry_fallback(self, url: str):
        fallback_opts = {
            "format": "best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": False,
        }
        with yt_dlp.YoutubeDL(fallback_opts) as ydl:
            ydl.download([url])
        print("Fallback MP4 download completed.")


if __name__ == "__main__":
    downloader = MediaDownloader()
    link = input("Enter TikTok or YouTube URL: ").strip()
    choice = input("Download as MP3 or MP4? ").strip().lower()
    downloader.download(link, choice)