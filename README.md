# Squadro - Phase 2

[<img src="https://www.randolph.ca/wp-content/uploads/2019/01/squadro_400x400_acf_cropped.jpg" style="display: block; margin-left: auto; margin-right: auto;" alt="Squadro" width="50%" height="auto">](https://www.youtube.com/watch?v=FQtM65YI8-o)

## Objectifs

Pour ce deuxième projet, vous aurez à créer une classe pour encapsuler le jeu Squadro. Vous aurez à réutiliser certain segment de code de votre module squadro.py.

## Prérequis

- [Git](https://git-scm.com/downloads/)
- [Python pour macOS](https://www.python.org/downloads/), [Python pour Windows](https://www.microsoft.com/fr-ca/p/python-39/9p7qfqmjrfp7)
- [VS Code](https://code.visualstudio.com/download/)

## Extension VS Code

Voici la liste des extensions **VS Code** que nous vous conseillons d'ajouter à votre configuration:

- Python (celui de Microsoft)
- GitLens $-$ Git supercharged
- Bracket Pair Colorizer 2
- indent-rainbow
- Live Share (*Pour le dépannage en ligne*)
- Live Share Extension Pack (*Pour le dépannage en ligne*)

## Commandes utile

Afficher l'aide:

``` bash
python3 main.py --help
```

Démarrer une partie à 2 joueurs:

``` bash
python3 main.py idul_du_joueur_1 idul_du_joueur_2
```

Démarrer une partie à 1 joueur:

``` bash
python3 main.py votre_idul
```

Lister les parties contre le serveur:

``` bash
python3 main.py idul_du_joueur_1 --parties
```

Lister les parties contre un autre joueur:

``` bash
python3 main.py idul_du_joueur_1 idul_du_joueur_2 --parties
```

Installer un module externe **Python**:

``` bash
pip3 install nom_du_module
```

Créer un bundle depuis un terminal:

``` bash
git bundle create squadro.bundle --all
```

Vérifier que le bundle a été créé avec succès:

``` bash
git bundle verify squadro.bundle
```

Unbundler un bundle:

``` bash
git clone squadro.bundle
```

## Art ASCII

Nous vous fournissons modèle d'affichage ainsi que la liste des caractères.

Assurez-vous d'utiliser **uniquement les caractères exigés** pour générer votre affichage.

```txt
Caractères pour la légendes:
  □ ■

Caractères pour les pions:
  Droite:  □□ ○

  Gauche: ○ □□

  Bas:      █
            ●  
  Haut:     ●
            █

Caractères pour les chemins:
  ┼ ─ |

Caractères pour les points:
  : .

Exemple complet:

Légende:
  □ = jowic42
  ■ = robot

       . | . : | : : | : : | : . | .
         █   . | .   |   . | .   ●     
  ...    ●     |     |     |     █      .
1 ──□□ ○─┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     |     |      .
  .      |     |     |     |     |    ...
2 ───────┼────□□ ○───█─────┼─────┼───────
  .      |     |     ●     |     |    ...
  ..     |     ●     |     |     |     ..
3 ───────┼─────█─────┼─────┼─────┼─○ □□──
  ..     |     |     |     |     |     ..
  .      |     |     |     |     |    ...
4 ───────┼─────┼───○ □□────┼─────┼───────
  .      |     |     |     |     |    ...
  ...    |     |     |     |     |      .
5 ──○ □□─┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     ●     |      .
       . | .   |     |     █   . | .   
       : | : . | . : | : . | . : | :
```

## Représentation de l'état

L'état du jeux est représenté par une liste de 2 dictionnaires:

```python
état = [
    {
        "nom": "jowic42",
        "pions": [0, 2, 6, 9, 12]
    },
    {
        "nom": "robot",
        "pions": [0, 9, 2, 6, 12]
    },
]
```

## Liens utile

- [Aide-mémoire Github Git](https://github.github.com/training-kit/downloads/fr/github-git-cheat-sheet.pdf)
- [Documentation Pytest](https://docs.pytest.org/en/latest/) [en anglais]
- [Vidéo expliquant les règles du jeu Squadro](https://www.youtube.com/watch?v=FQtM65YI8-o) [en anglais]
