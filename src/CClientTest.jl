import Libdl

ext = Libdl.dlopen("./a.out")
jl_ini = Libdl.dlsym(ext, :init_jl_runtime)
ext_init = Libdl.dlsym(ext, :main)
@show ccall(jl_ini, Cint, ())
@show ext
@show jl_ini
@show ext_init
@show ccall(ext_init, Cint, (Vector{String},), Vector{String}())



