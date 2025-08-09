## Bugs 
- [X] shift + h is not working
- [X] It seems I cannot go back to monochrome
- [X] Fix or remove useless tests
- [X] Fix the cell size => Should also resize the grid
- [X] Distorsion improvement : Fix the lens distortion 
- [ ] Full screen buggy, grid not big enough and loading scenes does not work well
- [ ] Distorsion improvement :Fix the kaleidoscope twist => It's not working well in full screen
- [ ] Shapes improvements : Koch snowflake => Looks awsome but very laggy
- [ ] Colors improvements : Aurora borealis could maybe be improved, more red

## Short term roadmap

- [X] Global README to explain the project 
- [X] Write a few tests
- [X] Write a task file to run tests and to run the demos
- [X] Additional shape types (circles, triangles)
- [X] Open the command guide with a key
- [X] GIF/MP4 export
- [X] Add new distortion types (swirl, ripple, flow)
- [X] Add options to play with the cell size
- [X] Add the name of the distortion, the intensity, and the number of cells on the screen
- [X] Add an option to export the parameters of the current scene (just export the params.json file) and find a way to load it automatically when the app is launched. Maybe reuse the save image feature, and save a json file with the parameters. Maybe add an option to iterate through all saved scenes
- [X] Get rid of the audio features, it's not working well
- [X] Clean up useless stuff in TODO.md

- [X] Add a keyboard shortcut to do previous distorsion/shape/color scheme
- [X] The menu is too big, on one column, maybe 2 columns now ? 
- [X] Clean up useless stuff in README.md (audio etc...)

- Add in README: 
  - [X] the new distorsions (from pulse, pulse not included)
  - [X] the new shapes (from koch snowflake)
  - [X] the new colors (from analogous)
  - [X] the size guide (and mention it in the number of combinations possible)
  - [X] the new indicators screen
  - [X] the saved/load scenes feature
  - [X] the previous/next scene feature
  - [X] how a distorsion function works, what parameters and what it basically does (compute next position and rotations based on ...)

- [X] Find cool combinations to showcase and save them
- [ ] Youtube video + Update README.md with the video link

- [ ] Refactor the shapes, colors, and distorsions to be more modular and easier to add new ones. (one file for each type of distorsion, one file for each shape, one file for each color scheme)
- [ ] Add a guide in the README.md to explain how to add new shapes, colors, and distorsions + update the modules explanations
- [ ] Prepare LinkedIn post to share the repo and the video

- [ ] Save as mp4 feature

- [ ] Add new shape types
- [ ] Add new color schemes (inspire from pastel color in archive)
- [ ] Add new distortion types (take a look at the new_distortions_again.md file for more ideas)

## Mid term roadmap

- [ ] Host on web ? pygbag https://github.com/pygame-web/pygbag
  - in a pull request, not working well
  - maybe need to migrate to webgl and use f*ckin' js ?
- [ ] Mouse interaction (attraction/repulsion)
  - in a pull request, not working well
- [ ] Audio reactive features
  - in a pull request, need to be redone from scratch
- [ ] Motion blur effects
- [ ] Preset scene system
- [ ] Particle systems