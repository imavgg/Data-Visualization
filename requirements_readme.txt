#管理套件版本 (requirements.txt)
#這一支檔案是負記錄了當前專案資料夾下程式所有依賴的套件及相對應的版本。下列五個是在本實作中將會使用到#的套件，若套件後面沒有特別指定版本號，安裝時將會自動安裝最新的版本。

Flask
Flask-Cors
numpy
scikit-learn
xgboost
xgboost -i https://pypi.tuna.tsinghua.edu.cn/simple
lightgbm
matplotlib
sklearn
#pip install -r requirements.txt
#假設程式在另一台電腦上執行時，要一個一個安裝套件很麻煩。因此可以直接透過 
#requirements.txt 紀錄專案中依賴的套件。並且輸入以下指令即可一次安裝所有指定的套件
