#!/usr/bin/env python3
"""Genera index.html con todo el contenido escrito en el HTML (sin depender de JavaScript).

Editar los datos de abajo y ejecutar:  python3 build.py
"""
import html, pathlib

def L(x):
    """Texto bilingüe: dict {'es','en'} -> dos spans; str -> igual en ambos idiomas."""
    if isinstance(x, dict):
        return f'<span class="es">{x["es"]}</span><span class="en">{x["en"]}</span>'
    return x

# ---------------------------------------------------------------- publicaciones
ARTICULOS = [
    dict(y=2026, kind={"es": "Artículo", "en": "Article"},
         t="O esvaziamento da raça e o Caribe epistêmico em <i>Úrsula</i> e <i>La maldición</i> (1859)",
         m="<i>Revista Iluminus</i> 3 (1): 1–8. ISSN 2966-1196",
         u="https://doi.org/10.18764/2966-1196v3n1e29852", l="DOI 10.18764/2966-1196v3n1e29852"),
    dict(y=2025, kind={"es": "Ensayo", "en": "Essay"},
         t="La celebración en el borde existencial: literatura caribeña en <i>Los cuentos de Juana</i> (1972) de Álvaro Cepeda Samudio",
         m={"es": "<i>Revista de Estudios Colombianos</i> 65 (enero–junio): 72–79. ISSN 2474-6819",
            "en": "<i>Revista de Estudios Colombianos</i> 65 (January–June): 72–79. ISSN 2474-6819"},
         u="https://colombianistas.org/ojs/index.php/rec/article/download/363/291/2006", l="PDF"),
    dict(y=2024, kind={"es": "Artículo", "en": "Article"},
         t="The Universal Symbolism of River Narratives in Modern Literature",
         m="<i>International Journal of Social Science and Humanity</i> 14 (1): 41–44. ISSN 2010-3646",
         u="https://doi.org/10.18178/ijssh.2024.14.1.1191", l="DOI 10.18178/ijssh.2024.14.1.1191"),
]
TESIS = [
    dict(y=2025, kind={"es": "Tesis de maestría", "en": "MA thesis"},
         t="Aproximación crítica a la novela <i>La maldición</i> (1859) de Manuel María Madiedo: la construcción de las fronteras culturales del Río Grande de la Magdalena",
         m={"es": "Universidad Nacional de Colombia, Maestría en Estudios Literarios. Directora: Carmen Elisa Acosta Peñaloza",
            "en": "Universidad Nacional de Colombia, MA in Literary Studies. Supervisor: Carmen Elisa Acosta Peñaloza"},
         u="https://repositorio.unal.edu.co/items/908231f8-3feb-4d94-8599-e0d5e3bde3ff", l={"es": "Repositorio UNAL", "en": "UNAL repository"}),
]
CREACION = [
    dict(y=2022, t="Civilización y otros cuentos",
         m={"es": "Cuentos. <i>Lua revista</i> 7–8. ISSN 2665-3974", "en": "Short fiction. <i>Lua revista</i> 7–8. ISSN 2665-3974"},
         u="https://civilizacion-y-otros-cuentos.netlify.app", l={"es": "Leer", "en": "Read"}),
    dict(y=2020, t="El mito de Sísifo",
         m={"es": "Cuento. <i>Lua revista</i> 3–4. ISSN 2665-3974", "en": "Short story. <i>Lua revista</i> 3–4. ISSN 2665-3974"}),
    dict(y="", t="El tren de la muerte que cruza por la vida",
         m={"es": "Cuento. Antología de la Red Nacional de Talleres de Escritura Creativa, Ministerio de Cultura. ISBN 978-958-56029-1-5",
            "en": "Short story. Anthology of the National Network of Creative Writing Workshops, Colombian Ministry of Culture. ISBN 978-958-56029-1-5"}),
]

# ---------------------------------------------------------------- ponencias
# (año, título, lugar, nuevo, enlace)
TALKS = [
 (2026, "Cepeda Samudio: entre la palabra y la imagen",
  {"es": "Conferencia y lanzamiento de la Galería Álvaro Cepeda Samudio. III FILBAC, Teatro de Bellas Artes, Barranquilla", "en": "Lecture and gallery launch. 3rd FILBAC book fair, Bellas Artes Theatre, Barranquilla"}, 1, None),
 (2026, "La poesía afrodiaspórica: ancestralidad y Caribe",
  {"es": "Charla a dos voces con Edna Rueda Abrahams. Banco de la República, La Cueva, Barranquilla", "en": "Conversation with the writer Edna Rueda Abrahams. Banco de la República, La Cueva, Barranquilla"}, 1,
  "https://www.banrepcultural.org/barranquilla/actividad/la-poesia-afrodiasporica-ancestralidad-y-caribe"),
 (2026, "Tierra fértil de sangre. Plantación, violencia e identidad en la narrativa del Gran Caribe",
  {"es": "Cátedra Maranhão: Diálogos Latinoamericanos, UFMA – Universidad del Atlántico (virtual)", "en": "Cátedra Maranhão: Latin American Dialogues, UFMA – Universidad del Atlántico (online)"}, 1, None),
 (2026, {"es": "Mesa redonda", "en": "Round table"},
  {"es": "II Congresso Internacional de Literatura Especulativa (CONIFE), UFMA, São Luís", "en": "2nd International Congress of Speculative Literature (CONIFE), UFMA, São Luís, Brazil"}, 1, None),
 (2025, "O Caribe literário colombiano: gênero e mestiçagem na obra de Marvel Moreno",
  "II Congresso Internacional de Linguagem, Literatura e Discurso (CILLID), UFMA, São Luís", 0, None),
 (2025, "La cima que contiene las más contradictorias sustancias: la novela del Caribe decimonónico en <i>La maldición</i> (1859) de Manuel María Madiedo",
  {"es": "CRISOL III, Jornada de jóvenes investigadores en literatura, Universidad Nacional de Colombia", "en": "CRISOL III early-career researchers' day, Universidad Nacional de Colombia"}, 0,
  "https://www.humanas.unal.edu.co/2026/unidades-academicas/departamentos/literatura/eventos/crisol/crisol-iii"),
 (2025, "Proyectos de nación en el siglo XIX: Capmany y Manuel María Madiedo",
  {"es": "Sesión inaugural del ciclo Historias Estelares en la Literatura Hispánica, con Alexander Ortega Marín (UFMA). Universidad del Atlántico y UFMA, 30 de octubre. Organizador y conferencista", "en": "Opening session of the Historias Estelares series, with Alexander Ortega Marín (UFMA). Universidad del Atlántico and UFMA, 30 October. Organizer and speaker"}, 0,
  "https://www.youtube.com/watch?v=pJVAoUS6vMc"),
 (2025, "Crafting Caribbean Knowledge: A Reading of José Félix Fuenmayor's <i>Con el doctor afuera</i> (1967)",
  "Society for Caribbean Studies, Postgraduate Conference", 0, None),
 (2024, "Territorios caribes, una lectura de <i>Con el doctor afuera</i> (1967)",
  {"es": "VII Congreso Internacional Literaturas del Siglo XXI, Universidad del Norte, Barranquilla", "en": "7th International Congress on 21st-Century Literatures, Universidad del Norte, Barranquilla"}, 0,
  "https://www.uninorte.edu.co/web/maestria-en-literatura-y-escrituras-creativas/congreso-literatura-2024"),
 (2024, "Cultural Mapping in Roberto Burgos Cantor's <i>Lo Amador</i>", "Society for Caribbean Studies, Main Conference", 0, None),
 (2024, "La territorialización en el siglo XIX colombiano: el caso del río Magdalena",
  {"es": "VII Encuentro de Egresados, Universidad del Atlántico", "en": "7th Alumni Meeting, Universidad del Atlántico"}, 0, None),
 (2024, "En diálogo con la forma de la novela: el territorio en <i>La vorágine</i>",
  {"es": "Conferencia, Universidad del Atlántico", "en": "Lecture, Universidad del Atlántico"}, 0, None),
 (2023, "La celebración en el borde existencial: literatura caribeña en <i>Los cuentos de Juana</i> (1972)",
  {"es": "XXIII Congreso de la Asociación de Colombianistas, Université de Tours, Francia", "en": "23rd Congress of the Association of Colombianists, Université de Tours, France"}, 0, None),
 (2023, "Las olas de las palabras: la metáfora fluvial en la creación literaria",
  {"es": "VII Simposio Nacional en Estudios Literarios, Universidad del Tolima", "en": "7th National Symposium on Literary Studies, Universidad del Tolima"}, 0, None),
 (2023, "The Coastal Baroque in Three Titles of <i>Los cuentos de Juana</i>",
  "46th Society for Caribbean Studies Annual Conference, De Montfort University, Leicester, UK", 0, None),
 (2023, "The Significance of the Magdalena River in Mid-19th Century Colombia",
  {"es": "Society for Caribbean Studies, Postgraduate Conference (virtual)", "en": "Society for Caribbean Studies, Postgraduate Conference (online)"}, 0, None),
 (2023, "Through the Meanders of the River: A Reading of Cultural Borders",
  {"es": "13th AAAD Interdisciplinary Conference, James Madison University, Virginia (virtual)", "en": "13th AAAD Interdisciplinary Conference, James Madison University, Virginia (online)"}, 0, None),
 (2022, "Narrativa cepediana",
  {"es": "Conferencia magistral, 50 años de <i>Los cuentos de Juana</i>, Universidad del Atlántico", "en": "Keynote, 50th anniversary of <i>Los cuentos de Juana</i>, Universidad del Atlántico"}, 0, None),
]

# ---------------------------------------------------------------- CV
EDU = [
 ("2024–", {"es": "Doctorado en Literatura", "en": "PhD in Literature (in progress)"}, "Universidad de los Andes, Bogotá"),
 ("2025", {"es": "Maestría en Estudios Literarios", "en": "MA in Literary Studies"},
  {"es": 'Universidad Nacional de Colombia. Tesis: <a href="https://repositorio.unal.edu.co/items/908231f8-3feb-4d94-8599-e0d5e3bde3ff">Aproximación crítica a la novela <i>La maldición</i> (1859) de Manuel María Madiedo: la construcción de las fronteras culturales del Río Grande de la Magdalena</a>. Directora: Carmen Elisa Acosta Peñaloza',
   "en": 'Universidad Nacional de Colombia. Thesis: <a href="https://repositorio.unal.edu.co/items/908231f8-3feb-4d94-8599-e0d5e3bde3ff">Aproximación crítica a la novela <i>La maldición</i> (1859) de Manuel María Madiedo: la construcción de las fronteras culturales del Río Grande de la Magdalena</a> (in Spanish). Supervisor: Carmen Elisa Acosta Peñaloza'}),
 ("2025", {"es": "Microcredencial en Fundamentos en Humanidades Digitales", "en": "Micro-credential in Digital Humanities"}, "Universidad de los Andes"),
 ("2025", {"es": "Diplomado en Didáctica para la Enseñanza Universitaria", "en": "Diploma in University Teaching"}, "Politécnico Superior de Colombia"),
 ("2020", {"es": "Licenciatura en Español y Literatura", "en": "B.Ed. in Spanish and Literature"},
  {"es": "Universidad del Atlántico. Tesis meritoria", "en": "Universidad del Atlántico. Thesis awarded distinction"}),
 ("2018-2", {"es": "Intercambio académico durante la Licenciatura", "en": "Exchange semester during the B.Ed."},
  "Universidad Distrital Francisco José de Caldas, sede Macarena, Bogotá"),
 ("2016", {"es": "Técnico en Audiovisuales", "en": "Technical degree in Audiovisual Production"}, "Escuela Distrital de Artes de Barranquilla"),
]
EXP = [
 ("2024–", {"es": "Profesor de Literatura Española, Literatura Latinoamericana de la Colonia y Taller de Inglés; coordinación del Semillero Maskeletras",
            "en": "Lecturer in Spanish Literature, Colonial Latin American Literature and English; coordinator of the Maskeletras research seedbed"}, "Universidad del Atlántico"),
 ("2025–", {"es": "Investigador integrante, Grupo de Investigación Literaria del Caribe GILKARÍ (COL0009199, categoría B MinCiencias)", "en": "Research group member, GILKARÍ Caribbean Literary Research Group (COL0009199, category B, MinCiencias)"}, "Universidad del Atlántico"),
 ("2026", {"es": "Evaluador de manuscrito", "en": "Peer reviewer"}, "Revista La Palabra (Tunja)"),
 ("2023–24", {"es": "Profesor bilingüe de proyectos (PBL), secundaria", "en": "Bilingual project-based learning teacher, secondary school"}, "Innova Schools, Bogotá"),
 ("2021–22", {"es": "Asistente docente de Estudios Literarios", "en": "Teaching assistant, Literary Studies"}, "Universidad Nacional de Colombia"),
 ("2020–24", {"es": "Investigador de estudios afroculturales", "en": "Researcher in Afro-Colombian cultural studies"}, "Fundación Sierra y Folclor, Bogotá"),
 ("2020", {"es": "Coordinador de museo", "en": "Museum coordinator"}, "Museo Etnográfico Miguel Ángel Builes, Medellín"),
 ("2019", {"es": "Taller literario Por las Rutas del Caribe Colombiano", "en": "Creative writing workshop Por las Rutas del Caribe Colombiano"}, "Fundación Pies Descalzos, Barranquilla"),
]
AWD = [
 ("2024–25", {"es": "Apoyo Impacto País para Doctorados", "en": "Impacto País doctoral grant"}, "Universidad de los Andes"),
 ("2024", {"es": "Egresado destacado", "en": "Outstanding alumnus award"}, "Universidad del Atlántico"),
 ("2021–22", {"es": "Becario, Facultad de Ciencias Humanas (tres semestres)", "en": "Graduate fellow, Faculty of Human Sciences (three terms)"}, "Universidad Nacional de Colombia"),
 ("2020", {"es": "Beca en Literatura Oral para Medios Digitales (con el grupo Sierra y Folclor)", "en": "Oral Literature for Digital Media grant (with the Sierra y Folclor group)"}, "IDARTES, Bogotá"),
 ("2017", {"es": "Ganador, concurso de fotografía, VI Cátedra Gabriel García Márquez, con «Prudencio en Macondo»", "en": "Winner, photography contest, 6th Gabriel García Márquez Chair, with «Prudencio en Macondo»"}, "Parque Cultural del Caribe"),
 ("2006", {"es": "Ganador, Concurso de Cuentos «La Jirafa»", "en": "Winner, «La Jirafa» short story contest"}, "La Cueva, Barranquilla"),
]

ORG = [
 ("2026", {"es": "Coorganizador del dossier «Ojo vulgar & Revista Iluminus (UFMA), Brasil 2026: reinventando o imaginário», con la plataforma cultural Ojo Vulgar",
           "en": "Co-organizer of the dossier «Ojo vulgar & Revista Iluminus (UFMA), Brasil 2026: reinventando o imaginário», with the cultural platform Ojo Vulgar"},
  '<i>Revista Iluminus</i> 3 (1), UFMA · <a href="https://periodicoseletronicos.ufma.br/index.php/iluminus/article/download/29799/14847/102286">editorial</a>'),
 ("2026–", {"es": "Comité organizador del dossier sobre literatura del Caribe colombiano (en preparación)",
            "en": "Organizing committee, dossier on Colombian Caribbean literature (in preparation)"}, "<i>Revista Iluminus</i>, UFMA"),
 ("2025–", {"es": "Coinvestigador y gestión editorial de la colección Manglares, proyecto Caribanías: Biblioteca del pensamiento caribeño (política editorial, conformación de los comités editorial y científico, gestión editorial de manuscritos)",
            "en": "Co-investigator and editorial management of the Manglares collection, Caribanías: Library of Caribbean Thought project (editorial policy, formation of the editorial and scientific boards, manuscript management)"},
  "Universidad del Atlántico, VIEPS (CH1139-PS2025)"),
 ("2025–", {"es": "Organizador del ciclo Historias Estelares en la Literatura Hispánica, integrado en 2026 a la Cátedra Maranhão: Diálogos Latinoamericanos",
            "en": "Organizer of the Historias Estelares lecture series, merged in 2026 into the Cátedra Maranhão: Latin American Dialogues"},
  "Universidad del Atlántico – Universidade Federal do Maranhão"),
]

# ---------------------------------------------------------------- fotos
PHOTOS = [
 ("cueva", "w", {"es": "Con Edna Rueda Abrahams, La Cueva, Barranquilla, 2026", "en": "With the writer Edna Rueda Abrahams, La Cueva, Barranquilla, 2026"}),
 ("cueva-retrato", "", {"es": "La Cueva, Barranquilla, 2026", "en": "La Cueva, Barranquilla, 2026"}),
 ("tours", "w", {"es": "XXIII Congreso de Colombianistas, Tours, 2023", "en": "Association of Colombianists, Tours, 2023"}),
 ("leicester-mapa", "", {"es": "Society for Caribbean Studies, Leicester, 2023", "en": "Society for Caribbean Studies, Leicester, 2023"}),
 ("egresados", "", {"es": "Encuentro de Egresados, Universidad del Atlántico, 2024", "en": "Alumni Meeting, Universidad del Atlántico, 2024"}),
 ("ua-juana", "", {"es": "«Reflexiones caribeñas en torno a los gestos de Juana», Universidad del Atlántico", "en": "On Cepeda Samudio's Juana, Universidad del Atlántico"}),
 ("uninorte", "", {"es": "Universidad del Norte, Barranquilla", "en": "Universidad del Norte, Barranquilla"}),
 ("leicester-juana", "", {"es": "Los cuentos de Juana en Leicester, 2023", "en": "Los cuentos de Juana in Leicester, 2023"}),
 ("sabanalarga", "", {"es": "Marvel Moreno, sede Sabanalarga, Universidad del Atlántico", "en": "On Marvel Moreno, Universidad del Atlántico, Sabanalarga"}),
 ("uniandes", "", {"es": "Grabación en la biblioteca, Universidad de los Andes", "en": "Recording at the library, Universidad de los Andes"}),
 ("tours-titulo", "", {"es": "«La celebración en el borde existencial», Congreso de Colombianistas, Tours, 2023", "en": "Paper at the Association of Colombianists, Tours, 2023"}),
 ("lente-caribe", "w", {"es": "Mención de honor, concurso de fotografía «Ruta de tradición por el Carnaval del Atlántico», Lente Caribe, 2017", "en": "Honourable mention, «Ruta de tradición por el Carnaval del Atlántico» photography contest, Lente Caribe, 2017"}),
 ("catedra-ggm", "", {"es": "Con «Prudencio en Macondo», ganadora del concurso de fotografía de la VI Cátedra Gabriel García Márquez, 2017", "en": "With «Prudencio en Macondo», winner of the photography contest, 6th Gabriel García Márquez Chair, 2017"}),
 ("catedra2017", "w", {"es": "VI Cátedra Gabriel García Márquez, Museo del Caribe, 2017", "en": "6th Gabriel García Márquez Chair, Museo del Caribe, 2017"}),
]

# ---------------------------------------------------------------- galería (salas, del repositorio galeria-acs)
SALAS = [
 (1, "La caída", "<i>La casa grande</i> · los soldados", "La violencia sin cuerpos: botas sobre una casa, un rey tumbado entre peones manchados."),
 (2, "La casa del Padre", "<i>La casa grande</i> · el Padre", "Autoridad que sigue mandando cuando el Padre ya no está: el sillón, el sombrero, la ficha que tumba a las demás, el peón en el lugar del rey."),
 (3, "Lo que la hermana no dice", "<i>La casa grande</i> · la Hermana", "El dolor que no se muestra y se queda adentro: en la taza, en los huesos."),
 (4, "Juana", "<i>Los cuentos de Juana</i>", "El juego que hace daño y el cuerpo de Juana que otros se reparten."),
 (5, "Sabanilla", "<i>Los cuentos de Juana</i> · «Sabanilla…»", "El pueblo fantasma dos veces: escrito por Elizabeth, fotografiado por Jesuymar."),
 (6, "Los que esperan", "<i>Todos estábamos a la espera</i>", "Dos cuentos sobre alguien que ya no está: Sammy en el bar y el padre en el estudio."),
 (7, "Sal de la caverna", "<i>La langosta azul</i> (1954)", "Un extranjero llega al pueblo buscando una langosta azul, y la cámara se queda mirando la calle."),
]
GALERIA = "https://galeria-acs.pages.dev/"

# ---------------------------------------------------------------- render
def pub(p):
    kind = f'<span class="tag">{L(p["kind"])}</span> ' if p.get("kind") else ""
    link = f' · <a href="{p["u"]}">{L(p["l"])}</a>' if p.get("u") else ""
    return (f'<div class="pub rv"><div class="yr">{p["y"]}</div><div><h3>{p["t"]}</h3>'
            f'<div class="meta">{kind}{L(p["m"])}{link}</div></div></div>')

def talk_html(y, t, m, new, u):
    link = ""
    if u:
        lab = "video" if "youtube" in u else L({"es": "programa", "en": "programme"})
        link = f' · <a href="{u}">{lab}</a>'
    return f'<div class="talk{" new" if new else ""} rv"><h3>{L(t)}</h3><div class="meta">{L(m)}{link}</div></div>'

PLIEGUE = 2024  # años anteriores a este quedan plegados en el celular

def talks():
    def block(items):
        out, last = [], None
        for it in items:
            if it[0] != last:
                out.append(f'<div class="yearhead">{it[0]}</div>'); last = it[0]
            out.append(talk_html(*it))
        return "\n".join(out)
    recent = [t for t in TALKS if t[0] >= PLIEGUE]
    older = [t for t in TALKS if t[0] < PLIEGUE]
    if not older:
        return block(recent)
    ys = sorted({t[0] for t in older})
    rng = f"{ys[0]}–{ys[-1]}" if len(ys) > 1 else str(ys[0])
    summ = L({"es": f"Ver {rng} ({len(older)} más)", "en": f"Show {rng} ({len(older)} more)"})
    return block(recent) + f'\n<details class="older" open><summary>{summ}</summary>\n' + block(older) + "\n</details>"

def rows(a):
    return "\n".join(f'<div class="row"><span class="d">{d}</span><span>{L(t)}<small>{L(s)}</small></span></div>' for d, t, s in a)

def photos():
    out = []
    for i, (k, cls, cap) in enumerate(PHOTOS):
        out.append(f'<figure class="{cls} rv"><button class="ph-open" data-i="{i}" aria-label="{html.escape(cap["es"])}">'
                   f'<img loading="lazy" src="img/{k}.jpg" alt="{html.escape(cap["es"])}"></button><figcaption>{L(cap)}</figcaption></figure>')
    return "\n".join(out)

def salas_list():
    return "\n".join(
        f'<li><button class="sala" data-n="{n}" aria-pressed="{"true" if n == 1 else "false"}"><b>{n}</b> {t}</button></li>'
        for n, t, s, l in SALAS)

def salas_detail():
    return "\n".join(
        f'<div class="sd" data-n="{n}"{"" if n == 1 else " hidden"}><p class="sn">Sala {n}</p><h4>{t}</h4><p class="src">{s}</p><p>{l}</p></div>'
        for n, t, s, l in SALAS)

tpl = pathlib.Path("plantilla.html").read_text(encoding="utf-8")
out = (tpl.replace("{{ARTICULOS}}", "\n".join(pub(p) for p in ARTICULOS))
          .replace("{{CREACION}}", "\n".join(pub(p) for p in CREACION))
          .replace("{{TALKS}}", talks())
          .replace("{{EDU}}", rows(EDU)).replace("{{EXP}}", rows(EXP)).replace("{{AWD}}", rows(AWD)).replace("{{ORG}}", rows(ORG))
          .replace("{{PHOTOS}}", photos())
          .replace("{{SALAS_LIST}}", salas_list()).replace("{{SALAS_DETAIL}}", salas_detail())
          .replace("{{GALERIA}}", GALERIA)
          .replace("{{N_TALKS}}", str(len(TALKS))))
out = out.replace("{{TESIS}}", "\n".join(pub(p) for p in TESIS))
out = out.replace('class="en"', 'class="en" lang="en"')

SITE = "https://roble.pages.dev"
META = {
 "es": dict(lang="es", url=SITE + "/", locale="es_CO", alt="en_US",
            desc="Doctorando en Literatura, Universidad de los Andes. Literatura del Caribe colombiano y del siglo XIX, territorio y río Magdalena, humanidades digitales."),
 "en": dict(lang="en", url=SITE + "/en/", locale="en_US", alt="es_CO",
            desc="PhD student in Literature, Universidad de los Andes. Nineteenth-century Colombian Caribbean literature, territory and the Magdalena River, digital humanities."),
}
def page(lang):
    m = META[lang]
    h = out
    h = h.replace('<html lang="es" data-lang="es">', f'<html lang="{m["lang"]}" data-lang="{m["lang"]}" data-page="{m["lang"]}">')
    h = h.replace("{{DESC}}", m["desc"]).replace("{{URL}}", m["url"]).replace("{{LOCALE}}", m["locale"]).replace("{{LOCALE_ALT}}", m["alt"])
    if lang == "en":
        h = h.replace('src="img/', 'src="../img/')
    assert "{{" not in h, "quedó un marcador sin reemplazar"
    return h
pathlib.Path("index.html").write_text(page("es"), encoding="utf-8")
pathlib.Path("en").mkdir(exist_ok=True)
pathlib.Path("en/index.html").write_text(page("en"), encoding="utf-8")
print("index.html y en/index.html generados:", len(out), "caracteres")
