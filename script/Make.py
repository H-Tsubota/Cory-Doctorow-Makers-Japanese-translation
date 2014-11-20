#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import re
import shutil
import MakeEpub3

def getParagraph(path):
	f = codecs.open(path,'r','utf-8')
	text = f.read()
	f.close()

	newText = ''
	patternForDeleteID = re.compile( '\sid="p[0-9]+"')
	pattern = re.compile(r'<p[a-zA-Z0-9\s="]*>.*?</p>', re.DOTALL)
	matchedList = pattern.findall(text)
	if matchedList:
		for e in matchedList:
			str = patternForDeleteID.sub('', e)
			str = str.replace('\r\n','')
			
			newText = newText + str

	return newText

def writePart(subDirName, partTitle, numChapter):
	rootdir = '../'
	
	xhtml = u'<?xml version="1.0" encoding="UTF-8"?>'
	xhtml += u'<!DOCTYPE html ['
	xhtml += u'<!ENTITY nbsp "&#160;">'
	xhtml += u'<!ENTITY amp "&#38;#38;">'
	xhtml += u'<!ENTITY gt "&#62;" >'
	xhtml += u']>'
	xhtml += u'<html xmlns="http://www.w3.org/1999/xhtml"  xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja" lang="ja">'
	xhtml += u'<head>'
	xhtml += u'<meta name="viewport" content="width=device-width,initial-scale=1.0" />'
	xhtml += u'<link rel="stylesheet" href="default.css" type="text/css" />'
	xhtml += u'<title>メイカーズ ' + partTitle + '</title>'
	xhtml += u'</head>'
	xhtml += u'<body>'
	xhtml += u'<h1>' + partTitle + '</h1>'
	
	part1dir = rootdir +'/' + subDirName
	for i in range(numChapter):
		xhtml += u'<hr />'
		xhtml += getParagraph(part1dir + '/chapter' + str(i+1) + '.html')

	xhtml += u'</body>'
	xhtml += u'</html>'

	f = open(subDirName + '.xhtml', 'w')
	f.write(xhtml.encode('utf-8'))
	f.close()
	
def main():
	# 必要ファイルを作成
	writePart(u'part1', u'第一部', 13)
	writePart(u'part2', u'第二部', 14)
	writePart(u'part3', u'第三部', 61)
	
	# Epub3にフォーマット
	epub3 = MakeEpub3.osEpub3()
	
	epub3.isVertical = True
	
	epub3.version = 1.0
	epub3.coverImage = '../resources/Cover.png'
	epub3.title = u'メイカーズ'
	epub3.creator = u'コリイ・ドクトロウ'
	epub3.translator = u'Haruka Tsubota'
	epub3.publisher = u'Haruka Tsubota'
	epub3.coverPage = '../resources/cover.xhtml'

	epub3.images.append('../resources/by-nc-sa.png')
	
	epub3.css.append('../default.css')
	epub3.css.append('../resources/colophon.css')
	epub3.css.append('../resources/cover.css')
	
	epub3.contents['Part1.xhtml'] = u'第一部'
	epub3.contents['Part2.xhtml'] = u'第二部'
	epub3.contents['Part3.xhtml'] = u'第三部'	
	epub3.contents['../resources/colophon.xhtml'] = u'奥付'

	# 書き出し
	epub3.save("Makers.epub")

if __name__ == '__main__':
	main()