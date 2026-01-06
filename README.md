# Adoc Link Checker (adocx)

Adoc Link Checker est un outil en ligne de commande permettant de détecter automatiquement les liens HTTP et HTTPS brisés dans des fichiers AsciiDoc (.adoc).

Il est conçu pour être :

* fiable (requête HEAD avec fallback GET),
* rapide (traitement parallèle),
* explicite (rapport JSON, aucune sortie implicite),
* facilement intégrable en CI/CD.

---

## Fonctionnalités

* Vérification des liens HTTP et HTTPS
* Support des IDs YouTube (video::ID[])
* Traitement parallèle configurable
* Exclusion de liens ou de domaines
* Rapport JSON structuré
* Analyse d’un fichier ou d’un dossier
* Cache des résultats pour éviter les requêtes redondantes

---

## Installation

### Prérequis

* Python 3.8 ou supérieur
* pip

### Installation depuis PyPI

pip install adoc-link-checker

La commande suivante devient disponible :

adocx

---

## Utilisation rapide

### Vérifier un fichier AsciiDoc

adocx check-links README.adoc --output report.json

### Vérifier un dossier

adocx check-links ./docs --output report.json

---

## Options principales

| Option         | Description                         | Défaut      |
| -------------- | ----------------------------------- | ----------- |
| FILE_OR_DIR    | Fichier .adoc ou dossier à analyser | obligatoire |
| --output       | Fichier JSON de sortie              | obligatoire |
| --timeout      | Timeout HTTP en secondes            | 15          |
| --max-workers  | Nombre de threads                   | 5           |
| --delay        | Délai entre requêtes en secondes    | 0.5         |
| --blacklist    | Domaine à ignorer, répétable        | aucun       |
| --exclude-from | Fichier de liens à exclure          | aucun       |
| -v ou -vv      | Verbosité INFO ou DEBUG             | aucun       |
| --quiet        | Logs erreurs uniquement             | désactivé   |

---

## Fichier d’exclusion

Un fichier d’exclusion permet d’ignorer certaines URLs.

Exemple de contenu :

# Commentaires autorisés

[https://example.com/temp](https://example.com/temp)
[https://dev.example.com](https://dev.example.com)

Utilisation :

adocx check-links ./docs --exclude-from exclude_urls.txt --output report.json

---

## Format du rapport JSON

Le rapport contient uniquement les fichiers ayant des liens cassés.

Exemple :

{
"docs/page.adoc": [
["[https://example.com/broken](https://example.com/broken)", "URL not accessible"]
]
}

---

## Comportement HTTP

* Requête HEAD prioritaire
* Fallback automatique vers GET
* Redirections suivies
* User-Agent réaliste
* Retries automatiques sur erreurs serveur

---

## Utilisation en CI

Exemple avec GitHub Actions :

* name: Check AsciiDoc links
  run: adocx check-links ./docs --output broken_links.json

Le code retour est toujours 0 même si des liens sont cassés.
Une option fail-on-broken est prévue.

---

## Développement

Installation en mode editable :

git clone [https://github.com/ton-org/adoc-link-checker.git](https://github.com/ton-org/adoc-link-checker.git)
cd adoc-link-checker
pip install -e .[dev]

Lancer les tests :

pytest

---

## Licence

Ce projet est sous licence MIT.
Voir le fichier LICENSE à la racine du dépôt.

---

## Commande CLI

Note : la commande CLI fournie par ce projet est adocx.
