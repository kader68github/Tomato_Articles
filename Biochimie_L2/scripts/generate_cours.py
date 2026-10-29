"""Cours L2 correspondant au TD n°1 — La structure des glucides."""
from docx_helpers import Builder, TEAL, NAVY, MUTED


def build():
    b=Builder('Cours')
    b.cover('La structure\ndes glucides','Stéréochimie • Représentations • Diholosides',
            'Un cours progressif pour passer de la formule ouverte d’un ose à la structure d’un diholoside, puis déterminer son pouvoir réducteur.',
            'Niveau L2 SNV. Prérequis : liaisons covalentes, groupes fonctionnels, notions de molécule et d’isomérie. Le chapitre suit les compétences évaluées dans le TD n°1.',
            'c00_couverture.png')

    # PAGE 2
    b.new_page('ENTRER DANS LE CHAPITRE','Objectifs et parcours','objectif')
    b.p('À la fin de ce chapitre, vous devrez savoir :')
    b.bullets([
        'classer un glucide et distinguer aldose, cétose, ose et oside ;',
        'lire une projection de Fischer, repérer les centres chiraux et attribuer la série D ou L ;',
        'reconnaître énantiomères, diastéréoisomères, épimères et anomères ;',
        'construire une projection de Haworth et nommer les formes cycliques ;',
        'décoder une liaison osidique et justifier le caractère réducteur d’un sucre.'
    ])
    b.h2('Sommaire interactif')
    t=b.table(['Module','Compétences travaillées','Page'],[
        ('1. Définir et classer','Glucides, oses, oligosides et polyosides','3'),
        ('2. Lire Fischer','Numérotation, D/L et chiralité','4'),
        ('3. Comparer les oses','Dénombrement et relations stéréochimiques','6'),
        ('4. Fermer le cycle','Hémiacétals, anomères et Haworth','10'),
        ('5. Relier deux oses','Liaison osidique et trois diholosides','14'),
        ('6. Conclure et vérifier','Pouvoir réducteur, méthode et entraînement','18'),
        ('7. Réviser','Erreurs fréquentes et fiche de synthèse','22'),
        ('Références','Sources et conventions du support','23'),
    ],[5.0,10.3,1.7],font=10)
    anchors=['classer','fischer','denombrement','cyclisation','liaison','reducteur','revision','references']
    for row,anchor in zip(t.rows[1:],anchors):
        p=row.cells[0].paragraphs[0]
        label=row.cells[0].text
        for r in list(p.runs):r._r.getparent().remove(r._r)
        from docx_helpers import internal_link
        internal_link(p,label,anchor,bold=True,size=10)
    b.callout('D/L décrit une configuration de référence. α/β décrit la configuration du carbone anomérique. (+)/(−) décrit le sens mesuré de rotation de la lumière polarisée. Ce sont trois informations différentes.',title='Trois notations à ne pas confondre',tone='gold')
    b.p('Les figures sont des représentations pédagogiques originales. En Haworth, les atomes d’hydrogène liés aux carbones sont implicites, sauf indication contraire.','Small')

    # PAGE 3
    b.new_page('MODULE 1 • DÉFINITIONS','1. Classer les glucides','classer')
    b.p('Les glucides comprennent notamment des polyhydroxyaldéhydes, des polyhydroxycétones et leurs dérivés, ainsi que les substances qui libèrent de tels composés par hydrolyse. Le terme « hydrate de carbone » est historique : il ne signifie pas que la molécule contient des molécules d’eau.')
    b.figure('c01_classification.png',width=15.5,caption='Classification selon le nombre d’unités osidiques. Les oses peuvent aussi être classés par fonction carbonyle et nombre de carbones.')
    b.table(['Catégorie','Critère','Exemples'],[
        ('Ose','Unité glucidique simple, non hydrolysable en oses plus petits','Glucose, fructose, ribose'),
        ('Diholoside','Deux unités osidiques reliées par une liaison osidique','Saccharose, lactose, maltose'),
        ('Oligoside','Quelques unités osidiques ; convention du cours : 2 à 10','Diholosides, raffinose (3 unités)'),
        ('Polyoside','Chaîne longue, souvent au-delà de 10 unités','Amidon, glycogène, cellulose'),
    ],[3.0,8.0,6.0],font=10)
    b.p('La borne entre oligoside et polyoside dépend des conventions. Un diholoside est un oligoside, et non un ose simple. Les polyosides peuvent être homopolyosides ou hétéropolyosides selon la nature de leurs unités.','Small')
    b.h2('Deux autres critères pour les oses')
    b.p('Aldose : fonction aldéhyde, généralement en C1. Cétose : fonction cétone, généralement en C2. Triose, tétrose, pentose et hexose désignent respectivement 3, 4, 5 et 6 carbones. Ainsi, le glucose est un aldohexose et le fructose un cétohexose.')
    b.p('À retenir : Cₙ(H₂O)ₙ décrit de nombreux oses simples, mais n’est ni une définition générale ni une propriété de tous les glucides. Les dérivés et les osides peuvent s’en écarter.','Small',before=4)

    # PAGE 4
    b.new_page('MODULE 2 • LA CHAÎNE OUVERTE','2. Lire une projection de Fischer','fischer')
    b.p('La projection de Fischer représente une chaîne carbonée verticale. Par convention, les traits horizontaux portent les substituants vers l’avant et les traits verticaux les éloignent de l’observateur. Ce n’est pas une photographie de la conformation réelle.')
    b.figure('c02_fischer.png',caption='D-glucose et D-fructose : même formule brute C₆H₁₂O₆, mais fonction carbonyle et connectivité différentes. Le carbone de référence D/L est surligné en vert.')
    b.h2('Numéroter avant de comparer')
    b.bullets([
        'Aldose : le carbone du groupe aldéhyde terminal est C1.',
        '2-cétose usuelle : C1 est le CH₂OH adjacent au carbonyle ; le carbone cétonique est C2.',
        'Pour un aldohexose ouvert, C2, C3, C4 et C5 sont chiraux ; C1 et C6 ne le sont pas.',
        'Pour le D-fructose ouvert, C3, C4 et C5 sont chiraux ; C1, C2 et C6 ne le sont pas.'
    ])
    b.callout('Une rotation de 180° dans le plan d’une projection de Fischer conserve son interprétation. Une rotation de 90° ou un seul échange gauche–droite ne doit pas être interprété comme la même molécule.',title='Règle de manipulation',tone='gold')

    # PAGE 5
    b.new_page('MODULE 2 • CONFIGURATION','3. Série D/L et activité optique','dl')
    b.p('Un carbone asymétrique est un carbone tétraédrique lié à quatre substituants différents. On le note souvent C*. Pour attribuer D ou L, on regarde le carbone chiral le plus éloigné du groupe carbonyle : Cn−1 dans les oses simples étudiés ici.')
    b.figure('c03_dl.png',width=15.8,caption='Le glycéraldéhyde sert de référence historique. Dans une projection de Fischer correctement orientée, OH à droite = D ; OH à gauche = L.')
    b.table(['Notation','Ce qu’elle indique','Comment l’obtenir'],[
        ('D / L','Configuration relative au glycéraldéhyde','Position du OH de référence en Fischer'),
        ('α / β','Configuration au carbone anomérique','Comparaison avec le centre de référence, dans une forme cyclique'),
        ('(+) / (−)','Sens de rotation du plan de polarisation','Mesure polarimétrique ; ne se déduit pas de D/L'),
    ],[2.4,6.3,8.3],font=10)
    b.h2('Chiralité ne garantit pas une rotation mesurée non nulle')
    b.p('Une molécule chirale pure peut être optiquement active. Mais un mélange racémique contient autant des deux énantiomères : leurs rotations se compensent. Une molécule possédant des centres chiraux peut aussi être achirale par symétrie interne, comme un composé méso. L’activité optique est une propriété de l’échantillon, pas d’un carbone isolé.')
    b.callout('Le D-fructose appartient à la série D et est lévogyre : on peut le noter D-(−)-fructose. Le signe « moins » ne contredit donc pas son appartenance à la série D.',title='Exemple décisif')

    # PAGE 6
    b.new_page('MODULE 3 • DÉNOMBRER','4. Compter les centres et les stéréoisomères','denombrement')
    b.p('Un centre chiral indépendant peut prendre deux configurations. Avec m centres indépendants, et en l’absence de compensation par symétrie, le nombre maximal de stéréoisomères est 2ᵐ. Pour les oses simples ouverts étudiés ici, cette borne est atteinte.')
    b.figure('c04_denombrement.png',caption='Détermination de m pour un aldose ou un 2-cétose. Les extrémités ne sont pas équivalentes dans ces oses simples.')
    b.table(['Ose ouvert','Centres chiraux','m','Total D + L','Par série'],[
        ('Aldotétrose','C2, C3','2','4','2 D + 2 L'),
        ('Aldopentose','C2, C3, C4','3','8','4 D + 4 L'),
        ('Aldohexose','C2, C3, C4, C5','4','16','8 D + 8 L'),
        ('Cétohexose','C3, C4, C5','3','8','4 D + 4 L'),
    ],[3.6,5.0,1.2,3.5,3.7],font=10)
    b.equation('Aldose : N = 2ⁿ⁻²   •   2-cétose (n ≥ 4) : N = 2ⁿ⁻³')
    b.p('La dihydroxyacétone est une exception à vérifier avant d’appliquer une formule : ce triose possède trois carbones mais aucun carbone chiral. Il n’existe qu’une structure de constitution correspondante, sans couple D/L.')
    b.callout('Ces dénombrements concernent les formes ouvertes. La cyclisation crée un centre anomérique supplémentaire et des formes α/β ; elle ne change pas le nombre de configurations de la chaîne ouverte.',title='Ne pas compter deux fois la même chose',tone='gold')

    # PAGE 7
    b.new_page('MODULE 3 • UNE FAMILLE À RECONNAÎTRE','5. Configurations des hexoses de la série D','familles')
    b.p('Les tableaux donnent la position du OH dans les projections de Fischer, du haut vers le bas. Ils constituent une clé de reconnaissance, pas une liste à apprendre sans comprendre la numérotation.')
    b.table(['D-aldohexose','C2','C3','C4','C5'],[
        ('D-allose','D','D','D','D'),('D-altrose','G','D','D','D'),
        ('D-glucose','D','G','D','D'),('D-mannose','G','G','D','D'),
        ('D-gulose','D','D','G','D'),('D-idose','G','D','G','D'),
        ('D-galactose','D','G','G','D'),('D-talose','G','G','G','D'),
    ],[5.0,3,3,3,3],font=9.5,caption='Les huit D-aldohexoses. Le glucose a la séquence D–G–D–D.')
    b.table(['D-cétohexose','C3','C4','C5'],[
        ('D-psicose (D-allulose)','D','D','D'),('D-fructose','G','D','D'),
        ('D-sorbose','G','G','D'),('D-tagatose','D','G','D'),
    ],[8.0,3,3,3],font=9.5,caption='Les quatre D-cétohexoses usuels. C2 porte la fonction cétone.')
    b.h2('Passer des aldoses aux cétoses')
    b.p('Le glycéraldéhyde est la référence de la série D/L et le point de départ de la filiation des aldoses. Le cétose le plus simple est la dihydroxyacétone. La filiation de Fischer est une classification formelle par allongement de chaîne : elle ne décrit pas, à elle seule, une voie métabolique.')
    b.callout('Pour identifier A dans le TD : six carbones, aldéhyde en C1, puis D–G–D–D → D-glucose. Pour B : six carbones, cétone en C2, puis G–D–D → D-fructose.',title='Application directe')

    # PAGE 8
    b.new_page('MODULE 3 • COMPARER','6. Isomères : choisir la bonne relation','stereoisomerie')
    b.p('Deux molécules de même formule brute peuvent différer par l’enchaînement des atomes ou seulement par leur disposition spatiale. Il faut donc comparer la constitution avant d’examiner les configurations.')
    b.figure('c05_stereoisomerie.png',caption='Classification des isomères. Les épimères sont des diastéréoisomères particuliers ; les anomères sont des épimères au carbone anomérique.')
    b.table(['Relation','Critère','Exemple'],[
        ('Constitutionnels','Connectivité différente','D-glucose / D-fructose'),
        ('Énantiomères','Images miroir non superposables ; tous les centres chiraux inversés','D-glucose / L-glucose'),
        ('Diastéréoisomères','Stéréoisomères non énantiomères','D-glucose / D-galactose'),
        ('Épimères','Un seul centre chiral inversé','D-glucose / D-mannose'),
        ('Anomères','Formes cycliques différant au seul carbone anomérique','α- et β-D-glucopyranose'),
    ],[3.8,8.0,5.2],font=9.6)
    b.callout('Une paire aldose/cétose est une paire d’isomères de constitution, souvent appelée isomères de fonction. Elle n’est pas une paire d’épimères, même si les deux oses ont le même nombre de carbones.',title='Priorité à la constitution',tone='gold')

    # PAGE 9
    b.new_page('MODULE 3 • ÉPIMÈRES','7. Le glucose et ses voisins','epimers')
    b.p('Deux épimères ne diffèrent que par la configuration d’un seul carbone chiral. Il faut préciser ce carbone : « épimère en C2 » est une réponse complète, « épimère » seul est moins précis.')
    b.figure('c06_epimers.png',caption='Deux épimères classiques du D-glucose dans la série D : D-mannose en C2 et D-galactose en C4.')
    b.table(['Centre inversé par rapport au D-glucose','Épimère correspondant'],[
        ('C2','D-mannose'),('C3','D-allose'),('C4','D-galactose'),('C5','L-idose'),
    ],[9.0,8.0],font=10)
    b.p('Si l’on ne restreint pas la recherche à la série D, l’inversion du seul C5 change aussi la série : l’épimère est alors le L-idose. Dans de nombreux exercices de L2, « les épimères du glucose » désigne les deux exemples classiques D-mannose et D-galactose ; il faut lire la restriction éventuelle de l’énoncé.','Small')
    b.callout('Comparer les positions des OH, et non leur nombre. Inverser un centre signifie échanger H et OH autour de ce carbone dans une projection de Fischer correctement orientée.',title='Le bon geste')

    # PAGE 10
    b.new_page('MODULE 4 • FERMER LE CYCLE','8. Cyclisation et carbone anomérique','cyclisation')
    b.p('En solution, un ose peut subir l’addition intramoléculaire d’un OH sur son propre carbonyle. Un aldose forme un hémiacétal cyclique ; un cétose forme traditionnellement un hémicétal cyclique. Le carbone carbonyle devient alors tétraédrique et peut devenir chiral : c’est le carbone anomérique.')
    b.figure('c07_cyclisation.png',caption='Cyclisation du D-glucose. L’attaque du carbonyle peut conduire aux deux configurations anomériques ; leur interconversion passe par la forme ouverte.')
    b.table(['Ose','Réaction intramoléculaire','Cycle obtenu','Carbone anomérique'],[
        ('D-glucose','OH de C5 sur C1','Glucopyranose : 6 atomes','C1'),
        ('D-fructose','OH de C5 sur C2','Fructofuranose : 5 atomes','C2'),
        ('D-fructose','OH de C6 sur C2','Fructopyranose : 6 atomes','C2'),
    ],[2.8,5.3,6.0,2.9],font=9.8)
    b.h2('Mutarotation')
    b.p('Les formes α et β et la forme ouverte coexistent en équilibre. Une forme anomérique pure évolue vers cet équilibre en solution : la rotation optique change progressivement. C’est la mutarotation. Elle nécessite l’ouverture du cycle, donc un carbone anomérique libre de type hémiacétal ou hémicétal.')
    b.callout('Le carbone anomérique n’est pas le numéro du carbone choisi au hasard : c’est celui qui portait la fonction carbonyle avant cyclisation.',title='Repère invariable')

    # PAGE 11
    b.new_page('MODULE 4 • DESSINER','9. De Fischer à Haworth : méthode','haworth')
    b.p('La projection de Haworth représente le cycle comme un polygone plan conventionnel. Elle indique les positions relatives des substituants, mais ne décrit pas la conformation tridimensionnelle réelle : les pyranoses adoptent notamment des conformations chaise.')
    b.figure('c08_fischer_haworth.png',caption='Méthode pour le D-glucose en orientation standard. Le OH de C5 intervient dans le cycle ; on ne le replace pas comme un OH libre.')
    b.h2('Les cinq étapes à automatiser')
    b.bullets([
        'Identifier la fonction carbonyle et numéroter la chaîne ouverte.',
        'Choisir le OH qui attaque : C5–OH donne ici un pyranose pour le glucose, un furanose pour le fructose.',
        'Dessiner le cycle avec son oxygène et placer C1 pour le glucose, C2 pour le fructose.',
        'Pour un D-ose orienté classiquement, placer le CH₂OH de référence vers le haut ; traduire droite → bas et gauche → haut aux centres conservés.',
        'Choisir α ou β et placer le OH anomérique ; vérifier la numérotation et les substituants.'
    ])
    b.callout('Dans l’orientation standard d’un D-ose : α = OH anomérique vers le bas ; β = vers le haut. Pour un L-ose, l’orientation du groupe de référence est inversée. Toujours revenir à la définition relative plutôt d’appliquer « bas/haut » sans vérifier l’orientation.',title='Convention, pas identité absolue',tone='gold')

    # PAGE 12
    b.new_page('MODULE 4 • CAS DU GLUCOSE','10. Les deux anomères du D-glucopyranose','anomeres_glucose')
    b.p('Le D-glucose cyclisé par l’OH de C5 possède un cycle à six atomes : cinq carbones, C1 à C5, et un oxygène. C6 reste hors du cycle dans le groupe CH₂OH porté par C5.')
    b.figure('c09_anomeres_glucose.png',caption='α- et β-D-glucopyranose. Les configurations de C2, C3, C4 et C5 sont identiques ; seule celle de C1 change.')
    b.table(['Position','α-D-glucopyranose','β-D-glucopyranose'],[
        ('OH en C1','Bas','Haut'),
        ('OH en C2','Bas','Bas'),
        ('OH en C3','Haut','Haut'),
        ('OH en C4','Bas','Bas'),
        ('CH₂OH en C5 (C6)','Haut','Haut'),
    ],[5.0,6.0,6.0],font=10)
    b.callout('α et β sont des configurations, pas des tailles de cycle. Les deux noms ci-dessus contiennent « pyranose » : ils désignent le même type de cycle. α/β n’indique pas non plus la série D/L.',title='Lire un nom complet')
    b.p('Le carbone anomérique libre peut retrouver la fonction carbonyle par ouverture du cycle. Le glucose est donc un sucre réducteur et peut présenter une mutarotation.','Small')

    # PAGE 13
    b.new_page('MODULE 4 • CAS DU FRUCTOSE','11. Anomérie et taille du cycle','anomeres_fructose')
    b.p('Le carbone anomérique du fructose est C2. Dans le fructofuranose, le cycle contient C2, C3, C4, C5 et O. Les groupes C1–CH₂OH et C6–CH₂OH restent hors du cycle.')
    b.figure('c09b_anomeres_fructose.png',width=14.5,caption='Anomères du D-fructofuranose : seule la configuration de C2 change.')
    b.figure('c10_fructose_cycles.png',width=15.0,caption='Dans le fructopyranose, C6 appartient au cycle ; ce n’est plus un substituant CH₂OH.')
    b.table(['Repère en orientation standard','β-D-fructofuranose'],[
        ('C2','OH vers le haut ; CH₂OH de C1 vers le bas'),
        ('C3 / C4','OH de C3 vers le haut ; OH de C4 vers le bas'),
        ('C5','CH₂OH de C6 vers le haut'),
    ],[6.0,11.0],font=9.8)
    b.p('À retenir : furanose/pyranose précise la taille du cycle ; α/β précise la configuration en C2. Ce sont deux informations indépendantes.','Small',before=4)

    # PAGE 14
    b.new_page('MODULE 5 • RELIER DEUX OSES','12. La liaison osidique','liaison')
    b.p('Une liaison osidique est une liaison C–O–C impliquant le carbone anomérique d’au moins un ose. Elle transforme la fonction hémiacétal ou hémicétal de ce donneur en acétal ou cétal. L’autre partenaire fournit un OH accepteur, qui peut être anomérique ou non.')
    b.figure('c13_liaison.png',caption='Bilan formel de condensation entre deux OH. La perte d’eau est un bilan, pas la description du mécanisme biosynthétique cellulaire.')
    b.equation('2 C₆H₁₂O₆ → C₁₂H₂₂O₁₁ + H₂O')
    b.h2('Lire une notation complète')
    b.p('α-D-glucopyranosyl-(1→4)-D-glucopyranose se lit ainsi : le donneur est un glucose de série D, sous forme pyranose, de configuration α en C1 ; son C1 est relié au OH de C4 du second glucose. Le suffixe « -osyl » identifie l’unité donneuse engagée dans la liaison.')
    b.table(['OH accepteur','Conséquence sur l’extrémité accepteuse'],[
        ('OH alcoolique non anomérique','Son carbone anomérique peut rester libre : diholoside réducteur.'),
        ('OH anomérique','Les deux carbones anomériques sont bloqués : diholoside non réducteur.'),
    ],[6.0,11.0],font=10)
    b.callout('Dans une biosynthèse, des sucres activés et des enzymes spécifiques assurent la formation de la liaison avec une stéréochimie contrôlée. Le schéma « deux oses − eau » ne prétend pas reproduire ce mécanisme.',title='Chimie formelle et biologie',tone='blue')

    # PAGE 15
    b.new_page('MODULE 5 • DIHOLOSIDE 1','12.1 Le saccharose','saccharose')
    b.p('Le saccharose associe une unité α-D-glucopyranose et une unité β-D-fructofuranose par leurs deux carbones anomériques : C1 pour le glucose et C2 pour le fructose.')
    b.figure('c11_saccharose.png',caption='Saccharose. Le cycle fructose a été tourné de 180° dans le plan pour rapprocher les deux carbones engagés ; cette rotation ne change pas sa configuration.')
    b.callout('Nom systématique : α-D-glucopyranosyl-(1↔2)-β-D-fructofuranoside.\nNotation abrégée : α-D-Glcp-(1↔2)-β-D-Fruf.',title='Nom à savoir décoder',tone='blue')
    b.table(['Question','Réponse argumentée'],[
        ('Quels oses ?','D-glucose + D-fructose'),
        ('Quelle liaison ?','Osidique α,β(1↔2), entre C1 du glucose et C2 du fructose'),
        ('Formule brute ?','C₁₂H₂₂O₁₁'),
        ('Réducteur ?','Non : les deux carbones anomériques sont engagés'),
        ('Mutarotation ?','Non, en l’absence d’hydrolyse : aucun anomère libre'),
    ],[4.2,12.8],font=10)
    b.p('La double flèche rappelle que les deux carbones anomériques participent à la liaison. La notation rencontrée dans le TD, « glucopyranosyl-(1→2)-fructofuranoside », désigne le même saccharose ; le suffixe « -oside » signale déjà l’engagement du centre anomérique du fructose.','Small')
    b.p('Après hydrolyse de la liaison, glucose et fructose retrouvent leurs centres anomériques libres : les produits libérés sont réducteurs. Le saccharose intact ne l’est pas.','Small')

    # PAGE 16
    b.new_page('MODULE 5 • DIHOLOSIDE 2','12.2 Le lactose','lactose')
    b.p('Le lactose associe le D-galactose au D-glucose. Le carbone anomérique C1 du galactose est relié au OH de C4 du glucose. Le C1 du glucose reste un hémiacétal libre.')
    b.figure('c11_lactose.png',caption='Forme explicitement décrite dans le TD : β-lactose, avec une extrémité glucopyranose de configuration β.')
    b.callout('β-D-galactopyranosyl-(1→4)-β-D-glucopyranose = β-lactose.\nNom général du disaccharide : β-D-Galp-(1→4)-D-Glcp.',title='Nom et précision anomérique',tone='blue')
    b.table(['Élément à vérifier','Dans le lactose'],[
        ('Donneur','β-D-galactopyranosyl : liaison partant de C1, configuration β'),
        ('Accepteur','D-glucopyranose : liaison reçue sur le OH de C4'),
        ('Différence galactose / glucose','Configuration du OH en C4 : opposée dans les deux oses'),
        ('Pouvoir réducteur','Oui : C1 du glucose encore hémiacétal'),
        ('Mutarotation','Oui : l’extrémité glucose peut passer de β à α via l’ouverture'),
    ],[5.2,11.8],font=10)
    b.p('Lorsque le nom « lactose » est employé sans α ou β devant l’unité glucose, il peut désigner le disaccharide réducteur dont l’extrémité réductrice s’interconvertit. Ici, l’énoncé impose β à cette extrémité : la structure dessinée est le β-lactose.','Small')
    b.equation('Lactose + H₂O → D-galactose + D-glucose  (hydrolyse)')

    # PAGE 17
    b.new_page('MODULE 5 • DIHOLOSIDE 3','12.3 Le maltose','maltose')
    b.p('Le maltose est constitué de deux unités D-glucose. Le C1 anomérique du premier glucose, en configuration α, est relié au OH de C4 du second. Le second glucose conserve son C1 anomérique libre.')
    b.figure('c11_maltose.png',caption='Forme décrite dans le TD : α-maltose. Le premier C1 est engagé ; le second C1, entouré de vert, reste réducteur.')
    b.callout('α-D-glucopyranosyl-(1→4)-α-D-glucopyranose = α-maltose.\nNom général du disaccharide : α-D-Glcp-(1→4)-D-Glcp.',title='Nom et précision anomérique',tone='blue')
    b.table(['Confusion fréquente','Distinction correcte'],[
        ('Maltose / saccharose','Maltose : glucose + glucose, un anomère libre.\nSaccharose : glucose + fructose, deux anomères engagés.'),
        ('Maltose / cellobiose','Maltose : liaison α(1→4).\nCellobiose : liaison β(1→4), entre deux glucoses.'),
        ('Maltose / isomaltose','Maltose : liaison (1→4).\nIsomaltose : liaison α(1→6).'),
    ],[5.2,11.8],font=10)
    b.p('Le maltose est réducteur et présente une mutarotation. Son hydrolyse libère deux molécules de D-glucose. Une liaison α(1→4) se retrouve dans l’amidon et le glycogène ; la cellulose contient des liaisons β(1→4).')
    b.equation('Maltose + H₂O → 2 D-glucose  (hydrolyse)')
    b.callout('Le préfixe α du maltose décrit la liaison du donneur. Un second α, placé devant « glucopyranose », décrit l’anomère libre de l’accepteur. Ces deux lettres ne portent pas sur le même carbone.',title='Lire deux fois, mais pas la même chose',tone='gold')

    # PAGE 18
    b.new_page('MODULE 6 • POUVOIR RÉDUCTEUR','13. Réducteur ou non : la décision','reducteur')
    b.p('Un sucre est réducteur lorsqu’une forme carbonyle peut être rendue accessible par ouverture d’un hémiacétal ou d’un hémicétal libre. Il peut alors réduire certains ions métalliques dans les conditions des tests classiques, en étant lui-même oxydé.')
    b.figure('c12_reducteur.png',caption='Diagnostic structural. La présence d’un OH anomérique libre est le critère décisif, pas la seule présence de nombreux OH.')
    b.table(['Sucre','Centre(s) anomérique(s)','Réducteur ?'],[
        ('Glucose / fructose libres','C1 / C2 libres','Oui'),
        ('Saccharose','C1 glucose et C2 fructose engagés','Non'),
        ('Lactose','C1 glucose libre','Oui'),
        ('Maltose','C1 du second glucose libre','Oui'),
    ],[5.0,8.2,3.8],font=10)
    b.h2('Et les cétones ?')
    b.p('Le fructose libre donne aussi un test positif avec les réactifs alcalins de Fehling ou Benedict : il s’isomérise via des intermédiaires ènediols en aldoses capables de réduire Cu²⁺. « Aldose » n’est donc pas un synonyme de « réducteur ».')
    b.p('Fehling/Benedict : formation d’un précipité de Cu₂O rouge brique dans les conditions du test. Tollens : dépôt d’argent métallique. Ces tests sont qualitatifs et dépendent du milieu ; d’autres espèces réductrices peuvent aussi réagir.','Small')
    b.callout('Ne pas conclure « non réducteur » uniquement parce qu’un sucre est dessiné sous forme cyclique : les hémiacétals libres s’ouvrent en solution.',title='Erreur à éviter',tone='gold')

    # PAGE 19
    b.new_page('MODULE 6 • MÉTHODE TRANSFÉRABLE','14. Du nom systématique à la structure','methode')
    b.p('Un nom de diholoside contient toutes les informations nécessaires au dessin. Il faut le lire de gauche à droite en identifiant le donneur, la liaison, puis l’accepteur.')
    b.h2('Procédure en six vérifications')
    b.bullets([
        'Nature des oses : glucose, galactose ou fructose ; vérifier la série D ou L.',
        'Taille des cycles : pyranose ou furanose.',
        'Configuration anomérique du donneur : α ou β.',
        'Numéros reliés : origine au carbone anomérique du donneur, arrivée sur le carbone accepteur.',
        'État de l’accepteur : « -ose » avec anomère libre ou « -oside » avec anomère engagé.',
        'Conclusion : vérifier la liaison, numéroter les carbones, puis rechercher un anomère libre.'
    ])
    b.table(['Nom courant','Liaison et unités','Réducteur'],[
        ('Saccharose','α-D-Glcp-(1↔2)-β-D-Fruf','Non'),
        ('Lactose','β-D-Galp-(1→4)-D-Glcp','Oui'),
        ('Maltose','α-D-Glcp-(1→4)-D-Glcp','Oui'),
    ],[3.4,10.5,3.1],font=10.5,caption='Les trois diholosides du TD. Tous ont pour formule brute C₁₂H₂₂O₁₁.')
    b.h2('Exemple guidé : β-D-Galp-(1→4)-β-D-Glcp')
    b.p('Placer un β-D-galactopyranose à gauche et un β-D-glucopyranose à droite. Repérer le OH anomérique du galactose et le OH de C4 du glucose, puis tracer le pont osidique C–O–C entre C1 et C4. Vérifier que la liaison part vers le haut en C1 du galactose. Le OH β en C1 du glucose reste présent : le β-lactose est réducteur.')
    b.callout('Glcp, Galp et Fruf sont des abréviations : Glc = glucose, Gal = galactose, Fru = fructose ; p = pyranose, f = furanose. Les lettres D, α et β restent indispensables.',title='Abréviations utilisées',tone='blue')

    # PAGE 20
    b.new_page('MODULE 6 • S’ENTRAÎNER','15. Autoévaluation avant le TD','entrainement')
    b.p('Répondre sans consulter la fiche de synthèse. Pour chaque item, donner une justification courte : la réponse seule ne suffit pas.')
    questions=[
        ('Q1 • Classification','Un aldotétrose possède-t-il quatre centres chiraux ? Donner son nombre de stéréoisomères ouverts.'),
        ('Q2 • Série','Un ose possède le OH de C5 à gauche dans une projection de Fischer correctement orientée. Peut-on conclure qu’il est L si son OH de C4 est à droite ?'),
        ('Q3 • Comparaison','Quelle relation précise unit D-glucose et D-mannose ? Et D-glucose et D-fructose ?'),
        ('Q4 • Anomérie','Dessiner α-D-glucopyranose, puis modifier uniquement le groupement nécessaire pour obtenir β-D-glucopyranose.'),
        ('Q5 • Fructose','Pourquoi le carbone anomérique du fructose est-il C2 et non C1 ? Quel OH faut-il engager pour obtenir un fructofuranose ?'),
        ('Q6 • Liaison','Décoder β-D-Galp-(1→4)-D-Glcp : donneur, accepteur, liaison et carbone anomérique libre.'),
        ('Q7 • Réduction','Un camarade affirme : « Le saccharose contient du glucose, donc il est réducteur ». Réfuter cette affirmation.'),
        ('Q8 • Formule','Justifier la formule brute C₁₂H₂₂O₁₁ d’un diholoside formé à partir de deux hexoses, puis indiquer la limite de ce calcul pour prévoir sa structure.'),
    ]
    for title,body in questions:
        b.h2(title);b.p(body)
    b.callout('Objectif : savoir expliquer le critère utilisé. Les réponses sont proposées à la page suivante ; le corrigé complet du TD fourni est dans le second document.',title='Conseil de travail',tone='blue')

    # PAGE 21
    b.new_page('MODULE 6 • VÉRIFIER SES RÉPONSES','16. Réponses de l’autoévaluation','reponses')
    b.table(['Item','Réponse et justification'],[
        ('Q1','Non. Un aldotétrose a 4 carbones mais seulement C2 et C3 chiraux : m = 2, donc 2² = 4 stéréoisomères ouverts, répartis en 2 D et 2 L.'),
        ('Q2','Oui, si C5 est bien le dernier centre chiral. La série dépend du centre chiral le plus éloigné du carbonyle, pas de C4.'),
        ('Q3','D-glucose / D-mannose : épimères en C2, donc aussi diastéréoisomères. D-glucose / D-fructose : isomères de constitution aldose/cétose.'),
        ('Q4','Inverser seulement la configuration en C1. En Haworth standard D, le OH anomérique passe de bas (α) à haut (β). Ne pas déplacer les autres OH.'),
        ('Q5','La fonction cétone est en C2 ; C1 est un CH₂OH. L’attaque de C5–OH sur C2 donne un cycle C2–C3–C4–C5–O, donc un furanose.'),
        ('Q6','Donneur : β-D-galactopyranosyl. Liaison C1→OH de C4 du D-glucopyranose. Le C1 du glucose reste libre : lactose réducteur.'),
        ('Q7','Dans le saccharose, le C1 anomérique du glucose est engagé dans la liaison avec C2 du fructose. Il ne peut plus s’ouvrir directement ; les deux anomères sont bloqués.'),
        ('Q8','Bilan formel : 2 × C₆H₁₂O₆ − H₂O = C₁₂H₂₂O₁₁. Cette formule ne précise ni les oses, ni les cycles, ni les configurations, ni les positions de liaison.'),
    ],[1.7,15.3],font=10.3)
    b.h2('Barème personnel de maîtrise')
    b.table(['Résultat','Action conseillée'],[
        ('7–8 réponses justes et justifiées','Passer au TD et vérifier surtout la qualité des dessins.'),
        ('5–6 réponses justes','Revoir les notions correspondant aux erreurs avant de mémoriser les noms.'),
        ('Moins de 5 réponses justes','Reprendre Fischer → Haworth → liaison → pouvoir réducteur dans cet ordre.'),
    ],[6.0,11.0],font=10)
    b.callout('Une réponse juste avec une justification fausse n’est pas maîtrisée. En stéréochimie, la relation entre les structures compte autant que le nom.',title='Critère de réussite',tone='gold')

    # PAGE 22
    b.new_page('MODULE 7 • FICHE DE SYNTHÈSE','17. Les réflexes à conserver','revision')
    b.table(['Avant de rendre une copie…','Vérification'],[
        ('J’ai identifié la fonction','Aldéhyde ou cétone ; numéro du carbone anomérique.'),
        ('J’ai numéroté les carbones','C1 aldéhyde ; C2 cétone pour les 2-cétoses du cours.'),
        ('J’ai justifié D/L','OH du dernier centre chiral, et non signe optique.'),
        ('J’ai nommé la relation','Constitution, énantiomérie, diastéréoisomérie, épimérie ou anomérie.'),
        ('J’ai contrôlé Haworth','Taille du cycle, série, α/β, positions des OH et CH₂OH.'),
        ('J’ai vérifié la liaison','Carbone donneur, carbone accepteur et configuration du donneur.'),
        ('J’ai conclu sur la réduction','Existence ou non d’un carbone anomérique libre.'),
    ],[7.0,10.0],font=10.3)
    b.h2('Sept erreurs fréquentes')
    b.bullets([
        'Confondre nombre de carbones et nombre de centres chiraux.',
        'Écrire D = dextrogyre ou L = lévogyre.',
        'Qualifier d’épimères deux oses de connectivité différente.',
        'Oublier que C2, et non C1, est anomérique dans le fructose.',
        'Placer un CH₂OH exocyclique en C5 du fructopyranose : C6 appartient déjà au cycle.',
        'Déclarer un diholoside réducteur simplement parce qu’il possède plusieurs OH.',
        'Oublier que α-lactose et β-lactose désignent des formes anomériques à l’extrémité réductrice.'
    ])
    b.callout('Aldohexose ouvert : 4 centres, 16 stéréoisomères.\nGlucose : anomère C1 ; fructose : anomère C2.\nSaccharose : non réducteur ; lactose et maltose : réducteurs.',title='Le minimum à savoir restituer')

    # PAGE 23
    b.new_page('POUR ALLER PLUS LOIN','Références et conventions','references')
    b.h2('Source pédagogique directe')
    b.p('TRAVAUX DIRIGÉS N°1 DE BIOCHIMIE STRUCTURALE — LA STRUCTURE DES GLUCIDES, SNV L2, 2026/2027. Document PDF de trois pages fourni par l’utilisateur, comprenant une page de filiation des oses et quatre exercices.')
    b.h2('Ouvrages de référence conseillés')
    refs=[
        'Nelson, D. L. & Cox, M. M. — Lehninger Principles of Biochemistry, 8e éd., Macmillan Learning, 2021. Chapitre consacré aux glucides et aux glycoconjugués.',
        'Berg, J. M., Tymoczko, J. L., Gatto, G. J. & Stryer, L. — Biochemistry, 9e éd., W. H. Freeman, 2019. Structure des glucides et liaisons glycosidiques.',
        'Voet, D., Voet, J. G. & Pratt, C. W. — Fundamentals of Biochemistry, 5e éd., Wiley, 2016. Stéréochimie et structure des osides.',
        'IUPAC–IUBMB — Nomenclature of Carbohydrates (Recommendations 1996). Référence pour la nomenclature et les conventions de représentation.'
    ]
    b.bullets(refs)
    b.h2('Conventions adoptées dans ce support')
    b.bullets([
        'Les oses sont représentés en séries D, sauf lorsqu’un énantiomère L est explicitement étudié.',
        'Les projections de Haworth utilisent l’orientation standard : groupe CH₂OH de référence vers le haut pour les D-oses.',
        'Les H liés aux carbones sont implicites dans les cycles ; tous les carbones utiles au TD sont numérotés.',
        'Une rotation de 180° du cycle fructose dans le saccharose facilite la représentation de la liaison ; elle ne modifie pas la structure.',
        'Les réactions de condensation sont données comme bilans formels. Les tests de réduction sont décrits dans leurs conditions usuelles.',
        'Les noms α-maltose et β-lactose précisent la forme de l’extrémité réductrice imposée par l’énoncé.'
    ])
    b.callout('Ce cours et le corrigé associé sont des supports pédagogiques originaux, et non la reproduction d’un corrigé officiel. Le corrigé explicite les hypothèses nécessaires lorsque l’énoncé est sous-spécifié.',title='Nature du document',tone='blue')
    b.p('Production : python-docx pour les documents Word ; matplotlib pour les figures scientifiques originales. Les illustrations sont intégrées aux fichiers .docx et restent modifiables via les scripts fournis.','Small',before=8)
    return b.save('Cours_Biochimie_L2_Structure_des_glucides.docx')

if __name__=='__main__':
    print(build())
