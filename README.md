# OpenMaya

## Conventions to follow:

- Blender Version 3.3+

- Make the Blender addon folder your local repo
  - Clone the online repo to %appdata%/Blender Foundation/Blender/{version number}/scripts/addons/OpenMaya

- Use black formatter
  - <a href="https://packagecontrol.io/packages/python-black">Sublime Text</a>
  - <a href="https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0">VS Code</a>

- Updating after modification
  - The best way to update the addon after an edit is to restart blender with the addon disabled and then enable it again afterwards.
  - This obviously sucks, so 99% of the time, use the <a href="https://blender-addons.org/reboot-addon/">re:Boot</a> addon.
    - I'm going to make an edit to this that maps it to F8.
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
