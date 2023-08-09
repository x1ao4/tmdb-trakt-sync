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

   脚本会根据您提供的信息生成一个名为 `config.json` 的配置文件并保存在脚本所在的目录中，再次运行脚本时会自动读取配置文件，不需要再次提供信息。
6. 脚本将自动从您的 TMDB 和 Trakt 账号中获取评分数据并按照设置进行同步。运行过程中，您可以在控制台看到各部影片的同步状态和评分数据。

## 注意事项
- 请确保您提供了正确有效的必要信息。
- 脚本会根据影片的 TMDB ID 进行匹配，当您从 TMDB 向 Trakt 同步时，可能会有一些影片在 Trakt 上没有对应的条目，这些影片将无法进行同步。
- 脚本运行过程耗时可能较长，特别是当有大量评分数据需要同步时，请耐心等待运行完成。
- 脚本会根据需要在存档文件中记录已同步的评分数据，当再次运行脚本时，脚本会跳过存档文件中存在的影片，避免重复评分。若同步后对评分做了修改，将无法使用脚本更新评分。
- 若脚本在运行过程中由于网络不稳定等因素造成了运行中断，已经处理过的数据不会受到影响，重新运行脚本就会继续处理剩余数据。
- 部分地区可能会由于网络原因造成 TMDB API 调用失败，无法运行脚本，请确保您的网络环境可以正常调用 TMDB API。
- 部分地区可能会由于网络原因造成 Trakt API 调用失败，无法运行脚本，请确保您的网络环境可以正常调用 Trakt API。

## 已知问题
- 脚本会在每次运行后记录同步时间，当再次运行脚本时，只会获取上次同步时间后新增的评分数据进行同步。由于目前无法通过 TMDB API 同时获取评分及评分时间，每次运行脚本时都会重新获取 TMDB 账号中的所有评分数据，若数据较多，获取时间可能较长。
- 在 TMDB 上有评分数据的影片将被默认为已观看状态，同步时若该影片在 Trakt 上是未观看状态，将被标记为已观看，若为电视节目，则会将整个节目标记为已观看，若该节目已经存在观看记录，则不会重新标记观看状态。若脚本在运行过程中发生了中断，可能会导致个别影片的观看状态标记失败。
- 首次运行时将会对所有数据进行同步，并记录已同步影片的 ID，若数据较多，耗时可能较长，请耐心等待。
<br>

# tmdb-trakt-sync
With tmdb-trakt-sync, you can synchronize movie and TV show ratings and watch history between your TMDB and Trakt accounts.

## Requirements
- Installed Python 3.0 or higher.
- Installed necessary third-party libraries: requests.
- Valid TMDB and Trakt accounts.

## Preparation
- Get a TMDB API key. Please apply for an API and get an API key in your TMDB account settings (for free).
- Get a Trakt API key. Please create a new API app in your Trakt account settings (for free) to get the Client ID and Client Secret. (Check the `Scrobble` and `Check In` options)

## Usage
1. Clone or download the repository to a directory on your computer.
2. Modify the parameters in the script as needed: `SYNC_FROM_TMDB_TO_TRAKT`, `SYNC_FROM_TRAKT_TO_TMDB`.
   - If you want to synchronize ratings from TMDB to Trakt, set `SYNC_FROM_TMDB_TO_TRAKT` to `True`, otherwise set it to `False`.
   - If you want to synchronize ratings from Trakt to TMDB, set `SYNC_FROM_TRAKT_TO_TMDB` to `True`, otherwise set it to `False`.
3. Modify the path in `start.command (Mac)` or `start.bat (Win)` to point to the directory where you store the `tmdb-trakt-sync.py` script.
4. Double-click `start.command` or `start.bat` to execute the `tmdb-trakt-sync.py` script.
5. The first run will require you to provide the following information in the console:

   - Your TMDB username.
   - Your TMDB password.
   - Your TMDB API key.
   - Your Trakt Client ID.
   - Your Trakt Client Secret.
   - Your Trakt Authorization Code.

   The script will generate a configuration file named `config.json` based on the information you provide and save it in the same directory as the script. When you run the script again, it will automatically load the configuration file and you will not need to provide the information again.
6. The script will automatically retrieve rating data from your TMDB and Trakt accounts and synchronize them according to your settings. During the run, you can see the synchronization status and rating data of each film in the console.

## Notes
- Please make sure you have provided correct and valid necessary information.
- The script matches movies and TV shows based on their TMDB IDs. When syncing from TMDB to Trakt, some movies or TV shows might not have corresponding entries on Trakt and therefore cannot be synced.
- The script may take a while to run, especially when there's a large amount of rating data to synchronize. Please be patient and wait for the script to complete.
- The script maintains an archive file to keep track of synchronized rating data. On subsequent runs, the script will skip movies and TV shows that already exist in the archive file to avoid duplicate ratings. If you modify ratings after synchronization, the script won't be able to update those ratings.
- If the script is interrupted during execution due to unstable network conditions or other factors, the already processed data will not be affected. You can resume processing the remaining data by running the script again.
- In some regions, network issues may cause TMDB API calls to fail, preventing the script from running. Ensure that your network environment can access the TMDB API.
- In some regions, network issues may cause Trakt API calls to fail, preventing the script from running. Ensure that your network environment can access the Trakt API.

## Known Issues
- The script records synchronization time after each run. When running again, it only retrieves new rating data added after last synchronization time. Since it is currently not possible to retrieve both ratings and rating times through TMDB API at once, all rating data in your TMDB account is retrieved every time you run this script. If there is a lot of data, retrieval time may be long.
- Movies and TV shows with ratings on TMDB are assumed to be watched. When syncing, if a movie on Trakt is marked as unwatched, it will be marked as watched, and for TV shows, the entire show will be marked as watched. If the show already has watch history, it won't re-mark the episodes. If the script is interrupted during execution, some movies’ or TV shows’ watch statuses might not be updated.
- The first run will sync all the data and record the IDs of synchronized movies and TV shows. If there's a large amount of data, the first run may take some time. Please be patient.
