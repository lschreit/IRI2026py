project('iri2026', 'fortran')

py_mod = import('python').find_installation()

fortran_sources = [
  'irisub.for',
  'irifun.for',
  'iritec.for',
  'irirtam.for',
  'iridreg.for',
  'igrf.for',
  'cira.for',
  'iriflip.for',
  'rocdrift.for',
]

runtime_data_files = [
  'ccir11.asc', 'ccir12.asc', 'ccir13.asc', 'ccir14.asc', 'ccir15.asc', 'ccir16.asc',
  'ccir17.asc', 'ccir18.asc', 'ccir19.asc', 'ccir20.asc', 'ccir21.asc', 'ccir22.asc',
  'ursi11.asc', 'ursi12.asc', 'ursi13.asc', 'ursi14.asc', 'ursi15.asc', 'ursi16.asc',
  'ursi17.asc', 'ursi18.asc', 'ursi19.asc', 'ursi20.asc', 'ursi21.asc', 'ursi22.asc',
  'mcsat11.dat', 'mcsat12.dat', 'mcsat13.dat', 'mcsat14.dat', 'mcsat15.dat', 'mcsat16.dat',
  'mcsat17.dat', 'mcsat18.dat', 'mcsat19.dat', 'mcsat20.dat', 'mcsat21.dat', 'mcsat22.dat',
  'dgrf1945.dat', 'dgrf1950.dat', 'dgrf1955.dat', 'dgrf1960.dat', 'dgrf1965.dat', 'dgrf1970.dat',
  'dgrf1975.dat', 'dgrf1980.dat', 'dgrf1985.dat', 'dgrf1990.dat', 'dgrf1995.dat', 'dgrf2000.dat',
  'dgrf2005.dat', 'dgrf2010.dat', 'dgrf2015.dat', 'dgrf2020.dat',
  'igrf2025.dat', 'igrf2025s.dat',
  'ibp_emp_coeffs.dat',
  'apf107.dat', 'ig_rz.dat',
]

fetch_fortran_sources = custom_target(
  'fetch-iri-fortran-sources',
  output: fortran_sources,
  command: [
    py_mod,
    files('tools/fetch_iri_assets.py'),
    '--kind', 'fortran',
    '--outdir', '@OUTDIR@',
  ],
  install: false
)

python_package_dir = py_mod.get_install_dir() / 'iri2026'

custom_target(
  'fetch-iri-runtime-data',
  output: runtime_data_files,
  command: [
    py_mod,
    files('tools/fetch_iri_assets.py'),
    '--kind', 'data',
    '--outdir', '@OUTDIR@',
  ],
  install: true,
  install_dir: python_package_dir
)

# Step 1: Build with f2py (generates .so with unpredictable ABI tag)
f2py_build = custom_target(
  'build-iri2026-f2py',
  input: [files('src/iri2026/iri26_minimal.pyf'), fetch_fortran_sources],
  output: ['f2py_build_stamp'], # dummy file to indicate build finished
  command: [
    py_mod, '-m', 'numpy.f2py',
    '-c', '@INPUT@', '-m', 'iri2026'
  ],
  install: false
)

find_so_script = '''
import glob, shutil, sys, os
sofiles = glob.glob("iri2026*.so")
if not sofiles:
    print("No .so files found in", os.getcwd())
    sys.exit(1)
shutil.copyfile(sofiles[0], "iri2026.so")
'''

# Step 2: Rename .so to fixed name and install in site-packages/iri2026
so_rename = custom_target(
  'fix-iri2026-so',
  input: f2py_build,
  output: ['iri2026.so'],
  command: [py_mod, '-c', find_so_script],
  install: true,
  install_dir: python_package_dir
)

# Step 3: Install Python wrapper.

install_data(
  ['python/iri2026/__init__.py'],
  install_dir: python_package_dir
)

