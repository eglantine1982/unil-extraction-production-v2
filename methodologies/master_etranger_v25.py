def phase_4_3_extraction_pages_filles(contenu, urls_deja_scrapees):
    import re, time

    print("🔍 Découverte automatique des sous-pages via regex...")
    regex_pattern = r"https://www\\.unil\\.ch[^\\s\"'>,)]+"
    urls_detectees = set()

    for page, texte in contenu.items():
        matches = re.findall(regex_pattern, texte)
        for lien in matches:
            if "bachelor-suisse" in lien or "master-suisse" in lien:
                continue
            urls_detectees.add(lien.strip(".,;!>\"'"))

    nouvelles_urls = list(urls_detectees - set(urls_deja_scrapees))
    print(f"📌 {len(nouvelles_urls)} nouvelles pages détectées automatiquement")

    for i, url in enumerate(nouvelles_urls):
        nom = f"fille_auto_{i+1}"
        print(f"➡️ Extraction automatique : {url}")
        contenu_page = extraire_contenu_page_unil(url, nom)
        if contenu_page:
            contenu[nom] = contenu_page
        time.sleep(2)

    print("🔧 Intégration manuelle du contenu spécifique à la Chine")
    contenu['contenu_dossier_chine_integre'] = "Contenu Chine à insérer manuellement ici."

    urls_critiques = [
        "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/sinscrire/delais-pour-le-depot-dune-candidature.html",
        "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/sinscrire/taxe-administrative.html",
        "https://www.unil.ch/immat/fr/home/menuinst/futurs-etudiants/sinscrire/nous-contacter.html"
    ]

    for url in urls_critiques:
        nom = url.split("/")[-1].replace(".html", "").replace("-", "_")
        print(f"🔒 Extraction page critique : {url}")
        contenu_page = extraire_contenu_page_unil(url, nom)
        if contenu_page:
            contenu[nom] = contenu_page
        time.sleep(2)

    print(f"✅ Phase 4.3 terminée : {len(contenu)} pages au total.")
    return contenu
