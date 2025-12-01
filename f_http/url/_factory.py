from f_http.url.main import URL


class Factory:
    """
    ===========================================================================
     Factory class for URL.
    ===========================================================================
    """
    
    @staticmethod
    def mp4() -> URL:
        """
        =======================================================================
         Return a sample of mp4 url.
        =======================================================================
        """
        url = 'https://v77.tiktokcdn-eu.com/a9f8fb735ae74af640e578560e9d0132/692ef2eb/video/tos/maliva/tos-maliva-ve-0068c799-us/o8SkAs6EP4UcCIdiYF61b4BsgEiBzUQI1axlB/?a=1233&bti=MzU8OGYpNHYpNzo5ZjEuLjpkLTptNDQwOg%3D%3D&ch=0&cr=13&dr=0&er=0&lr=all&net=0&cd=0%7C0%7C0%7C&cv=1&br=4176&bt=2088&cs=0&ds=6&ft=JS-FgDDwNj6VQQdGntpisdLJarXqYlabMFtMhWLrK&mime_type=video_mp4&qs=0&rc=NTYzM2c7PDY0NWQ6ZWdpOEBpanRkbHQ5cm46NzMzZzczNEBiYmMvL18zNjMxNDViNl8vYSMtXy1uMmQ0XmphLS1kMS9zcw%3D%3D&vvpl=1&l=20251201220706C2C4CE161670282E9634&btag=e00090000'
        return URL(url=url)
    
    @staticmethod
    def mp3() -> URL:
        """
        =======================================================================
         Return a sample of mp3 url.
        =======================================================================
        """
        url = ('https://sf16-ies-music-va.tiktokcdn.com/obj/ies-music-ttp-dup'
               '-utx27578563599396866847.mp3')
        return URL(url=url)

    @staticmethod
    def jpeg() -> URL:
        """
        =======================================================================
         Return a sample of jpeg url.
        =======================================================================
        """
        url = ('https://p16-sign-va.tiktokcdn.com/tos-maliva-avt-0068'
           '/ba67b11de451691939223e9d978e613a~tplv-tiktokx-cropcenter:720:720.jpeg?dr=14579&refresh_token=a4719621&x-expires=1764770400&x-signature=UxoHBpu05ykyOLSLvCZOD8IA4RA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=2472a6c6&idc=maliva')
        return URL(url=url)
