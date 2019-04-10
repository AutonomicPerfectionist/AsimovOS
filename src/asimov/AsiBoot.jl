__precompile__(true)

module AsiBoot
using Revise
using Distributed
export dispatch, extensions_dir
#include("EventDispatch.jl")
#include("Enabler.jl")
#include("Topics.jl")
import REPL
using EventDispatch
using Enabler
using Topics
#using PyCall
import Pkg
import Pkg.TOML
#import Libdl

const config_loc = "etc/asimov-local/config.toml"
const config_dir = "etc/asimov-local/config.d"
const enabler_overrides_loc = "etc/asimov-local/enables.toml"
const extensions_dir = "usr/share/asimov/extensions"
const system_ext_dir = "usr/share/asimov/system/extensions"


function load_c_extensions(folder::String)
	registered_extensions = Dict()
        for (root, subdirs, files) in walkdir(folder)
                #@info "Extension root: $root"
                for filename in files
                        file_path = joinpath(root, filename)
                        file_extension = split(filename, ".")[end]
                        ext_name = split(filename, ".")[1]
                        #@info "\t- file $filename (full path: $file_path), type: $file_extension"
                        if file_extension == "dylib" 
                                @info "\tEvaluating file $file_path"
                                #ext = Libdl.dlopen(file_path)
				#jl_init = Libdl.dlsym(ext, :init_jl_runtime)
				#ccall(jl_init, Cvoid, ())
				#ext_init = Libdl.dlsym(ext, :init)
				#ccall(ext_init, Cvoid, ())
                        end
                end
        end
end

function load_julia_extensions(folder::String)
	#folder = system_ext_dir
	@info "Loading Julia extensions in $folder"
	registered_extensions = Dict()
	for (root, subdirs, files) in walkdir(folder)
                #@info "Extension root: $root"
		push!(LOAD_PATH, root)
                for filename in files
                        file_path = joinpath(root, filename)
                        file_extension = split(filename, ".")[end]
			ext_name = split(filename, ".")[1]
                        #@info "\t- file $filename (full path: $file_path), type: $file_extension"
			if file_extension == "jl"
				@info "\tEvaluating file $file_path"
				#include(file_path)
				#eval(Meta.parse(read(open(file_path), String)))
				Base.require(Main, Symbol(ext_name))
			end
                end
        end
end



function jl_repl(args::String)
	#tty = REPL.Terminals.TTYTerminal("xterm", stdin, stdout, stderr)
	#line_edit_repl = REPL.LineEditREPL(tty, true)
	#REPL.accessible(AsiBoot)
	#REPL.run_repl(line_edit_repl)
	Base.exec_options(Base.JLOptions())
	return
end
precompile(jl_repl, (String,))

function init()
	topic_manager::TopicManager = TopicManager(dispatch)
	#pyasiev.set_event_type(AsiEvent)
	conf::Dict{Any, Any} = build_configuration(config_loc, config_dir)
        #logLevel::Int64 = logging.INFO
	#if conf["system"]["debug"] == "True"
	#	logLevel = logging.DEBUG
	#end
	enabler_overrides::Dict{String, Bool} = Pkg.TOML.parsefile(enabler_overrides_loc)	
	#logging.basicConfig(level=logLevel)
	#Since boot is not an extension, this must be called manually
  	registerTopic(topic_manager, "/asimov/boot/lifecycle")
	registerTopic(topic_manager, "/asimov/boot/config")
	registerTopic(topic_manager, "/asimov/boot/finished")

		
	load_extensions(extensions_dir, enabler_overrides)
	
	atexit(() -> @EventDispatch.e_dispatch("/asimov/system/on_shutdown",[]))

	@EventDispatch.event_listener "/asimov/system/shutdown" shutdown
	@EventDispatch.event_listener "/asimov/system/extensions/jl_repl/start_repl" jl_repl
	topic_manager.namespaces["asimov"]["boot"]["config"](conf)
	@info "Ran topic 1"
	topic_manager.namespaces["asimov"]["boot"]["lifecycle"]("start")
	@EventDispatch.e_dispatch "/asimov/system/log/info" ["TESTING INFO OVER TOPICS"]
	#py"""
#from asimov import event_dispatch; from asimov.event import AsimovEvent
#	"""
#	@EventDispatch.e_dispatch "/asimov/extension/cli/add_command" [py"lambda self, x: event_dispatch.dispatch_event(AsimovEvent(\"/asimov/system/extensions/jl_repl/start_repl\", [x]))", "jl", "Invoke the Julia interpreter, with access to AsiBoot"]
	topic_manager.namespaces["asimov"]["boot"]["finished"]()
	dispatch_event(dispatch, AsiEvent("/asimov/boot/finished", []))
	#dispatch_event(dispatch, AsiEvent("/asimov/services/test", []))
	#wait()
end

function shutdown()
	#dispatch_event(dispatch, AsiEvent("/asimov/system/on_shutdown", []))
	exit()
end

function load_extensions(folder::String, overrides::Dict{String, Bool})
	"""
	Load extensions in folder and run Enabler scripts
	"""
	@info "Loading extensions"
	#dispatch_event(dispatch, AsiEvent("/asimov/system/load_extensions", [folder, overrides]))
	
end

function build_configuration(main, folder)
	"""
	Build the master configuration dictionary. Main is the file
	location of the primary configuration, and folder is the directory
	where secondary files are located
	"""
	if !endswith(folder, '/')
        	folder *= '/'
	end
	#TODO Load and combine secondary configs
	return Pkg.TOML.parsefile(main)
end

@Base.ccallable function asi_init()::Cint
	push!(LOAD_PATH, "asimov")
	#precompile(jl_repl, (PyObject,))
	ccall((:setpgrp, "libc"), Int32, ())
	#add_event_listener(dispatch, "/asimov/system/load_extensions", load_julia_extensions)
	#load_extensions(system_ext_dir)
	#load_extensions(boot.extensionsDir)
	@time load_julia_extensions(system_ext_dir)
	load_julia_extensions(extensions_dir)
	#load_c_extensions(extensions_dir)
	
	0
end


@Base.ccallable function julia_main(ARGS::Vector{String})::Cint
	#Base.require(Main, :AsiBoot)
	AsiBoot.init()
	return 0
end

end

