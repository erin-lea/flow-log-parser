## Project directory contents
`main.py`: The main program.  
`protocol-numbers-1.csv`: A CSV file that maps protocol numbers to protocol names (e.g. 6 -> TCP). Required for the program to work. ([file source](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml))

## Running the code
This program only requires Python to be installed in order to run. Use the command  
`python main.py [flow log filename] [lookup csv filename]`,  
where [flow log filename] is the filepath to the flow log data file and [lookup csv filename] is the filepath to the lookup table csv.

## Assumptions
This program only supports the default log format, and the only supported version is 2. It also assumes that any protocol number listed in the flow log data is an actual Assigned Internet Protocol Number used by the IANA.

## Additional notes
All tag and protocol names have are standardized to lowercase in order to ensure case insensitivity in processing.