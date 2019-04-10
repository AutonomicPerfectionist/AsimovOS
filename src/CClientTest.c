#include "julia.h"

extern int julia_main(jl_array_t*);
extern int init_jl_runtime();

int main(int argc, char *argv[])
{
	init_jl_runtime();
	jl_array_t *ARGS = (jl_array_t*)jl_get_global(jl_base_module, jl_symbol("ARGS"));
    jl_array_grow_end(ARGS, argc - 1);
    for (int i = 1; i < argc; i++) {
        jl_value_t *s = (jl_value_t*)jl_cstr_to_string(argv[i]);
        jl_arrayset(ARGS, s, i - 1);
    }
	julia_main(ARGS);

}
