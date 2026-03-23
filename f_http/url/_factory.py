class Factory:
    """
    ============================================================================
     Factory for UUrl Test URLs.
    ============================================================================
    """

    @staticmethod
    def mp4() -> str:
        """
        ====================================================================
         Sample TikTok video URL (mp4 via mime_type query param).
        ====================================================================
        """
        return ('https://v77.tiktokcdn-eu.com/video/tos/maliva/'
                '?mime_type=video_mp4&qs=0')

    @staticmethod
    def mp3() -> str:
        """
        ====================================================================
         Sample TikTok music URL (mp3 in path).
        ====================================================================
        """
        return ('https://sf16-ies-music-va.tiktokcdn.com/obj/'
                'ies-music-ttp-dup-utx27578563599396866847.mp3')

    @staticmethod
    def jpeg() -> str:
        """
        ====================================================================
         Sample TikTok avatar URL (jpeg in path).
        ====================================================================
        """
        return ('https://p16-sign-va.tiktokcdn.com/tos-maliva-avt'
                '/avatar~tplv-tiktokx-cropcenter:720:720.jpeg'
                '?dr=14579&x-expires=1764770400')

    @staticmethod
    def no_suffix() -> str:
        """
        ====================================================================
         URL with no detectable suffix.
        ====================================================================
        """
        return 'https://example.com/path/without/extension'
