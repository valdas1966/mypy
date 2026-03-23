# ApiTikTok

## Purpose
Public facade for TikTok on RapidAPI. Each method delegates to an
Endpoint class — ApiTikTok itself contains zero logic.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `users_by_id` | `(id_user) -> list[dict]` | Fetch user by numeric id |
| `users_by_id_unique` | `(id_user_unique) -> list[dict]` | Fetch user by unique id |
| `videos_by_user` | `(id_user, limit?) -> list[dict]` | Fetch videos by user |
| `videos_new_by_user` | `(id_user, created) -> list[dict]` | Fetch videos after timestamp |
| `hashtags_by_keyword` | `(keyword, limit?) -> list[dict]` | Search hashtags |
| `videos_by_hashtag` | `(id_hashtag, limit?) -> list[dict]` | Fetch videos by hashtag |
| `followers_by_user` | `(id_user, limit?) -> list[dict]` | Fetch followers |
| `music_by_id` | `(id_music) -> list[dict]` | Fetch music info |
| `videos_by_music` | `(id_music, limit?) -> list[dict]` | Fetch videos by music |
| `comments_by_video` | `(id_video, limit?) -> list[dict]` | Fetch comments |

## Inheritance
No base class. Pure delegation to `endpoints/` classes.

## Dependencies
- All endpoint classes in `endpoints/i_1_*/`

## Usage Example
```python
from f_proj.rapid_api.tiktok import ApiTikTok

rows = ApiTikTok.users_by_id(id_user='123456')
rows = ApiTikTok.videos_by_user(id_user='123456', limit=100)
```
