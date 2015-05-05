__author__ = 'Dai Tianyu (dtysky)'

from PIL import Image
import os, json

ModuleName='Shear'

conf = json.load(open('../ImageForTest/conf.json', 'r'))['conf']

FileAll = []

for root,dirs,files in os.walk('../ImageForTest'):
    for f in files:
    	name, ex=os.path.splitext(f)
        if ex in ['.jpg', '.bmp']:
        	FileAll.append((root+'/', name, ex))

def sh_format(sh):
	r, d = format(sh, 'f').split('.')
	r = '0' + r[0] if len(r) == 1 else '1' + r[1]
	d = float('0.' + d)
	res = ''
	for i in xrange(16):
		d = d * 2
		res += '1' if d >= 1 else '0'
		d = d - 1 if d >= 1 else d
	return r + res


def color_format(color):
	res = bin(color)[2:]
	for i in xrange(8 - len(res)):
		res = '0' + res
	return res

def create_dat(im):
	data_src = im.getdata()
	xsize, ysize = im.size
	data_res = ''
	all_size = xsize * ysize - 1
	for y in range(ysize):
		for x in range(xsize):
			data_res += color_format(xsize - 1 - x) + '\n'
			data_res += color_format(ysize - 1 - y) + '\n'
			data_res += color_format(data_src[(ysize - 1 - y) * xsize + (xsize - 1 - x)]) + '\n'
	return data_res[:-1]

dat_index = ''

for root, name, ex in FileAll:
	im_src = Image.open(root + name + ex)
	xsize, ysize = im_src.size
	first = False
	for c in conf:
		shu = float(c['shu'])
		shv = float(c['shv'])
		dat_res = open('../FunSimForHDL/%s-%sx%s.dat' % (name, c['shu'], c['shv']), 'w')
		dat_res.write('%d\n%d\n' % (xsize, ysize))
		if not first:
			dat_res.write('%s\n%s\n' % (sh_format(shu), sh_format(shv)))
			dat_res.write(create_dat(im_src))
		else:
			dat_res.write('%s\n%s' % (sh_format(shu), sh_format(shv)))
		first = True
		dat_index += '%s-%sx%s\n' % (name, c['shu'], c['shv'])
		dat_res.close()

dat_index = dat_index[:-1]
dat_index_f = open('../FunSimForHDL/imgindex.dat','w')
dat_index_f.write(dat_index)
dat_index_f.close()