# lsp-test
exercise python LSP statically to debug stuff

## what is this

pretty much just takes some file and range info and returns references like the multilspy library would do. Here's the important part in `test_lsp.py`:

```python
def find_references(server, file_path, line, character):
    """Find references for symbol at given position"""
    # Convert file path to URI format
    uri = uris.from_fs_path(file_path)
    
    # Create position dictionary
    position = {'line': line, 'character': character}
    
    # Find references (include declarations by default)
    return server.references(uri, position, exclude_declaration=False)
```


## Setup

clone this repo, setup venv, install reqs:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Example

Clone [marshmallow repo](https://github.com/marshmallow-code/marshmallow) locally

Run code-dot with debug logs to get some output when gathering refrences.

```console
2025-03-06 15:06:20,940 - DEBUG - code_graph.generator:428 - ref_file: tests/base.py, ref_line: 212, ref_col: 25, ref_end: 29
2025-03-06 15:06:20,942 - WARNING - code_graph.generator:454 - Error verifying call from UserSchema: Unexpected response from Language Server: None
```

Plug in the range info from the debug output into this static script to confirm
a valid JSON repsonse. You just need the file path, line number (`ref_line`), and start character (`ref_col`) for the starting point.

```shell
LOCAL_CLONE="<path to local clone>/marshmallow"

python test_lsp.py $LOCAL_CLONE/tests/base.py 212 25
```

Should get a valid JSON response:

```json
[
  {
    "uri": "file:///Users/jarhanco/code/github/marshmallow/tests/base.py",
    "range": {
      "start": {
        "line": 212,
        "character": 25
      },
      "end": {
        "line": 212,
        "character": 29
      }
    }
  }
]
```