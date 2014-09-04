## Introduction

This program provides directive for RST, which embedding visio file(only vsd format).

## Usage

In `conf.py`, please write following:

	```
	# extensions = []
	extensions = ['sphinxcontrib.visio']
	```
.

and write `rst` file as following:

	```
	... visioimg:: {visio_filename}
		e.t.c.
	```
.

 `visioimg` directive can used as `image` directive and this is the option for `name` and `page`:
 
 ```
 ... visioimg:: {visio_filename}
	:page:1

... visioimg:: {visio_filename}
	:name: circle
 ```
.

Note that `{visio_filename}` is absolute path or relation path from root(not
source directly).

## Requirements

* Python3
* Sphinx for Python3
* visio2img

