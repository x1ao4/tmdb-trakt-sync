# tmdb-trakt-sync
使用 tmdb-trakt-sync 可以在您的 [TMDB](https://www.themoviedb.org/) 和 [Trakt](https://trakt.tv/) 账号之间同步电影和电视节目的评分数据及观看历史。

## 运行条件
- 安装了 Python 3.0 或更高版本。
- 安装了必要的第三方库：requests。
- 有可用的 TMDB 和 Trakt 账号。

## 准备工作
- 获取 TMDB API 密钥。请在 TMDB 账号设置中（免费）申请 API 并获取 API 密钥。
- 获取 Trakt API 密钥。请在 Trakt 账号设置中（免费）创建新的 API 应用程序以获取客户端 ID 和客户端密钥。(需要勾选 `Scrobble` 和 `Check In` 选项)

## 使用方法
1. 将仓库克隆或下载到计算机上的一个目录中。
2. 根据需要，修改脚本中的参数：`SYNC_FROM_TMDB_TO_TRAKT`、`SYNC_FROM_TRAKT_TO_TMDB`。
   - 如果您想将评分从 TMDB 同步到 Trakt，请将 `SYNC_FROM_TMDB_TO_TRAKT` 设置为 `True`，否则设置为 `False`。
   - 如果您想将评分从 Trakt 同步到 TMDB，请将 `SYNC_FROM_TRAKT_TO_TMDB` 设置为 `True`，否则设置为 `False`。
3. 修改 `start.command (Mac)` 或 `start.bat (Win)` 中的路径，以指向您存放 `tmdb-trakt-sync.py` 脚本的目录。
4. 双击运行 `start.command` 或 `start.bat` 脚本以执行 `tmdb-trakt-sync.py` 脚本。
5. 首次运行时需要您在控制台中提供以下信息：
   - 您的 TMDB 用户名。
   - 您的 TMDB 密码。
   - 您的 TMDB API 密钥。
   - 您的 Trakt 客户端 ID（Client ID）。
   - 您的 Trakt 客户端密钥（Client Secret）。
   - 您的 Trakt 授权码（Authorization Code）。
   脚本会根据您提供的信息生成一个名为 `config.json` 的配置文件并保存在脚本所在的目录中，再次运行脚本时会自动读取配置文件，不需要再提供信息。
6. 
  
