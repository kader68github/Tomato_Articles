"""Corrigé détaillé et argumenté du TD n°1 fourni."""
from docx_helpers import Builder, TEAL, NAVY, MUTED


def build():
    b=Builder('Corrigé')
    b.cover('TD n°1\nLa structure des glucides','Vrai/Faux • Isomérie • Fischer/Haworth • Diholosides',
            'Chaque réponse est justifiée à partir de la structure : identification des carbones, comparaison des configurations, lecture des liaisons et recherche d’un carbone anomérique libre.',
            'Correspondance intégrale avec les quatre exercices du PDF fourni. Les imprécisions de l’énoncé sont signalées ; les choix nécessaires sont explicités, notamment pour l’« isomère » du glucose et le diholoside de l’exercice 3.',
            'c00_couverture.png')

    # PAGE 2
    b.new_page('LIRE LE CORRIGÉ','Conventions et réponses en un regard','guide')
    b.p('Les structures A et B ont été redessinées à partir de l’énoncé. Les noms et les liaisons sont vérifiés par la numérotation des carbones, et non par simple reconnaissance visuelle.')
    b.table(['Exercice','Réponses essentielles','Pages'],[
        ('1 • Vrai/Faux','1. Faux ; 2. Vrai ; 3. Faux ; 4. Faux ; 5. Faux dans sa formulation rigoureuse, avec nuance.','3–4'),
        ('2 • Relations','Aldose/cétose ; épimères C2 ; aldose/cétose ; anomères ; aldose/cétose ; épimères C4 ; diastéréoisomères.','5–6'),
        ('3 • A et B','A = D-glucose ; B = D-fructose. Cyclisation, anomères et construction d’un diholoside.','7–13'),
        ('4 • Diholosides','1. Saccharose non réducteur ; 2. β-lactose réducteur ; 3. α-maltose réducteur.','14–17'),
        ('Synthèse','Méthode de vérification et erreurs à éviter.','18–19'),
    ],[3.5,11.8,1.7],font=10)
    b.h2('Trois conventions de lecture')
    b.bullets([
        'Fischer : chaîne correctement orientée, carbonyle en haut ; la série D/L dépend du dernier carbone chiral.',
        'Haworth : orientation standard des D-oses, groupe CH₂OH de référence vers le haut ; OH anomérique α vers le bas et β vers le haut.',
        'Les atomes H portés par les carbones sont implicites dans les cycles. Les carbones sont numérotés lorsqu’une question le demande.'
    ])
    b.callout('Deux questions sont sous-spécifiées : « dessiner l’isomère de A » ne dit pas lequel ; « le diholoside formé par ces deux oses » ne précise pas explicitement la liaison. Nous donnons l’interprétation la plus probable, puis les autres possibilités.',title='Rigueur de la correction',tone='gold')
    b.p('Abréviations : Glc = glucose ; Gal = galactose ; Fru = fructose ; p = pyranose ; f = furanose. Les réponses sont construites à partir de l’énoncé joint ; elles ne constituent pas un corrigé officiel de l’enseignant.','Small')

    # PAGE 3
    b.new_page('EXERCICE 1 • JUSTIFIER ET CORRIGER','1. Vrai ou faux — affirmations 1 à 3','ex1a')
    b.question('1','« Un aldotétrose est un sucre formé par 3 carbones et une fonction aldéhyde. »')
    b.rich([('FAUX. ',{'bold':True,'color':'AC4545'}),'Le préfixe « tétr- » indique quatre atomes de carbone. Un aldotétrose possède quatre carbones et une fonction aldéhyde. Un aldose à trois carbones est un aldotriose, représenté par le glycéraldéhyde.'])
    b.callout('Un aldotétrose est un ose à quatre carbones portant une fonction aldéhyde.',title='Phrase corrigée')
    b.p('Argument structurel : dans un aldotétrose ouvert, C1 porte CHO, C2 et C3 sont chiraux, et C4 est CH₂OH. Le nombre de carbones ne doit pas être confondu avec le nombre de centres chiraux.','Small')
    b.question('2','« L’ose appartient à la série D si le OH sur le carbone n−1 est à droite sur la projection de Fischer. »')
    b.rich([('VRAI. ',{'bold':True,'color':'2C795C'}),'Pour les oses simples étudiés, le dernier carbone chiral, Cn−1, est le carbone asymétrique le plus éloigné du groupe carbonyle. Dans une projection de Fischer correctement orientée, son OH à droite définit la série D ; à gauche, il définit la série L.'])
    b.p('Exemple : dans le D-glucose et le D-fructose, tous deux à six carbones, c’est le OH de C5 qui sert de référence. Dans les deux structures du TD, il est à droite.')
    b.callout('D/L est une convention de configuration. Cela ne signifie pas que tous les D-oses sont dextrogyres (+), ni que tous les L-oses sont lévogyres (−).',title='Précision indispensable',tone='gold')
    b.question('3','« Les oligosides font partie du groupe des oses simples. »')
    b.rich([('FAUX. ',{'bold':True,'color':'AC4545'}),'Les oligosides sont constitués de plusieurs unités osidiques reliées par des liaisons osidiques. Leur hydrolyse libère des oses plus petits. Les oses simples, eux, ne sont pas hydrolysables en unités osidiques plus petites.'])
    b.callout('Les oligosides sont des osides formés de quelques unités osidiques ; les diholosides en contiennent deux.',title='Phrase corrigée')
    b.p('Exemples : saccharose → glucose + fructose ; lactose → galactose + glucose ; maltose → glucose + glucose. Le suffixe « -oside » ne désigne donc pas un ose simple.','Small')

    # PAGE 4
    b.new_page('EXERCICE 1 • NUANCES IMPORTANTES','1. Vrai ou faux — affirmations 4 et 5','ex1b')
    b.question('4','« Le glycéraldéhyde est le précurseur de tous les cétoses. »')
    b.rich([('FAUX. ',{'bold':True,'color':'AC4545'}),'Le glycéraldéhyde est un aldotriose et la référence historique des séries D/L. Dans la classification généalogique de Fischer, il est à l’origine de la filiation des aldoses. Le cétose le plus simple est la dihydroxyacétone, un céto triose de formule C₃H₆O₃.'])
    b.callout('Le glycéraldéhyde est la référence des aldoses ; la dihydroxyacétone est le cétose le plus simple.',title='Phrase corrigée')
    b.p('Le mot « précurseur » est ici employé dans le sens de la filiation structurale de Fischer, et non comme l’affirmation qu’aucune interconversion métabolique n’existe entre trioses phosphates. Des interconnexions métaboliques ne rendent pas l’énoncé initial correct.')
    b.question('5','« Un carbone asymétrique (C*) ou chiral est doué d’activité optique et peut dévier la lumière polarisée. »')
    b.rich([('FAUX DANS SA FORMULATION RIGOUREUSE. ',{'bold':True,'color':'AC4545'}),'Un atome de carbone isolé ne possède pas une activité optique. La présence de carbones asymétriques favorise la chiralité d’une molécule, mais l’activité optique observée dépend de la molécule et de la composition de l’échantillon.'])
    b.table(['Situation','Activité optique observée'],[
        ('Molécule chirale, énantiomère majoritaire ou pur','Rotation non nulle possible ; son sens et son amplitude se mesurent.'),
        ('Mélange racémique : 50 % de chaque énantiomère','Rotations opposées qui se compensent : rotation nulle.'),
        ('Composé méso, malgré des centres chiraux','Molécule achirale par symétrie : rotation nulle.'),
    ],[8.0,9.0],font=10)
    b.callout('Une molécule chirale présente dans un échantillon non racémique peut faire tourner le plan de polarisation de la lumière. Le sens et l’amplitude de cette rotation sont des propriétés mesurables de l’échantillon.',title='Phrase corrigée')
    b.p('Nuance pédagogique : si l’enseignant utilise cette phrase comme raccourci pour « un composé chiral pur est optiquement actif », l’idée attendue peut être « vrai ». Toutefois, telle qu’elle est écrite, l’affirmation attribue l’activité au carbone et néglige racémiques et composés méso : la correction rigoureuse est ci-dessus.','Small')

    # PAGE 5
    b.new_page('EXERCICE 2 • CLASSER LES PAIRES','2. Comparaisons 1 à 4','ex2a')
    b.figure('x03_decision.png',width=15.0,caption='Arbre de décision : constitution d’abord, puis relation spatiale. La réponse la plus précise est privilégiée.')
    b.question('1','D-glycéraldéhyde / dihydroxyacétone')
    b.rich([('Paire aldose–cétose. ',{'bold':True,'color':TEAL}),'Le premier possède un aldéhyde en C1 ; la seconde possède une cétone en C2. Tous deux ont trois carbones et la formule C₃H₆O₃, mais leur connectivité diffère. Ce sont des isomères de constitution, pas des épimères.'])
    b.question('2','D-glucose / D-mannose')
    b.rich([('Épimères en C2. ',{'bold':True,'color':TEAL}),'Les deux aldohexoses ont la même constitution. Leurs OH sont opposés seulement en C2 ; C3, C4 et C5 sont identiques. Ils sont donc aussi des diastéréoisomères, mais « épimères en C2 » est la réponse la plus précise.'])
    b.question('3','D-glucose / D-fructose')
    b.rich([('Paire aldose–cétose. ',{'bold':True,'color':TEAL}),'Même formule C₆H₁₂O₆, mais aldéhyde en C1 pour le glucose et cétone en C2 pour le fructose. La différence porte sur la constitution : il ne s’agit pas d’une simple inversion de centre chiral.'])
    b.question('4','α-D-glucose / β-D-glucose')
    b.rich([('Anomères. ',{'bold':True,'color':TEAL}),'En supposant la même taille de cycle, usuellement le glucopyranose, les deux formes ne diffèrent que par la configuration du carbone anomérique C1. Ce sont donc aussi des épimères et des diastéréoisomères.'])
    b.p('Sans précision de cycle, « α-D-glucose » et « β-D-glucose » sont des noms abrégés. La comparaison attendue dans le TD porte sur α- et β-D-glucopyranose.','Small')

    # PAGE 6
    b.new_page('EXERCICE 2 • ÉVITER LES CONFUSIONS','2. Comparaisons 5 à 7 et bilan','ex2b')
    b.question('5','D-ribose / D-ribulose')
    b.rich([('Paire aldose–cétose. ',{'bold':True,'color':TEAL}),'Le D-ribose est un aldopentose ; le D-ribulose est un 2-cétopentose. Tous deux ont cinq carbones et la formule C₅H₁₀O₅, mais la fonction carbonyle occupe une position différente. Ce sont des isomères de constitution.'])
    b.question('6','D-galactose / D-glucose')
    b.rich([('Épimères en C4. ',{'bold':True,'color':TEAL}),'La seule différence de configuration se situe en C4 : OH à gauche pour le D-galactose en Fischer, à droite pour le D-glucose. Les deux oses sont aussi des diastéréoisomères.'])
    b.question('7','D-mannose / D-galactose')
    b.rich([('Diastéréoisomères, mais pas épimères. ',{'bold':True,'color':TEAL}),'Le D-mannose présente la séquence G–G–D–D en C2–C3–C4–C5 ; le D-galactose présente D–G–G–D. Deux centres diffèrent : C2 et C4. Ce ne sont donc ni des épimères, ni des énantiomères.'])
    b.table(['Paire du TD','Réponse la plus précise','Autre relation correcte'],[
        ('D-glycéraldéhyde / DHA','Aldose–cétose','Isomères de constitution'),
        ('D-glucose / D-mannose','Épimères en C2','Diastéréoisomères'),
        ('D-glucose / D-fructose','Aldose–cétose','Isomères de constitution'),
        ('α / β-D-glucopyranose','Anomères en C1','Épimères ; diastéréoisomères'),
        ('D-ribose / D-ribulose','Aldose–cétose','Isomères de constitution'),
        ('D-galactose / D-glucose','Épimères en C4','Diastéréoisomères'),
        ('D-mannose / D-galactose','Diastéréoisomères','Diffèrent en C2 et C4'),
    ],[6.3,5.5,5.2],font=9.5)
    b.callout('DHA = dihydroxyacétone. Pour une paire d’énantiomères, il aurait fallu inverser tous les centres chiraux, par exemple D-glucose et L-glucose. Aucune paire proposée dans cet exercice n’est énantiomère.',title='Contrôle final',tone='blue')

    # PAGE 7
    b.new_page('EXERCICE 3 • IDENTIFIER A ET B','3.1 Série et carbone asymétriques — questions 1 et 2','ex3a')
    b.figure('x01_identification.png',width=15.8,caption='Reconstitution fidèle des deux oses du TD. Le fond vert repère le dernier carbone chiral ; le fond jaune, la fonction carbonyle.')
    b.question('1','À quelle série appartiennent A et B ?')
    b.rich([('A et B appartiennent à la série D. ',{'bold':True,'color':TEAL}),'Chacun possède six carbones. Le dernier centre chiral est C5 : son OH est à droite dans les deux projections de Fischer. La position du OH de référence donne D, indépendamment de la fonction aldose ou cétose.'])
    b.question('2','Combien de carbones asymétriques possèdent-ils ?')
    b.table(['Ose','Carbones non chiraux','Carbones chiraux','Nombre'],[
        ('A • D-glucose','C1 : CHO ; C6 : CH₂OH','C2, C3, C4, C5','4'),
        ('B • D-fructose','C1 et C6 : CH₂OH ; C2 : C=O','C3, C4, C5','3'),
    ],[3.5,6.0,5.6,1.9],font=10)
    b.p('Justification : un centre chiral tétraédrique porte quatre substituants différents. Les carbones du carbonyle sont trigonaux, et les carbones CH₂OH portent deux hydrogènes identiques : ils ne sont pas des centres asymétriques.')
    b.callout('A est un aldohexose : D-glucose. B est un cétohexose : D-fructose. Leurs noms seront justifiés par les configurations des autres centres dans les questions suivantes.',title='Identification')

    # PAGE 8
    b.new_page('EXERCICE 3 • ÉPIMÈRES DU GLUCOSE','3.2 Nom de A et épimères — question 3','ex3b')
    b.question('3a','Quel est le nom de l’ose A ?')
    b.rich([('A est le D-glucose. ',{'bold':True,'color':TEAL}),'La chaîne comporte six carbones et un aldéhyde en C1 : c’est un aldohexose. Les OH de C2, C3, C4 et C5 sont respectivement à droite, gauche, droite, droite. Cette signature D–G–D–D correspond au D-glucose.'])
    b.question('3b','Quels sont ses épimères ?')
    b.p('Deux épimères classiques, tous deux dans la série D, sont attendus dans ce chapitre :')
    b.bullets([
        'D-mannose : épimère du D-glucose en C2 ; seule la configuration de C2 est inversée.',
        'D-galactose : épimère du D-glucose en C4 ; seule la configuration de C4 est inversée.'
    ])
    b.figure('c06_epimers.png',width=16.2,caption='Les deux épimères usuels à retenir. Les cases dorées signalent le centre qui diffère du D-glucose.')
    b.h2('Réponse exhaustive si l’énoncé ne restreint pas la série')
    b.p('Le D-glucose possède quatre centres chiraux ; inverser chacun d’eux séparément donne quatre épimères : D-mannose (C2), D-allose (C3), D-galactose (C4) et L-idose (C5). Inverser C5 fait changer la série D en L.')
    b.callout('Réponse de base : D-mannose et D-galactose, en précisant C2 et C4. Si « tous les épimères » est demandé sans restriction à la série D, ajouter D-allose et L-idose.',title='Ce que permet d’affirmer l’énoncé',tone='gold')

    # PAGE 9
    b.new_page('EXERCICE 3 • ISOMÈRE ET DÉNOMBREMENT','3.3 Miroir du glucose et nombre d’isomères — questions 4 et 5','ex3c')
    b.question('4','« Dessiner l’isomère de l’ose A et le nommer. »')
    b.rich([('Interprétation proposée : l’énantiomère, soit le L-glucose. ',{'bold':True,'color':TEAL}),'Le mot « isomère » seul ne définit pas une structure unique. Dans la progression habituelle du TD, on attend souvent l’image miroir du D-glucose. Pour la construire, on inverse les quatre centres : la séquence D–G–D–D devient G–D–G–G.'])
    b.figure('x02_enantiomere.png',width=14.8,caption='Le L-glucose est l’énantiomère du D-glucose : tous les centres chiraux sont inversés, pas seulement le carbone de référence C5.')
    b.p('Autres réponses possibles si un autre type d’isomère était demandé : D-mannose est un diastéréoisomère/épimère ; D-fructose est un isomère de constitution. Une clarification de l’énoncé serait nécessaire pour imposer l’un de ces choix.','Small')
    b.question('5','Quelle formule donne le nombre d’isomères de cet ose ?')
    b.p('Pour un aldose ouvert à n carbones, le nombre de centres chiraux est m = n − 2. Ici n = 6, donc m = 4. Chaque centre peut prendre deux configurations :')
    b.equation('N = 2ᵐ = 2ⁿ⁻² = 2⁴ = 16 aldohexoses ouverts')
    b.callout('Il existe 16 aldohexoses stéréoisomères au total : 8 de la série D et 8 de la série L. Ce nombre ne comprend pas les cétohexoses comme le fructose.',title='Résultat et périmètre',tone='blue')

    # PAGE 10
    b.new_page('EXERCICE 3 • PASSER EN HAWORTH','3.4 Les deux formes demandées — question 6','ex3d')
    b.p('Il faut représenter l’anomère α-D-pyranose de l’aldose A et l’anomère β-D-furanose du cétose B, puis les nommer et numéroter leurs carbones.')
    b.figure('x05_cycles_demandes.png',width=16.5,caption='Réponses dessinées : α-D-glucopyranose et β-D-fructofuranose. Les carbones anomériques, C1 et C2, sont mis en évidence.')
    b.table(['Vérification','α-D-glucopyranose','β-D-fructofuranose'],[
        ('Cycle','C1–C2–C3–C4–C5–O : 6 atomes','C2–C3–C4–C5–O : 5 atomes'),
        ('Carbone anomérique','C1 ; OH vers le bas pour α','C2 ; OH vers le haut pour β'),
        ('OH conservés','C2 bas ; C3 haut ; C4 bas','C3 haut ; C4 bas'),
        ('Carbones hors cycle','C6 dans CH₂OH, vers le haut','C1 et C6 dans deux CH₂OH'),
    ],[3.7,6.65,6.65],font=9.8)
    b.h2('Pourquoi ces noms ?')
    b.p('A est le glucose et son cycle à six atomes est un pyranose : α-D-glucopyranose. B est le fructose et son cycle à cinq atomes est un furanose : β-D-fructofuranose. Dans l’orientation standard du β-D-fructofuranose, le OH anomérique est en haut et le CH₂OH de C1 en bas ; le CH₂OH de C6 est en haut.')
    b.callout('Une erreur classique consiste à mettre C6 dans un CH₂OH exocyclique tout en appelant la structure fructofuranose : ici, C1 et C6 sont bien hors cycle. Dans un fructopyranose, en revanche, C6 appartiendrait au cycle.',title='Contrôle de la numérotation',tone='gold')

    # PAGE 11
    b.new_page('EXERCICE 3 • EXPLIQUER L’ANOMÉRIE','3.5 Origine des formes α et β — question 7','ex3e')
    b.question('7','Comment obtient-on les deux anoméries α et β ?')
    b.p('La cyclisation résulte de l’attaque intramoléculaire d’un oxygène alcoolique sur le carbone carbonyle, suivie de transferts de protons. Le carbone carbonyle, initialement trigonal plan, devient tétraédrique. Selon la face du carbonyle impliquée, le nouveau OH anomérique prend l’une ou l’autre configuration.')
    b.table(['Ose','Addition cyclique','Produit'],[
        ('A • D-glucose','OH de C5 sur le carbonyle C1','Hémiacétal cyclique ; C1 devient anomérique'),
        ('B • D-fructose','OH de C5 sur le carbonyle C2','Hémicétal cyclique ; C2 devient anomérique'),
    ],[3.3,6.1,7.6],font=10.3)
    b.figure('c07_cyclisation.png',width=16.3,caption='Exemple du glucose : deux configurations en C1. Les autres centres chiraux ne changent pas. Les flèches entre anomères résument un équilibre via la forme ouverte.')
    b.h2('Formation et interconversion ne sont pas le même processus')
    b.p('La fermeture du cycle forme les anomères. En solution, leur interconversion, ou mutarotation, nécessite une réouverture transitoire en forme carbonyle, puis une refermeture. Elle n’est pas obtenue par simple rotation d’une liaison C–O du cycle fermé.')
    b.callout('α/β décrit la configuration relative du nouveau centre anomérique. Dans les projections standards des D-oses du TD : OH anomérique en bas = α ; en haut = β.',title='Conclusion à rédiger',tone='blue')
    b.p('Le mécanisme peut être catalysé en milieu acide ou basique. À ce niveau, il suffit d’identifier l’attaque du carbonyle, la création du centre anomérique et le passage par la forme ouverte pour l’interconversion.','Small')

    # PAGE 12
    b.new_page('EXERCICE 3 • CONSTRUIRE UN DIHOLOSIDE','3.6 Saccharose et pouvoir réducteur — question 8','ex3f')
    b.callout('Hypothèse retenue : relier les deux carbones anomériques des formes demandées en question 6, soit C1 du glucose et C2 du fructose. On obtient le saccharose, également présent dans l’exercice 4.',title='Hypothèse explicite',tone='gold')
    b.figure('c11_saccharose.png',width=16.6,caption='Diholoside construit : saccharose. La liaison relie les deux centres anomériques ; le cycle fructose est tourné dans le plan pour rendre la liaison lisible.')
    b.h2('Nom et liaison')
    b.p('Nom complet : α-D-glucopyranosyl-(1↔2)-β-D-fructofuranoside. La liaison est une liaison O-osidique α,β(1↔2), plus précisément une liaison glucosyl–fructosyl entre C1 du glucose et C2 du fructose.')
    b.equation('D-glucose + D-fructose → saccharose + H₂O  (bilan formel)')
    b.equation('C₆H₁₂O₆ + C₆H₁₂O₆ → C₁₂H₂₂O₁₁ + H₂O')
    b.h2('Le diholoside est-il réducteur ?')
    b.rich([('Non. ',{'bold':True,'color':'AC4545'}),'Le C1 anomérique du glucose et le C2 anomérique du fructose sont tous deux engagés dans la liaison. Le glucose est engagé comme acétal et le fructose comme cétal : aucun des deux cycles ne peut s’ouvrir directement en carbonyle. Le saccharose intact est donc non réducteur et ne présente pas de mutarotation.'])
    b.p('En revanche, après hydrolyse, les oses libérés retrouvent leurs carbones anomériques libres et deviennent réducteurs. La perte d’un OH anomérique libre, et non la simple présence du fructose, justifie la réponse.','Small')

    # PAGE 13
    b.new_page('EXERCICE 3 • PORTÉE DE LA RÉPONSE','3.7 Pourquoi préciser la liaison ?','ex3g')
    b.p('La seule donnée « glucose + fructose » ne suffit pas à définir un diholoside unique. Il faut aussi préciser les tailles de cycle, les configurations et les carbones reliés. Même avec α-D-glucopyranose et β-D-fructofuranose, le choix du OH accepteur doit être indiqué.')
    b.table(['Information','Déterminée par A et B ?','Dans la réponse retenue'],[
        ('Nature et série des oses','Oui','D-glucose et D-fructose'),
        ('Cycles et anomères','Oui, après la question 6','α-D-Glcp et β-D-Fruf'),
        ('Carbones reliés','Non, pas explicitement dans la question 8','C1 ↔ C2, choix conduisant au saccharose'),
        ('Pouvoir réducteur','Découle du choix de liaison','Non, car les deux anomères sont engagés'),
    ],[4.0,5.7,7.3],font=10)
    b.h2('Un contre-exemple montre l’ambiguïté')
    b.p('Si le C1 du glucose était relié au OH de C4 du fructose, on construirait un autre diholoside, noté par exemple α-D-Glcp-(1→4)-β-D-Fruf. Le C2 anomérique du fructose resterait libre et ce produit serait réducteur. Il ne serait donc pas licite d’affirmer « non réducteur » sans préciser la liaison.')
    b.h2('Lire correctement la rotation du dessin')
    b.figure('x04_rotation.png',width=14.8,caption='Une rotation de 180° dans le plan change ce qui est dessiné en haut et en bas, mais conserve la molécule et sa configuration β.')
    b.callout('Pour une question d’examen, écrire : « En reliant les deux carbones anomériques indiqués, on obtient le saccharose, de liaison α,β(1↔2), non réducteur. » Cette formulation rend l’hypothèse visible et la conclusion rigoureuse.',title='Réponse robuste',tone='blue')

    # PAGE 14
    b.new_page('EXERCICE 4 • DÉCODER LES TROIS NOMS','4. Noms, formules et réduction — vue d’ensemble','ex4a')
    b.p('Les trois composés sont des diholosides formés à partir de deux hexoses. Leur formule brute commune est C₁₂H₂₂O₁₁ ; leurs structures et leur pouvoir réducteur diffèrent. Les formules développées de Haworth sont données dans les pages suivantes.')
    b.table(['N°','Lecture structurale','Nom','Réducteur ?'],[
        ('1','α-D-Glcp-(1↔2)-β-D-Fruf\nDeux carbones anomériques engagés','Saccharose','Non'),
        ('2','β-D-Galp-(1→4)-β-D-Glcp\nC1 du glucose libre','β-lactose\n(lactose, forme β)','Oui'),
        ('3','α-D-Glcp-(1→4)-α-D-Glcp\nC1 du second glucose libre','α-maltose\n(maltose, forme α)','Oui'),
    ],[.9,8.1,4.5,3.5],font=10)
    b.h2('Règle générale employée pour chaque réponse')
    b.bullets([
        'Le suffixe « -osyl » identifie le sucre donneur dont le carbone anomérique est engagé.',
        'La flèche donne le carbone anomérique de départ et le carbone accepteur d’arrivée.',
        'Un accepteur terminé par « -ose » peut conserver un anomère libre ; un « -oside » a son anomère engagé.',
        'Pour conclure à la réduction, rechercher un hémiacétal ou hémicétal capable de s’ouvrir.'
    ])
    b.callout('Le lactose et le maltose proposés précisent l’anomère de leur extrémité réductrice. Les noms généraux « lactose » et « maltose » restent corrects, mais « β-lactose » et « α-maltose » sont plus fidèles aux formules imposées.',title='Précision des noms',tone='blue')
    b.equation('Bilan commun : 2 C₆H₁₂O₆ − H₂O = C₁₂H₂₂O₁₁')
    b.p('Une même formule brute ne permet pas de distinguer ces trois diholosides. La connectivité et la stéréochimie sont indispensables.','Small')

    # PAGE 15
    b.new_page('EXERCICE 4 • COMPOSÉ 1','4.1 Saccharose : deux anomères bloqués','ex4b')
    b.callout('α-D-glucopyranosyl-(1→2)-β-D-fructofuranoside\n= α-D-glucopyranosyl-(1↔2)-β-D-fructofuranoside\n= saccharose',title='Nom',tone='blue')
    b.figure('c11_saccharose.png',width=15.0,caption='Formule de Haworth du saccharose. Le pont osidique relie C1 du glucose à C2 du fructose.')
    b.h2('Identification et formule')
    b.p('Unités : α-D-glucopyranose et β-D-fructofuranose. Liaison : O-osidique entre les deux carbones anomériques, de configuration α du côté glucose et β du côté fructose. Formule brute : C₁₂H₂₂O₁₁. Abréviation : α-D-Glcp-(1↔2)-β-D-Fruf.')
    b.h2('Justification du caractère non réducteur')
    b.p('Le carbone C1 du glucose n’est plus un hémiacétal, mais un acétal ; le carbone C2 du fructose n’est plus un hémicétal, mais un cétal. Aucun OH anomérique libre ne subsiste. L’ouverture directe en forme carbonyle est impossible pour les deux unités, donc le saccharose est non réducteur.')
    b.table(['Test structural','Résultat'],[
        ('OH anomérique libre ?','Aucun'),
        ('Ouverture directe d’un cycle ?','Impossible sans rupture de la liaison osidique'),
        ('Mutarotation du diholoside intact ?','Non'),
        ('Après hydrolyse ?','Glucose et fructose libérés : réducteurs'),
    ],[7.0,10.0],font=10)
    b.p('La double flèche (1↔2) est une notation explicite lorsque les deux centres anomériques sont engagés. La notation (1→2) de l’énoncé, accompagnée du suffixe « fructofuranoside », désigne bien la même structure.','Small')

    # PAGE 16
    b.new_page('EXERCICE 4 • COMPOSÉ 2','4.2 β-lactose : un anomère reste libre','ex4c')
    b.callout('β-D-galactopyranosyl-(1→4)-β-D-glucopyranose\n= β-lactose',title='Nom',tone='blue')
    b.figure('c11_lactose.png',width=16.5,caption='Formule demandée : β-lactose. Le C1 du galactose est engagé dans la liaison ; le C1 du glucose reste libre, en configuration β.')
    b.h2('Identification et formule')
    b.p('Unités : β-D-galactopyranose à l’origine de la liaison et β-D-glucopyranose à l’extrémité réductrice. Liaison : β-O-osidique (1→4), de C1 du galactose vers le OH de C4 du glucose. Formule brute : C₁₂H₂₂O₁₁. Nom général : β-D-Galp-(1→4)-D-Glcp.')
    b.h2('Justification du caractère réducteur')
    b.p('Le C1 du galactose est bloqué, mais le C1 du glucose reste un hémiacétal libre. Ce cycle peut s’ouvrir pour donner la forme aldéhyde, puis se refermer en α ou β. Le β-lactose est donc réducteur et présente une mutarotation.')
    b.table(['Point de contrôle','Vérification sur la formule'],[
        ('Pourquoi galactose ?','OH de C4 du donneur orienté vers le haut en Haworth standard'),
        ('Pourquoi β au départ ?','Liaison anomérique du galactose du côté haut, cis au CH₂OH de référence'),
        ('Pourquoi (1→4) ?','Départ en C1 du galactose, arrivée sur C4 du glucose'),
        ('Pourquoi β-lactose ?','Le OH du C1 libre du glucose est vers le haut dans la forme dessinée'),
    ],[5.0,12.0],font=10)
    b.p('La forme α du lactose diffère seulement à l’extrémité réductrice glucose. La liaison β(1→4) du galactose reste inchangée. L’hydrolyse du lactose libère D-galactose et D-glucose.','Small')

    # PAGE 17
    b.new_page('EXERCICE 4 • COMPOSÉ 3','4.3 α-maltose : deux glucoses, un seul anomère engagé','ex4d')
    b.callout('α-D-glucopyranosyl-(1→4)-α-D-glucopyranose\n= α-maltose',title='Nom',tone='blue')
    b.figure('c11_maltose.png',width=13.8,caption='α-maltose : deux unités glucose ; le second C1 anomérique reste libre, en configuration α.')
    b.h2('Identification et formule')
    b.p('Unités : deux D-glucopyranoses. Le premier est engagé en α sur son C1 ; le second reçoit la liaison sur son OH de C4 et conserve un C1 anomérique de configuration α. Liaison : α-O-osidique (1→4). Formule brute : C₁₂H₂₂O₁₁. Nom général : α-D-Glcp-(1→4)-D-Glcp.')
    b.h2('Justification du caractère réducteur')
    b.p('Le second glucose possède encore un OH anomérique libre. Son cycle peut s’ouvrir en aldéhyde et se refermer avec une autre configuration. Le maltose est donc réducteur et présente une mutarotation, même si le premier glucose a son carbone anomérique bloqué.')
    b.table(['Point de contrôle','Vérification sur la formule'],[
        ('Nature des deux unités','Deux glucoses : OH de C4 vers le bas avant engagement'),
        ('Liaison du donneur','α(1→4), vers le bas en C1 en orientation standard'),
        ('Extrémité réductrice','OH en C1 du second glucose vers le bas : forme α'),
        ('Hydrolyse','Libération de deux D-glucoses'),
    ],[5.0,12.0],font=9.8)
    b.callout('Il suffit d’un carbone anomérique libre pour qu’un diholoside soit réducteur. Il n’est pas nécessaire que les deux le soient.',title='Conclusion générale',tone='blue')

    # PAGE 18
    b.new_page('SYNTHÈSE DU TD','5. Vérifier une copie en quatre étapes','synthese')
    b.h2('1 • Identifier les oses avant de les nommer')
    b.p('Compter les carbones, localiser le carbonyle et lire la configuration du dernier centre chiral. Pour A : aldohexose D–G–D–D → D-glucose. Pour B : cétohexose G–D–D → D-fructose.')
    b.h2('2 • Comparer les structures au bon niveau')
    b.p('Constitution différente : isomères de constitution. Même constitution mais toutes les configurations inversées : énantiomères. Sinon, stéréoisomères non miroir : diastéréoisomères. Un seul centre inversé : épimères. Au carbone anomérique de formes cycliques : anomères.')
    b.h2('3 • Contrôler chaque dessin')
    b.bullets([
        'Numéros des carbones, taille du cycle et position de l’oxygène.',
        'Série D/L et orientation du groupe de référence.',
        'OH anomérique α ou β, sans modifier les autres centres.',
        'Pour le fructose, distinguer C1 et C6 exocycliques dans le furanose.'
    ])
    b.h2('4 • Justifier la réduction par la liaison')
    b.table(['Diholoside','Liaison','Anomère libre','Conclusion'],[
        ('Saccharose','Glucose C1 ↔ fructose C2','Aucun','Non réducteur'),
        ('β-lactose','Galactose C1 → glucose C4','C1 du glucose','Réducteur'),
        ('α-maltose','Glucose C1 → glucose C4','C1 du second glucose','Réducteur'),
    ],[3.2,6.2,4.4,3.2],font=10)
    b.callout('Une bonne copie ne se contente pas de noms : elle montre le carbone de référence D/L, précise le centre d’épimérie, numérote les cycles et identifie le ou les anomères libres.',title='Critères d’une réponse argumentée')
    b.h2('Autocontrôle rapide')
    b.p('Puis-je justifier chaque vrai/faux ? Puis-je tracer le L-glucose sans erreur ? Puis-je expliquer pourquoi le fructose libre est réducteur mais pas le saccharose ? Puis-je distinguer α-maltose et maltose ? Si oui, les compétences centrales du TD sont acquises.')

    # PAGE 19
    b.new_page('NOTES ET RÉFÉRENCES','Portée scientifique du corrigé','references_corr')
    b.h2('Choix explicites effectués')
    b.table(['Point de l’énoncé','Traitement dans ce corrigé'],[
        ('Exercice 1, item 5','Correction rigoureuse de l’attribution de l’activité optique à un carbone ; distinction molécule chirale, racémique et méso.'),
        ('Exercice 2, anomères','Même taille de cycle supposée, conformément à l’usage de l’exercice : glucopyranose.'),
        ('Exercice 3, épimères','D-mannose et D-galactose comme réponses classiques ; liste exhaustive ajoutée sans restriction de série.'),
        ('Exercice 3, « isomère »','Énantiomère L-glucose proposé comme interprétation probable, sans le présenter comme unique.'),
        ('Exercice 3, diholoside','Saccharose construit en reliant les deux centres anomériques ; hypothèse annoncée et contre-exemple donné.'),
        ('Exercice 4, noms','β-lactose et α-maltose pour respecter l’état anomérique imposé à l’extrémité réductrice.'),
    ],[5.0,12.0],font=10)
    b.h2('Sources et approfondissement')
    b.bullets([
        'Document source : TRAVAUX DIRIGÉS N°1 DE BIOCHIMIE STRUCTURALE — LA STRUCTURE DES GLUCIDES, SNV L2, 2026/2027, PDF fourni par l’utilisateur.',
        'Nelson, D. L. & Cox, M. M. — Lehninger Principles of Biochemistry, 8e éd., Macmillan Learning, 2021 : glucides, stéréochimie et pouvoir réducteur.',
        'Berg, J. M., Tymoczko, J. L., Gatto, G. J. & Stryer, L. — Biochemistry, 9e éd., W. H. Freeman, 2019 : structure des oses et liaisons glycosidiques.',
        'IUPAC–IUBMB — Nomenclature of Carbohydrates (Recommendations 1996) : conventions de dénomination et de représentation.'
    ])
    b.callout('Le présent document est un corrigé pédagogique original établi à partir de l’énoncé fourni. Les hypothèses sont signalées afin de distinguer ce qui est imposé par le TD de ce qui relève d’un choix de construction.',title='Transparence',tone='blue')
    b.p('Complément conseillé : Cours_Biochimie_L2_Structure_des_glucides.docx. Les deux documents sont modifiables dans Word ; les scripts python-docx et les figures sources sont fournis dans le dossier de production.','Small')
    return b.save('Corrige_detaille_TD1_Biochimie_L2.docx')

if __name__=='__main__':
    print(build())
