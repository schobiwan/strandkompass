# -*- coding: utf-8 -*-
"""Meereskompass bauen: erzeugt die fertige Website in dist/.

Aufruf: python3 build.py   (vorher einmal npm ci für esbuild, lightningcss und purgecss)

Inhalte stehen in data.py und credits.json, der Seitengenerator im Paket sk/.
"""
import os, shutil
from sk.core import OUT, SPECIES
from sk.assets import build_assets, finalize
from sk.pages.home import build_home
from sk.pages.species import build_arten_index, build_species
from sk.pages.pairs import build_pairs
from sk.pages.year import build_year
from sk.pages.seas import build_seas
from sk.pages.looks import build_looks
from sk.pages.guide import build_guide
from sk.pages.info import build_beach, build_gear, build_legal, build_404, build_about


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    build_assets()
    build_home()
    build_arten_index()
    for s in SPECIES:
        build_species(s)
    build_pairs()
    build_year()
    build_seas()
    build_beach()
    build_gear()
    build_legal()
    build_404()
    build_looks()
    build_guide()
    build_about()
    finalize()
    print("Dateien:", sum(len(fs) for _, _, fs in os.walk(OUT)))


if __name__ == "__main__":
    main()
