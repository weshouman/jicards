### Docker variables ###
TAG        := gimp_dev

### Current plugin ###
## Use of core as the entry file for the plugin is a convention by this script
## to ease switching between demos, even though that is not always the case
CURR_DEMO := 01
CURR_TEST := 01

# Use EXEC := DEMO_ID.core if the whole demos directory is to be shared
#  that's useful for:
#    1. Plugins that interact with each other
#       in general when we want to have multiple plugins loaded in the container
#    2. Plugins that have a complex structure and core.py is located in a subdir
#  in general don't forget adding the __init__.py next to the core.py
#  in such situations
# EXEC     := ${CURR_DEMO}.core

# Plugins that gets registered through the GUI still has their name clearly stated
#  as they are usually copied next to each other in the plugin directory
# for example use EXEC := image_word_maker.py with CURR_DEMO := 01

EXEC       := core

### In-container directories ###
C_IN_DIR   := /tmp/in
C_PI_DIR   := /root/.gimp-2.8/plug-ins
C_OUT_DIR  := /tmp/out

### Host directories ###
MAIN_DIR   := ${CURDIR}

SCRIPTS_DIR := ${MAIN_DIR}/scripts/

DEMOS_DIR  := ${MAIN_DIR}/demos
DEMO_DIR   := ${DEMOS_DIR}/${CURR_DEMO}

PLUGIN_DIR := ${DEMO_DIR}/src
TESTS_DIR  := ${DEMO_DIR}/tests
INPUT_DIR  := ${TESTS_DIR}/${CURR_TEST}/in
OUTPUT_DIR := ${TESTS_DIR}/${CURR_TEST}/out

build:
	docker build -t $(TAG) . -f Dockerfile

run_gui:
	docker run -it --rm \
	 -e DISPLAY=$${DISPLAY} \
	 -v /tmp/.X11-unix:/tmp/.X11-unix \
	 -v $(INPUT_DIR):$(C_IN_DIR):ro \
	 -v $(PLUGIN_DIR):$(C_PI_DIR) \
	 -v $(OUTPUT_DIR):$(C_OUT_DIR) \
	 $(TAG) \
	 gimp

run_bash:
	docker run -it --rm \
	 -e DISPLAY=$${DISPLAY} \
	 -v /tmp/.X11-unix:/tmp/.X11-unix \
	 -v $(INPUT_DIR):$(C_IN_DIR):ro \
	 -v $(PLUGIN_DIR):$(C_PI_DIR) \
	 -v $(OUTPUT_DIR):$(C_OUT_DIR) \
	 $(TAG) \
	 /bin/bash

run_batch:
	docker run -it --rm \
	 -e DISPLAY=$${DISPLAY} \
	 -v /tmp/.X11-unix:/tmp/.X11-unix \
	 -v $(INPUT_DIR):$(C_IN_DIR):ro \
	 -v $(PLUGIN_DIR):$(C_PI_DIR) \
	 -v $(OUTPUT_DIR):$(C_OUT_DIR) \
	 $(TAG) \
	 gimp -idf \
	  --batch-interpreter python-fu-eval \
	  -b "import sys;sys.path=['.']+sys.path;import $(SCRIPT);$(SCRIPT).run('$(C_IN_DIR)', '$(C_OUT_DIR)')" \
	  -b "pdb.gimp_quit(1)"

# -i == --no-interface [cli]
# -d == --no-data [gradients, pallets or brushes]
# -f == --no-fonts [text support]

backup:
	# rsync a copy of the INPUT_DIR and PLUGIN_DIR

fix_display_not_found:
	# This shall be run only once after each login
	# following this comment https://stackoverflow.com/questions/28392949/running-chromium-inside-docker-gtk-cannot-open-display-0#comment57024354_28395350
	xhost +local:docker

# USAGE:
# make generate_demo DEMO_ID=03 DEMO_NAME="Some name"
generate_demo:
	${SCRIPTS_DIR}/demo_generator.bat ${DEMOS_DIR} ${DEMO_ID} ${DEMO_NAME}