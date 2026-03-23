# EndpointVideosNewByUser

## Purpose
Fetch videos published by a user after a given timestamp.

## Config
- `_path`: `'user/posts'`
- `_name_list`: `'videos'`
- `_stop_if`: overridden to stop fetching when video creation date is older than target

## Inheritance
`EndpointVideosNewByUser` -> `Endpoint`

## Dependencies
- `f_proj.rapid_api.tiktok.endpoints.i_0_base.Endpoint`
