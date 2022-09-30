# Reactor run!

This container will reproduce a bug that the reactor run does not like any deviation from
providing two arguments. This means:

 - Providing two arguments, the reactor and flags, no keywords, works (case1)
 - You can't provide a kwarg (case 2)
 - You can't leave out arguments and assume a defalt (case 3).
 
## Usage

First, build the demo container.

```bash
$ docker build -t flux-bug .
```

## Before bug fix

We were calling `handle.flux_reactor_run()` and we needed to call `handle.reactor_run()`.

You can reproduce the bug by way of running the container, which will start flux and then use the
entrypoint.sh to run three different cases (the ones above):

```bash
$ docker run -it flux-bug
```
```console

======== 😸️ Preparing example for working case1! 😸️ ========
handle.flux_reactor_run(reactor, 1)
😹️ There was no exception for case1! yay!

======== 😸️ Preparing example for broken case2! 😸️ ========
handle.flux_reactor_run(flags=1)
Traceback (most recent call last):
  File "/code/example.py", line 60, in <module>
    main(case, state)
  File "/code/example.py", line 37, in main
    watcher_count = handle.flux_reactor_run(flags=1)
TypeError: FunctionWrapper.__call__() got an unexpected keyword argument 'flags'

======== 😸️ Preparing example for broken case3! 😸️ ========
handle.flux_reactor_run()
Traceback (most recent call last):
  File "/code/example.py", line 60, in <module>
    main(case, state)
  File "/code/example.py", line 42, in main
    watcher_count = handle.flux_reactor_run()
  File "/opt/spack/opt/spack/linux-ubuntu22.04-x86_64_v3/gcc-11.2.0/flux-core-master-w57ow5sqbyknqvy45xwzba3daq7iwsks/lib/flux/python3.10/flux/wrapper.py", line 177, in __call__
    raise WrongNumArguments(
flux.wrapper.WrongNumArguments: 
The wrong number of arguments has been passed to wrapped C function:
Expected 2 arguments, received 0
Name: flux_reactor_run
C signature: int(*)(struct flux_reactor *, int)
Arguments: []
Handle type: <ctype 'struct flux_handle_struct *'>
          
2022-09-30T00:09:34.861452Z broker.err[0]: rc2.0: /bin/bash /entrypoint.sh Exited (rc=1) 0.3s
2022-09-30T00:09:34.872368Z broker.err[0]: cleanup.1: flux-job: Canceled 2 jobs (0 errors)
2022-09-30T00:09:34.889630Z broker.err[0]: cleanup.2: flux-queue: 1 pending jobs
```

If you want to interactively debug, enter the container using a bash entrypoint:

```console
$ docker run -it --entrypoint bash flux-bug
# flux start --test-size=4
``` 

And you can run the example.py directly with any case:

```bash
$ python example.py case1
$ python example.py case2
$ python example.py case3
...

======== 😸️ Preparing example for working case1! 😸️ ========
handle.flux_reactor_run(reactor, 1)
😹️ There was no exception for case1! yay!
root@c564560fc464:/code# python example.py case3
```

And vim and IPython are installed if you want to poke around. Happy debugging! 🐛️

## After bug fix

Calling `handle.reactor_run()` instead of `handle.flux_reactor_run()`.


```console
$ docker run -it flux-bug

======== 😸️ Preparing example for working case1! 😸️ ========
handle.reactor_run(reactor, 1)
😹️ There was no exception for case1! yay!

======== 😸️ Preparing example for broken case2! 😸️ ========
handle.reactor_run(flags=1)
😹️ There was no exception for case2! yay!

======== 😸️ Preparing example for broken case3! 😸️ ========
handle.reactor_run()

```
