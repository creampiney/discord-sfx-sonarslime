# Discord SonarSlime Bot (Sound Effect Bot)
This bot will show sound effects which are added in server. Python is mainly used in the project.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Sound Effect Board](#sfx-board)
    - [Options Board](#option-board)

## Installation <a name="installation"></a>
- Download this project's files, put all files in one folder.
- Create `config.json` in the same folder and write as the following: 
    ```json
    {"DISCORD_TOKEN":"<YOUR_BOT_TOKEN>"}
    ```
    replace `<YOUR_BOT_TOKEN>` with your bot's token id from discord developer portal.
- Install python and related packages/libraries which are labelled in `requirements.txt`
- Run `bot.py`, don't forget to invite your bot in your server.

## Usage <a name="usage"></a>
### Sound Effect Board <a name="sfx-board"></a>
To open sound effect board, type `-sf` on the discord chat and sound effect board will appear.

![Sound Effect Board](https://github.com/creampiney/discord-sfx-sonarslime/blob/main/pic/sf-board.png)

For the server which newly use this bot, there will be 5 initial sound effects:
|   Sound Effect  |                     Link                    |
|:---------------:|:-------------------------------------------:|
| Illuminati      | https://www.youtube.com/watch?v=sahAbxq8WPw |
| Quack           | https://www.youtube.com/watch?v=nucoyLwGsoY |
| Detective Conan | https://www.youtube.com/watch?v=RsyxFQ23Ezk |
| YEAY            | https://www.youtube.com/watch?v=kp42doFyeiM |
| Kahoot          | https://www.youtube.com/watch?v=hnnUD9-hD8A |

When you click on the blue button, sound effect will play. You can stop playing sfx by pressing red `Stop Sound Effect` button.

### Options Board <a name="option-board"></a>
Press the green button labelled `Refresh / Add or Remove SFX`.

![Options Board]()

Five options will appears as following:
|   Button   |                                          Function                                          |
|:----------:|:------------------------------------------------------------------------------------------:|
| Refresh    | Refresh the sound effect board.                                                            |
| Add SFX    | Add sound effect in recent server's sfx board.                                             |
| Remove SFX | Remove sound effects in recent server's sfx board.                                         |
| Info       | List information of selected button, including name, link, adder, and date which is added. |
| Rename     | Rename the button.                                                                         |

