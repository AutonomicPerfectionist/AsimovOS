module InitTest
@info "Evaluating Test"
function __init__()
	@info "RUNNING __INIT__"
	push!(LOAD_PATH, ".")
	Base.require(Main, :Test2)
	
end


end
