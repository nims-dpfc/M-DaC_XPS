==========================
 XPS
==========================

XPSのデータ変換手順

1．XPS生データ（survey1本のでOK）:MIDATA001.104.spe

2．PHI作成変換ツール:MPExport.exe

3．#1を#2で変換したテキストデータ: MIDATA001.104.txt

4．#3から，FNDを作るツール: txttocsvforphi.py

5．#3から#4で変換したFNDファイル: MIDATA001.104.csv

6．FNDファイルからスペクトルの図を作成するツール: csvtograph.py

7．#5から#6で作成したPNGファイル: MIDATA001.104.png

.. code-block::

	MPExpoter.exe -Filename:MIDATA001.104.spe -TSV

.. code-block::
	python txttocsvforphi.py MIDATA001.104.txt

.. code-block::
	python csvtograph.py MIDATA001.104.csv

For more information, refer to the `the documentation`__.

.. __: https://github.com/nims-dpfc/Materials_Data_Repository/

Instrallation
=============

ここにインストールの手順が入ります。

Documentation
=============

ここにドキュメントがはいります。