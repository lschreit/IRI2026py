# IRI2026 Python Package

This package provides Python bindings for the IRI2026 ionospheric model, built from Fortran sources.

## Source and data files

The package does not keeps IRI Fortran sources (`*.for`) and runtime data (`ccir*.asc`, `ursi*.asc`, `mcsat*.dat`, `dgrf*.dat`, `igrf*.dat`, `apf107.dat`, `ig_rz.dat`, etc.) in the git repository.

During `pip install .`, the build downloads the required files from `https://irimodel.org/IRI-2026/`, compiles the extension with the downloaded Fortran files, and installs the runtime data into the package. IRI license is to be respected.

## Build and Install

From the root directory, run:

```sh
pip install .
```

This will:
- Download required IRI Fortran + runtime data files
- Build the Fortran extension from the downloaded sources
- Install the Python package and runtime data files

## Runtime behavior

```python
import iri2026
```
