const GC_KEEP = []

#__precompile__(false)
module M
#push!(Main.GC_KEEP, M)
import Base.CoreLogging
push!(LOAD_PATH, "asimov")
#include("asimov/AsiBoot.jl")
import AsiBoot
import MsgPack
import EventDispatch

function dispatch_event(topic::String, args::Vector{UInt8})
	a = MsgPack.unpack(args)
	try
		EventDispatch.dispatch_event_jl(EventDispatch.dispatch, EventDispatch.AsiEvent(topic, a))
	catch e
		bt = catch_backtrace()
                showerror(stderr, e)
                Base.show_backtrace(stderr, bt)
                println(stderr, "")
	end
end

#push!(Main.GC_KEEP, dispatch_event)

function init()
	#Base.CoreLogging.disable_logging(Base.CoreLogging.Info)
	try
		AsiBoot.asi_init()
		@time AsiBoot.init()
	catch e
		bt = catch_backtrace()
		showerror(stderr, e)
		Base.show_backtrace(stderr, bt)
		println(stderr, "")
		@info "CAUGHT ERROR, ENTERING DEBUG SHELL"
		Base.exec_options(Base.JLOptions())
	end
end

end
