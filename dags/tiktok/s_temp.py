logger = 5

def run_next(challenge_id: str, cursor: int) -> (str, int):
    logger.start(adds=f'challenge_id={challenge_id}, cursor={cursor}')
    response = get_response(challenge_id=challenge_id, cursor=cursor)
    upload_json(challenge_id=challenge_id, response=response)
    response = response.json()
    has_more = response['data']['hasMore']
    videos = len(response['data']['videos']
    logger.finish(adds=f'challenge_id={challenge_id},cursor={cursor},has_more={has_more},videos={videos}')
