# Design Philosophy - TTPForge

By far the fastest and easiest way to create an automated simulation of 
attacker TTPs is to simply write a script that downloads
any required attacker tooling and then runs the appropriate commands. 
We'll refer to all such scripts (bash/powershell/python/etc.) as "interpreter scripts."
Interpreter scripts are delightfully simple and quick to implement; 
however, attempts to scale attack simulation efforts based on collections of interpreter
scripts quickly run into a variety of problems listed below. TTPForge attempts to solve
these problems while keeping TTP development just as fast and simple as interpreter scripts
- click each link to see how the project aims to address that particular challenge:

1. [High-Fidelity Telemetry Generation](steps.md)
1. [Reliable Post-Execution Cleanup](cleanup-actions.md)
1. [Convenient and Powerful Command Line Arguments](args.md)
1. [Composability - Avoiding Reinventing the Wheel](steps.md#subttp-step)