import os
from pathlib import Path
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
    1073741824: 'Common'
}

def extract_queries():

    resp = get_query_collection()
    if not resp['IsSuccesfull']:
        print(f'Error retrieving queries: {resp["ErrorMessage"]}', file=sys.stderr)
        return

    root = Path('queries')
    for query_group in resp['QueryGroups']:
        language = language_map[query_group['Language']]
        dir = Path(root, language, query_group['PackageType'], query_group['Name'])
        print(f'Creating {dir}')
        dir.mkdir(parents=True, exist_ok=True)

        for query in query_group['Queries']:
            if query['Source']:
                path = Path(dir, query['Name'])
                print(f'Extracting {query["Name"]} to {path}')
                with path.open('w') as f:
                    f.write(query['Source'])
            else:
                print(f'No source found for {query["Name"]}')


if __name__ == '__main__':

    extract_queries()
