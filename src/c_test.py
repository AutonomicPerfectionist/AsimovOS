from ctypes import *
import sys
import ctypes

lib = cdll.LoadLibrary("a.out")

LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)

lib.main.argtypes = [c_int, LP_LP_c_char]

argc = len(sys.argv)
argv = (LP_c_char * (argc + 1))()
for i, arg in enumerate(sys.argv):
    enc_arg = arg.encode('utf-8')
    argv[i] = ctypes.create_string_buffer(enc_arg)

lib.main(argc, argv)
#lib.julia_main()
