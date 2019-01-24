.PHONY: clean

motd: src/py/motd.py
	cp $< build/$@

naming: src/py/naming.py
	cp $< build/$@

clean:
	rm -rf build
