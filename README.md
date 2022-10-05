# PDF Recycler
A simple gui program to convert a pdf to jpg. Written in python using [PySimpleGui](https://www.pysimplegui.org/en/latest/).

Under the hood it uses the pip module [pdf2image](https://pypi.org/project/pdf2image/).

# Installation

Clone or download this repository and execute 'pdf-recycler.py'.

# Requirements

### python and pip
On Windows download the installer from [https://www.python.org/](https://www.python.org/)

On linux install it with your package manager.

Debain, Ubuntu, PopOS

```
$ sudo add-apt-repository universe
$ sudo apt install python3-pip python3-tk
```

Fedora

```
$ sudo dnf install python3-pip python3-tkinter
```

Arch

```
$ sudo pacman -Sy python-pip tk
```


### pdf2image and pysimplegui (pip or pip3 depends on distro)

```
$ pip install pdf2image pysimplegui
```
