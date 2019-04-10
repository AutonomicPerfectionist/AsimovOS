__precompile__(true)
module Cluster

using EventDispatch
using Distributed
using Random

struct AsiClusterManager <: ClusterManager

end

function __init__()
    #Add a command (get_workers, called workers in CLI), to CLI on prerun_hook. Does not run if CLI is disabled because prerun_hook is never sent
    @EventDispatch.event_listener("/asimov/extension/cli/prerun_hook", () -> @EventDispatch.e_dispatch("/asimov/extension/cli/add_command", [get_workers, "workers", "Print workers available in cluster"]))
    @EventDispatch.event_listener "/asimov/extension/master/boot" (args)->addprocs(AsiClusterManager(), [""])
    atexit(Distributed.terminate_all_workers)
end    

function addprocs(manager::AsiClusterManager, addr::Array{String})
    @EventDispatch.e_dispatch "/asimov/system/log/info" ["Adding processes"]
    Distributed.init_bind_addr()
    Distributed.cluster_cookie(randstring(Distributed.HDR_COOKIE_LEN))
    Distributed.cluster_mgmt_from_master_check()

    lock(Distributed.worker_lock)
    try
        Distributed.addprocs_locked(Distributed.LocalManager(Sys.CPU_THREADS, true))
    finally
        unlock(Distributed.worker_lock)
    end
end

function launch(manager::AsiClusterManager, params::Dict, launched::Array, c::Condition)

end

function manage(manager::AsiClusterManager, id::Integer, config::WorkerConfig, op::Symbol)

end


function get_workers(args::String)
	println("$(workers())")
end

end
