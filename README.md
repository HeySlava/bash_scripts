# create_venv.sh

`create_venv.sh` is a simple shell script that creates a Python virtual environment and installs packages from a requirements file.

## Usage

To create a virtual environment and activate it in the current directory, run:

```bash
./create_venv.sh
```


By default, the virtual environment will be created in the `/tmp/_venv` directory. To specify a different path for the virtual environment, pass the path as an argument:

```bash
./create_venv.sh /path/to/venv
```

To install packages from a `requirements.txt` file in the current directory, use the `-r` option:

```bash
./create_venv.sh -r
```

The script will search for a `requirements.txt` file in the current directory and in its parent directories until it reaches the user's home directory. Once a `requirements.txt` file is found, the script will install the packages listed in the file.

To install individual packages, simply pass them as arguments to the script:

```bash
./create_venv.sh -- flask numpy pandas
```

## Limitations

The script assumes that `python3`, `virtualenv`, and `pip` are already installed on the system. If they are not, you will need to install them before running the script.
