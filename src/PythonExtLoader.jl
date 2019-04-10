__precompile__(false)
module PythonExtLoader

@show LOAD_PATH

#using AsiBoot
using EventDispatch
@info "Used EventDispatch"
using PyCall
@info "Used PyCall"
pushfirst!(PyVector(pyimport("sys")["path"]), ".")
@info "Pushed system path"
@pyimport asimov.boot as boot
@info "Imported first module"
@pyimport logging as logging
@pyimport asimov.topics as topics
@pyimport os as os
@pyimport configobj
@pyimport asimov.extension as extension
@pyimport asimov.enabler as enabler
@pyimport asimov.event_dispatch as pyev
@pyimport asimov.event as pyasiev
@info "Imported modules"
function load_python_extensions(folder::String, overrides::Dict{String, Bool})
	@info "Loading Python Extensions in $folder"
	registered_extensions = Dict()
	for (root, subdirs, files) in walkdir(folder)
		@info "Extension root: $root"
		for filename in files
			file_path = joinpath(root, filename)
			file_extension = split(filename, ".")[end]
			@info "\t- file $filename (full path: $file_path), type: $file_extension"
					
		end
	end
	extension.load_extensions(folder)
	println("Registered extensions: $(extension.get_registered_extensions())")
	extension.set_enabler(enabler.Enabler(extension.get_registered_extensions(), Dict(), overrides))
	@async pull_python_events()
	@async gen_asi_events()
end

function gen_asi_events()
	while true
		yield()
		try
			request = pyasiev.creation_q[:get](false)
			@info "Generating AsiEvent"
			args = request[:args]
			@show args
			@show pyasiev
			@show pyasiev.created_dict
			pyasiev.update_created_dict(request[:id], AsiEvent(args...))
			@show pyasiev.created_dict
			@info "Setting waiter"
			request[:set]()
			@show request
		catch
		end
	end

end

function pull_python_events()
	while true
		yield()
		try
			#pyev.lock[:acquire]()
			EventDispatch.dispatch_event(dispatch, pyev.q[:get](false))
		catch
		finally
			#pyev.lock[:release]()
		end
	end
end

function dispatch_ev_python(ev)
	pyev.dispatch_event_python(ev)
end
#@EventDispatch.event_listener "/asimov/system/dispatch_external" dispatch_ev_python
@EventDispatch.event_listener "/asimov/system/load_extensions" load_python_extensions

function __init__()
	@info "Running PythonExtLoader.__init__"
	pyev.set_jl_dispatch(dispatch, EventDispatch, dispatch_event, add_event_listener, AsiEvent)
	logLevel = logging.DEBUG
	#if confDict["system"]["debug"]:
	#       logLevel = logging.DEBUG
	logging.basicConfig(level=logLevel)
	#clusterName = conf.getClusterName()
end

end
