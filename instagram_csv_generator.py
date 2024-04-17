import requests
from bs4 import BeautifulSoup

def get_usernames(username):
    following_usernames = []
    followers_usernames = []

    # URL de la page de profil d'utilisateur sur Instagram pour les personnes suivies
    following_url = f"https://www.instagram.com/{username}/following/"

    # Effectuer une requête GET pour obtenir le contenu de la page des personnes suivies
    following_response = requests.get(following_url)
    if following_response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
        following_soup = BeautifulSoup(following_response.text, 'html.parser')

        # Trouver les balises <span> contenant les noms d'utilisateur des personnes suivies
        following_section = following_soup.find('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')
        following_usernames = extract_usernames_from_section(following_section)
    else:
        print("Erreur : Impossible de récupérer les personnes suivies.")

    # URL de la page de profil d'utilisateur sur Instagram pour les abonnés
    followers_url = f"https://www.instagram.com/{username}/followers/"

    # Effectuer une requête GET pour obtenir le contenu de la page des abonnés
    followers_response = requests.get(followers_url)
    if followers_response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
        followers_soup = BeautifulSoup(followers_response.text, 'html.parser')

        # Trouver les balises <span> contenant les noms d'utilisateur des abonnés
        followers_section = followers_soup.find('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')
        followers_usernames = extract_usernames_from_section(followers_section)
    else:
        print("Erreur : Impossible de récupérer les abonnés.")

    return following_usernames, followers_usernames

def extract_usernames_from_section(section):
    if section:
        # Extraire les noms d'utilisateur à partir des balises <a> dans la section
        usernames = [a.text for a in section.find_all('a')]
        return usernames
    else:
        print("Erreur : Aucune section trouvée.")
        return []

def main():
    # Nom d'utilisateur Instagram
    username = input("Entrez le nom d'utilisateur Instagram : ")

    # Récupérer les noms d'utilisateur des personnes suivies et des abonnés
    following_usernames, followers_usernames = get_usernames(username)

    if following_usernames and followers_usernames:
        print("Noms d'utilisateur des personnes suivies :")
        print(following_usernames)
        print("\nNoms d'utilisateur des abonnés :")
        print(followers_usernames)
    else:
        print("Impossible de récupérer les données du profil.")

if __name__ == '__main__':
    main()
