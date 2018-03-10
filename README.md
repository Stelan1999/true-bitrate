# true-bitrate

Little command-line tool to find out true audio file bit rate

## Description

`true-bitrate` command-line tool can find out, what is the true or real bit rate of any audio file supported by ffmpeg. Derived from and mainly developed in [Maurits van der Schee](https://github.com/mevdschee)'s [FakeFLAC](http://www.maurits.vdschee.nl/fakeflac/), I just added some enhanced output and fixed some dependencies.

## Usage

First install `ffmpeg` and `python2-scipy` packages (and also `python2-matplotlib` for debug purposes). Python 2.7 is required to run this properly. Finally you can just open a command line in true-bitrate folder and run `true-bitrate "my-file.mp3"`.

## Status

`maintained`
