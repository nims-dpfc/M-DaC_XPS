XPS
====

フォルダに含まれるファイルの説明
--------------------------------

========================= =========================================================================================================================================================
program名		  説明
========================= =========================================================================================================================================================
MPExport.exe              ULVAC-PHI製変換ツール（.spe,.proのファイルからtxtファイルを作成するツール）
txttocsvforphi.py	  txtファイルからFND(Formatted Numerical Data)のcsvファイルを作成するツール
csv2graph.py		  FND(Formatted Numerical Data)のcsvファイルからスペクトルの図を作成するツール（グラフ表示、主要パラメータ表示なし）
csv2graph_for_jupyter.py  FND(Formatted Numerical Data)のcsvファイルからスペクトルの図を作成するツール（jupyter notebookで使用時、グラフ表示、主要パラメータ表示あり）
txt2raw_XPS_survey.py	  txtファイルから装置出力パラメータを抽出するツール
xps_raw_templateXML.xml	  装置出力パラメータ抽出に使用するテンプレートファイル
raw2primary_XPS_survey.py 装置出力パラメータファイルから主要パラメータを抽出するツール
xrd_primary_template.xml  主要パラメータ抽出に使用するテンプレートファイル
execute.py		  rasファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までを一度に行うツール
execute_jupyter.py	  rasファイルからスペクトルの図作成、装置出力パラメータ、主要パラメータの抽出までをjupyter notebook上で一度に行い、図の表示、主要パラメータを表示するツール
README.rst		  使い方の説明
=========================  =========================================================================================================================================================


1．source/XPS_PHI_QUANTERA_survey.spe: XPS生データサンプル

2．MPExport.exe: PHI作成変換ツール

3．source/XPS_PHI_QUANTERA_survey.txt: #1を#2で変換したテキストデータ

4．txttocsvforphi.py: #3から，FND(Formatted Numerical Data)を作るツール

5．source/XPS_PHI_QUANTERA_survey.csv: #3から#4で変換したFNDファイル

6．csvtograph.py: FND(Formatted Numerical Data)ファイルからスペクトルの図を作成するツール

7．source/XPS_PHI_QUANTERA_survey.png: #5から#6で作成したPNGファイル

コマンド
========
sourceディレクトリに移動します::

	cd source

.spe形式のファイルをテキストファイルに変換します::

	../MPExpoter.exe -Filename:XPS_PHI_QUANTERA_survey.spe -TSV

テキストファイルをフォーマットされた数値データ(csv)に変換します::

	python ../txttocsvforphi.py XPS_PHI_QUANTERA_survey.txt

csvファイルから画像を作成します::

	python ../csvtograph.py XPS_PHI_QUANTERA_survey.csv

For more information, refer to the `the documentation`__.

.. __: https://github.com/nims-dpfc/Materials_Data_Repository/

Instrallation
=============

ここにインストールの手順が入ります。

Documentation
=============

ここにドキュメントがはいります。
