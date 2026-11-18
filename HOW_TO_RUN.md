# Run project

- To run project, first you need to move to the root of project.

`cd <your_project_path>`

- Create a new virtual environment

`python -m venv .venv`

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

`pip --version`

- If not:

`pip install --upgrade pip`

- After those, you now can install all needed dependencies:

`pip install -e .`

- While at the project's root directory, use this command to run project:

`python src/main.py`

- Done! Everything is easy like that! If you want to exit the venv, just run `deactivate`
