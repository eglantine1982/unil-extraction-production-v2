# Configuration URLs UNIL Master Étranger - Version Production CORRIGÉE
# URLs complètes validées par l'utilisateur

URLS_MASTER_ETRANGER_COMPLETES = [
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/delais.html",
    "https://www.unil.ch/unil/fr/home/menuinst/etudier/masters.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/master-a-temps-partiel.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/taxe-administrative.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/permis-pour-etudes---visa.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/conditions-particulieres.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/deroulement-dune-admission.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/sinscrire-en-ligne-et-prepar.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/cours-satellites-et-cours-intensifs-de-francais.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/equivalences.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/medecine.html",
    "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/droit-allemand.html"
]

def get_full_urls():
    """Retourne la liste complète des URLs validées à extraire"""
    return URLS_MASTER_ETRANGER_COMPLETES

def get_base_url():
    """Retourne l'URL de base principale UNIL"""
    return "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/"
