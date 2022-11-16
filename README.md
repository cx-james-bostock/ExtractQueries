# ExtractQueries

Extract CxQL queries from a CxSAST instance. This program uses the
[Checkmarx Python
SDK](https://github.com/checkmarx-ts/checkmarx-python-sdk) to extract
the CxQL queries from a CxSAST instance and write them to the local
filesystem.

## Usage

Invoking the `ExtractQueries.py` script with either the `-h` or
`--help` command line options generats a usage message:

```
usage: ExtractQueries.py [-h] [-n] [-o DIR] [-v]

Extract queries from a CxSAST instance

options:
  -h, --help            show this help message and exit
  -n, --no-cx           Do not extract out-of-the-box queries
  -o DIR, --output-dir DIR
                        Extract queries to the specified directory
  -v, --verbose         Verbose output (may be specified multiple times)
  ```
  