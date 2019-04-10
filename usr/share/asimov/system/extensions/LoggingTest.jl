__precompile__(true)
module LoggingTest
#using AsiBoot
using EventDispatch
#export info


function __init__()
@info "Test completed successfully!"
@EventDispatch.event_listener "/asimov/system/log/info" info
end

function info(msg::String)
	@info msg
end

#@EventDispatch.event_listener "/asimov/system/log/info" info

#add_event_listener(dispatch, "/asimov/system/log/info", info)
end
