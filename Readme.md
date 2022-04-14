## Readme

## 使用方式
`python app.py`  

## Git 首次下載:
* git clone https://github.com/imavgg/Data-Visualization.git 需先下載本端。
* 複製（Fork）一份原作的專案到你自己的 GitHub 帳號底下。
* cd Data-Visualization
* git checkout -b "your branch name" :設一個新的branch 名字。

## 開發本地專案

* 請在自己forked的專案下獨立開發，確認無誤再往下走以Git推送至此。

## Git 推送
* git checkout "your branch" : 切換到自己設定的分支下。
* git remote -v : 查看自己推送的遠端位子名稱 ---> 會出現類似以下(遠端名可能是Data-Visualization 但也可能出現別的ex:origin)

```
Data-Visualization     https://github.com/imavgg/Data-Visualization.git (fetch)
Data-Visualization      https://github.com/imavgg/Data-Visualization.git (push)
```
* git pull "遠端名"  "your branch name" : 需要先讓本地端版本與git上一致
* git add . :增加內容
* git status :查看改變內容
* git commit -m  "your words" :說明推送文字

* git push "遠端名" "your branch name" :推上你的BRANCH，可於此github上確認以及檢察。


* 接下來，我會收到你每次的推送紀錄，會以Pull request方式合併專案。

## 其他可能用到的指令:
* git branch -a : 查看全部遠端branch (如果忘記自己的branch)
