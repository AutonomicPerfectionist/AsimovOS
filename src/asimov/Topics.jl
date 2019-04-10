
module Topics
using EventDispatch
export TopicManager, Topic, registerTopic
struct Topic
	dispatch::Dispatch
	topicName::String
end

function (t::Topic)(args...; kwargs...)
	dispatch_event(t.dispatch, AsiEvent(t.topicName, args))
end

mutable struct TopicManager
	dispatch::Dispatch
	namespaces::Dict{String, Union{Dict, Topic}}

	TopicManager(d) = new(d, Dict())	
end


function registerTopic(manager::TopicManager, name::String; msgType = nothing)
	parts = split(name, "/")
	namespace = manager.namespaces
	if length(parts) >= 1
		for n in 2:(length(parts)-1)
			if !(parts[n] in keys(namespace))
				namespace[parts[n]] = Dict{String, Union{Topic, Dict}}()
			end
			namespace = namespace[parts[n]]
		end
	end
	namespace[parts[length(parts)]] = Topic(manager.dispatch, name)
end


end
