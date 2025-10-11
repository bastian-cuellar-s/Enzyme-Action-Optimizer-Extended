# Contributing

Please do not commit generated files (like __pycache__ or *.pyc). Use a virtual environment and add generated files to .gitignore.

To resync after the history rewrite run:

```powershell
git fetch origin
git reset --hard origin/main
git clean -fdx
```
