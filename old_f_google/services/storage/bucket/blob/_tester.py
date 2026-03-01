from old_f_google.services.storage import Storage


def test_blob() -> None:
    """
    ========================================================================
     Test Blob creation using factory methods.
    ========================================================================
    """
    name_bucket = 'test_blob_3'
    name_blob = 'tiktok.mp4'
    url = 'https://v15m.tiktokcdn-eu.com/ad8ded295e9297e0689eedcc0529f38d/687bf4cf/video/tos/maliva/tos-maliva-ve-0068c799-us/o4TEpQUiQvzIqeeCiylDfIGj9XAFgLRAYq6QIk/?a=1233&bti=M0BzMzU8OGYpNzo5Zi5wIzEuLjpkNDQwOg%3D%3D&ch=0&cr=13&dr=0&er=0&lr=all&net=0&cd=0%7C0%7C0%7C&cv=1&br=2982&bt=1491&cs=0&ds=6&ft=7h_H6m9pfxPRusrOFTeK_acwHAKXtsvQWfQEeLrq-tPD1Inz&mime_type=video_mp4&qs=0&rc=OmhlOjQ4aDRoNTNoaDpnOUBpamtsdnM5cm9rNDMzaTczNEAvNC9eX2M0XzUxLmEtNGAvYSMuaGZvMmRzcnBhLS1kMTJzcw%3D%3D&vvpl=1&l=202507190339578B5BF9B11DD0479C4805&btag=e00090000'
    storage = Storage.Factory.rami()
    bucket = storage.create_bucket(name=name_bucket)
    bucket.upload_from_url(name=name_blob, url=url)
    blob = bucket.get_blob(name=name_blob)
    print(blob.size)
    assert blob
    assert blob.name == name_blob
    assert blob.size == 12
    storage.delete_bucket(name=name_bucket)
    