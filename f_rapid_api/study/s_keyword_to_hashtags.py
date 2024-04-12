from f_rapid_api.c_tiktok import TikTok


c = TikTok()
keyword = 'gaza'
res = c.keyword_to_hashtags(keyword=keyword)
for i, hashtag in enumerate(res):
    print(i, hashtag)