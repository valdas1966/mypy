from proj.rapid_api.c_tiktok import TikTok


def single(id_user: str) -> None:
    t = TikTok()
    print(t.user.info(id_user=id_user))


def multi(users: list[str]) -> None:
    t = TikTok()
    for user in users:
        is_exist = t.user.info(id_user=user).is_exist
        print(f'{user},', is_exist)


user_valid = '107955'
user_invalid = '12345'

single(id_user=user_valid)
single(id_user=user_invalid)


# users = ['107955', '12345']
# multi(users=users)