
import argparse
from extract     import *
from debug_args  import IN_PARAMS

debug = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Extractor for SquareSoft PSX Games developed by Square Product Division 3")

    group = parser.add_mutually_exclusive_group(required=True)

    help_bin       = "For retail .BIN / ISOs of Xenogears, Chrono Cross and Dewprism / Threads of Fate."
    help_hedexeimg = "For .HED and .IMG files found within demos for Chrono Cross and Dewprism / Threads of Fate."
    help_exeimg    = "For the PSX_CD.EXE and CDROM.IMG files found in Xenogears 1997 Taikenban build."

    group.add_argument('-b',   '--bin',       nargs=1, help=help_bin,       metavar=('.BIN'))
    group.add_argument('-hei', '--hedexeimg', nargs=3, help=help_hedexeimg, metavar=('.HED', '.EXE', '.IMG'))
    group.add_argument('-ei',   '--exeimg',   nargs=2, help=help_exeimg,    metavar=('.EXE', '.IMG'))

    parser.add_argument('-o', '--output', nargs=1, default = [''], help='Output folder to write files to', metavar=('outpath'))

    if not debug:
        args = parser.parse_args()
    else:
        version = "DP_USA"
        discnum = "disc1"
        args = parser.parse_args(['-b', IN_PARAMS[version][discnum], '-o', '../S3Res/'])
        #args = parser.parse_args(['-hei', IN_PARAMS["DP_JP_TAIKEN_SP5"]["hed"],  IN_PARAMS["DP_JP_TAIKEN_SP5"]["exe"], IN_PARAMS["DP_JP_TAIKEN_SP5"]["img"], '-o', '../S3Res/'])
        #args = parser.parse_args(['-ei', IN_PARAMS["XG_JP_TAIKEN"]["exe"], IN_PARAMS["XG_JP_TAIKEN"]["img"], '-o', '../S3Res/'])
        #args = parser.parse_args(['-h'])

    if args.bin:         extract_fs_bin(args.bin[0], args.output[0])
    elif args.hedexeimg: extract_fs_hedexeimg(args.hedexeimg[0], args.hedexeimg[1], args.hedexeimg[2], args.output[0] )
    elif args.exeimg:    extract_fs_exeimg(args.exeimg[0], args.exeimg[1], args.output[0] )
