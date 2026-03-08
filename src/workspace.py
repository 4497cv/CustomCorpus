
import os
import sys

os.chdir("..")
workspace_path = os.getcwd()
key_path = ""
articles_path = ""
texts_path = ""

def set_workspace_path(path, debug = 1):
    global workspace_path
    if(os.path.exists(path)):
        workspace_path = path
        if(debug): print("set new workspace: %s" % path)
    else:
        print(">> ERROR: Path does not exist: %s" % path)
        sys.exit()   

def get_workspace_path() -> str:
    global workspace_path
    return workspace_path

def get_guardian_key_path():
    global key_path, workspace_path
    key_path = os.path.join(workspace_path, "cfg", "guardian_key.txt")
    if(os.path.exists(key_path)):
        return key_path
    else:
        print(">> ERROR: Guardian key was not found in %s" % key_path)
        sys.exit()

def get_articles_path(debug = 0):
    global articles_path, workspace_path
    articles_path = os.path.join(workspace_path, "temp","guardian", "articles")

    if(os.path.exists(articles_path)):
        if(debug): print("Path exists for articles %s" % articles_path)
    else:
        if(debug): print("New path created for articles %s" % articles_path)
        os.makedirs(articles_path, exist_ok=True)

    return articles_path

def get_texts_path(debug = 0):
    global texts_path, workspace_path
    texts_path = os.path.join(workspace_path, "temp","guardian", "texts")

    if(os.path.exists(texts_path)):
        if(debug): print("Path exists for articles %s" % texts_path)
    else:
        if(debug): print("New path created for articles %s" % texts_path)
        os.makedirs(texts_path, exist_ok=True)

    return texts_path