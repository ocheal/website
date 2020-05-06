Source code to generate static files for ocheal.github.io

Internally uses flask to host a dynamic webserver, and Frozen-Flask to build static files which can be hosted on github pages

```sh
# nav to /website/
cd website/

# Run the flask web server at localhost:5000
python __init__.py

# Host a web server from frozen files
python __init__.py --frozen

# Build the static files without hosting
python __init__.py --build 
```