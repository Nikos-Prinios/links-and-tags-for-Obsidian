import os
import re
import json
from collections import defaultdict, Counter
import unicodedata
from keywords import tags
import shutil

# Paths
original_vault_path = "path_of_your_original_vault"
vault_path = "path_for_the_vault_copy"
defs_path = os.path.join(vault_path, 'glossary')
os.makedirs(defs_path, exist_ok=True)

if not os.path.exists(defs_path):
    os.makedirs(defs_path)


def copy_folder_to_desktop(source_path: str):
    desktop_path = "/home/colonel/Bureau/"
    folder_name = os.path.basename(source_path)
    destination_path = os.path.join(desktop_path, folder_name)
    if os.path.exists(destination_path):
        print(shutil.rmtree(destination_path))
    shutil.copytree(source_path, destination_path)

def clean_filename(name):
    """Nettoie les noms des fichiers."""
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = re.sub(r'[<>:"|?*\\/ ]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name.lower()

'''def initialize_glossary_files():
    """Crée un fichier vide pour chaque terme dans le glossaire s'il n'existe pas déjà."""
    for term in tags:
        clean_term = clean_filename(term)
        file_path = os.path.join(defs_path, f"{clean_term}.md")
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {term}\n\nDéfinition à compléter.\n")
'''

def initialize_glossary_files():
    """Crée un fichier vide pour chaque terme dans le glossaire s'il n'existe pas déjà."""
    for term in tags:
        clean_term = clean_filename(term)
        file_path = os.path.join(defs_path, f"{clean_term}.md")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {term}\n\nDéfinition à compléter.\n")


def remove_md_links_tags(content):
    """Supprime les liens et tags Markdown d'un contenu."""
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)
    return content


def link_and_tag_md(content):
    """Crée des liens et vérifie les tags."""
    modified_terms = set()
    for term in tags:
        clean_term = clean_filename(term)
        pattern = re.compile(f"(?<!\\[\\[)\\b{re.escape(term)}\\b(?!\\]\\])", flags=re.IGNORECASE)
        content, count = pattern.subn(f"[[{clean_term}|{term}]]", content)
        if count > 0:
            modified_terms.add(term)
    return content, modified_terms



def process_files(filepath):
    """Traite les fichiers Markdown : suppression et ajout de liens."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = remove_md_links_tags(content)
    content, modified_terms = link_and_tag_md(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return modified_terms


def process_defs(term, links):
    """Crée ou met à jour les fichiers de définition dans le glossaire."""
    clean_term = clean_filename(term)  # Appliquer le nettoyage pour les fichiers de glossaire
    file_path = os.path.join(defs_path, f"{clean_term}.md")
    articles = "\n### Articles :\n" + '\n'.join(f"- [[{link}]]" for link in links)
    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            content = re.sub(r'Articles :[\s\S]*', '', content)
            f.seek(0)
            f.write(f"# {term}\n\n{content.strip()}\n{articles}")
            f.truncate()
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {term}\n\nDéfinition à compléter.\n{articles}")


def clean_tag(tag):
    """Nettoie le tag en remplaçant les espaces par des tirets et en le mettant en minuscules."""
    return tag.replace(' ', '-').lower()
  

def find_tags_in_content(content, tags):
    """Trouve et retourne un ensemble de tous les tags présents dans le contenu."""
    found_tags = set()
    for tag in tags:
        if re.search(fr'\b{re.escape(tag)}\b', content, flags=re.IGNORECASE):
            found_tags.add(clean_tag(tag))
    return found_tags
  

def add_tags_to_file(filepath, tags_set):
    """Ajoute des tags à la fin d'un fichier Markdown."""
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        # Assurez-vous qu'il y a deux sauts de ligne avant les tags, sauf si le fichier est vide
        if tags_set:  # Ajouter des tags seulement s'ils sont présents
            tag_line = '\n\n' + ' '.join(f'#{tag}' for tag in tags_set) if content.strip() else ' '.join(f'#{tag}' for tag in tags_set)
            f.seek(0, os.SEEK_END)  # Se déplacer à la fin du fichier
            f.write(tag_line)
          

def process_files_with_tags(vault_path, tags, excluded_folder="glossary"):
    """Parcourt tous les fichiers Markdown du vault, à l'exception d'un dossier exclu, et ajoute les tags appropriés si des mots clés sont trouvés."""
    for root, dirs, files in os.walk(vault_path):
        if excluded_folder in os.path.split(root)[-1]:  # Exclut le dossier spécifié
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    found_tags = find_tags_in_content(content, tags)
                    if found_tags:
                        add_tags_to_file(filepath, found_tags)


copy_folder_to_desktop(original_vault_path)
initialize_glossary_files()

links_to_terms = defaultdict(set)
for root, dirs, files in os.walk(vault_path):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            modified_terms = process_files(filepath)
            for term in modified_terms:
                links_to_terms[term].add(os.path.splitext(file)[0])

process_files_with_tags(vault_path, tags, "glossaire")
