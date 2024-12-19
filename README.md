# Pyrlang Elixir Example

## Prerequisites

- a working Python environment (e.g. [virtualenv](https://virtualenv.pypa.io/en/latest/)) is assumed
- install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` vis [rustup](https://rustup.rs/)
    to compile [pyrlang-term](https://github.com/Pyrlang/Term)
- install [Poetry](https://python-poetry.org/docs/#installation)
- install Python dependencies `poetry install`
- install [Elixir](https://elixir-lang.org/install.html)

## Run the Demo

- in one window: `elixir --name erl@127.0.0.1 --cookie COOKIE example.exs`
- in another: `python example.py`
- observe the output in both
