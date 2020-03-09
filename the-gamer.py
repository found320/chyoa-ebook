#!/usr/bin/env python3
import anytree
import os
import sys
import json
from pprint import pprint
from urllib.parse import unquote

debugChapter = "604266"
roots = {"TheDespaxas-trunk.524999", "The-Gamer,-Chyoa-edition.12004"}
ignore = {"|Ignore-this|.604266"}


def debug_print(message, check):
    if debugChapter in check:
        pprint(message)


def add_to_tree(
    parentNode, choice,
):
    if parentNode != None and choice in roots:
        return
    if choice in ignore:
        return
    with open("./{}.json".format(choice), "r") as data:
        member = json.load(data)
        # print(member['name'])
        debug_print(member, member["file_path"])
        debug_print(choice, member["file_path"])
        print(choice)
    #Found a link that was a child 
    if (
        parentNode == None
        or member["prev_question"].strip() == parentNode.question.strip()
    ):
        # Rename field to avoid collision
        member["title"] = member.pop("name")
        self = anytree.Node(choice, parent=parentNode, **member)
        debug_print("new node added", self.name)
    #Found a link that wasn't a child
    else:
        debug_print(
            "Chapter: {} is not child of {} returning".format(
                member["name"], parentNode.name
            ),
            member["file_path"],
        )
        debug_print(
            "Question '{}' doesn't match '{}'".format(
                member["prev_question"], parentNode.question
            ),
            member["file_path"],
        )
        return None
    #Recurse The child nodes
    if member["choices"]:
        for choice in member["choices"]:
            choice = unquote(choice)
            debug_print("Adding {} to tree".format(choice), member["file_path"])
            if parentNode == None or not anytree.search.find_by_attr(
                parentNode, choice
            ):
                add_to_tree(self, choice)
    #No children let's return
    else:
        debug_print(
            "Chapter: {} leaf".format(member["title"]), member["title"],
        )
        return None
    return self


def main():
    workingDir = sys.argv[1]
    os.chdir(workingDir)
    test = add_to_tree(None, "The-Gamer,-Chyoa-edition.12004")

    with open("../tree.txt", "w") as file:
        for pre, fill, node in anytree.RenderTree(test):
            file.write("%s%s\n" % (pre, unquote(node.name)))

    from anytree.exporter import DotExporter

    DotExporter(test).to_picture("../tree.svg")
    # DotExporter(test).to_picture("../tree.png")


if __name__ == "__main__":
    main()
