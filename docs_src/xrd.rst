XRD
===

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
execute.py		 rasファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までを一度に行うツール
execute_jupyter.py	 rasファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までをjupyter notebook上で一度に行い、図の表示、主要パラメータを表示するツール
README.rst		 使い方の説明
======================== =========================================================================================================================================================

コマンド
--------

rasファイルをフォーマットされた数値データ(csv)に変換します::

	python ras2csv.py --encoding sjis ../source/XRD_RIGAKU.ras

カレントディレクトリにXRD_RIGAKU.csvが作成されます。

csvファイルから画像を作成します::

	python csv2graph.py XRD_RIGAKU.csv

カレントディレクトリにXRD_RIGAKU.pngが作成されます。

rasファイルから装置出力パラメータを抽出します::

	python ras2raw_XRD.py ../source/XRD_RIGAKU.ras --encoding sjis ../source/xrd_raw_template.xml raw.xml

第3引数で指定したファイル名で装置出力パラメータが作成されます。

装置出力パラメータから主要パラメータを抽出します::

	python raw2primary_XRD.py ../source/XRD_RIGAKU.ras --encoding sjis ../source/xrd_raw_template.xml primary.xml

第3引数で指定したファイルで主要パラメータが作成されます。

.. note::

	各プログラムの基本的な使い方は上に示した通りです。

	コマンドを一つずつ実行するのではなく、まとめて可視化、
	メタ情報抽出を行うようにバッチ処理を行いたい場合は、
	Rigaku_XRD_tools(batch) で、:

	execute_XRD.py

	を利用して処理を行います。

	execute_XRD.py は、上記のコマンドをまとめて行うプログラムです。:

	python execute_XRD.py ../source/XRD_RIGAKU.ras

	を実行すると、../XRD_RIGAKUというフォルダを作成し、その中にFND(Formatted Numerical Data)、
 	スペクトルの図、装置出力パラメータ、主要パラメータファイルを出力します。
	連続変換を行いたい場合などに使用します。

	jupyter notebook 上で画像やパラメータの確認を行いながら実行するには execute_jupyter.py を使用してください。:

	python execute_XRD_jupyter.py ../source/XRD_RIGAKU.ras


For more information, refer to the `the documentation`__.

.. __: https://nims-dpfc.github.io/Materials_Data_Repository/

Instrallation
-------------

ここにインストールの手順が入ります。

Documentation
-------------

ここにドキュメントがはいります。
