# Test task for SmartTIME project

![Lint & test](https://github.com/SynKolbasyn/smart_time_test/actions/workflows/ci.yml/badge.svg)

## Deploy guide

1. First of all you need OS such as [windows](https://microsoft.com/windows) or linux distribution (for example [ubuntu](https://ubuntu.com/)).
2. Second step is install dependencies: [git](https://git-scm.com/) & [uv](https://github.com/astral-sh/uv)

    Optrional, if you haven't got python, you may install it using ```uv```:
    ```bash
    uv python install
    ```

3. Clone this repo:
    ```bash
    git clone https://github.com/SynKolbasyn/smart_time_test.git
    ```

4. Change the working directory:
    ```bash
    cd smart_time_test
    ```

5. Configure server: copy ```template.env``` to ```.env``` and set the correct values for variables in this file:
    <details>
    <summary>For linux</summary>

    ```bash
    cp template.env .env
    ```
    </details>

    <details>
    <summary>For windows</summary>

    ```bash
    copy template.env .env
    ```
    </details>

    ---
    
    * If you want to run server in production mode, set ```DJANGO_DEBUG``` variable to ```False```, otherwise to ```True```.
    * Don't forgot to set ```DJANGO_SECRET_KEY```, this is very important for production mode.
    * Select database name by setting the ```DJANGO_DB``` variable

6. Run the server by using the following command (you may optionaly specify the host and port, or just only port):
    ```bash
    uv run --no-dev smart_time_test/manage.py runserver <host:port>
    ```

---

## Testing
* Linter:
    ```bash
    uv run flake8 --toml-config pyproject.toml --verbose smart_time_test
    ```

* Formatter:
    ```bash
    uv run black --check --diff --verbose smart_time_test
    ```

* Tests:
    ```bash
    cd smart_time_test
    uv run manage.py test
    ```
