from __future__ import annotations

import argparse
import io
import shutil
import urllib.request
import zipfile
from pathlib import Path

USER_AGENT = "iri2026-build-fetcher"

FORTRAN_SOURCES = [
    "irisub.for",
    "irifun.for",
    "iritec.for",
    "irirtam.for",
    "iridreg.for",
    "igrf.for",
    "cira.for",
    "iriflip.for",
    "rocdrift.for",
]

DATA_FILES = [
    *[f"ccir{month}.asc" for month in range(11, 23)],
    *[f"ursi{month}.asc" for month in range(11, 23)],
    *[f"mcsat{month}.dat" for month in range(11, 23)],
    "dgrf1945.dat",
    "dgrf1950.dat",
    "dgrf1955.dat",
    "dgrf1960.dat",
    "dgrf1965.dat",
    "dgrf1970.dat",
    "dgrf1975.dat",
    "dgrf1980.dat",
    "dgrf1985.dat",
    "dgrf1990.dat",
    "dgrf1995.dat",
    "dgrf2000.dat",
    "dgrf2005.dat",
    "dgrf2010.dat",
    "dgrf2015.dat",
    "dgrf2020.dat",
    "igrf2025.dat",
    "igrf2025s.dat",
    "ibp_emp_coeffs.dat",
    "apf107.dat",
    "ig_rz.dat",
]

IRI2026_ARCHIVE_URLS = [
    "https://irimodel.org/IRI-2026/00_iri.zip",
    "https://irimodel.org/IRI-2026/00_iri2026.zip",
]
COMMON_ARCHIVE_URLS = [
    "https://irimodel.org/COMMON_FILES/00_ccir-ursi.zip",
]
INDEX_FILE_URLS = {
    "apf107.dat": "https://irimodel.org/indices/apf107.dat",
    "ig_rz.dat": "https://irimodel.org/indices/ig_rz.dat",
}


def _download_to_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def _extract_selected_from_zip(
    zip_bytes: bytes,
    destination: Path,
    needed: set[str],
) -> None:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for member in archive.infolist():
            base_name = Path(member.filename).name.lower()

            if not base_name or base_name not in needed:
                continue

            target = destination / base_name
            target.parent.mkdir(parents=True, exist_ok=True)

            with archive.open(member) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)


def _download_first_available_archive(urls: list[str]) -> bytes:
    last_error: Exception | None = None
    for url in urls:
        try:
            return _download_to_bytes(url)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"Could not download archive from any known URL: {urls}") from last_error


def _ensure_files_from_archives(destination: Path, required: set[str]) -> None:
    archive_payload = _download_first_available_archive(IRI2026_ARCHIVE_URLS)
    _extract_selected_from_zip(archive_payload, destination, required)

    missing_after_iri_archive = {name for name in required if not (destination / name).exists()}
    common_candidates = missing_after_iri_archive.intersection(
        {*(f"ccir{m}.asc" for m in range(11, 23)), *(f"ursi{m}.asc" for m in range(11, 23))}
    )
    if common_candidates:
        common_payload = _download_first_available_archive(COMMON_ARCHIVE_URLS)
        _extract_selected_from_zip(common_payload, destination, common_candidates)


def _ensure_index_files(destination: Path, required: set[str]) -> None:
    for name in required.intersection(INDEX_FILE_URLS):
        target = destination / name
        if target.exists():
            continue
        target.write_bytes(_download_to_bytes(INDEX_FILE_URLS[name]))


def _ensure_assets(kind: str, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    required = set(FORTRAN_SOURCES if kind == "fortran" else DATA_FILES)

    _ensure_files_from_archives(outdir, required)
    if kind == "data":
        _ensure_index_files(outdir, required)

    missing = sorted(name for name in required if not (outdir / name).exists())
    if missing:
        raise FileNotFoundError(f"Missing required IRI {kind} files after download: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download required IRI build/runtime assets.")
    parser.add_argument("--kind", choices=["fortran", "data"], required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    _ensure_assets(args.kind, args.outdir)


if __name__ == "__main__":
    main()
