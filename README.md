# BAC2

BAC 2.0 is a ground up rewrite of the BAC tool intended to unify and simplify the maintenance and use of the tool, and provide a platform on which new functionality can built.

Key points:
* Developed in Python
* Python API encapsulates core functionality
* Python API codes wrap around other libraries and services, e.g. Radical CyberTools
* Command line user interface wraps around API
* Commands take the form bac build [options]

Structure of this project:
├── api - top level API directory
│   └── bac - API code
│       ├── build - build layer API top level directory
│       ├── present - present layer API top level directory
│       └── simulate - simulate layer API top level directory
├── client - client code
├── docs - documentation
└── glue - remote workflow code
    └── AWS - Amazon EC2 glue scripts
