from joinwith import joinwith as __join

HEX = "HEX"
RGB8 = "RGB8"
RGB16 = "RGB16"
HSV = "HSV"
HLS = "HLS"

LST_FRM = [HEX, RGB8, RGB16, HSV, HLS]
FORMATS = __join(LST_FRM, ', ', ', or ', '"{}"')
