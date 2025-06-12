import os
import re


class Rename:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def renommer_avec_regex(self, season=None, season_regex=None, episode_regex=r'[Ss](\d+)[Ee](\d+)', dry=True):
        total_fichiers = 0
        fichiers_renommes = 0
        infos = []
        print(season, season_regex, episode_regex, self.folder_path)
        for filename in os.listdir(self.folder_path):
            chemin_fichier = os.path.join(self.folder_path, filename)
            if os.path.isfile(chemin_fichier):
                total_fichiers += 1
                saison_num = season

                # Si la saison n’est pas précisée manuellement, on tente de la déduire avec la regex
                if saison_num is None and season_regex:
                    season_match = re.search(season_regex, filename)
                    if season_match:
                        saison_num = season_match.group(1)

                # Extraction de l'épisode
                episode_match = re.search(episode_regex, filename)
                if episode_match:
                    if saison_num is None and episode_match.lastindex > 1:
                        saison_num = episode_match.group(1)
                        episode_num = episode_match.group(2)
                    else:
                        episode_num = episode_match.group(1)
                else:
                    print(f"Aucun épisode trouvé pour: {filename}")
                    continue

                if saison_num is None:
                    print(f"Aucune saison trouvée pour: {filename}")
                    continue

                nouveau_nom = f"s{str(saison_num).zfill(1)}e{str(episode_num).zfill(2)}{os.path.splitext(filename)[1]}"
                chemin_nouveau_fichier = os.path.join(self.folder_path, nouveau_nom)

                if not dry:
                    os.rename(chemin_fichier, chemin_nouveau_fichier)

                fichiers_renommes += 1
                info = f"Renommé: '{filename}' -> '{nouveau_nom}'"
                infos.append(info)

        pourcentage = (fichiers_renommes / total_fichiers * 100) if total_fichiers else 0
        return round(pourcentage, 2), infos
