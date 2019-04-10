__precompile__(true)
module LogTest2
using EventDispatch

function info(msg::String)
	@info "Message from LogTest2: $msg"
end
function __init__()
	#@EventDispatch.event_listener "/asimov/system/log/info" info
end
end
