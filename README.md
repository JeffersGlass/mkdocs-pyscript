# mkdocs-pyscript
`mkdocs-pyscript` is a plugin for [mkdocs](https://mkdocs.org/) that allows you to transform [code blocks](https://www.mkdocs.org/user-guide/writing-your-docs/#fenced-code-blocks) into executable Python scripts that run in the user's browser, with no backend server, using [PyScript](https://github.com/pyscript/pyscript).

## Installation

Install the plugin into your environment using `pip`, or your favorite environment manager that ues PYPI:

```sh
pip3 install mkdocs-pyscript
```

Enable the plugin by adding it to `mkdocs.yaml`:

```
plugins:
    - mkdocs-pyscript
```

## Usage

With this plugin enabled, all Python [fenced code blocks](https://www.mkdocs.org/user-guide/writing-your-docs/#fenced-code-blocks) (type `py` or `python` or any other label that maps to `lang-python`) will have an added LOAD button in the lower-right corrner. When clicked, the code block will be transformed into an editable code snippet (using [codemirror](https://codemirror.net/)). When the user clicks on the green "run" arrow in the lower right corner, or pressed SHIFT+ENTER when focused, will run the inner Python code using PyScript.

The included code is run in a [Web Worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), so as not to block the main thread. Each snippet is run in a separate web worker; variables, objects, and names are not shared between executions of the same cell.

### `pre` and `post` code

Some demo code snippets may require setup and/or teardown code to properly function, which don't necessarily need to be displayed to the user. To run a chunk of Python code before any code the user runs in a particular code editor, add the `.py-pre` class to a fenced code block immediately before the user-visible code block, using the style of the [attr_list](https://python-markdown.github.io/extensions/attr_list/) markdown plugin. To run a chunk of code after a user runs a particular code editor add the `.py-post` class to a fenced code block immediately after the user-visible code block:

````
```{.py .py-pre}
print("This is some pre-code")
```

```py
print("This is the main tag")
# Only this code will be displayed in the code editor
```

```{.py .py-post}
print("This is some post code")
```
````

## Configuration

`mkdocs-pyscript` supports  options that can be set in `mkdocs.yaml` to control the behavior of the plugin

### `pyscript_version`

The `pyscript_version` property of the plugin controls the version of PyScript that is loaded. If not specified, the current default version is `snapshots/2023.09.1.RC2`.


To support both pre-release snapshots and released versions of PyScript, the provided value is inserted into the following string:

```py
SCRIPT = f'https://pyscript.net/{pyscript_version}/core.js'
```

That is, to load a specific release or snapshot, use:
```yaml
#Load a release
plugins:
    - mkdocs-pyscript:
        pyscript_version: "releases/2023.11.1"

#Load a snapshot
plugins:
    - mkdocs-pyscript:
        pyscript_version: "snapshots/2023.11.1.RC3"

#Load the most recent (unstable) build:
plugins:
    - mkdocs-pyscript:
        pyscript_version: "unstable"
```

### `selective`

By default, `mkdocs-pyscript` turns *all* blocks with type `py` or `python` into exectuable code snippets. To cause only selected blocks to be transformed:

  1. Set the `selective` property to `true`:
```yaml
plugins:
    - mkdocs-pyscript:
        selective: true
```
  2. Specify `.pyscript` as an additional class for the codeblocks that you want to be runnable:

````py
```{.py .pyscript}
print("Hello, world!")
```
````