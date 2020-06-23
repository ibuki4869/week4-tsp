Build@Mercari 2020 Week4 - Travelling Salesman PRoblem Challenges.

* 巡回セールスマン問題をとくアルゴリズムを考えて実装してください。
* `solution_yours_{0-6}.csv` をあなたのアルゴリズムでといた結果で上書きしてください。
* あなたの解法の*path length*を[scoreboard]に書いてください

[scoreboard]: https://docs.google.com/spreadsheets/d/1t4ScULZ7aZpDJL8i9AVFQfqL7sErjT5i3cmC1G5ecR8/edit?usp=sharing

<h4>アルゴリズム　two_opt.py</h4>

2-opt法とgreedyを用いた。  
**推しポイント**  
```
if score < score_best:
    score_best = score 
    order_best = order_improved  
    order_random = order_best
if N < 129:  
    order_random = list(np.random.permutation(N))
order_random = list(np.roll(order_random, 3)) 
```
order_random:現在の経路  
order_best:過去最短の経路  
通常の2-opt法は全ての入れ替えを考え、より良いスコアが出れば更新するというものだが、全ての入れ替えを考えず、order_randomの頭から○番目の地点のみの入れ替えだけを考え、order_bestを更新することを繰り返すと2-opt法よりも良いスコアが出ることが分かった!!!頭からの地点を考えるため、繰り返す際に経路の頭を変えている。  
実際、N=512において、512地点全ての入れ替えを考えた時の距離は21150.03 mだったが、order_randomの頭から300地点までの入れ替えのみを考えて、それを800回繰り返すと20935.42 mとなった。



[参考文献]を見て、2-opt法でまずは書いてみようと思ったが、参考文献のコードをそのまま用いると、計算量が大きすぎてN=2048に対応できなかったため、頂いていたgreedyを同時に用いることにした。  
参考文献のコードは「初期経路をrandomで与え、2-opt法で2つの経路を入れ替えていくことで最短経路を見つける」というものだ。しかし、入れ替える作業が多いほど計算時間が長くなるため、初期経路をrandomで与えたり、Nが大きくなったりすると計算するのにとても時間を要する。  
まず、初期経路をrandomにすることによる計算量を初期経路にgreedyを与えることで改善させた。greedyの結果を用いると、すでにある程度交差の少ない経路になっているため、入れ替える回数がrandomの経路よりも格段に少なくなる。  
次に、Nが大きくなる時の計算量に関しては、N=512まででは全ての入れ替えパターンを実行するようにしているが、N=2048は経路の頭の0から1000の間で入れ替えるパターンを考えさせ、経路の頭の位置を変えてもう一度2-opt法を行うというのを繰り返すようにした。この1000という値については根拠があるものではなく、考察の余地がある。  


<h4>改善したい点</h4>

ここで、2-opt法は初期値に依存することについて触れておく。2-opt法は2つの経路を入れ替えるだけなので、クロスがない経路に2-opt法を用いても距離は変わらない。  
それ故、初期値を最短距離の解に近いものにするべきなのだが、greedyがあまり良くないため、randomで計算できるN=128まではrandomで計算した。そのため、毎回結果が変わるNが存在する。これをrandomにせず、greedyと他のアルゴリズムでいくつかの初期値を与えて、それらを2-opt法で改善させたときに、最も短いものを結果にするなどの工夫をすると、よりよくなると考えられる。

また、入れ替える経路のパターンについてだが、最短距離を考える以上、真反対の点が繋がることがないため、全てのパターンを考える必要がない。もし、このパターンを少なくすることができれば、より早く、N=2048に関してはより短距離な結果を出せるようになると考えられる。  
（更新）上記のように考えていたが、やはり入れ替えは全部の点で考えた方が良さそうであることが分かった。というのも、greedyを初期値とした場合、遠方の点がつながっていることがあるため、距離が近い点だけの入れ替えを考えると遠方のつながりが改善されない。やはり、greedyを初期値にするなら現在の2-optが最善であると考えられる。  
初期値に遠方のつながりがないものを使用すれば、上記の改善方法も活きてくると思われる。

表：N=2048で2-opt法を用いた時の入れ替えパターンを考える範囲と計算時間と距離（繰り返し200回）

|入れ替えるデータ数| 500| 600 | 700 | 1000 |
| :---: | :---: | :---: | :---: | :---: |
| 計算時間[sec]| 179.6971 | 256.5885 | 352.5641 | 809.2435 |
| 距離 [m] | 44246.01 | 44104.56 | 41827.48 | 41324.17 |

より少ない入れ替えデータ数で、より短い距離を出せるようにしたい。

[参考文献]: http://codecrafthouse.jp/p/2016/08/traveling-salesman-problem/#opt
