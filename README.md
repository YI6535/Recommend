# Recommend


## Description
http://www.grappa.univ-lille3.fr/~mary/cours/stats/centrale/reco/paper/MatrixFactorizationALS.pdf
を参考にALC_WRを実装しました。



## Usage
* https://grouplens.org/datasets/movielens から取得したデータ(MovieLens 100K Dataset)を`data`の下に保存。


* `notebook/data_analysis.ipynb`を実行すると、`data`の下に実装に必要なデータが保存されます。


* ``` python ALS_WR.py EPOCHS NOIZE_RATE0 COMMON_LEN ```を実行すると`output`の下に学習後のデータが保存されます。
