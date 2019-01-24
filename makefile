BUILD_DIR = out
INSTALL_DIR = ~/bin

.PHONY: all install uninstall clean

all: $(BUILD_DIR)/motd $(BUILD_DIR)/naming

install: $(BUILD_DIR)/motd $(BUILD_DIR)/naming
	cp $(BUILD_DIR)/motd $(INSTALL_DIR)/
	cp $(BUILD_DIR)/naming $(INSTALL_DIR)/

uninstall:
	rm -rf $(INSTALL_DIR)/motd
	rm -rf $(INSTALL_DIR)/naming

clean:
	rm -rf $(BUILD_DIR)

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

$(BUILD_DIR)/motd: src/py/motd.py $(BUILD_DIR)
	cp $< $@
	chmod +x $@

$(BUILD_DIR)/naming: src/py/naming.py $(BUILD_DIR)
	cp $< $@
	chmod +x $@
