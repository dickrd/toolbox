BUILD_DIR = out
INSTALL_DIR = ~/bin
DEPENDENCIES = structure

.PHONY: all install uninstall structure clean

all: motd naming

install: motd naming
	cp $(BUILD_DIR)/motd $(INSTALL_DIR)/
	cp $(BUILD_DIR)/naming $(INSTALL_DIR)/

uninstall:
	rm -rf $(INSTALL_DIR)/motd
	rm -rf $(INSTALL_DIR)/naming

structure:
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

motd: src/py/motd.py $(DEPENDENCIES)
	cp $< $(BUILD_DIR)/$@
	chmod +x $(BUILD_DIR)/$@

naming: src/py/naming.py $(DEPENDENCIES)
	cp $< $(BUILD_DIR)/$@
	chmod +x $(BUILD_DIR)/$@
