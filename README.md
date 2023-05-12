# OpenMaya

Design the Jak level of your dreams with OpenMaya, the open-source (and code-free) level builder for Blender.

## Table of Contents

- :electric_plug:[Compatibility](#compatibility)
- :scroll:[Installation](#installation)
- :nut_and_bolt:[Tutorial](#tutorial)
- :clipboard:[Features](#features)
- :dollar:[Support](#support)
  - <a href="https://ko-fi.com/himhamrex">Ko-fi</a>
- :paperclip:[ Related](#related)
  - Links
- :black_nib:[Contributing](#contributing)
- :calendar:[Upcoming](#upcoming)

## Compatibility:

- <a href="https://download.blender.org/release/">Blender</a> 3.3+ minimum system requirements
  - Previous versions may work but will not be actively supported.
- <a href="https://opengoal.dev/">OpenGOAL</a> minimum system requirements

## Installation:

- If you're using a release, just download the `.zip` file, don't extract it
- To make your own release, put all of the contents of this repo into a folder, then put that folder in a `.zip`
- There must be a subfolder in the `.zip` or it won't work
- In Blender, choose `Edit > Preferences… > Add-ons > Install…` and select the `.zip`
- In the same window, you should be able to update at any time. This will pull the most recent release from github.
- Automatic updates may be finnicky for now, but manual ones are very easy.

## Tutorial:




- Creating a custom Jak level with OpenMaya
  - Ensure OpenMaya is updated before you begin.
  - Model your level's geometry with Blender.
  - Use the `n` toolbar tabs associated with OpenMaya to customize your level.
    - For now, enter your level's information. All fields validate data, so they'll let you know if you made a mistake.
  - Use the `Shift + A` menu to add actors to your scene.
    - Return to the toolbar to edit the data of the currently selected actor as needed.
  - When you'd like to test your level, hit export on the toolbar.
- Loading your custom level

## Features:

- Manual and/or automatic updater built into Blender's interface
- Add and position OpenGOAL actors in 3D space
- Modify custom properties within individual actors
  - Documentation
- Update files en masse or individually with precise exporting
  - Level Info
  - Actor Info
  - Level Geometry

## Support:

Thank you for checking out this open source software!
I pour a lot of time, effort, and love into creating and maintaining it.
Developing and improving software like this is not only my passion but also my way of contributing to the open source community.
If you find my software useful and would like to support my work, <a href="https://ko-fi.com/himhamrex">consider making a donation through Ko-fi</a>.
Your contribution can help me cover the costs of maintaining and improving this software.
I appreciate any amount you can give, no matter how small.
Your support will help me continue to develop high-quality software that is free and accessible to everyone.
Thank you for your consideration and for being a part of the open source community!

## Related:

- YouTube
- Sound Tool
- OpenGOAL website
- Mod Launcher

## Contributing:

- Tools
  - <a href="https://download.blender.org/release/">Blender</a> 3.3+
  - Text editor for Python/C/C++
    - Recommended: Black Formatter
      - <a href="https://packagecontrol.io/packages/python-black">Black Formatter</a> for Sublime Text
      - <a href="https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0">Black Formatter</a> for VS Code
  - <a href="https://opengoal.dev/">OpenGOAL</a>
  - Github (duh)
    - Recommended: Make the Blender addon folder your local repo
      - Clone the repo to `%appdata%/Blender Foundation/Blender/{version number}/scripts/addons/OpenMaya`
      - This way, all changes to the project can be immediately loaded into Blender

- Updating after modification
  - The best way to update the addon after an edit is to restart blender with the addon disabled and then enable it again afterwards.
  - This obviously sucks, so 99% of the time, use the <a href="https://blender-addons.org/reboot-addon/">re:Boot</a> addon
    - I made an <a href="https://github.com/himham-jak/re-Boot-with-Keymap/releases">edit</a> to this that maps it to `Ctrl+F8` and improves a few things.
  - The least effective update method is to use `F3 > Reload Scripts`, which kinda does nothing useful

- Naming Conventions
  - Variables/functions in snake_case
  - Constants in UPPER_SNAKE
  - Classes inherited from Blender types should follow their naming conventions
  - Custom classes in PascalCase
  - Class methods use `cls` in place of `self`
  - Double quotes for top level, single if nested

- Document Structure
  - """Info Docstring"""
  - Imports
    - Third Party
    - Built-ins
    - Custom Modules
  - Constants
  - Classes
  - Functions
  - Registration

## Upcoming:

- level_menu.py
  - Config Save
    - Working directory: custom_levels folder
    - Collapse Add actor menu?
    - Add actors at top or bottom of add menu?
    - Gizmo visibility
    - Choose between toolbar
      - and <a href="https://blender.stackexchange.com/questions/214228/how-do-i-add-a-new-panel-to-the-properties-editor">properties area</a> for OpenMaya
  - Error Messages
    - Popups
- saved_actors.json
    - a user created file of preset actors with all associated custom properties
    - automatically added to the "saved" subfolder of the "add actor" menu
- save_actor.py
    - writes the above file from an operator in the actor menu when user requests
- map_reference.py
  - One operator, called from level_menu: Import World Reference
- add_actors.py
  - Import meshes from OG export out folder (might require rewriting extractor)
  - Remove from Scene Collection after creation
- Dev options
  - Create json structure from actor
    - Can just add new custom properties to a new actor, export that, then add to actor_types.json
  - Playtest
    - Use the pre-made bash scripts
  - Move add actors to bottom of add list
- Experimental options
  - Toggle in Preferences
  - Turns on potentially error producing features
- Debug mode
- Verbose Output

## Eventually:

- <a href="https://github.com/CGCookie/blender-addon-updater">Auto Updates</a>
- <a href="https://devtalk.blender.org/t/gizmogroup-gizmo-gt-button-2d-not-working-on-autoload/6791">2D Overlays</a>
  - Show contents of crates
  - Show type of eco on top of vents etc
- actor_types.json
  - Add more actors
    - Bodies of water
    - Nav-mesh
    - Swing poles
    - Spider webs
    - Platforms
    - Particles
  - Add more custom properties
    - light-index?
    - buzzers: movie-pos: where put cell
  - Multiselect actors and change all their properties at once

- export.py
  - Export Functionality
    - Upgrade to writing the level and actor info into the .glb itself
  - Bezier curves for paths

- Missions
  - Fish
  - Rats
  - Rings
  - Mountain Pass Race (Countdown)
  - Basin Race (Beat record)
  - Mirrors
  - Break object
  - Kill enemy
  - Step on switch
  - Hit switch
  - Collect xyz
  - Cells
  - Cutscene
  
  
- Automatically run macro on export
  - jak-project/scripts/shell/
