# OpenMaya

## Installation:

- If you're using a release, just download the `.zip` file, don't extract it
- To make your own release, put all of the contents of this repo into a folder, then put that folder in a `.zip`
- There must be a subfolder in the `.zip` or it won't work
- In Blender, choose `Edit > Preferences… > Add-ons > Install…` and select the `.zip`

## Tutorial:

- To do

## Features:

- To do

## Conventions to follow while contributing:

- Blender Version 3.3+

- Recommendation: Make the Blender addon folder your local repo
  - Clone the repo to %appdata%/Blender Foundation/Blender/{version number}/scripts/addons/OpenMaya

- Use black formatter (I have it format on save)
  - <a href="https://packagecontrol.io/packages/python-black">Sublime Text</a>
  - <a href="https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0">VS Code</a>

- Updating after modification
  - The best way to update the addon after an edit is to restart blender with the addon disabled and then enable it again afterwards.
  - This obviously sucks, so 99% of the time, use the <a href="https://blender-addons.org/reboot-addon/">re:Boot</a> addon
    - I made an <a href="https://github.com/himham-jak/re-Boot-with-Keymap/releases">edit</a> to this that maps it to `Ctrl+F8`
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
  - Classes
  - Functions
  - Registration
  
- Logic Principles (these are mostly here for my benefit) 
  - Single-responsibility
    - Methods of a class should be alternatives to each other, not sequential steps
  - Open-closed
    - Abstract classes should be extended by subclasses, not modified to add code
  - Liskov substitution
    - Subclasses should be able to be substituted for their parents, any extra input should be handled by the initializer
  - Interface segregation
    - Use an intermediate subclass to integrate functionality for two different types of subclasses
    - Use composition
  - Dependency inversion
    - Classes should only depend on abstract classes

## To Do:

- level_menu.py
  - Config Save
    - Working directory: custom_levels folder
  - Error Messages
    - Popups
- actor_types.json
  - Actor Type Data Class
    - Automate Actor Add Button Creation
      - Use json module
- map_reference.py
  - One operator, called from level_menu: Import World Reference
- export.py
  - Export Functionality
    - Data Structure
    - Geometry Export
    - f strings
    - .bak backups
- actor_menu.py
  - Custom Properties
  - Display in a PropertyGroup
- mesh.glb
  - Actor Meshes
    - Try new model exporter
    - Import from OG export out folder
