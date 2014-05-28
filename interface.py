from jcli import jcli

def interpret(srces, maxTicks, callbacks=None, builtins=None):
    return jcli.jcli_exec(srcs, maxTicks, callbacks, builtins)
