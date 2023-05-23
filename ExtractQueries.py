import argparse
import os
from pathlib import Path
import sys
from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_query_collection

language_map = {
    1: 'CSharp',
    2: 'Java',
    4: 'CPP',
    8: 'JavaScript',
    16: 'Apex',
    32: 'VbNet',
    64: 'VbScript',
    128: 'ASP',
    256: 'VB6',
    512: 'PHP',
    1024: 'Ruby',
    2048: 'Perl',
    4096: 'Objc',
    8192: 'PLSQL',
    16384: 'Python',
    32768: 'Groovy',
    65536: 'Scala',
    131072: 'Go',
    524288: 'Kotlin',
    2097152: 'Cobol',
    4194304: 'RPG',
    8388608: 'Swift',
    16777216: 'Dart',
    33554432: 'Lua',
    1073741824: 'Common'
}

def extract_queries(args):

    resp = get_query_collection()
    if not resp['IsSuccesfull']:
        print(f'Error retrieving queries: {resp["ErrorMessage"]}', file=sys.stderr)
        return

    root = Path(args.output_dir, 'queries')
    for query_group in resp['QueryGroups']:
        if args.no_cx and query_group['PackageType'] == 'Cx':
            continue
        language = language_map[query_group['Language']]
        if query_group['PackageType'] == 'Project':
            dir = Path(root, language, f'Project_{query_group["ProjectId"]}', query_group['Name'])
        elif query_group['PackageType'] == 'Team':
            dir = Path(root, language, f'Team_{query_group["OwningTeam"]}', query_group['Name'])
        else:
            dir = Path(root, language, query_group['PackageType'], query_group['Name'])
        if args.verbose > 0:
            print(f'Creating {dir}')
        dir.mkdir(parents=True, exist_ok=True)

        for query in query_group['Queries']:
            if query['Source']:
                path = Path(dir, query['Name'])
                if args.verbose > 1:
                    print(f'Extracting {query["Name"]} to {path}')
                with path.open('w') as f:
                    f.write(query['Source'])
            elif args.verbose > 1:
                print(f'No source found for {query["Name"]}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extract queries from a CxSAST instance')
    parser.add_argument('-n', '--no-cx', action='store_true',
                        help='Do not extract out-of-the-box queries')
    parser.add_argument('-o', '--output-dir', default='.', metavar='DIR',
                        help='Extract queries to the specified directory')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Verbose output (may be specified multiple times)')
    args = parser.parse_args()
    extract_queries(args)
