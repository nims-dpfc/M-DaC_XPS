==========================
 XPS
==========================

フォルダに含まれるファイルの説明
=============================

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
