

# 使い方
## データの準備

`\\legspin\share\01_projects` ディレクトリを
`da-nttf-water-leakage/data/original` にコピーする

以下の元データが存在することを仮定します。
```
data/original/20170814/rousui/元画像
data/original/20170814/rousui/アノテーション画像
```
次に、trainingデータ用のディレクトリとvalidationデータ用のディレクトリを作成します。
```
mkdir data/for_analysis
mkdir data/for_analysis/train
mkdir data/for_analysis/val
```
次に、以下のコードを実行します。
```
python preprocess.py
```
実行が終了すると、自動的に分割されたデータがtrain, val以下に生成されます。


## 基本的な学習
da-nttf-water-leakageディレクトリ以下にいるとして
```
python train.py GPU OUTPUT_PATH CONFIG_FILE
```
とすると `OUTPUT_PATH` の下に以下のファイルが出力される。

```
README.md 用いたNetwork、augmentation、学習パラメータ、結果などがまとめられている
train.py 学習用スクリプト
config.py　実験設定ファイル (中身は上で指定したCONFIG_FILEと同一)
loss.png 
accuracy.png
log
```

## 結果の共有

実験結果はmaster branchに共有することにする

```

# master branchにいるとしてda-nttf-water-leakage/result/test/ 以下のファイルをgithubにコミットする
git add result/test # test以下のファイルをadd。snapshotなどは.gitignoreの設定で無視される
git commit -m "ここに説明を書く"
# 結果をリモートレポジットリに反映する
git push origin master
```

## チューニング
以下の条件を変えることを想定。
* 深層学習のネットワーク 
* 損失関数
* 精度評価関数
* データ拡張手法
* データ正規化手法
* 訓練パラメータ

これらの条件を変えるには `config.py` を編集する。 `config.py` の中身は以下のようになっている。
各モジュールから使いたいクラス、関数を選んで `config.py` を書き換え、 `train.py` を実行すればよい。
`config.py` は実験の度に書き換えるが `da-nttf-water-leakage` 直下のものは共有しなくても良い。
```
batch_size = 20
epoch = 100
val_epoch = 10
snapshot_epoch = 100
size = (256, 384)  # resizeまたはcropされる画像の大きさ
train_data_root = "./data/for_analysis/train"  # 訓練用データ格納ディレクトリ
val_data_root = "./data/for_analysis/val"  # 評価用データ格納ディレクトリ

network = "UNET"  # network.py に定義されているクラス
lossfun = "dice_coef_binary_cross_entropy_loss"  # loss.pyに定義されている関数
accfun = "dice_coef"  # loss.pyに定義されている関数
classifier = "BinarySegmentationClassifier"  # classifier.pyに定義されているクラス
augmentation_list = ["random_flip", "random_shift",  # augmentations.pyに定義されている関数
                     "random_rotate", "add_gaussian_noise", "high_contrast"]
normalization = "simple_normalization"  # normalizations.pyに定義されている関数

# train_params
lr = 0.001  # learning rate 学習率
weight_decay_factor = 0.00001  # weight decay factor
```

例えば損失関数を `dice_coef_binary_cross_entropy_loss` から `dice_coef_loss` に変えるには

```lossfun = "dice_coef_binary_cross_entropy_loss"``` 

の行を

```lossfun = "dice_coef_loss"```

と書き換えればいい。

どのような関数やクラスが用意されているかは、プロジェクトのドキュメントを参照する。
https://s3-ap-northeast-1.amazonaws.com/da-docs/da-nttf-water-leakage/index.html

# 新しい関数の追加
すでに用意されているもの以外にもデータ拡張、ネットワーク、損失関数などを使いたいときはそれぞれに対応するファイルに新しく関数、クラスを追加して良い。
ただし、gitで新しいbranchを作ってからそこにcommitし、完成したらpull requestを送ること。


# snapshotを使って学習を再開する方法

snapshotを使って学習を再開するには `train.py` 実行時にオプション引数 `--resume` を指定します。
```
python train.py GPU OUTPUT_PATH CONFIG_FILE --resume SNAPSHOT_FILE
```
例えば `result/20170824_1_tsutsui/` にある `config.py` と　`snapshot_epoch_200` を使用してepoch 200から学習を再開するには以下のようにします。ここでは別のフォルダにconfig.pyをコピーしてepochを書き換えた後に学習を再開し、そこに結果を出力するものとします。

```
mkdir result/test
cp result/20170824_1_tsutsui/config.py result/test/config.py 
(result/test/config.pyのepochを書き換える
python train.py 1 ./result/test ./result/test/config.py --resume ./result/20170824_1_tsutsui/snapshot_epoch_200 
```
ターミナルに `resume trainer:./result/20170824_1_tsutsui/snapshot_epoch_200` と表示されれば正しくsnapshotがloadされています。
