from old_f_google.services.storage import Storage, Bucket


def test_bucket() -> None:
    """
    ========================================================================
     Test bucket creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    bucket_valid: Bucket = storage.get_bucket('noteret_mp4')
    assert bucket_valid
    assert bucket_valid.name == 'noteret_mp4'
    bucket_invalid: Bucket = storage.get_bucket('noteret_mp4_invalid')
    assert not bucket_invalid


def test_upload_from_pc() -> None:
    """
    ========================================================================
     Test upload_from_pc().
    ========================================================================
    """
    name_bucket = 'test_upload_from_pc'
    path = 'g:\\temp\\test_1.xlsx'
    storage = Storage.Factory.rami()
    bucket = storage.create_bucket(name_bucket)
    bucket.upload_from_pc(name='test_1.xlsx', path=path)
    assert bucket.names_blobs() == ['test_1.xlsx']
    blob = bucket.get_blob('test_1.xlsx')
    assert blob.name == 'test_1.xlsx'
    storage.delete_bucket(name=name_bucket)


def test_upload_from_url() -> None:
    """
    ========================================================================
     Test upload_from_url().
    ========================================================================
    """
    name_bucket = 'test_upload_from_url_2'
    url = 'https://www.google.com'
    storage = Storage.Factory.rami()
    bucket = storage.create_bucket(name=name_bucket)
    bucket.upload_from_url(name='google.html', url=url)
    assert bucket.names_blobs() == ['google.html']
    blob = bucket.get_blob('google.html')
    assert blob.name == 'google.html'
    storage.delete_bucket(name=name_bucket)
    

def test_upload_from_url_large() -> None:
    """
    ========================================================================
     Test upload_from_url_large().
    ========================================================================
    """
    name_bucket = 'test_upload_from_url_large'
    url = 'https://v15m.tiktokcdn-eu.com/ad8ded295e9297e0689eedcc0529f38d/687bf4cf/video/tos/maliva/tos-maliva-ve-0068c799-us/o4TEpQUiQvzIqeeCiylDfIGj9XAFgLRAYq6QIk/?a=1233&bti=M0BzMzU8OGYpNzo5Zi5wIzEuLjpkNDQwOg%3D%3D&ch=0&cr=13&dr=0&er=0&lr=all&net=0&cd=0%7C0%7C0%7C&cv=1&br=2982&bt=1491&cs=0&ds=6&ft=7h_H6m9pfxPRusrOFTeK_acwHAKXtsvQWfQEeLrq-tPD1Inz&mime_type=video_mp4&qs=0&rc=OmhlOjQ4aDRoNTNoaDpnOUBpamtsdnM5cm9rNDMzaTczNEAvNC9eX2M0XzUxLmEtNGAvYSMuaGZvMmRzcnBhLS1kMTJzcw%3D%3D&vvpl=1&l=202507190339578B5BF9B11DD0479C4805&btag=e00090000'
    storage = Storage.Factory.rami()
    bucket = storage.create_bucket(name=name_bucket)
    bucket.upload_from_url(name='tiktok.mp4', url=url)
    assert bucket.names_blobs() == ['tiktok.mp4']
    blob = bucket.get_blob('tiktok.mp4')
    assert blob.name == 'tiktok.mp4'
    storage.delete_bucket(name=name_bucket)
