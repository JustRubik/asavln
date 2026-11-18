# Run project

- To run project, first you need to move to the root of project.

```Bash
cd <your_project_path>
```

- Create a new virtual environment

```Bash
python -m venv .venv
```

(Only run this command if there is NO `.venv/`)

(I strongly recommend using `.venv`, because I did config it in .gitignore)

- Then activate the environment:

```Bash
# For Linux users
source .venv/bin/activate

# For Windows users
.venv\Scripts\Activate.ps1
```

- Make sure that `pip` is updated to at least `26.3`:

```Bash
pip --version
```

- If not:

```Bash
pip install --upgrade pip
```

- After those, you now can install all needed dependencies:

```Bash
pip install -e .
```

- While at the project's root directory, use this command to run project:

```Bash
python src/main.py
```

- Done! Everything is easy like that! If you want to exit the venv, just run `deactivate`
