module EventDispatch

export AsiEvent, Dispatch, event_listener, dispatch_event, add_event_listener, remove_event_listener, dispatch, e_dispatch
using Base.Threads
import MsgPack
struct AsiEvent
	type::String
	data::Union{Array, Tuple, Nothing}
	AsiEvent(t) = new(t, nothing)
	AsiEvent(t, d) = new(t, d)
	AsiEvent(t, d, a...)= new(t, d)
end

struct Dispatch
	events::Dict{String, Array}
	Dispatch() = new(Dict())
end

const dispatch = Dispatch()
const dispatch_external_topic = "/asimov/system/dispatch_external"

macro event_listener(topic, func)
	return esc(:(add_event_listener(dispatch, $topic, $func)))
end

macro e_dispatch(topic, params)
	return esc(:(dispatch_event(dispatch, AsiEvent($topic, $params))))
end

function dispatch_event_jl(dis::Dispatch, event::AsiEvent)
@sync begin
	if event.type in keys(dis.events)
		listeners = dis.events[event.type]
		return_vals = []
		for listener in listeners
			if !(event.data == nothing || length(event.data) == 0)
				#@async needed for updated worldage, @sync needed to prevent segfault, FIXME
				@async listener(event.data...)
			else
				@async listener()
			end
		end
	end
	#if event.type != dispatch_external_topic
		#dispatch_event(dis, AsiEvent(dispatch_external_topic, [event]))
	#end
	yield()
end
end
function dispatch_event(dis::Dispatch, event::AsiEvent)
	b = MsgPack.pack(event.data)
	s = length(b)
	#@info "CCalling DispatchGo on $event.type with data $b and size $s"
	ccall(:DispatchGo, Cvoid, (Cstring, Ptr{Cuint}, Csize_t), event.type, b, s)
		#return filter(x -> !is(nothing, x),return_vals)
end

function has_listener(dispatch::Dispatch, event_type::String, listener)
	if event_type in keys(dispatch.events)
		return listener in dispatch.events[event_type]
	else
		return false
	end
end


function add_event_listener(dispatch::Dispatch, event_type::String, listener)
	@info "Adding event listener for $event_type"
	if !(has_listener(dispatch, event_type, listener))
		listeners = get(dispatch.events, event_type, [])
		push!(listeners, listener)
		dispatch.events[event_type] = listeners
	end
end

function remove_event_listener(dispatch::Dispatch, event_type, listener)
	if has_listener(dispatch, event_type, listener)
		#listeners = dispatch.events[event_type]
		#if length(listeners) == 1
			# Only this listener remains so remove the key
		#	delete!(dispatch.events, event_type)
	
		#else
		#	println("REMOVE EVENT LISTENER UNIMPLEMENTED")
		#end
	end
end


end
