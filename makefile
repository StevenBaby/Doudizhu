
.PHONY: main
main: ui
	python src/main.py

src/ui/%.py: src/ui/%.ui
	PySide6-uic $< -o $@

UI+= src/ui/monitor.py

.PHONY:ui
ui: $(UI)

.PHONY: clean
clean:
	rm -rf $(UI)
