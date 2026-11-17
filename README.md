# ASAVLN

Application of SLAM in Automonous Vehicle Localization and Navigation

## About

This project is presenting an application of SLAM algorithm in real-time locating and navigating automobile.

## Members

- Đặng Huy Hiếu (*)   -   20223771
- Lê Anh Vương        -   20224212
- Lê Mạnh Quốc Trung  -   20224175
- Lê Thị Hằng         -   20223955

## Run project

- To run project, first you need to move to the root of project.

`cd <your_project_path>`

- Create a new virtual environment

`python -m venv .venv`

(Only run this command if there is no `.venv/`)
(I strongly recommend using `.venv`, because I did config it in .gitignore)

- Then activate the environment:

```Bash
# For Linux users
source .venv/bin/activate

# For Windows users
.venv\Scripts\Activate.ps1
```

- After those, you now can install all needed dependencies:

`pip install -e .`

- While at the project's root directory, use this command to run project:

`python src/main.py`

- Done! Everything is easy like that! If you want to exit the venv, just run `deactivate`


## License
Copyright (c) 2026 JustRubik.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See [LICENSE](LICENSE) for the full text.
