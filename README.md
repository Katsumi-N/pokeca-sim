pokeca-sim
====

Overview

## Description
ポケモンカードの一人回し用シミュレーターです. 
デッキコードから公式サイトの画像をダウンロードし, シミュレーターで一人回しができます. 

## Demo
![pokeca_sim](https://user-images.githubusercontent.com/61781055/105462937-b8e78400-5cd2-11eb-86c9-f60d95dcb42d.gif)
・シャッフル
・ドロー
・デッキ確認
・デッキから指定したカードをドロー
の機能が実装されています。

## Install

`pip install -r requirements.txt`
で関連ライブラリをインストールできます。
そのうちexeファイルも追加します

## Usage
`python simulate.py --deck_code=xx8Ycc-z91o6X-J8xxx8 --driver_dir="(path to choromedriver)"`
windows環境のみdriver_dirの指定が必要なようです
## Author

[Katsumi-N](https://github.com/Katsumi-N)
