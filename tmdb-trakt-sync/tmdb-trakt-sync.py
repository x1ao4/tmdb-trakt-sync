import requests
import datetime
import webbrowser
import json
import os

# 设置选项
SYNC_FROM_TMDB_TO_TRAKT = True
SYNC_FROM_TRAKT_TO_TMDB = True

# 定义存档文件路径
archive_file = 'archive.json'

# 检查存档文件是否存在
if os.path.exists(archive_file):
    # 从文件中加载存档数据
    with open(archive_file, 'r') as f:
        archive = json.load(f)
else:
    # 创建一个空的存档数据字典
    archive = {
        'rated_movies_tmdb': [],
        'rated_shows_tmdb': [],
        'rated_movies_trakt': [],
        'rated_shows_trakt': []
    }

# 检查是否存在配置文件，如果不存在则创建一个
config_file = 'config.json'
if not os.path.exists(config_file):
    # 用您自己的API密钥、用户名和密码替换以下值
    TMDB_USERNAME = input('Please enter your TMDB username: ')
    TMDB_PASSWORD = input('Please enter your TMDB password: ')
    TMDB_API_KEY = input('Please enter your TMDB API key: ')
    TRAKT_CLIENT_ID = input('Please enter your Trakt Client ID: ')
    TRAKT_CLIENT_SECRET = input('Please enter your Trakt Client Secret: ')

    # 将用户重定向到 Trakt 的授权页面
    auth_url = f'https://trakt.tv/oauth/authorize?response_type=code&client_id={TRAKT_CLIENT_ID}&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
    webbrowser.open(auth_url)

    # 获取用户输入的授权码
    auth_code = input('Please enter your Authorization Code: ')
    print()

    # 使用授权码获取 access_token
    url = 'https://api.trakt.tv/oauth/token'
    data = {
        'code': auth_code,
        'client_id': TRAKT_CLIENT_ID,
        'client_secret': TRAKT_CLIENT_SECRET,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, json=data)
    access_token = response.json()['access_token']

    # 将配置保存到文件中
    config = {
        'TMDB_USERNAME': TMDB_USERNAME,
        'TMDB_PASSWORD': TMDB_PASSWORD,
        'TMDB_API_KEY': TMDB_API_KEY,
        'TRAKT_CLIENT_ID': TRAKT_CLIENT_ID,
        'TRAKT_CLIENT_SECRET': TRAKT_CLIENT_SECRET,
        'TRAKT_ACCESS_TOKEN': access_token
    }
    with open(config_file, 'w') as f:
        json.dump(config, f)

    # 重新加载配置文件
    with open(config_file, 'r') as f:
        config = json.load(f)
    TMDB_USERNAME = config['TMDB_USERNAME']
    TMDB_PASSWORD = config['TMDB_PASSWORD']
    TMDB_API_KEY = config['TMDB_API_KEY']
    TRAKT_CLIENT_ID = config['TRAKT_CLIENT_ID']
    TRAKT_CLIENT_SECRET = config['TRAKT_CLIENT_SECRET']
    TRAKT_ACCESS_TOKEN = config['TRAKT_ACCESS_TOKEN']

else:
    # 从文件中加载配置
    with open(config_file, 'r') as f:
        config = json.load(f)
    TMDB_USERNAME = config['TMDB_USERNAME']
    TMDB_PASSWORD = config['TMDB_PASSWORD']
    TMDB_API_KEY = config['TMDB_API_KEY']
    TRAKT_CLIENT_ID = config['TRAKT_CLIENT_ID']
    TRAKT_CLIENT_SECRET = config['TRAKT_CLIENT_SECRET']
    TRAKT_ACCESS_TOKEN = config['TRAKT_ACCESS_TOKEN']

# 创建一个请求令牌
url = 'https://api.themoviedb.org/3/authentication/token/new'
params = {'api_key': TMDB_API_KEY}
response = requests.get(url, params=params)
request_token = response.json()['request_token']

# 验证用户名和密码
url = 'https://api.themoviedb.org/3/authentication/token/validate_with_login'
params = {'api_key': TMDB_API_KEY, 'username': TMDB_USERNAME, 'password': TMDB_PASSWORD, 'request_token': request_token}
response = requests.get(url, params=params)
request_token = response.json()['request_token']

# 创建一个新的会话ID
url = 'https://api.themoviedb.org/3/authentication/session/new'
params = {'api_key': TMDB_API_KEY, 'request_token': request_token}
response = requests.get(url, params=params)
session_id = response.json()['session_id']

# 获取TMDB账户ID
url = 'https://api.themoviedb.org/3/account'
params = {'api_key': TMDB_API_KEY, 'session_id': session_id}
response = requests.get(url, params=params)
account_id = response.json()['id']

try:
    # 获取TMDB账户中的电影评分数据
    rated_movies_tmdb_dict = dict()
    url = f'https://api.themoviedb.org/3/account/{account_id}/rated/movies'
    params = {'api_key': TMDB_API_KEY, 'session_id': session_id}
    response = requests.get(url, params=params)
    total_pages = response.json()['total_pages']
    for page in range(1, total_pages + 1):
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/movies'
        params = {'api_key': TMDB_API_KEY, 'session_id': session_id, 'page': page}
        response = requests.get(url, params=params)
        for movie in response.json()['results']:
            rated_movies_tmdb_dict[movie['id']] = {
                'rating': movie['rating'],
                'title': movie['title']
            }
            # 将电影ID添加到存档数据中
            if movie['id'] not in archive['rated_movies_tmdb']:
                archive['rated_movies_tmdb'].append(movie['id'])
    
    # 获取TMDB账户中的电视剧评分数据
    rated_shows_tmdb_dict = dict()
    url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv'
    params = {'api_key': TMDB_API_KEY, 'session_id': session_id}
    response = requests.get(url, params=params)
    total_pages = response.json()['total_pages']
    for page in range(1, total_pages + 1):
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv'
        params = {'api_key': TMDB_API_KEY, 'session_id': session_id, 'page': page}
        response = requests.get(url, params=params)
        for show in response.json()['results']:
            rated_shows_tmdb_dict[show['id']] = {
                'rating': show['rating'],
                'title': show['name']
            }
            # 将电视剧ID添加到存档数据中
            if show['id'] not in archive['rated_shows_tmdb']:
                archive['rated_shows_tmdb'].append(show['id'])
    
    # 获取Trakt账户中的电影评分数据
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID,
        'Authorization': f'Bearer {TRAKT_ACCESS_TOKEN}'
    }
    url = f'https://api.trakt.tv/sync/ratings/movies'
    if 'last_sync_time' in archive:
        url += f'?start_at={archive["last_sync_time"]}'
    response = requests.get(url, headers=headers)
    rated_movies_trakt_dict=dict()
    for movie in response.json():
        rated_movies_trakt_dict[movie['movie']['ids']['tmdb']]=movie['rating']
        # 将电影ID添加到存档数据中
        if movie['movie']['ids']['tmdb'] not in archive['rated_movies_trakt']:
            archive['rated_movies_trakt'].append(movie['movie']['ids']['tmdb'])
    
    # 获取Trakt账户中的电视剧评分数据
    url = f'https://api.trakt.tv/sync/ratings/shows'
    if 'last_sync_time' in archive:
        url += f'?start_at={archive["last_sync_time"]}'
    response = requests.get(url, headers=headers)
    rated_shows_trakt_dict=dict()
    for show in response.json():
        rated_shows_trakt_dict[show['show']['ids']['tmdb']]=show['rating']
        # 将电视剧ID添加到存档数据中
        if show['show']['ids']['tmdb'] not in archive['rated_shows_trakt']:
            archive['rated_shows_trakt'].append(show['show']['ids']['tmdb'])
    
    # 将更新后的存档数据保存到文件中
    with open(archive_file, 'w') as f:
        json.dump(archive, f)
    
    # 获取Trakt账户中的电影观看状态
    url = f'https://api.trakt.tv/sync/history/movies'
    response = requests.get(url, headers=headers)
    watched_movies_trakt = response.json()
    
    # 获取Trakt账户中的电视剧观看状态
    url = f'https://api.trakt.tv/sync/history/shows'
    response = requests.get(url, headers=headers)
    watched_shows_trakt = response.json()
    
    if SYNC_FROM_TMDB_TO_TRAKT:
        # 遍历每部电影并同步评分数据
        for rated_movie_tmdb in rated_movies_tmdb_dict:
            # 检查电影是否已经在存档数据中
            if rated_movie_tmdb in archive['rated_movies_trakt']:
                continue
    
            # 在Trakt库中查找匹配的电影
            movie_trakt_id = rated_movie_tmdb
            movie_trakt_rating_int = int(rated_movies_tmdb_dict[rated_movie_tmdb]['rating'])
            movie_trakt_title = rated_movies_tmdb_dict[rated_movie_tmdb]['title']
    
            # 检查电影是否已经在Trakt上标记为已观看
            watched = False
            for watched_movie_trakt in watched_movies_trakt:
                if watched_movie_trakt['movie']['ids']['tmdb'] == movie_trakt_id:
                    watched = True
                    break
    
            # 如果电影未标记为已观看，则将其标记为已观看
            if not watched:
                url = f'https://api.trakt.tv/sync/history'
                data = {
                    "movies": [
                        {
                            "ids": {
                                "tmdb": movie_trakt_id
                            }
                        }
                    ]
                }
                response = requests.post(url, json=data, headers=headers)
                print(f"Marking \"{movie_trakt_title}\" as watched on Trakt")
    
            # 更新评分数据并打印信息
            if movie_trakt_id not in rated_movies_trakt_dict.keys():
                url = f'https://api.trakt.tv/sync/ratings'
                data = {
                    "movies": [
                        {
                            "ids": {
                                "tmdb": movie_trakt_id
                            },
                            "rating": movie_trakt_rating_int
                        }
                    ]
                }
                response = requests.post(url, json=data, headers=headers)
                print(f"Rating \"{movie_trakt_title}\" with {movie_trakt_rating_int} on Trakt")
    
            # 将电影ID添加到存档数据中
            archive['rated_movies_trakt'].append(rated_movie_tmdb)
    
            # 将更新后的存档数据保存到文件中
            with open(archive_file, 'w') as f:
                json.dump(archive, f)
    
        # 遍历每部电视剧并同步评分数据
        for rated_show_tmdb in rated_shows_tmdb_dict:
            # 检查电视剧是否已经在存档数据中
            if rated_show_tmdb in archive['rated_shows_trakt']:
                continue
    
            # 在Trakt库中查找匹配的电视剧
            show_trakt_id = rated_show_tmdb
            show_trakt_rating_int = int(rated_shows_tmdb_dict[rated_show_tmdb]['rating'])
            show_trakt_title = rated_shows_tmdb_dict[rated_show_tmdb]['title']
    
            # 检查电视剧是否已经在Trakt上标记为已观看
            watched = False
            for watched_show_trakt in watched_shows_trakt:
                if watched_show_trakt['show']['ids']['tmdb'] == show_trakt_id:
                    watched = True
                    break
    
            # 如果电视剧未标记为已观看，则将其标记为已观看
            if not watched:
                # 检查Trakt账户中是否存在具有相同tmdb ID的其他电视剧记录
                duplicate = False
                for rated_show_trakt in rated_shows_trakt_dict:
                    if rated_show_trakt == show_trakt_id:
                        duplicate = True
                        break
    
                # 如果不存在重复记录，则将电视剧标记为已观看
                if not duplicate:
                    url = f'https://api.trakt.tv/sync/history'
                    data = {
                        "shows": [
                            {
                                "ids": {
                                    "tmdb": show_trakt_id
                                }
                            }
                        ]
                    }
                    response = requests.post(url, json=data, headers=headers)
                    print(f"Marking \"{show_trakt_title}\" as watched on Trakt")
    
            # 更新评分数据并打印信息
            if show_trakt_id not in rated_shows_trakt_dict.keys():
                url = f'https://api.trakt.tv/sync/ratings'
                data = {
                    "shows": [
                        {
                            "ids": {
                                "tmdb": show_trakt_id
                            },
                            "rating": show_trakt_rating_int
                        }
                    ]
                }
                response = requests.post(url, json=data, headers=headers)
                print(f"Rating \"{show_trakt_title}\" with {show_trakt_rating_int} on Trakt")
    
            # 将电视剧ID添加到存档数据中
            archive['rated_shows_trakt'].append(rated_show_tmdb)
    
            # 将更新后的存档数据保存到文件中
            with open(archive_file, 'w') as f:
                json.dump(archive, f)
    
    if SYNC_FROM_TRAKT_TO_TMDB:
        # 遍历每部电影并同步评分数据
        for rated_movie_trakt in rated_movies_trakt_dict:
            # 检查电影是否已经在存档数据中
            if rated_movie_trakt in archive['rated_movies_tmdb']:
                continue
    
            # 在TMDB库中查找匹配的电影
            movie_tmdb_id = rated_movie_trakt
            movie_tmdb_rating_int=int(rated_movies_trakt_dict[rated_movie_trakt])
    
            # 获取电影标题
            url = f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}'
            params = {'api_key': TMDB_API_KEY}
            response = requests.get(url, params=params)
            movie_tmdb_title = response.json()['title']
    
            # 如果找到匹配项，则更新评分数据并打印信息
            if movie_tmdb_id not in rated_movies_tmdb_dict.keys():
                url = f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}/rating'
                params = {'api_key': TMDB_API_KEY, 'session_id': session_id, 'value': movie_tmdb_rating_int}
                response = requests.post(url, params=params)
                print(f"Rating \"{movie_tmdb_title}\" with {movie_tmdb_rating_int} on TMDB")
    
            # 将电影ID添加到存档数据中
            archive['rated_movies_tmdb'].append(rated_movie_trakt)
    
            # 将更新后的存档数据保存到文件中
            with open(archive_file, 'w') as f:
                json.dump(archive, f)
    
        # 遍历每部电视剧并同步评分数据
        for rated_show_trakt in rated_shows_trakt_dict:
            # 检查电视剧是否已经在存档数据中
            if rated_show_trakt in archive['rated_shows_tmdb']:
                continue
    
            # 在TMDB库中查找匹配的电视剧
            show_tmdb_id = rated_show_trakt
            show_tmdb_rating_int=int(rated_shows_trakt_dict[rated_show_trakt])
    
            # 获取电视剧标题
            url = f'https://api.themoviedb.org/3/tv/{show_tmdb_id}'
            params = {'api_key': TMDB_API_KEY}
            response = requests.get(url, params=params)
            show_tmdb_title = response.json()['name']
    
            # 如果找到匹配项，则更新评分数据并打印信息
            if show_tmdb_id not in rated_shows_tmdb_dict.keys():
                url = f'https://api.themoviedb.org/3/tv/{show_tmdb_id}/rating'
                params = {'api_key': TMDB_API_KEY, 'session_id': session_id, 'value': show_tmdb_rating_int}
                response = requests.post(url, params=params)
                print(f"Rating \"{show_tmdb_title}\" with {show_tmdb_rating_int} on TMDB")
    
            # 将电视剧ID添加到存档数据中
            archive['rated_shows_tmdb'].append(rated_show_trakt)
    
            # 将更新后的存档数据保存到文件中
            with open(archive_file, 'w') as f:
                json.dump(archive, f)
    
except Exception as e:
    # 在这里处理异常
    print()
    print(f"An error occurred. Please check your network connection and try again.")
finally:
    # 更新存档文件中的 last_sync_time 键
    archive['last_sync_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 将更新后的存档数据保存到文件中
    with open(archive_file, 'w') as f:
        json.dump(archive, f)

