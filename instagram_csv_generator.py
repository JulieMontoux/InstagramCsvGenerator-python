import os
import instaloader
import csv
import threading

def get_followers_and_following(username, password):
    # Créer une instance d'Instaloader
    L = instaloader.Instaloader()

    # Se connecter à Instagram
    L.login(username, password)

    # Récupérer le profil de l'utilisateur cible
    profile = instaloader.Profile.from_username(L.context, username)

    # Récupérer les followers
    followers = set(profile.get_followers())

    # Récupérer les personnes suivies
    following = set(profile.get_followees())

    return followers, following

def generate_csv(username, password):
    # Récupérer les followers et les personnes suivies
    followers, following = get_followers_and_following(username, password)

    # Trouver les correspondances entre les followers et les personnes suivies
    matching_usernames = followers.intersection(following)
    non_matching_followers = followers - following
    non_matching_following = following - followers

    # Créer un dossier pour stocker les fichiers CSV s'il n'existe pas déjà
    if not os.path.exists('data'):
        os.makedirs('data')

    # Enregistrer les correspondances dans un fichier CSV
    with open('data/correspondances.csv', 'w', newline='') as csvfile:
        fieldnames = ['username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in matching_usernames:
            writer.writerow({'username': user.username})

    # Enregistrer les non-correspondances des followers dans un fichier CSV
    with open('data/non_correspondances_followers.csv', 'w', newline='') as csvfile:
        fieldnames = ['username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in non_matching_followers:
            writer.writerow({'username': user.username})

    # Enregistrer les non-correspondances des personnes suivies dans un fichier CSV
    with open('data/non_correspondances_following.csv', 'w', newline='') as csvfile:
        fieldnames = ['username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in non_matching_following:
            writer.writerow({'username': user.username})

    return "Fichiers CSV enregistrés avec succès."

def main():
    # Entrer les informations d'identification
    username = input("Entrez votre nom d'utilisateur Instagram : ")
    password = input("Entrez votre mot de passe Instagram : ")

    # Lancer la génération des CSV dans un thread séparé
    threading.Thread(target=generate_csv, args=(username, password)).start()

if __name__ == '__main__':
    main()
