critical:
- drawing pi (connected to Arduino/GRBL):
  - [x] recalibrate dimensions
  - [x] remove processing of comments in file
  - [x] detecting errors in GRBL
  - [x] check for other delays, reduce delays by sending batches (5 seems about right)
  - [x] get it successfully running an unmodified gcode file (prob with script stuff before/after)
  - [x] burn multiple files
  - [x] get user-generated images to burn in a relative position (correct location)
  - [x] !!! process user-generated image queueing & burn loop, in threads in parallel with main base-image generation burn loop.
  - [ ] get camera, burn loops, and audio running in separate threads.
  - [x] test file saving in various failure scenarios (power going out / everything cutting at different times)
  - [ ] get script into runnable format, taking in the base image reference that we want to burn in this session.
- image-display pi:
  - [x] write function to stack images
  - [x] write file via scp to drawing Pi
  - [ ] check for presence of drawing Pi file, and send "locked"/"unlocked" to GC
  - [ ] handle serial communication from GC to communicate about button & image state (start, images, reset, submit)
  - [ ] handle display of image to external monitor (and clearing from)
- other:
  - [ ] get code into Github
  - [ ] write/communicate usage instructions
  - [ ] develop backup plans for various things not working (main failure cases)
  - [ ] better logging so Alan can see what's going on

medium:
- [ ] ignition sequence in code -- if not done, will have to manually light before starting up.
- [ ] poofers code -- if not done, will have to poof manually.
- [ ] figure out limit switch integration
- [ ] homing! (in case of power shutoff) -- if not done, will have to manually re-zero before starting up.
- [ ] get all the atax (drawing pi) code onto new, beefier pi& SD card -- if not done, pi might be slower to process everything.

low:
- [ ] refactor ignition function to its own function
- [ ] shortcut to open UGS more easily (add start_ugs to path)
- [ ] keyboard interacitivy (for "admin" to do things or check on/update state)