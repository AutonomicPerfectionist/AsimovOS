module Enabler


mutable struct ExtEnabler

	extensions
	enabled::Array
	enable_functions
	overrides::Dict{String, Bool}
	function ExtEnabler(ext, e_funcs, overrides)
		self = new(ext, [], e_funcs, overrides)
		resolve_enable!(self)
		return self
	end

end


function resolve_enable!(enabler::ExtEnabler)
	@debug "Resolving extension enabled states"
	
	for ext in values(enabler.extensions)
		println("ENABLE NOT IMPLEMENTED FOR EXTENSION $(ext)")
	end
end


end
