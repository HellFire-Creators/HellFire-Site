# Overview
**CURRENT STATE**: Literally just me messing around to get familiar with Django, will start work on actual site tommorow  
Framework:  [Django](https://www.djangoproject.com/)  
Venv Manager: [Poetry](https://python-poetry.org/)  
Development/Demo Host: [Render](render.com)  
Production Host: Undecided, maybe [Render](render.com) (see [issue #6](https://github.com/orgs/HellFire-Creators/projects/1/views/1?pane=issue&itemId=47061276))  

# Development Setup
1. Create and clone a branch of the [dev](https://github.com/HellFire-Creators/HellFire-Site/tree/dev) branch for whatever your implementing. Use a descriptive name.
2. Install [pipx](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
3. Install [Poetry](https://python-poetry.org/docs/) with pipx: ```pipx install poetry```
  - Use ```poetry add <package>``` to install packages for the project.
4. Wherever you cloned your branch, run ```poetry shell``` to activate the virtual enviroment
5. You can use ```python manage.py runserver``` to start the server
6. See the [Django Documentation](https://docs.djangoproject.com/en/5.0/) for more

