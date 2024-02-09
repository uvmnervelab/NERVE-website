#!/usr/bin/env python3

import argparse
import os
import yaml
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

def load_bibtex(file:str, bibfile=False) -> dict:
    '''Parse .bib file to a Python dictionary. Currently
    only supports one BibTeX entry.'''

    # abbreviates a method to convert LaTeX to unicode text
    lt = LatexNodes2Text()

    # returns a bibtexparser.bibdatabase.BibDatabase item
    if bibfile:
        with open(file, 'r') as f:
            db = bibtexparser.load(f)
    else:
        db = bibtexparser.loads(file)

    # returns a list of dictionaries (could support multiple bib entries)
    for entry in db.entries:
        for k, v in entry.items():
            entry[k] = lt.latex_to_text(v)
    
    return entry

def filter_keys(entry: dict):

    # move to YAML eventually
    keys_to_keep = [
        'title',
        'author',
        'year',
        'month',
        'journal',
        'url',
        'volume',
        'number'
    ]

    sub = {}
    for k in keys_to_keep:
        try:
            sub[k] = entry[k]
        except KeyError:
            print(f'No entry for {k}.')

    return sub

def convert_values(entry: dict) -> list:

    if 'author' in entry.keys():
        entry['author'] = entry['author'].split(' and ')
    
    for k in entry:
        try:
            entry[k] = int(entry[k])
        except (TypeError, ValueError):
            continue
    
    return entry

def get_key_abbrev(entry: dict):
    
    try:
        auth1 = entry['author'][0][0:2]
        auth2 = entry['author'][1][0:2]
        year_str = str(entry['year'])[-2:]

        return auth1 + auth2 + year_str
    
    except:
        print("Something went wrong with key abbreviation.")

    
def add_image(entry: dict) -> dict:

    # placeholder, for now
    try:
        key = get_key_abbrev(entry)
        fname = '/assets/images/figures/' + key + '.jpg'
        entry['image_path'] = fname

        return entry
    except:
        print("Something went wrong adding the image.")

def merge_with_papers(entry, file):

    # load papers.yml
    with open(file, "r") as stream:
        try:
            papers = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return
    # add new entry to the top of the papers list
    papers['categories'][0]['pubs'].insert(0, entry)

    # write back to papers.yml
    with open(file, 'w') as f:
        yaml.dump(papers, f, allow_unicode=True, sort_keys=False)

def invoke_url2bib(url: str):
    # url2bib is invoked at the terminal, it seems

    call_str = 'url2bib ' + str(url)
    bib = os.popen(call_str).read()

    return bib



def main():

    parser = argparse.ArgumentParser(description="Convert a BibTeX citation a YAML entry, and insert that entry.")
    parser.add_argument("url", type=str, help="The URL to fetch DOIs from, or filepath to BibTeX entry.")
    parser.add_argument("--papers", required=False, type=str, help="papers.yml file", default='../_data/papers.yml')
    args = parser.parse_args()

    url = args.url
    
    if '.bib' in url:
        print('Loading from .bib')
        entry = load_bibtex(url, bibfile=True)
    else:
        print('Loading from URL')
        bib = invoke_url2bib(url)
        try:
            entry = load_bibtex(bib)
        except UnboundLocalError:
            print("No BibTeX citation found.")
            return 

    sub = filter_keys(entry)
    sub = convert_values(sub)
    sub = add_image(sub)

    print(sub)

    merge_with_papers(sub, args.papers)
    print('Entry added.')



if __name__ == "__main__":
    main()