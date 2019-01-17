Welcome to M-DaC Tutorial
=====================================================

| NIMS_ では計測機器メーカーなどと協力して材料データに関する各種変換ツール(Materials Data Conversion Tools)を開発しています。
| M-Dac では、これらのツールをMITライセンスのもとで公開しています。
| これらのツールは `Jupyter Notebook`_ でも実行できます。

News
===========

| [2019 January 30] version 1.0.0 released. XPS(ULVAC-PHI対応)、XRD(Rigaku対応)のツールを公開しました。
|

Quick Start
===========

リポジトリをクローンまたはzipでダウンロードします。::

	git clone https://github.com/nims-dpfc/M-DaC_XPS.git myproject
	cd myproject

.. index::
	single: proxy(git)

.. note::

	fatal: unable to access 'https://github.com/...': Couldn't resolve host 'github.com' のエラーが出た場合はプロキシの設定を行ってください。
	
	プロキシの設定は以下のように行います。::

		git config --global http.https://github.com/nims-dpfc/M-DaC_XPS.git.proxy http://[proxy]:[port]

	[proxy],[port]は使用環境に合わせて設定します。


ツールディレクトリに移動します。::

	cd PHI_XPS_survey_narrow_tools

コマンドを実行します。::

	MPExport.exe -Filename:"..\source\XPS_PHI_QUANTERA_survey.spe" -TSV

	python txt2csv.py "XPS_PHI_QUANTERA_survey.txt"

	python csv2graph.py "XPS_PHI_QUANTERA_survey.csv"

	python txt2raw_XPS_survey.py "XPS_PHI_QUANTERA_survey.txt" xps_raw_template.xml raw.xml

	python raw2primary_XPS_survey.py raw.xml xps_primary_template.xml primary.xml

カレントディレクトリに各種変換されたファイルが作成されます。

`Jupyter Notebook`_ で実行する場合は jupyter notebook を立ち上げます。::

	jupyter notebook

チュートリアルにある「 `Jupyter Notebookでの実行`_ 」を参考に各種コマンドを実行します。
``xps_survey.ipynb`` を使用すると簡単に実行できます。

XPS_surveyの実行方法についての動画です。

.. raw:: html

    <div style="text-align: center; margin-bottom: 2em;">
    <iframe width="100%" height="350" src="https://www.youtube.com/embed/Nr256kGc-6o?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>


Online documentation (and example of use):
    https://nims-dpfc.github.io/MDAC_XPS/

Source code repository (and issue tracker):
    https://github.com/nims-dpfc/

Contents
========
.. toctree::
   :maxdepth: 2

   About
   Installation
   Tutorial
   FAQ <faq>
   LICENSE
   Terms of Service <terms_of_service>

License
=======
    MIT -- see the file ``LICENSE_MIT.txt`` for details.

.. _NIMS: https://www.nims.go.jp/
.. _Jupyter Notebook: http://jupyter.org/
.. _Jupyter Notebookでの実行: xps_survey.ipynb



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

