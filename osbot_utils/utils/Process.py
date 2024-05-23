import os
import signal
import subprocess


#def run_process(executable, params = None, cwd='.'):
#    return Process.run(executable, params, cwd)

def chmod_x(executable_path):
    return run_process("chmod", ['+x', executable_path])

class Process:

    @staticmethod
    def run(executable, params = None, cwd='.', **run_kwargs):
        params = params or []
        if type(params) is str:
            params = [params]
        run_params = [executable] + params
        error      = None
        stderr     = ''
        stdout     = ''
        kwargs = { 'cwd'    : cwd             ,
                   'stdout' : subprocess.PIPE ,
                   'stderr' : subprocess.PIPE ,
                   'timeout': None }
        kwargs = { **kwargs , **run_kwargs }                 # merge dictionaries with run_kwargs taking precedence
        try:
            result      = subprocess.run(run_params, **kwargs)
            stderr      = result.stderr.decode()
            stdout      = result.stdout.decode()
            status      = "ok"
        except subprocess.TimeoutExpired as timeout_error:
            if timeout_error.stderr:
                stderr = timeout_error.stderr.decode()
            if timeout_error.stdout:
                stdout = timeout_error.stdout.decode()
            error  = timeout_error
            status = 'error'
        except Exception as exception:
            error  = exception
            status = 'error'
        return {
                "cwd"       : cwd                   ,
                "error"     : error                 ,
                "kwargs"    : kwargs                ,
                "runParams" : run_params            ,
                "status"    : status                ,
                "stdout"    : stdout                ,
                "stderr"    : stderr
            }
    @staticmethod
    def stop(pid):
        return os.kill(pid, signal.SIGKILL)

    # exec helpers
    @staticmethod
    def exec_open(file_path, cwd='.'): return Process.run("open", [file_path], cwd)


kill_process  = Process.stop
run_process   = Process.run
exec_open     = Process.exec_open
exec_process  = Process.run
process_run   = Process.run
start_process = Process.run
stop_process  = Process.stop




#def run_process(executable, params = None, cwd='.'):
#    return Process.run(executable, params, cwd)