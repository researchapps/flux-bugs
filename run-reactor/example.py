#!/usr/bin/env/python3

import flux.job
import flux
import signal
import sys

cases = {"case1": "working", "case2": "broken", "case3": "broken"}

def main(case, state):
    print(f'\n======== 😸️ Preparing example for {state} {case}! 😸️ ========')

    fluxsleep = flux.job.JobspecV1.from_command(['sleep', '5'])
    handle = flux.Flux()
    flux_future = flux.job.submit_async(handle, fluxsleep)

    reactor = handle.get_reactor()
    reactor_interrupted = False

    def reactor_interrupt(handle, *_args):
        #  ensure reactor_interrupted from enclosing scope:
        nonlocal reactor_interrupted
        reactor_interrupted = True
        handle.reactor_stop(reactor)

    with handle.signal_watcher_create(signal.SIGINT, reactor_interrupt):
        with handle.in_reactor():
    
            # This works - two position arguments (reactor and flag)
            if case == "case1":
                 print("handle.reactor_run(reactor, 1)")
                 watcher_count = handle.reactor_run(reactor, 1)

            # This doesn't work - not providing the reactor and specifying flags
            elif case == "case2":
                print("handle.reactor_run(flags=1)")
                watcher_count = handle.reactor_run(flags=1)

            # This also doesn't work - should assume defaults                    
            elif case == "case3":
                print("handle.reactor_run()")
                watcher_count = handle.reactor_run()

        if reactor_interrupted:
            raise KeyboardInterrupt

        if watcher_count < 0:
            print(f"🙀️ There was an exception for {case}:")
            handle.raise_if_exception()
        else:
            print(f"😹️ There was no exception for {case}! yay!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Please specify case1, case2, or case3 as the only argument.')
    case = sys.argv[1].lower()
    if case not in cases:
        sys.exit(f"{case} is not a known case, please choose from {cases.keys()}")
    state = cases[case]   
    main(case, state)
