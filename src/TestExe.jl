Base.@ccallable function julia_main(ARGS::Vector{String})::Cint

eval(Meta.parse("""println("Testing")"""))
end
