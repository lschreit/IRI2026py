IRI:
	meson setup builddir --prefix=/
	meson compile -C builddir
	cp -R src/python ../

clean:
	rm -r ../python || echo "Nothing to remove in ../python"
	meson clean -C builddir || echo "Nothing to clean in builddir"
	rm src/python/iri/iri2026.so || echo "Nothing to remove iri2026.so"
