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

- Clone [marshmallow repo](https://github.com/marshmallow-code/marshmallow) locally
- Run code-dot with debug logs to get some output when gathering refrences.
- Plug in the range info from the debug output into this static script to confirm
a valid JSON repsonse

```shell
LOCAL_CLONE="<path to local clone>/marshmallow"

python test_lsp.py $LOCAL_CLONE/tests/base.py 86 33
```

Should get a valid JSON response:

```json
[
  {
    "uri": "file:///Users/jarhanco/code/github/marshmallow/tests/base.py",
    "range": {
      "start": {
        "line": 12,
        "character": 35
      },
      "end": {
        "line": 12,
        "character": 50
      }
    }
  },
  {
    "uri": "file:///Users/jarhanco/code/github/marshmallow/tests/base.py",
    "range": {
      "start": {
        "line": 86,
        "character": 18
      },
      "end": {
        "line": 86,
        "character": 33
      }
    }
  },
  {
    "uri": "file:///Users/jarhanco/code/github/marshmallow/tests/base.py",
    "range": {
      "start": {
        "line": 237,
        "character": 18
      },
      "end": {
        "line": 237,
        "character": 33
      }
    }
  }
]
```