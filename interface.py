from jcli import jcli

def interpret(srces, maxSteps, reductionsPerStep, step,
              callbacks=None, builtins=None):
    return jcli.jcli_exec(srces, maxSteps, step, reductionsPerStep,
                          callbacks, builtins)
