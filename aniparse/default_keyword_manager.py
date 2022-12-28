from aniparse import KeywordManager


def get_default_keyword_manager():
    default_keywords = [
        {
            "identifiable": True,
            "searchable": True,
            "valid": True,
            "keywords": {
                "audio_term": ["AAC", "MP3"]
            }
        },
        {
            "identifiable": True,
            "searchable": False,
            "valid": True,
            "keywords": {
                "video_term": ["H.264", "H.265"]
            }
        }
    ]
    default_entries = {
        "audio_term": ["Dual Audio", "Multi Audio"],
        "video_term": ["H264", "H.264", "10 bit", "10 bits", "8 bit", "8 bits"],
        "video_resolution": ["480p", "720p", "1080p", "2160p", "4K", "480i", "720i", "1080i"],
        "subtitles": ["Multi Subs", "Multiple Subtitle", "Multiple Subtitles"],
        "source": ["Blu-Ray"]
    }

    keyword_manager = KeywordManager()
    keyword_manager.load_keywords(default_keywords)
    keyword_manager.load_entries(default_entries)
    return keyword_manager
