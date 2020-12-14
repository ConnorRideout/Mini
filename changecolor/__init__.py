"""Available functions are lighten, darken, saturate, desaturate, and invert.
Type 'help(<func>)' for more information about a specific function."""

import colorsys


def _validation(intype, val, retype, bit):
	if bit not in [8,16]:
		raise ValueError("'bit' must be 8 or 16")
	if intype.upper() not in (modes := 'HEX, RGB, HSV, or HLS'):
		raise ValueError("'inputMode' must be '{}'".format(modes))
	if retype.upper() not in modes:
		raise ValueError("'returnMode' must be '{}'".format(modes))
	if intype == 'HEX':
		if (v:=len(val.lstrip('#'))) != 6 and v != 12:
			raise ValueError("HEX values must have a length of 6 (8-bit) or 12 (16-bit)")
	elif type(val) not in [list, tuple] or len(val) != 3:
		raise ValueError("'value' must be a list or tuple of 3 integers if 'inputType' is '{}'".format(intype.upper()))
	return

def _HEX(value, bit, retype='HSV'):
	lv = len(v:=value.lstrip('#'))
	lrgb = [int(v[i:i+lv//3], 16) for i in range(0, lv, lv//3)]
	rgb = _RGB(lrgb, bit, 'RGB')
	return rgb if retype == 'RGB' else colorsys.rgb_to_hsv(*rgb)

def _RGB(value, bit, retype='HSV'):
	rgb = [(n>>8)/255 for n in value] if bit == 16 else [n/255 for n in value]
	return rgb if retype == 'RGB' else colorsys.rgb_to_hsv(*rgb)

def _HSV(value, bit, retype='HSV'):
	x, y, z = value
	hsv = [x/360, y/100, z/100]
	return [round(255*n) for n in colorsys.hsv_to_rgb(*hsv)] if retype == 'RGB' else hsv

def _HLS(value, bit, retype='HSV'):
	x, y, z = value
	rgb = colorsys.hls_to_rgb(x/360, y/100, z/100)
	return [round(255*n) for n in rgb] if retype == 'RGB' else colorsys.rgb_to_hsv(*rgb)

def _output(newVal, retype):
	if retype == 'HEX':
		return '#'+''.join([format(round(255*n), '02x') for n in colorsys.hsv_to_rgb(*newVal)])
	elif retype == 'RGB':
		return [round(255*n) for n in colorsys.hsv_to_rgb(*newVal)]
	elif retype == 'HLS':
		a, b, c = colorsys.rgb_to_hls(*colorsys.hsv_to_rgb(*newVal))
	return [round(n) for n in [360*a, 100*b, 100*c]]


def lighten(inputType, value, percent=25, returnType='HEX', bit=8):
	_validation(inputType, value, returnType, bit)
	a, b, c = globals()['_'+inputType.upper()](value, bit)
	newVal = [a, b, min(c+percent/100,1)]
	return _output(newVal, returnType.upper())

def darken(inputType, value, percent=25, returnType='HEX', bit=8):
	_validation(inputType, value, returnType, bit)
	a, b, c = globals()['_'+inputType.upper()](value, bit)
	newVal = [a, b, max(c-percent/100,0)]
	return _output(newVal, returnType.upper())

def saturate(inputType, value, percent=25, returnType='HEX', bit=8):
	_validation(inputType, value, returnType, bit)
	a, b, c = globals()['_'+inputType.upper()](value, bit)
	newVal = [a, min(b+percent/100,1), c]
	return _output(newVal, returnType.upper())

def desaturate(inputType, value, percent=25, returnType='HEX', bit=8):
	_validation(inputType, value, returnType, bit)
	a, b, c = globals()['_'+inputType.upper()](value, bit)
	newVal = [a, max(b-percent/100,0), c]
	return _output(newVal, returnType.upper())

def invert(inputType, value, returnType='HEX', bit=8):
	"""Invert the provided color. Attributes:
	-inputType (type:string)
		The data type of the input. One of HEX, RGB, HSV, or HLS
	-value (type:list of 3 ints OR string)
		The data. If 'inputType' is "HEX", must be a string. Otherwise,
		must be a list of 3 integers
	-returnType (type:string; default="HEX")
		The data type to return. One of HEX, RGB, HSV, or HLS
	-bit (type:int; default=8)
		The color bit depth. One of 8 or 16"""
	_validation(inputType, value, returnType, bit)
	conv = globals()['_'+inputType.upper()](value, bit, 'RGB')
	a, b, c = [1-n for n in conv]
	newVal = colorsys.rgb_to_hsv(a, b, c)
	return _output(newVal, returnType.upper())

def help(func=None):
	"""the provided color. Attributes:
	-inputType (type:string)
		The data type of the input. One of HEX, RGB, HSV, or HLS
	-value (type:list of 3 ints OR string)
		The data. If 'inputType' is "HEX", must be a string. Otherwise,
		must be a list of 3 integers
	-percent (type:int; default=25)
		Percent to change the color by. Integer between 1 and 100
	-returnType (type:string; default="HEX")
		The data type to return. One of HEX, RGB, HSV, or HLS
	-bit (type:int; default=8)
		The color bit depth. One of 8 or 16"""
	if not func:
		print(__doc__)
	elif func == 'invert':
		print(invert.__doc__)
	elif func in ['lighten','darken','saturate','desaturate']:
		print(func.capitalize(), help.__doc__)
	else:
		raise ValueError("incorrect argument; must be one of lighten, darken, saturate, desaturate, invert")