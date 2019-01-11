フォルダに含まれるファイルの説明
--------------------------------

======================== =========================================================================================================================================================
program名		 説明
======================== =========================================================================================================================================================
ras2csv.py		 rasファイルからFND(Formatted Numerical Data)のcsvファイルを作成するツール
csv2graph.py		 FND(Formatted Numerical Data)のcsvファイルからスペクトルの図を作成するツール（グラフ表示、主要パラメータ表示なし）
csv2graph_for_jupyter.py FND(Formatted Numerical Data)のcsvファイルからスペクトルの図を作成するツール（jupyter notebookで使用時、グラフ表示、主要パラメータ表示あり）
ras2raw_XRD.py		 rasファイルから装置出力パラメータを抽出するツール
xrd_raw_template.xml	 装置出力パラメータ抽出に使用するテンプレートファイル
raw2primary_XRD.py	 装置出力パラメータファイルから主要パラメータを抽出するツール
xrd_primary_template.xml 主要パラメータ抽出に使用するテンプレートファイル
batch_exe_XRD.py	 rasファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までを一度に行うツール
README.rst		 使い方の説明
======================== =========================================================================================================================================================

Jupyter Notebook での実行
-------------------------

Anaconda Prompt を立ち上げ、ダウンロードディレクトリ配下の ``Rigaku_XRD_tools`` に移動します。::

	cd [download directory]/Rigaku_XRD_tools

Jupyter notebook を立ち上げます。::

	jupyter notebook

Jupyter notebook から ``xrd_rigaku.ipynb`` をクリックして実行します。
Jupyter Notebook での使い方は `XRD for jupyter notebook <rigaku_xrd.ipynb>`_ を参照してください。

コマンド
--------

``.ras``形式のファイルをフォーマットした数値データ(``.csv``)に変換します::

	python ras2csv.py --encoding sjis ../source/XRD_RIGAKU.ras

カレントディレクトリに ``XRD_RIGAKU.csv`` を出力します。

.. note::

	``-h`` オプションをつけて実行すると、ヘルプを表示します。::

		python ras2csv.py -h

``.csv`` 形式のファイルから画像を作成します::

	python csv2graph.py XRD_RIGAKU.csv

カレントディレクトリに ``XRD_RIGAKU.png `` を出力します。

``.ras`` 形式のファイルから装置出力パラメータを抽出し、 ``raw.xml`` を出力します::

	python ras2raw_XRD.py ../source/XRD_RIGAKU.ras --encoding sjis xrd_raw_template.xml raw.xml

.. note::

	``--stdout`` のオプションをつけると標準出力にも出力します。::

		python ras2raw_XRD.py ../source/XRD_RIGAKU.ras --encoding sjis xrd_raw_template.xml raw.xml --stdout

装置出力パラメータファイル ``raw.xml`` から主要パラメータを抽出し、 ``primary.xml`` に出力します::

	python raw2primary_XRD.py raw.xml xrd_primary_template.xml primary.xml

バッチ処理
----------

上記のコマンドをまとめて実行できると便利です。
batch_exe_XRD.py は、上記のコマンドをまとめて行うプログラムです。::

	python batch_exe_XRD.py ../source/XRD_RIGAKU.ras

を実行すると、 ``../result/XRD_RIGAKU`` というフォルダを作成し、その中にFND(Formatted Numerical Data)、
スペクトルの図、装置出力パラメータ、主要パラメータファイルを出力します。
連続変換を行いたい場合などに使用します。

