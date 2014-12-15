# use unshare -n to avoid network access!

def runner():
    #     error: Could not find suitable distribution for Requirement.parse('pyOpenSSL')
    
    other_errors = []
    while True:
        x = todo.pop()
        # the special builder builds a protobuf of the results, but
        # not the actually installed output.
        output = nix_build(x)

        if not py_dep_error(output):
            other_errors.append(output)
            continue

        # other errors go into an output log.

        rewrite_dependencies(x, py_dep_error(output))
