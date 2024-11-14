import pytest
import sys
import unittest
import os
import zipfile
from main import GitVisualizer

def test_m():
    assert 1 == 1

def test_project_1():
    date = '2024-11-29'
    visualizer = GitVisualizer('.venv/project_1', date)
    uml = """@startuml
"commit 98b4339" --> "commit 79f2b6a"
151d8d4 : tree
"commit 79f2b6a" --> 151d8d4
"commit bcaf80a" --> "commit 98b4339"
7d74734 : tree
"commit 98b4339" --> 7d74734
2171fdd : tree
"commit bcaf80a" --> 2171fdd
50c27e7 : blob
"151d8d4" -> 50c27e7 : .DS_Store
0c1f553 : blob
"151d8d4" -> 0c1f553 : .editorconfig
aac13e3 : blob
"151d8d4" -> aac13e3 : Dockerfile
425985e : blob
"151d8d4" -> 425985e : blocks
119a650 : blob
"151d8d4" -> 119a650 : images
eb5b4e5 : blob
"151d8d4" -> eb5b4e5 : index.html
8b57327 : blob
"151d8d4" -> 8b57327 : nginx.conf
2ce8c03 : blob
"151d8d4" -> 2ce8c03 : pages
6b4b269 : blob
"151d8d4" -> 6b4b269 : readme.md
e2cb621 : blob
"151d8d4" -> e2cb621 : texts
2074ed3 : blob
"151d8d4" -> 2074ed3 : vendor
"7d74734" -> 50c27e7 : .DS_Store
"7d74734" -> 0c1f553 : .editorconfig
"7d74734" -> aac13e3 : Dockerfile
"7d74734" -> 425985e : blocks
"7d74734" -> 119a650 : images
"7d74734" -> eb5b4e5 : index.html
"7d74734" -> 8b57327 : nginx.conf
"7d74734" -> 2ce8c03 : pages
"7d74734" -> e2cb621 : texts
"7d74734" -> 2074ed3 : vendor
"2171fdd" -> 50c27e7 : .DS_Store
"2171fdd" -> 0c1f553 : .editorconfig
"2171fdd" -> aac13e3 : Dockerfile
103b1b8 : blob
"2171fdd" -> 103b1b8 : images
201a44b : blob
"2171fdd" -> 201a44b : index.html
8a4575e : blob
"2171fdd" -> 8a4575e : nginx.conf
92e230a : blob
"2171fdd" -> 92e230a : styles
3ae5a6c : blob
"2171fdd" -> 3ae5a6c : texts.md
@enduml"""
    assert (visualizer.visualize() == uml)

def test_project_2():
    date = '2024-11-29'
    visualizer = GitVisualizer('.venv/project_2', date)
    uml = """@startuml
"commit 8df3c47" --> "commit 5e4b4be"
"commit 8047782" --> "commit 5e4b4be"
f15e30f : tree
"commit 5e4b4be" --> f15e30f
"commit d83beca" --> "commit 8df3c47"
2fab559 : tree
"commit 8df3c47" --> 2fab559
"commit 0dd1eca" --> "commit d83beca"
930569b : tree
"commit d83beca" --> 930569b
"commit f659454" --> "commit 0dd1eca"
b8ac865 : tree
"commit 0dd1eca" --> b8ac865
"commit ff91d00" --> "commit f659454"
dd3ac18 : tree
"commit f659454" --> dd3ac18
d5bef33 : tree
"commit ff91d00" --> d5bef33
"commit 2ea358f" --> "commit 8047782"
e1870c0 : tree
"commit 8047782" --> e1870c0
"commit 0dd1eca" --> "commit 2ea358f"
9bddeca : tree
"commit 2ea358f" --> 9bddeca
c6cac69 : blob
"f15e30f" -> c6cac69 : empty.txt
e69de29 : blob
"f15e30f" -> e69de29 : hello.c
83f0351 : blob
"f15e30f" -> 83f0351 : hello.py
954cab5 : blob
"f15e30f" -> 954cab5 : index.html
ac37036 : blob
"f15e30f" -> ac37036 : info.txt
"f15e30f" -> e69de29 : myfile.txt
9848698 : blob
"f15e30f" -> 9848698 : readme.md
"2fab559" -> e69de29 : empty.txt
"2fab559" -> e69de29 : hello.c
f2db9da : blob
"2fab559" -> f2db9da : hello.py
"2fab559" -> 954cab5 : index.html
"2fab559" -> ac37036 : info.txt
"2fab559" -> 9848698 : readme.md
"930569b" -> f2db9da : hello.py
"930569b" -> 954cab5 : index.html
"930569b" -> ac37036 : info.txt
"930569b" -> 9848698 : readme.md
"b8ac865" -> f2db9da : hello.py
"b8ac865" -> 954cab5 : index.html
"b8ac865" -> ac37036 : info.txt
b917a72 : blob
"dd3ac18" -> b917a72 : hello.py
"dd3ac18" -> 954cab5 : index.html
"dd3ac18" -> ac37036 : info.txt
"d5bef33" -> b917a72 : hello.py
6b820fd : blob
"d5bef33" -> 6b820fd : info.txt
"e1870c0" -> c6cac69 : empty.txt
"e1870c0" -> 83f0351 : hello.py
"e1870c0" -> 954cab5 : index.html
"e1870c0" -> ac37036 : info.txt
"e1870c0" -> e69de29 : myfile.txt
"9bddeca" -> 83f0351 : hello.py
"9bddeca" -> 954cab5 : index.html
"9bddeca" -> ac37036 : info.txt
"9bddeca" -> e69de29 : myfile.txt
@enduml"""
    assert (visualizer.visualize() == uml)

def test_project_2_data():
    date = '2023-11-29'
    visualizer = GitVisualizer('.venv/project_2',date)
    uml = """@startuml
@enduml"""
    assert (visualizer.visualize() == uml)

def test_project_3():
    date = '2024-12-31'
    visualizer = GitVisualizer('.venv/project_3', date)
    uml = """@startuml
"commit dd465ed" --> "commit f5928bd"
4e14287 : tree
"commit f5928bd" --> 4e14287
"commit e96c9c2" --> "commit dd465ed"
c641a60 : tree
"commit dd465ed" --> c641a60
2d7f016 : tree
"commit e96c9c2" --> 2d7f016
ca028fb : blob
"4e14287" -> ca028fb : 1.txt
e69de29 : blob
"4e14287" -> e69de29 : one.txt
"4e14287" -> e69de29 : two.txt
"c641a60" -> e69de29 : one.txt
"c641a60" -> e69de29 : two.txt
"2d7f016" -> e69de29 : one.txt
@enduml"""
    assert (visualizer.visualize() == uml)