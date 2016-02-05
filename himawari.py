#!/usr/bin/env python3

from io import BytesIO
from json import loads
from time import strptime, strftime
from PIL import Image
from urllib.request import urlopen
import argparse

def main():

	level = 4
	height = 550
	width = 550
	outfile = ''
	format = ''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--lod", choices=[4,8,16,20], help="Set level of detail for image. Valid values: 4, 8, 16, 20", type=int)
	parser.add_argument("-f", "--format", choices=["png","jpg","bmp","tiff","pcx","ppm","im","eps","gif","spi","webp"], help="Output format.")
	parser.add_argument("-o", "--out", help="Name of output file.")

	args = parser.parse_args()
	if args.lod is not None:
		level = args.lod
	if args.out is not None:
		outfile = args.out
	if args.format is not None:
		format = args.format

	with urlopen("http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json") as latest_json:	
		latest = strptime(loads(latest_json.read().decode("utf-8"))["date"], "%Y-%m-%d %H:%M:%S")

	print("Latest: {} GMT\n".format(strftime("%Y/%m/%d/%H:%M:%S",latest)))

	url_format = "http://himawari8.nict.go.jp/img/D531106/{}d/{}/{}_{}_{}.png"

	img = Image.new('RGB',(width*level, height*level))

	print("Downloading: 0/{}".format(level*level), end="\r")

	for x in range(level):
		for y in range(level):
			with urlopen(url_format.format(level,width,strftime("%Y/%m/%d/%H%M%S",latest), x, y)) as tile_w:
				tileData = tile_w.read()

			tile = Image.open(BytesIO(tileData))

			img.paste(tile, (width*x, height*y, width*(x+1), height*(y+1)))
			print ("Downloading: {}/{}".format(x*level + y + 1, level*level), end="\r")

	print("\nFinished\n")

	if outfile == '':
		if format == "png":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".png"
		elif format == "jpg":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".jpg"
		elif format == "bmp":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".bmp"
		elif format == "tiff":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".tiff"
		elif format == "pcx":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".pcx"
		elif format == "ppm":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".ppm"
		elif format == "im":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".im"
		elif format == "eps":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".eps"
		elif format == "gif":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".gif"
		elif format == "spi":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".spi"
		elif format == "webp":
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".webp"
		else:
			outfile = strftime("%Y-%m-%d-%H%M%S",latest) + ".png"

	if outfile[-4:] == ".png":
		img.save(outfile, "PNG")
	elif outfile[-4:] == ".jpg":
		img.save(outfile, "JPEG")
	elif outfile[-4:] == ".bmp":
		img.save(outfile, "BMP")
	elif outfile[-5:] == ".tiff":
		img.save(outfile, "TIFF")
	elif outfile[-4:] == ".pcx":
		img.save(outfile, "PCX")
	elif outfile[-4:] == ".ppm":
		img.save(outfile, "PPM")
	elif outfile[-3:] == ".im":
		img.save(outfile, "IM")
	elif outfile[-4:] == ".eps":
		img.save(outfile, "EPS")
	elif outfile[-4:] == ".gif":
		img.save(outfile, "GIF")
	elif outfile[-4:] == ".spi":
		img.save(outfile, "SPIDER")
	elif outfile[-5:] == ".webp":
		img.save(outfile, "WEBP")
	else:		
		img.save(outfile + ".png", "PNG")

if __name__ == "__main__":
	main()