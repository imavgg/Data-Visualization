# 啟用步驟
1. 下載資料夾檔案

2. Flask 伺服器
    * Install Flask `pip install flask`
    * flask run (default: app.py)
        * Output shows -> Running on http://127.0.0.1:5000/
3. Ngrok轉外部HTTP可取
    * Download [ngrok.exe](https://dashboard.ngrok.com/get-started/setup), and login to make authtoken first(must!!!)

    * Run command in ngrok command line:
    `ngrok authtoken {$your_token_from_pc}`
    `ngrok.exe http 5000` 
