from joinwith import joinwith as __join

HEX = "HEX"
RGB = "RGB"
HSV = "HSV"
HLS = "HLS"

LST_FRM = [HEX, RGB, HSV, HLS]
FORMATS = __join(LST_FRM, ', ', ', or ', '"', '"')
