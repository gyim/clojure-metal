## clojure-metal
-----------------

## Goals

To provide a super fast booting Clojure interpreter with "good enough" performance. The goal of this interpreter is not to
beat the Clojure JVM implementation, but instead to fill the space of a fast scripting/native interpreter without the need
of an external compiler.

## Tech

This interpreter is being written in RPython and is compiled via the PyPy tool chain. The PyPy toolchain has the ability to freeze
the state of an interpreter before translation. Thus the plan is to port most of the Clojure JVM implementation to RPython.
Then clojure.core can be loaded, compiled, and run. At this point the interpreter can be frozen and translated to a native application.
Thus all the startup code in the core libraries will not need to be re-run whenever the interpreter is loaded.

## Status
Current status is very minimal. The plans are as follows:

1) Port Lazy Seq, Chunked Seq, etc. (25% done)
2) Port PersistentVector (50% done)
3) Port PersistentHashMaps
4) Port symbols, and keywords
5) Port var, namespace, and atom
6) Port the reader
7) Write a compiler
8) Write the interpreter
9) JIT enable the interpreter


## License

Clojure-metal will carry the same license as Clojure on the JVM, and will not accept patches from authors without a clojure CA. The idea here is that some day it would be nice to see clojure-metal become an official port. Allowing code from random submitters would torpedo this objective.

## Copyrights
Copyright © 2013 Rich Hickey, Timothy Baldridge and contributors

Distributed under the Eclipse Public License, the same as Clojure.

## Q/A

Q: I see Rich Hickey's name in the copyright, is he working on this project?
A: No. Large portions of this project are simply ported from the Java Code, thus the copyright notice.