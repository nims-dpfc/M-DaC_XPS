Installation
============

python 環境がない場合は、 `Anaconda <https://www.anaconda.com/download/>`_ をインストールしてください。

Jupyter Notebook で実行する場合には、 Anaconda Prompt で ``plotly`` をインストールしてください。::

	 pip install plotly

.. note::

	環境によっては、プロキシの設定が必要です。プロキシ経由でインストールするには以下のコマンドを実行します。::
	
		pip --proxy http://[proxy]:[port] install plotly

	[proxy],[port]は使用環境に合わせて設定します。

.. index::
	single: proxy(pip)


- matplotlib
- matplotlib-scalebar
- numpy
- pandas

などのライブラリがない場合は ``pip`` などでインストールしてください。
動作中の環境にインストールされているライブラリ一覧は ``library_list.txt`` にあります。

.. index::
	single: Installation
