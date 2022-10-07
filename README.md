# OpenMaya

## Conventions to follow:

- Blender Version 3.3+

- Recommendation: Make the Blender addon folder your local repo
  - Clone the repo to %appdata%/Blender Foundation/Blender/{version number}/scripts/addons/OpenMaya

- Use black formatter (I have it format on save)
  - <a href="https://packagecontrol.io/packages/python-black">Sublime Text</a>
  - <a href="https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0">VS Code</a>

- Updating after modification
  - The best way to update the addon after an edit is to restart blender with the addon disabled and then enable it again afterwards.
  - This obviously sucks, so 99% of the time, use the <a href="https://blender-addons.org/reboot-addon/">re:Boot</a> addon.
    - I made an <a href="https://github.com/himham-jak/re-Boot-with-Keymap/releases">edit</a> to this that maps it to Ctrl+F8.
  - The least effective update method is to use F3 > Reload Scripts, which kinda does nothing useful.

- Naming Conventions
  - Variables/functions in snake_case
  - Classes in PascalCase(self)
  - Class methods cls_<method_name>(cls)
  - Double quotes for top level, single inside

- Document Structure
  - """Info Docstring"""
  - Imports
  - Classes
  - Functions
  - Registration
  
- Logic Principles
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

- Config Save
  - Not having to reselect your Open Goal folder
- Menu Items
  - PropertyGroup
- Live Input Validation
  - using re
- Actor Type Data Class
  - Automate Actor Add Button Creation
    - use json
- Import World Reference
- Export Functionality
  - Data Structure
  - Geometry Export
  - f strings
- Error Messages
  - popups
- Actor Info
  - Custom Properties
- Actor Meshes
  - Import?
  - Creation
