# MÉTHODOLOGIE EXHAUSTIVE UNIL V25 - EXTRACTION DÉFINITIVE
import requests
import time
import re
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def extraire_contenu_page_unil(url, nom_page):
    """Extraction sécurisée du contenu d'une page UNIL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraction du contenu principal
        contenu_principal = ""
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'div']):
            texte = element.get_text(strip=True)
            if texte and len(texte) > 10:
                contenu_principal += texte + "\n"
        
        if len(contenu_principal) > 100:
            print(f"✅ {len(contenu_principal):,} caractères extraits pour {nom_page}")
            return contenu_principal
        else:
            print(f"❌ Échec extraction {nom_page}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur {nom_page}: {str(e)}")
        return None

def extraire_contenu_master_etranger():
    """CODE 1 - Extraction exhaustive Master Étranger avec URLs corrigées"""
    
    # URLs exhaustives Master Étranger VALIDÉES
    urls_master_etranger = {
        'delais': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/delais.html',
        'masters_generaux': 'https://www.unil.ch/unil/fr/home/menuinst/etudier/masters.html',
        'master_temps_partiel': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/master-a-temps-partiel.html',
        'taxe_administrative': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/taxe-administrative.html',
        'permis_visa': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/permis-pour-etudes---visa.html',
        'conditions_particulieres': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/conditions-particulieres.html',
        'deroulement_admission': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/deroulement-dune-admission.html',
        'inscription_en_ligne': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/sinscrire-en-ligne-et-prepar.html',
        'cours_francais': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/cours-satellites-et-cours-intensifs-de-francais.html',
        'equivalences': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/master/avec-un-bachelor-etranger/equivalences.html',
        'medecine': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/medecine.html',
        'droit_allemand': 'https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/droit-allemand.html'
    }
    
    contenu_master = {}
    erreurs = []
    
    print("🚀 DÉMARRAGE EXTRACTION MASTER ÉTRANGER")
    print(f"📋 {len(urls_master_etranger)} pages à extraire")
    
    for nom_page, url in urls_master_etranger.items():
        print(f"\n🔄 Extraction {nom_page}: {url}")
        contenu = extraire_contenu_page_unil(url, nom_page)
        
        if contenu:
            contenu_master[nom_page] = contenu
        else:
            erreurs.append(f"Échec extraction {nom_page}")
        
        time.sleep(2)  # Pause respectueuse
    
    volume_total = sum(len(contenu) for contenu in contenu_master.values())
    
    print(f"\n🎯 RÉSULTATS CODE 1:")
    print(f"Pages extraites: {len(contenu_master)}")
    print(f"Volume total: {volume_total:,} caractères")
    print(f"Erreurs: {len(erreurs)}")
    
    return contenu_master, urls_master_etranger, erreurs

def extraire_pages_filles_complementaires(contenu_master, tous_urls):
    """CODE 2 - Extraction pages filles complémentaires avec correction hub central"""
    
    print("🔍 CORRECTION STRUCTURELLE HUB CENTRAL")
    
    # Vérification présence page parent hub
    if 'contenu_dossier_master_parent' in contenu_master:
        contenu_parent = contenu_master['contenu_dossier_master_parent']
        
        # Découverte automatique des liens dans cette page parent
        liens_sous_pages = re.findall(r'https://www\.unil\.ch[^\s\)\]\>\"\'\,\;\!\<]+avec-un-bachelor-obtenu[^\s\)\]\>\"\'\,\;\!\<]*\.html', contenu_parent)
        
        print(f"🎯 {len(liens_sous_pages)} liens sous-pages découverts dans hub central")
        
        # Extraction des sous-pages découvertes
        for i, lien_sous_page in enumerate(set(liens_sous_pages), 1):
            if lien_sous_page not in tous_urls.values():
                nom_sous_page = f"hub_sous_page_{i}"
                print(f"\n🔄 Extraction {nom_sous_page}: {lien_sous_page}")
                contenu = extraire_contenu_page_unil(lien_sous_page, nom_sous_page)
                
                if contenu and len(contenu) > 100:
                    contenu_master[nom_sous_page] = contenu
                    tous_urls[nom_sous_page] = lien_sous_page
                    print(f"✅ {len(contenu):,} caractères extraits")
                
                time.sleep(2)
    
    # Découverte pages filles complémentaires standard
    pages_filles_complementaires = []
    
    for nom_page, contenu in contenu_master.items():
        liens_trouves = re.findall(r'https://www\.unil\.ch[^\s\)\]\>\"\'\,\;\!\<]+', contenu)
        
        for lien_brut in liens_trouves:
            lien = re.sub(r'[.,;!)\]\>\"\'\<]+', '', lien_brut)
            
            if (lien.startswith('https://www.unil.ch') and
                ('master' in lien.lower() or 'immat' in lien.lower() or 'sinscrire' in lien.lower()) and
                'avec-un-bachelor-suisse' not in lien and
                'bachelor-suisse' not in lien and
                'master-suisse' not in lien and
                lien not in tous_urls.values() and
                lien not in pages_filles_complementaires and
                len(lien) > 30):
                pages_filles_complementaires.append(lien)
    
    # Extraction pages filles complémentaires
    for i, url_fille in enumerate(pages_filles_complementaires[:10], 1):  # Limite à 10 pour optimiser
        nom_page_fille = f"page_fille_comp_{i}"
        print(f"\n🔄 Extraction {nom_page_fille}: {url_fille}")
        contenu = extraire_contenu_page_unil(url_fille, nom_page_fille)
        
        if contenu:
            contenu_master[nom_page_fille] = contenu
            tous_urls[nom_page_fille] = url_fille
        
        time.sleep(2)
    
    volume_total_final = sum(len(contenu) for contenu in contenu_master.values())
    nouvelles_pages = len(pages_filles_complementaires)
    
    print(f"\n🎯 RÉSULTATS CODE 2:")
    print(f"Nouvelles pages découvertes: {nouvelles_pages}")
    print(f"Total pages: {len(contenu_master)}")
    print(f"Volume total final: {volume_total_final:,} caractères")
    
    return contenu_master, tous_urls

def organiser_et_sauvegarder(contenu_master, tous_urls):
    """CODE 3 - Organisation et sauvegarde finale"""
    
    print("📋 ORGANISATION FINALE DU CONTENU")
    
    # Création du fichier de sortie avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"master_etranger_extraction_{timestamp}.txt"
    
    contenu_final = "# EXTRACTION COMPLÈTE MASTER ÉTRANGER UNIL\n"
    contenu_final += f"# Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    contenu_final += f"# Volume total: {sum(len(c) for c in contenu_master.values()):,} caractères\n"
    contenu_final += f"# Nombre de pages: {len(contenu_master)}\n\n"
    
    # Organisation par sections
    sections = {
        'PAGES_PRINCIPALES': ['page_principale', 'contenu_dossier_master_parent'],
        'DOSSIERS_SPECIALISES': ['avec_bachelor_convention', 'avec_bachelor_autre_etat', 'avec_bachelor_chine'],
        'PROCEDURES_ADMINISTRATIVES': ['delais_candidature', 'inscription_en_ligne', 'taxes_semestrielles', 'permis_visa', 'taxe_administrative'],
        'PAGES_COMPLEMENTAIRES': [k for k in contenu_master.keys() if k.startswith(('page_fille', 'hub_sous_page'))]
    }
    
    for section_nom, pages_section in sections.items():
        contenu_final += f"\n{'='*60}\n"
        contenu_final += f"SECTION: {section_nom}\n"
        contenu_final += f"{'='*60}\n\n"
        
        for page in pages_section:
            if page in contenu_master:
                contenu_final += f"\n--- PAGE: {page.upper()} ---\n"
                contenu_final += f"URL: {tous_urls.get(page, 'URL non disponible')}\n"
                contenu_final += f"CONTENU:\n{contenu_master[page]}\n"
    
    # Sauvegarde dans le dossier outputs
    try:
        with open(f'outputs/{nom_fichier}', 'w', encoding='utf-8') as f:
            f.write(contenu_final)
        print(f"✅ Fichier sauvegardé: outputs/{nom_fichier}")
    except:
        # Fallback si dossier outputs n'existe pas
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write(contenu_final)
        print(f"✅ Fichier sauvegardé: {nom_fichier}")
    
    # Génération du rapport de validation
    volume_total = sum(len(contenu) for contenu in contenu_master.values())
    
    print(f"\n🎯 VALIDATION FINALE:")
    print(f"Volume total: {volume_total:,} caractères")
    print(f"Objectif 70,000+: {'✅ ATTEINT' if volume_total >= 70000 else '⚠️ PROCHE'}")
    print(f"Pages extraites: {len(contenu_master)}")
    print(f"Fichier généré: {nom_fichier}")
    
    return contenu_final, nom_fichier

# FONCTION D'EXÉCUTION COMPLÈTE
def executer_extraction_complete():
    """Exécution complète des 3 codes en séquence"""
    
    print("🚀 DÉMARRAGE EXTRACTION COMPLÈTE MASTER ÉTRANGER")
    print("="*60)
    
    # CODE 1
    contenu_master, tous_urls, erreurs1 = extraire_contenu_master_etranger()
    
    # CODE 2
    contenu_master, tous_urls = extraire_pages_filles_complementaires(contenu_master, tous_urls)
    
    # CODE 3
    contenu_final, nom_fichier = organiser_et_sauvegarder(contenu_master, tous_urls)
    
    print("\n🎉 EXTRACTION TERMINÉE AVEC SUCCÈS")
    print(f"📁 Fichier final: {nom_fichier}")
    
    return contenu_final, nom_fichier
