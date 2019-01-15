フォルダに含まれるファイルの説明
--------------------------------

========================= =========================================================================================================================================================
program名		  説明
========================= =========================================================================================================================================================
MPExport.exe              ULVAC-PHI製変換ツール（.spe,.proのファイルからtxtファイルを作成するツール）
txt2csv.py		  txtファイルからFND(Formatted Numerical Data)のcsvファイルを作成するツール
csv2graph.py		  FND(Formatted Numerical Data)のcsvファイルからスペクトルの図を作成するツール
txt2raw_XPS_survey.py	  txtファイルから装置出力パラメータを抽出するツール
xps_raw_templateXML.xml	  装置出力パラメータ抽出に使用するテンプレートファイル
raw2primary_XPS_survey.py 装置出力パラメータファイルから主要パラメータを抽出するツール
xps_primary_template.xml  主要パラメータ抽出に使用するテンプレートファイル
batch_exe_XPS.py	  speファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までを一度に行うツール
README.rst		  使い方の説明
========================= =========================================================================================================================================================

Jupyter Notebook での実行
-------------------------

Anaconda Prompt を立ち上げ、ダウンロードディレクトリ配下の PHI_XPS_survey_narrow_tools に移動します。::

	cd [download directory]/PHI_XPS_survey_narrow_tools

Jupyter notebook を立ち上げます。::

	jupyter notebook

Jupyter notebook から ``xps_survey.ipynb`` を利用すると簡単に実行できます。
Jupyter notebook での使い方は `XPS for jupyter notebook <xps_survey.ipynb>`_ を参照してください。


コマンド
--------

``.spe`` 形式のファイルをテキストファイルに変換します。::

	MPExport.exe -Filename:"..\source\XPS_PHI_QUANTERA_survey.spe" -TSV

カレントディレクトリに ``XPS_PHI_QUANTERA_survey.txt`` を出力します

.. note::

	``MPExport.exe`` は Windows用実行ファイルです。``-Filename:`` の後に変換元のファイル名を記述します。
	カレントディレクトリ以外の場所を指定する場合のパスは Windows の記述形式で指定します。

	(例).. |yen| source |yen| XPS_PHI_QUANTERA_survey.spe

	その他のオプションについては、::

		MPExport.exe

	を単体で実行して参照してください。

.. warning::

	linuxなどで動作させる場合には、``wine`` などのwindowアプリケーション対応ソフトを使用して動作させてください。
	

``.txt`` 形式のファイルをフォーマットした数値データ(``.csv``)に変換します::

	python txt2csv.py "XPS_PHI_QUANTERA_survey.txt"

カレントディレクトリに ``XPS_PHI_QUANTERA_survey.csv`` を出力します

.. note::

	``-h`` オプションをつけて実行すると、ヘルプを表示します。::

		python txt2csv.py -h

``.csv`` 形式のファイルから画像を作成します::

	python csv2graph.py "XPS_PHI_QUANTERA_survey.csv"

カレントディレクトリに ``XPS_PHI_QUANTERA_survey.png`` を出力します

.. note::

	ファイル名に日本語が含まれる場合、対応するフォントが存在しないとエラーとなり画像が作成されない場合があります。
	その場合は、csv2graph.py、batch_exe_XPS.py の日本語フォント対応部分を確認してください。

	csv2graph.py: 56行目 or batch_exe_XPS.py: 237行目 ::

		fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryo.ttc', size=14)

	フォントがない場合には、独立行政法人 情報処理推進機構が提供しているIPAフォントなどを利用することができます。

	https://ipafont.ipa.go.jp/old/ipafont/download.html

	上記サイトからTTFファイルのIPAゴシックをダウンロードし、解凍した ``ipag.ttf`` を適当なフォルダ(ex. PHI_XPS_survey_narrow_tools)にコピーして::

		cp ipag.ttf [download directory]/PHI_XPS_survey_narrow_tools

	FontPropertiesのfnameに指定します。

	csv2graph.py: 56行目 or batch_exe_XPS.py: 237行目 ::

		fp = FontProperties(fname=r'ipag.ttf', size=14)


``.txt`` 形式のファイルから装置出力パラメータを抽出し、 ``raw.xml`` を出力します::

	python txt2raw_XPS_survey.py "XPS_PHI_QUANTERA_survey.txt" xps_raw_template.xml raw.xml

.. note::

	``--stdout`` のオプションをつけると標準出力にも出力します。::

		python txt2raw_XPS_survey.py "XPS_PHI_QUANTERA_survey.txt" xps_raw_template.xml raw.xml --stdout

装置出力パラメータファイル ``raw.xml`` から主要パラメータを抽出し、 ``primary.xml`` に出力します::

	python raw2primary_XPS_survey.py raw.xml xps_primary_template.xml primary.xml

バッチ処理
----------

上記のコマンドをまとめて実行できると便利です。
batch_exe_XPS.py は、上記のコマンドをまとめて行うプログラムです。::

	python batch_exe_XPS.py "../source/XPS_PHI_QUANTERA_survey.spe"

を実行すると、 ``../result/XPS_PHI_QUANTERA_survey`` というフォルダを作成し、その中にFND(Formatted Numerical Data)、
スペクトルの図、装置出力パラメータ、主要パラメータファイルを出力します。
連続変換を行いたい場合などに使用します。

Movie
-----

NIMS のサンプル動画です。こんな感じで動画が入ります。↓

.. raw:: html

    <div style="text-align: center; margin-bottom: 2em;">
    <iframe width="100%" height="350" src="https://www.youtube.com/embed/Nr256kGc-6o?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>

.. raw:: html

    <div style="text-align: center; margin-bottom: 2em;">
    <iframe width="100%" height="350" src="https://www.youtube.com/embed/J9K0bDkOFxU?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>

.. |yen| unicode:: U+00A5
   :trim:
