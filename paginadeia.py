from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import openai
import PyPDF2
import json
import re

# Descargar recursos de NLTK

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configuración de OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("Key leída:", repr(OPENAI_API_KEY))  # <- esto muestra si tiene espacios o None

openai.api_key = OPENAI_API_KEY

pdf_text = """
    Competencia Lingüística
Actividades
Eje temático
“Consumos problemáticosen jóvenes: las apuestas en
línea”
2
3
Hoja de ruta
La propuesta de
actividades que
presentamos permite
abordar la comprensión
discursiva de una
problemática social
actual: “Consumos
problemáticos en
jóvenes: las apuestas en
línea”.
Desde el punto de vista de la aproximación didáctica de las
prácticas letradas en el Nivel Superior, nuestro objetivo será
acompañar la comprensión de los discursos circulantes en torno
del tema, la puesta en relación de posicionamientos sobre la
cuestión y la producción de textos que puedan dar cuenta del
estado de la problemática.
En definitiva, a través de un tema de importancia social, nuestra
pretensión es acompañar la comprensión de textos en grados
crecientes y la producción discursiva que permita sortear el
examen de ingreso al Colegio Militar de la Nación.
4
Desagregado del corpus: textos, descripciones y
actividades.
5
Texto Descripción Actividad
Imagen gráfica de El juego del
calamar de Hwang Dong-hyuk
(Capítulo I: “Luz verde, luz
roja”).
Serie de televisión
surcoreana que aborda la
vida de un jugador en la
ruina.
El Puntapié. Visualización,
análisis de la temática y de
fragmentos dialógicos.
Cut de streaming: “Clase
turista” perteneciente al sitio
Estación Sur.
Entrevista en la que se
aborda la ludopatía juvenil.
Entrevistada: Julieta
Calmels.
El Puntapié. Escucha
orientada: selección de
segmentos, análisis y puesta
en común.
El juego del calamar de Hwang
Dong-hyuk (Capítulo I: “Luz
verde, luz roja”).
Capítulo de la serie de
televisión surcoreana
En Marcha. Primera escala.
Análisis de la estructura
narrativa y de la temática de la
propuesta.
Ley N° 6330. Ciudad de Buenos
Aires. Prevención y
concientización del juego
patológico y asistencia a
quienes lo padecen y a sus
familiares.
Texto legislativo que aborda
consumos problemáticos
vinculados con los juegos de
azar.
En Marcha. Primera escala.
Deconstrucción de la
estructura de la definición.
Artículo del Ministerio de
Salta
Sitio de difusión de difusión
de las actividades de
gobierno.
En Marcha. Primera escala.
Comparación de conceptos.
Aproximación a las
explicaciones.
Artículo de La Nación Artículo periodístico que
retoma los resultados de una
investigación sobre
apuestas en línea realizadas
por jóvenes.
En Marcha. Segunda escala.
Análisis de paratextos.
Ejercitación con conectores e
inferencias.
Artículo de La Nación
“¿Jugamos una fichita en el
recreo?”
Artículo hipervinculado con
el anterior. Su producción es
periodística bajo
asesoramiento profesional.
En Marcha. Segunda escala.
Elaboración de resúmenes
comparativos de fuentes.
Sitio web de Opina Argentina Sitio de difusión de la
consultora de opinión.
En Marcha. Segunda escala.
Análisis de datos y puesta en
contraste de resultados.
Artículo (UNLP), “Las
apuestas online bajo la lupa”
Sitio de divulgación CyT
(UNLP)
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
Artículo (UBA), “Apuestas
online. Adicción al juego en la
adolescencia”
Sitio de divulgación de la
Facultad de Farmacia y
Bioquímica (UBA)
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
6
Artículo académico
(CONICET), “Apuestas
deportivas online y jóvenes
en Argentina: entre la
sociabilidad, el dinero y el
riesgo”
Sitio Ludopédio,
especializado en
investigaciones vinculadas
con el fútbol.
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
“Pautas para evitar que los
adolescentes apuesten
online”
Sitio del Ministerio de
Justicia.
Apuntes de cierre.
Socialización de
recomendaciones
ministeriales.
Actividades
Objetivos
• Que los ingresantes analicen y comprendan formas de
construcción discursiva de debates propios de las ciencias
humanas y sociales.
• Que los ingresantes comprendan el sentido de las
enunciaciones como fruto de un entramado polifónico y
argumentativo.
• Que los ingresantes se aproximen a discursos acerca de los
consumos problemáticos juveniles, en especial, el tema de las
apuestas en línea.
• Que los ingresantes puedan realizar producciones escritas en
los que den cuenta de una controversia actual.
• Que los ingresantes reflexionen sobre una problemática que
afecta especialmente a las juventudes.
El Puntapié
1. Observar la imagen publicitaria de la serie surcoreana llamada “El
juego del calamar”.
7
2. Luego, preguntarse: ¿han visto la serie?, ¿qué recuerdos generales
tienen de ella?, ¿en qué problema se centra la trama?
3. Vuelvan a la imagen y describan en dos o tres líneas la gráfica de la serie.
Para hacerlo,tengan en cuenta las relaciones que pueda haber entre las imágenes
del afiche y el título de la obra audiovisual.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………...
4. Reflexionar sobre los sentidos a los que alude el título: ¿a qué refiere el
nombre de la serie?, ¿en qué consiste el juego infantil mencionado?,
¿cuál es la diferencia entre el juego infantil y el juego de la serie?
5. Para continuar con la relación juego y vida, escuchar el streaming
“Clase turista” perteneciente al sitio Estación Sur.
Particularmente, se espera que pueda responder de a pares las siguientes
consignas a partir de la entrevista:
a. ¿Quién es la entrevistada y qué cargo ocupa en el gobierno de la provincia
de Buenos Aires?
Audio: "La ludopatía se vuelve problemática cuando altera ámbitos de la vida"
https://radiocut.fm/audiocut/embed/mini/julieta-calmels-ludopatia-se-vuelveproblematica-cuando-altera-ambitos-vida/
8
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
b. ¿Cuál es la representación dominante sobre consumos problemáticos?
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
c. ¿Cuáles son las alertas respecto de los consumos problemáticos que señala
Calmels? Para responder utilice los términos esporádico- permanente.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
d. Extraiga fragmentos en los que la funcionaria mencione el rol del Estado,
de la tecnología y de la publicidad frente al problema. Transcriba dichos
segmentos en el cuadro que presentamos a continuación:
Cita textual1
Rol del Estado
Rol de la tecnología
Rol de la publicidad
e. En un momento, Calmels enuncia: “Muchas veces cortar de golpe con lo
que uno tiene una relación compulsiva, ustedes dijeron sacar el celular,
es parte de lo que hacen los adultos, suele desencadenar grandes crisis”.
Para analizar este fragmento, proponemos delimitar dos conceptos:
Enunciado2
: el enunciado es una manifestación, concreta y real de la actividad
verbal.
1 Se espera trabajar con aspectos vinculados con los PdV alusivos a partir del uso de comillas
que marcan los límites entre el discurso citante y citado.
2
9
Discursos argumentativos: posiciones a las que apunta un segmento o
enunciado.
● Para recuperar el sentido, es necesario analizar el vínculo entre el primer
segmento (A) y la EVALUACIÓN RESULTANTE (B).
● Este tipo de análisis permite arribar al posicionamiento que ofrece el
LOCUTOR -es decir, el responsable de la enunciación- en el discurso. En el
caso del recuadro, podemos decir que estamos frente a una advertencia
de esa figura discursiva.
● Estas continuaciones discursivas constituyen la argumentación a la que apunta el
enunciado
● Por último, las relaciones entre A y B pueden responder a las formas: POR
LO TANTO o SIN EMBARGO de acuerdo con las continuaciones discursivas
que vehiculizan. Así, POR LO TANTO manifiesta una consecuencia y SIN
EMBARGO una restricción.
f. Para sistematizar esta actividad, proponemos el análisis de los
siguientes segmentos:
● “Un consumo se vuelve problemático cuando altera una esfera de
nuestra vida”.
MD: cambios de conductas son signos de alerta PLT (padres y
allegados)...…………………………………………………………………………………………
Posicionamiento enunciativo del LOCUTOR: ………………………………
Considerando esas nociones, es posible afirmar que el sentido de la cita
puede ser analizada retomando el propio enunciado (A) y, a su vez,
identificando los posicionamientos argumentativos suscitados en pos de la
construcción de sentido (B):
Por ejemplo: prohibir el uso del celular suele desencadenar crisis (A) POR LO
TANTO es necesario que los adultos sean cuidadosos (B)”.
10
● “El consumo y la oferta del mercado deben ser regulados por el
Estado”
MD: El Estado es el responsable de las regulaciones SE
…………………………………………………………………………………………………………….
Posicionamiento enunciativo del LOCUTOR: …………………………………..
g. Finalmente, considerando lo analizado anteriormente, ¿cuáles serían las
recomendaciones a los padres?, ¿cuál debería ser el rol del Estado?,
¿cuáles son las políticas o líneas de acción que propone la provincia de
Buenos Aires?
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
6. A modo de cierre, se indica la visualización del capítulo: “Luz verde, luz roja”
de El juego del calamar.
En marcha
Primera escala: encendiendo motores
El juego patológico no es una problemática nueva, sin embargo, las tecnologías
han dado un impulso a su proliferación dado que facilitan el alcance mediante
un click. Por esa razón, el sistema de apuestas digitales constituye una
preocupación de la sociedad en su conjunto. En los últimos años, la difusión de
estos juegos de azar ha ameritado que organismos estatales e instituciones
privadas se manifestaran sobre la cuestión. En particular, en este segmento se
trabajará con el capítulo “Luz verde, luz roja” de la serie, con la Ley N°
6330/2020, con un artículo publicado en el sitio web de la Secretaría de Prensa
y de Comunicación del Gobierno de Salta y con artículo periodístico de La
Nación que difunde una investigación sobre la ludopatía en Argentina.
11
7. El capítulo “Luz verde, luz roja” puede dividirse en dos partes: una en la
que el protagonista está fuera del juego y otra en la que está dentro. Respecto
de cada una de ellas, ¿qué situaciones son narradas en cada segmento? Elabore
en un texto teniendo en cuenta los siguientes requerimientos:
● Una introducción con la mención del audiovisual, la enunciación de la
temática tratada y el objetivo por el que la leemos.
● Un desarrollo en el que sean contrastadas las dos partes en las que puede
dividirse la acción en la serie y los sucesos fundamentales.
● Un cierre en el que se recuperen los objetivos propuestos en la
introducción.
En el primer ……………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
A modo de cierre, ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
8. Para continuar profundizando en el tema, lea el texto de la Ley N°
6330/2020, “Prevención y concientización del juego patológico y asistencia a
quienes lo padecen y a sus familiares”. Asimismo, complete el cuadro con la
información que se solicita.
12
Concepto Definición (40 palabras como máximo)
Juegos de Apuesta
Juego Patológico
Publicidad de juegos de
apuesta
Promoción de juegos de
apuesta
9. De acuerdo con lo analizado en “Luz verde, luz roja”, ¿cuáles de los
conceptos definidos en la ley se abordan en la serie El juego del calamar? Elija
uno de ellos y fundamente en unas pocas líneas.
En la serie El juego del calamar se aborda la idea de ………………………………………..
dado que ………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………...
Link: https://www.argentina.gob.ar/normativa/provincial/ley-6330-123456789-0abc-defg-033-6000xvorpyel/actualizacion
13
10. Las definiciones se componen de un concepto a definir y de una definición
propiamente dicha. Luego de leer el texto del Gobierno de Salta, preste
especial atención a la definición de “ludopatía”.
En efecto, el siguiente esquema facilita la explicación de la idea de “definición”:
Concepto Marca de
definición
Categoría
clasificatoria
Rasgos característicos
Ludopatía se llama impulso
incontrolable
por las apuestas o el azar a pesar de
causarnos pérdidas económicas y
consecuencias negativas para el trabajo,
familia y amigos.
11. Siguiendo el mismo patrón, reconstruya la definición de “juego
recreativo”. Para ello, tomen en consideración el siguiente fragmento del texto
del Ministerio de Prensa y Comunicación del Gobierno de Salta.
Concepto Marca de Categoría Rasgos característicos
Se trata de una adicción que afecta a todas las clases sociales con mayor
incidencia en la adolescencia, especialmente entre los varones. No es lo
mismo el juego recreativo que funciona como actividad de esparcimiento que
el problemático que anula nuestra voluntad haciendo necesario la intervención
de un profesional de la salud.
Link: https://www.salta.gob.ar/prensa/noticias/el-ministerio-de-salud-advierte-sobre-el-incremento-de-la-ludopatia-entreadolescentes-y-jovenes-96004
Se llama ludopatía digital al impulso incontrolable por las apuestas o el azar a pesar de
causarnos pérdidas económicas y consecuencias negativas para el trabajo, familia y
amigos.
14
definición clasificatoria
Juego
recreativo
12. Elabore un texto en el que se comparen las definiciones de “juego
recreativo” y de “juego patológico”. Tenga en cuenta dos cuestiones:
● La definición de “juego” se utilizará como punto de partida de la
introducción.
● Son conceptos en contraste por lo que será necesario un conector que
marque diferencias (“por el contrario”3
, por ejemplo). Utilicen un
marcador textual distinto para dar cuenta de esa función.
● Son definiciones que se enuncian en dos textos del corpus, por lo tanto,
citarlos de acuerdo con la normativa APA4
.
Por “juego” se entiende ………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
3 https://educaciodigital.cat/ioc-batx/moodle/pluginfile.php/14531/mod_page/content/16/Conectores_textuales.pdf
4
https://udesa.edu.ar/como-citar
15
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
A modo de cierre, ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
Segunda escala: a fondo
Esta sección del recorrido de actividades propone, por un lado, la
lectura y el análisis conjunto del artículo de La Nación titulado “El 16% de
los jóvenes reconoce que realiza apuestas online, según un estudio de
Opina Argentina”; por otro, se indica el seguimiento de un hipertexto
inserto en dicho artículo de La Nación. Esta puesta en relación
pretende determinar en qué cuestiones se centra la discusión
acerca de las apuestas en línea.
Actividades
1. Para comenzar esta segunda etapa proponemos la aproximación al
artículo a través del enlace que se adjunta a continuación. Por lo tanto, proceda
a abrir el vínculo y a analizar algunos elementos paratextuales. Particularmente,
confeccionen una lista con tres paratextos que consideren exclusivos de los
artículos periodísticos mediados por tecnologías. Coloquen sus respuestas en el
cuadro diseñado para tal fin.
PARATEXTO FUNCIÓN
Link: https://www.lanacion.com.ar/sociedad/el-16-de-los-jovenes-reconoce-que-realiza-apuestas-onlinesegun-un-estudio-de-opina-argentina-nid30052024/
16
2. Elaboramos una reflexión sobre los rasgos característicos que tienen los
textos que circulan en la web y sobre las exigencias que demandan al lector.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
3. Retomando el título, determine a quién corresponde la afirmación “El 16%
de los jóvenes reconoce que realiza apuestas online”. Fundamente la respuesta
señalando algún elemento presente en el paratexto que estamos analizando.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
4. Dado que estamos frente a un informe presentado a partir de una
investigación, los datos obtenidos permiten sacar algunas conclusiones.
Analice algunas derivaciones posibles que se desprenden de la pesquisa.
Aspecto Porcentaje Relación Inferencia de Opina
Conocimiento de
personas afectadas por
la ludopatía
por lo tanto
Conocimiento entre
personas jóvenes de
sujetos afectados por la
ludopatía
por lo tanto
Personas que admiten
apostar
sin embargo
17
5. Teniendo en cuenta los resultados obtenidos en el esquema podemos
proponer algunas conclusiones. Completamos los espacios en pequeños grupos
y, luego, compartimos las producciones.
● Introducción: proponer una presentación de la consultora Opina
Argentina (seguir el hipervínculo en el cuerpo del texto) y del trabajo
realizado sobre ludopatía.
● Desarrollo: plantear la relación entre ludopatía y juventud siguiendo los
datos obtenidos por la consultora y su análisis en el cuadro del punto
anterior. A su vez, incorporar dos posibles acciones del Estado para
enfrentar la problemática de la que se da cuenta en el estudio.
● Conclusión: delimitar la importancia de la investigación en relación con
el tema abordado.
Opina Argentina ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
En cuanto a la relación entre ludopatía y juventud,
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
En lo vinculado con el rol del Estado, la encuesta ……………………………………………….
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
18
En definitiva, ………..…………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
6. Para cerrar la segunda etapa, seguir el primer hipervínculo en el cuerpo
del artículo que hemos trabajado. Leer el texto. Para ello, centrarse en:
● Título: “¿Jugamos una fichita en el recreo?”.
● Autora y especialistas consultados.
● Destinatarios posibles.
● Formato interactivo del artículo.
● Imágenes ilustrativas.
● Relatos en primera persona.
Luego proponer acciones para enfrentar institucionalmente el problema de las
apuestas en línea.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
Tercera escala: a la pesca de las voces
Esta última sección nos invita a ir un poco más allá. En efecto, busca
profundizar en las ideas que han emergido de las escalas anteriores.
Por ello, para finalizar este recorrido, proponemos la lectura y
análisis de tres textos que abordan la problemática desde la
comunidad académica. Los dos primeros de ellos son artículos de
19
la agencia de noticias de la Universidad Nacional de La Plata (UNLP)
y de la Universidad de Buenos Aires (UBA); el tercero es un artículo
académico de un investigador del CONICET. ¡Exploremos el discurso
un poco más!
Actividades
1. Hasta el momento hemos leído textos de circulación masiva que abordan
un problema acuciante entre los jóvenes: las apuestas en línea. En este
caso, nos aproximamos a la discursividad académica mediante textos
centrados en dicha temática. Para comenzar, siguiendo el link, lean el
texto propuesto por la UNLP. A continuación, responda las siguientes
preguntas:
a. La agencia de la UNLP decide llamar a la sección en la que publica
el artículo “Bajo la lupa” ¿Qué sentidos evoca la frase? De a pares,
expresen dos interpretaciones posibles.
Sentido 1: ……………………………………………………………………………………………………
Sentido 2: ……………………………………………………………………………………………………
b. Observe el texto, ¿cómo se organiza estructuralmente? ¿De qué
manera se despliegan los temas asociados con la problemática? ¿Qué
efecto produce esa organización en el lector?
…………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………..
……………………………………………………………………………………………………………………..
c. En el artículo se señala:
“La ludopatía digital (...) puede afectar a todas las clases sociales y
generar problemas financieros, laborales y familiares”. Proponga un MD
para la afirmación que se construya con PLT.
20
2. Tanto César Barletta como Soledad Fuster señalan que es necesario que se
realicen acciones tendientes a limitar el crecimiento de la adicción al juego en
línea. Complete el cuadro que se adjunta:
Profesional Acción a realizar Entidad encargada
3. Retomando los ejes organizadores podemos decir que dos profesionales
señalan la importancia de ejecutar acciones para atender la problemática. A
partir de las citas, reconstruya el MD.
a. Barletta considera que “es fundamental implementar medidas legales
efectivas para proteger a la población de los riesgos asociados con estas
actividades”.
b. Por su parte, Fuster entiende que es “esencial incorporar una
perspectiva digital en la Educación Sexual Integral”.
MD: ………………………………………………………………………………………………………………
……………….PLT................................................................................................................De
allí que la enunciación resulte asertiva/refutativa (Tachar lo que no
corresponde).
MD: no hay marco normativo para proteger a la población PLT
……………………………………………………………………………………………………………………….
De allí que el posicionamiento del locutor es
……………………………………………………………………………………………………………………….
21
4. Para finalizar con este artículo, complete en los espacios de puntos las
conclusiones obtenidas:
Respecto de la problemática vinculada con las apuestas en línea, tanto Barletta
como Fuster consideran que se deben realizar acciones para su abordaje. Por
un lado, …………………………………………………………………………………………..
……………………….. Por otro, ……………………………………………………………………………………..
…………………………………………………………………………………………………………….…………………
…………………………………………………………………………………………. En consecuencia,
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
5. Lea el copete del artículo “Apuestas online. Adicción al juego en la
adolescencia” de Laura Deluca. A posteriori, respondan las siguientes
preguntas:
a. ¿Cómo se define la adicción al juego?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
b. ¿Qué institución internacional se cita como fuente?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
6. En el apartado que se ocupa de adolescencia, se enuncia: “Nuestra
MD: la incorporaración de la perspectiva digital en la materia ESI resulta
fundamental SE
…………………………………………………………………………………………………………………….
De allí que el posicionamiento del locutor es
………………………………………………………………………………………………………………………
22
investigación bipartidista ha llegado a una conclusión solemne: Meta ha estado
dañando a nuestros niños y adolescentes, cultivando la adicción para aumentar
las ganancias corporativas”,
a. ¿A quién corresponde la cita? ¿Qué rol cumple socialmente el
responsable de la enunciación?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
b. Propongan un MD para ese enunciado. Utilicen palabras vinculadas
con “responsabilidad” o “culpabilidad”.
c. El reclamo hacia la empresa Meta se asienta en el funcionamiento del
mecanismo de recompensa. En no más de cinco renglones describa dicho
mecanismo.
Un mecanismo de recompensa es ………………………………………………………………………..
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
d. Finalmente, Deluca despliega algunas recomendaciones para abordar el
problema. Enúncielas en las líneas de puntos.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
MD: ……………………………………………………………………………………………………………….
……………………………………………………………………………………………………De allí que
la posición del locutor es
……………………………………………………………………………………………………………………….
23
7. Para finalizar esta última escala, les proponemos la lectura de un artículo
académico. Esto supone que el lenguaje del texto será más técnico y que las
ideas sostenidas serán presentadas con mayor rigurosidad porque para la
publicación de artículos académicos es necesaria la aprobación de un tribunal
de expertos. Dicho esto, observe de los elementos paratextuales, completen el
cuadro e indiquen su función de cada paratexto.
Paratexto Función
8. Luego, determine qué paratextos son característicos del discurso académico
y cuáles son transversales a diferentes formas discursivas.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
9. El primer párrafo del apartado “Introducción” cumple una función específica.
Para determinarlo, opte por una de las posibilidades.
El primer párrafo…
a. presenta datos generales sobre una opinión.
b. contextualiza una problemática.
c. describe una serie de problemas vinculados.
Justifique su respuesta utilizando uno de los siguientes conectores: DADO
QUE/ DEBIDO A QUE.
24
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
10. En el segundo párrafo se enuncian factores que inciden en que la
problemática de las apuestas alcance dimensiones importantes. Elija una y
explique por qué ese aspecto incide en el problema.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
11. En el tercer párrafo aparece una citación autoral entre paréntesis: (Etuk et
al.,2022). ¿Qué indica cada uno de los elementos contenidos en dicho signo de
puntuación?
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
12. Pasamos al análisis del quinto párrafo. ¿Qué cuestiones se explicitan allí?
¿Por qué resulta importante esta información en el artículo académico?
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
13. Finalmente, en el último párrafo de la “Introducción” se enuncian tres ejes
de abordaje para el desarrollo. Transcríbalos en los siguientes espacios:
a. ………………………………………………………………………………………………………………………
b. ………………………………………………………………………………………………………..…………….
c. ………………………………………………………………………………………………………..……………
Primer apartado: las apuestas, la diversión y la socialización juvenil masculina
25
d. En el primer párrafo se utiliza la palabra driver, ¿a qué se refiere? ¿De
dónde procederá su uso? Proponga una hipótesis en la línea punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
e. Las motivaciones juveniles para apostar son dos. En un texto de cuatro
líneas, explique qué características, según Branz y Murzi, tienen estos
factores motivantes.
De acuerdo con la investigación de Branz y Murzi (2024), existen dos
grandes factores motivacionales que inciden en las apuesta adolescentes,
por un lado,
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Por otro lado, ………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Segundo apartado: la forma de apreciar lo deportivo
f. En el penúltimo párrafo se utiliza la palabra tipsters, ¿a qué se refiere?
¿De dónde procederá su uso? Proponga una hipótesis en la línea
punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
g. Branz y Murzi (2024) señalan que “Las apuestas, con la posibilidad de
competir en tiempo real, trastocan en buena medida esas formas
26
tradicionales de observar y relacionarse con un partido o evento para los
espectadores, ya que introducen un elemento de cálculo y de eventual
beneficio personal.” Complete el texto fundamentando la afirmación con dos
razones que aporte el artículo.
Branz y Murzi (2024), entienden que …………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
… Se basan en que, por un lado,
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Por otro lado, ………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Tercer apartado: entre el azar y el saber
h. En el último párrafo se utilizan comillas en la palabra “chicanas”, ¿a qué
se debe su uso? ¿Qué significa la palabra? Proponga una hipótesis en la
línea punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
i. El trabajo de campo de Branz y Murzi (2024) se interesa por las estrategias
utilizadas por los jóvenes para potenciar logros en las apuestas. Entre las
respuestas, encuentran que señalan que la suerte y el conocimiento se
vinculan con el éxito. Complete el texto
27
fundamentando cuál de los dos factores es mejor valorado por los
jóvenes. Incluya una cita textual.
El trabajo de campo de Branz y Murzi (2024) demuestra que
……………………………………………………………………………………………………………………….
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
… Sin embargo, el conocimiento …………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
j. ¿Cómo se titulan las conclusiones? Transcriba el título. Luego, relacione
los tres factores considerados fundamentales en la parte final del escrito.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
k. En la conclusión, sobre los entrevistados se afirma: “el origen del dinero
apostado es importante en sus valoraciones: apostar (y perder) dinero
ganado con el trabajo propio es legítimo, mientras que perder dinero
otorgado por los padres o prestado genera más auto-cuestionamientos
morales.“ Proponga un MD para ese enunciado. Utilice palabras vinculadas
con “legitimidad” o “culpabilidad”.
MD: creen que ……………………………………………………………………………………………..
…………………………………………………………………PLT ………………………………………….
28
l. Finalmente, en el párrafo final se enuncia: “las apuestas deportivas entre
los jóvenes tensionan la relación conceptual entre trabajo y ocio”.
Explique brevemente en qué consiste dicha tensión.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
m. Para concluir el abordaje del tema, se propone leer y difundir las
recomendaciones aportadas por el Ministerio de Justicia de la Nación.
Una idea puede ser socializar los factores que inciden en la problemática
y teléfonos de ayuda.
……………………………………………………………………………………………………………………..
De allí que la posición del locutor es
……………………………………………………………………………………………………………………….
29
Ministerio de Justicia
Pautas para evitar que los
adolescentes apuesten online
30
¿Qué son los juegos en línea?
A través de Internet, los juegos en línea son aquellos en los
interviene el azar generando adicción y siendo obligatorio arriesgar
nuestro dinero. Por ejemplo, los casinos online; apuestas deportivas
y loterías virtuales.
La habilidad del jugador queda relegada a un segundo plano. Las
posibilidades de ganar se reducen a un porcentaje ínfimo que está
condicionado por la suerte del participante.
El peligro del consumo problemático
Un consumo problemático implica perder el auto-control dañando
nuestra salud física y/o psíquica y perjudicando los vínculos
personales, familiares o laborales. No importa el objeto de consumo
sino la forma en que la persona se relaciona con él. Puede ser
alcohol, tabaco, drogas, tecnología, compras, alimentación o los
juegos en línea que nos llevan a la ludopatía.
Diversión no es adicción
El juego en línea se vuelve problemático cuando se realiza en forma
recurrente. Se llama ludopatía digital al impulso incontrolable por
las apuestas o el azar a pesar de causarnos pérdidas económicas y
consecuencias negativas para nuestro trabajo, familia y amigos.
Se trata de una adicción que afecta a todas las clases sociales con
mayor incidencia en la adolescencia, especialmente entre los
varones. No es lo mismo el juego recreativo que funciona como
31
actividad de esparcimiento que el problemático que anula nuestra
voluntad haciendo necesario la intervención de un profesional de la
salud.
Cinco factores que hacen populares a los juegos en línea entre los
adolescentes
● Publicidad agresiva en TV y redes sociales. Equipos de fútbol, youtubers,
tiktokers, celebridades e influencers promocionan las apuestas.
● Falta de regulación de la actividad a nivel nacional.
● Facilidad para acceder a medios de pago como billeteras virtuales.
● Disponibilidad de las plataformas virtuales para jugar las 24 horas, los
siete días de la semana.
● Libre acceso, alcanza con ingresar a la página o descargar la aplicación
de la casa de apuestas, cargar nuestros datos, medios de pago y
contactar por WhatsApp para que nos carguen crédito.
Regulación jurídica de los juegos online de apuestas en Argentina
Argentina no tiene una ley nacional sobre juegos en línea. Hay 17
provincias que dictaron su propia legislación. El gran problema
consiste en los sitios ilegales que no están sometidos a ningún
32
control estatal haciendo publicidad por redes sociales donde
incentivan a los adolescentes para que apuesten su dinero.
Los menores de 18 años no pueden participar
en apuestas
Pese a la prohibición, los adolescentes suelen
falsear datos y documentación o crear
perfiles falsos con información de algún
adulto para poder apostar.
Pautas que podrían indicar que un adolescente
abusa de los juegos de azar online
● Cambios significativos en el comportamiento o estado de ánimo como
ansiedad, irritabilidad, cambios de humor repentinos, aislamiento social.
● Pérdida de interés repentina en otras actividades que antes disfrutaba
como deportes, estudios o relaciones sociales y que ahora reemplazar
por el juego online.
● Preocupación constante por el juego como hablar constantemente
sobre apuestas, consultar resultados de manera compulsiva o buscar en
forma reiterada oportunidades para jugar.
● Problemas financieros como dificultades para pagar deudas o rápido
agotamiento de sus recursos económicos sin una explicación clara.
● Aumento del tiempo que dedica al juego.
● Negación o minimización del problema como justificar su
comportamiento o mentir sobre la cantidad de tiempo o dinero que
dedica al juego.
33
Consejos para padres y maestros que quieran prevenir la adicción en
los adolescentes por los juegos en línea:
● Generá una comunicación abierta. Animalos a que te compartan sus
preocupaciones y experiencias.
● Establecé límites. Reduciles el tiempo y el dinero que le dedican al juego.
● Concientizá. Informales sobre los riesgos asociados al juego de azar y a la
ludopatía digital.
● Promové actividades alternativas. Incentivalos a participar en actividades
recreativas, deportivas o artísticas.
● Educá sobre seguridad en línea. Enseñales la importancia de la
privacidad online y el manejo seguro de su información personal.
● Predicá con el ejemplo. Usá equilibradamente los dispositivos
electrónicos y juegos en línea.
● Supervisá el tiempo que pasan frente a las pantallas y qué tipo de juegos
eligen.
● Buscá ayuda profesional si es necesario.
Si querés más información sobre los consumos problemáticos,
podés consultar la ley 26.934, Plan Integral para el Abordaje de los
Consumos Problemáticos (Plan IACOP).
Si vos o alguien que conocés necesita ayuda, llamá al 108 o escribí
"ludopatía" en Boti, el WhatsApp de la Ciudad (11 5050-0147)

LICENCIATURA EN ENFERMERÍA
GUÍA DE ESTUDIO EXAMEN INGRESO
ASIGNATURA: ANATOMÍA FUNCIONAL
INTRODUCCIÓN
La anatomía funcional o fisiológica es una subdivisión del estudio de las estructuras que componen el
cuerpo humano. El estudio de la anatomía funcional está enfocado en las estructuras y órganos y la
forma en que estos funcionan.
Este enfoque se conoce también como anatomía macroscópica, pues su estudio se basa en las
estructuras corporales capaces de verse sin la utilización de un microscopio. La anatomía funcional se
separa de la anatomía microscópica (histología), y la anatomía del desarrollo (embriología) y se divide
a su vez en anatomía sistemática, regional y clínica.
La anatomía funcional relaciona los enfoques de anatomía sistemática, regional y clínica o aplicada,
para estudiar cómo funcionan las estructuras y órganos del cuerpo humano.
El estudio funcional de las estructuras puede dividirse en sistemas, como el estudio funcional delsistema
nervioso central, o en regiones, como la anatomía funcional de la corteza cerebral o del corazón.
De esta manera, se puede estudiar la anatomía funcional de diversas partes corporales como: del
aparato locomotor, desde sus componentes activos como los músculos, hasta los componentes
pasivos que son los huesos y articulaciones. Se estudian también las estructuras funcionales de las
vísceras que proporcionan los movimientos peristálticos que permiten la progresión del contenido
intestinal. Otro importante objeto de estudio de la anatomía funcional es la dinámica del corazón y su
sistema circulatorio.
También encontramos anatomía funcional de la masticación, fonación o deglución, entre muchos otros
estudios.
En general, la anatomía funcional es usada para darlemayor valor y aclararlas descripciones anatómicas
sistemáticas y regionales. A través de este enfoque, se relacionan la forma y la función de todas las
estructuras corporales.
2
OBJETIVO de la GUIA DE ESTUDIOS
Esta guía de estudio tiene como objetivo que usted reconozca, con un enfoque global, a la Anatomía
funcional, junto a la Física y la Química, como fundamentos científicos básicos de las actuaciones en su
futura carrera como profesional de la salud, para la solución de problemas específicos y que valore la
importancia de la anatomía funcional en su formación profesional y la importancia que reviste para el
desempeño de sus funciones específicas.
3
UNIDAD 1: NIVEL de ORGANIZACIÓN CELULAR
1- NIVELES DE ORGANIZACIÓN DE LOS SERES VIVOS
Los seres vivos poseen una estructura corporal altamente organizada que les permite llevar a cabo
todas sus funciones vitales. En ellos es posible observar una jerarquía que puede ser estudiada
considerando tres niveles de organización: química, biológica y ecológica.
NIVEL QUÍMICO: Estudiado en la GUIA DE ESTUDIO de Elementos Básicos de las Ciencias Exactas
NIVEL BIOLÓGICO
(es el que abordaremos en esta guía de estudios)
NIVEL ECOLÓGICO
CELULAR TISULAR
ORGÁNICO
SISTEMÁTICO
INDIVIDUO
POBLACIÓN COMUNIDAD
ECOSISTEMA BIÓSFERA
NIVEL CELULAR Todos los seres vivos están formados por células por esto es tan importante saber
cómo son las células y cómo funcionan. Algunos organismos son unicelulares, ejemplo: bacterias,
mientras que otros son multicelulares el ser humano, por ejemplo.
NIVEL TISULAR Formado por los tejidos. Un tejido es un conjunto de células que tienen una misma
función. Ejemplos: tejido óseo, conectivo, muscular y nervioso.
NIVEL ORGÁNICO Formado por los órganos. Un órgano es la agrupación de varios tejidos, que trabajan
conjuntamente para que el órgano realice una función determinada. Ejemplo: estómago, cerebro,
hígado, corazón.
NIVEL SISTEMÁTICO Formado por aparatos y sistemas. Un aparato resulta de la agrupación de órganos
compuestos por dos más variedades de tejido, por ejemplo: aparato digestivo y cardiovascular;
mientras que un sistema resulta de la agrupación de órganos compuestos por una sola variedad de
tejido, por ejemplo: sistema nervioso y muscular.
NIVEL DE INDIVIDUO Se refiere al organismo multicelular que resulta de la agrupación de aparatos y
sistemas que funcionan juntos de manera coordinada y con gran precisión. Para nuestro estudio, elser
humano.
CÉLULA
Concepto: la célula es la unidad anatómica funcional y genética de los seres vivos. Todas las células
tienen una estructura común: la membrana plasmática, el citoplasma y el material genético o ADN. Se
distinguen dos clases de células: las células procariotas (sin núcleo) y las células eucariotas, mucho más
evolucionadas y que presentan núcleo, citoesqueleto en el citoplasma y orgánulos membranosos con
funciones diferenciadas.
Funciones vitales de la célula
Las células tienen la capacidad de realizar las tres funciones vitales: nutrición, relación y reproducción
4
La función de nutrición. Es la función de captación de materia y energía.
Nutrición heterótrofa. Es la nutrición en la que se capta materia orgánica. En la naturaleza esta
materia solo la producen los seres vivos, por lo tanto, alimentarse de materia orgánica quiere
decir alimentarse de otros organismos, ya sean vivas o muertas. En una primera etapa se produce
la digestión de los alimentos hasta llegar a unas moléculas pequeñas (nutrientes) capaces de
entrar en las células. Dentro de ellas, en unos orgánulos denominados mitocondrias, reaccionan
con el oxígeno (la denominada respiración celular), liberando la energía que precisa el ser vivo. El
resto de las moléculas de nutrientes se utilizan para crear reservas de energía o para generar
estructuras y así crecer.
La función de relación. Es la captación de estímulos y la emisión de respuestas adecuadas.
• Los estímulos pueden ser químicos, táctiles, luminosos o acústicos.
• Las respuestas pueden ser movimientos, secreciones o simplemente crecimientos
direccionales, como sucede con las raíces de las plantas respeto al agua (quimiotropisma) o con
las ramas respeto a la luz (fototropismo)
La función de reproducción. Es la generación de nuevos individuos. Hay dos tipos de reproducción,
la reproducción asexual y la reproducción sexual.
La reproducción asexual. Es aquella en la que los descendentes son genéticamente idénticos al
progenitor, es decir tienen la misma información en su ADN. Un ejemplo de reproducción asexual
es el de una rama de geranio que se rompe y se planta en tierra. Al cabo de un tiempo la rama
genera raíces y se forma un nuevo geranio. En la reproducción asexual sólo hay un progenitor y un
proceso de multiplicación celular en el cual las células hijas son idénticas a la célula madre. Este
tipo de división celular se denomina mitosis.
La forma de las células está determinada básicamente porsu función. La forma puede variar en función
de la ausencia de pared celular rígida, de lastensiones de uniones a células contiguas, de la viscosidad
del citosol, de fenómenos osmóticos y de tipo de citoesqueleto interno.
Membrana celular o plasmática se caracteriza porque:
a. Rodea a toda la célula y mantiene su integridad.
b. Está compuesta por dos sustancias orgánicas: proteínas y lípidos, específicamente fosfolípidos
c. Los fosfolípidos están dispuestos formando una doble capa (bicapa lipídica), donde se encuentran
sumergidas las proteínas.
d. Es una estructura dinámica.
e. Es una membrana semipermeable o selectiva, esto indica que sólo pasan algunas
sustancias (moléculas) a través de ella.
f. Tiene la capacidad de modificarse y en este proceso forma poros y canales
Funciones de la membrana celular
a. Regula el paso de sustancias hacia el interior de la célula y viceversa. Esto quiere decir que
incorpora nutrientes al interior de la célula y permite el paso de desechos hacia el exterior.
b. Como estructura dinámica, permite el paso de ciertas sustancias e impide el paso de otras.
c. Aísla y protege a la célula del ambiente externo.
Citoplasma. Se caracteriza porque:
a. Es una estructura celular que se ubica entre la membrana celular y el núcleo.
b. Contiene un conjunto de estructuras muy pequeñas, llamadas organelos celulares.
c. Está constituido por una sustancia semilíquida.
d. Químicamente, está formado por agua, y en él se encuentran en suspensión, o disueltas,
5
distintas sustancias como proteínas, enzimas, líquidos, hidratos de carbono, sales minerales,
etcétera.
6
e. Funciones del citoplasma
f. Nutritiva. Al citoplasma se incorporan una serie de sustancias, que van a ser transformadas o
desintegradas para liberar energía.
g. De almacenamiento. En el citoplasma se almacenan ciertas sustancias de reserva.
h. Estructural. El citoplasma es el soporte que da forma a la célula y es la base de sus movimientos.
Los organelos u organelas celulares
Son pequeñas estructuras intracelulares,
delimitadas por una o dos membranas.
Cada una de ellas realiza una determinada
función, permitiendo la vida de la célula.
Por la función que cumple cada organelo,
la gran mayoría se encuentra en todas las
células, a excepción de algunos, que sólo
están presentes en ciertas células de
determinados organismos.
Mitocondrias
En los organismos heterótrofos, las mitocondrias
son fundamentales para la obtención de la
energía.
Son organelos de forma elíptica, están
delimitados por dos membranas, una externa y
lisa, y otra interna, que presenta pliegues,
capaces de aumentar la superficie en el interior
de la mitocondria. Poseen su propio material
genético llamado ADN mitocondrial.
La función de la mitocondria es producir la mayor
cantidad de energía útil para el trabajo que debe
realizar la célula. Con ese fin, utiliza la energía
contenida en ciertas moléculas. Por ejemplo,
tenemos el caso de la glucosa.
Esta molécula se transforma primero en el citoplasma y posteriormente en el interior de la
mitocondria, hasta CO 2 (anhídrido carbónico),
H 2O (agua) y energía. Esta energía no es ocupada directamente,sino que se almacena en una molécula
especial llamada ATP (adenosin trifosfato).
El ATP se difunde hacia el citoplasma para ser ocupado en las distintas reacciones en las cuales se
requiere de energía. Al liberar la energía, el ATP queda como ADP (adenosin difosfato), el cual vuelve a
la mitocondria para transformarse nuevamente en ATP.
El material genético: constituido por una o varias moléculas de ADN. Según esté o no rodeado por
una membrana, formando el núcleo, se diferencian dos tipos de células: las procariotas (sin núcleo)
y las eucariotas (con núcleo).
7
Célula procariota
Las células procariotas son aquellas que no tienen núcleo diferenciado, de manera que su ADN se
encuentra localizado en el citoplasma pero no encerrado en una cubierta membranosa como ocurre
con las células eucariotas. Además contienen membrana celular, pared celular, citoplasma y
ribosomas. Prácticamente todas las células procariotas son organismos unicelulares.
Tipos de células procariotas:
 Arqueas: Microorganismos unicelulares muy primitivos. La diferencia a nivel molecular entre arquea
y bacteria es muy elevada, por ello se clasifican en grupos distintos.
 Bacterias: Organismos microscópicos más evolucionados.
En la siguiente imagen se observa una célula procariota, la bacteria Mycrobacterium tuberculosis. Esta
bacteria contiene estructuras adicionales de las básicas, como pili o flagelo.
Las células eucariotas, además de la estructura básica de la célula (membrana, citoplasma y material
genético) presentan una serie de estructuras fundamentales para sus funciones vitales:
a. El sistema endomembranoso: es el conjunto de estructuras membranosas (orgánulos)
intercomunicadas que pueden ocupar casi la totalidad del citoplasma.
b. Orgánulos transductores de energía: son las mitocondrias y los cloroplastos. Su función es la
producción de energía a partir de la oxidación de la materia orgánica (mitocondrias) o de energía
luminosa (cloroplastos).
c. Estructuras carentes de membranas: están también en el citoplasma y son los ribosomas, cuya
función essintetizar proteínas; y el citoesqueleto, que da dureza, elasticidad y forma a las células,
además de permitir el movimiento de las moléculas y orgánulos en el citoplasma.
d. El núcleo: mantiene protegido al material genético y permite que las funciones de transcripción
y traducción se produzcan de modo independiente en el espacio y en el tiempo.
En el exterior de la membrana plasmática de la célula procariota se encuentra la pared celular, que
protege a la célula de los cambios externos. El interior celular es mucho más sencillo que en las
eucariotas; en el citoplasma se encuentran los ribosomas, prácticamente con la misma función y
estructura que las eucariotas pero con un coeficiente de sedimentación menor. También se
encuentran los mesosomas, que son invaginaciones de la membrana. No hay, por tanto, citoesqueleto
ni sistema endomembranoso. El material genético es una molécula de ADN circular que está
condensada en una región denominada nucleoide. No está dentro de un núcleo con membrana y no se
distinguen nucléolos.
CRECIMIENTO Y DIFERENCIACIÓN CELULAR: CICLO CELULAR
El ciclo celular se describe como la secuencia general de acontecimientos que se producen durante la
vida de una célula eucariota y se divide en cuatro fases diferenciadas:
1) La mitosis o fase M, corresponde a la fase de división celular.
8
2) Luego viene la fase G1 (del término gap o intervalo) que ocupa la mayor parte del ciclo.
3) Le sigue la fase S, o fase de síntesis de ADN.
4) Durante la fase G2 se prepara la mitosis con una célula tetraploide que entra en la fase M y en
el comienzo de un nuevo ciclo celular.
La duración temporal del ciclo es variable, y aunque en un cultivo de laboratorio, es de 16 a 24 horas ,
en las células de un organismo pluricelular puede ir de 8 horas a más de 100 días. Algunas células muy
diferenciadas como las neuronas o las células musculares nunca se dividen y asumen un estado
quiescente conocido como fase G0.
El arranque y desarrollo del ciclo es regulado por, señales tanto internas como externas, y dispone de
varios puntos de control que determinan su progreso y si el estado de la célula es correcto,
deteniéndole si no se desarrolla de manera exacta.
Las proteínas que regulan estos procesos reciben el nombre de ciclinas y proteincinasas dependientes
de ciclinas. Se sintetizan durante una fase del ciclo y se degradan por completo en la fase siguiente. Un
ciclina se une específicamente a su o sus proteinacinasas dependientes y fosforilan proteínas nucleares
como las histonas para reorganizar el material nuclear y el citoesqueleto y permitir que la fase
sedesarrolle. Hay también inhibidores de las cinasas dependientes de ciclina que detienen el ciclo
celular en respuestas a señales contrarias a la proliferación, como el contacto con otras células, el daño
del DNA, la diferenciación terminal y la senescencia (o detención definitiva
DIFERENCIACIÓN NORMAL
La diferenciación celular es el proceso por el cual una célula cambia su estructura de manera que pueda
realizar una función específica. Las células bien diferenciadas son células maduras, completamente
relacionadas que están listas para cumplir con su función particular.
Cada tipo celular tiene características, funciones, y lapsos de vida específicos, aunque todos se han
diferenciado de la célula original o zigoto.
Las primeras células de un ser humano procedentes del zigoto son denominadas células
totipotenciales, por ser capaces de diferenciarse en todo tipo de células especializadas; proceso que
comienza a los 4 días de desarrollo. De una célula totipotencial se puede obtener un organismo
funcional. A medida que se diferencian restringen su potencial y se convierten en células
pluripotenciales, que pueden desarrollarse en varios, pero ya no en todos los tipos celulares. De estas
células ya no es posible obtener un organismo.
A medida que avanza la diferenciación se van desarrollando los distintos tipos de tejidos del cuerpo.
Con la especialización y la maduración muchas células pierden la capacidad de reproducción. En cambio
otras denominadas células troncales o células madre conservan la capacidad de división.
En los adultos estas células sólo, pueden diferenciarse en un tipo concreto de célula especializada
(ej.: las células sanguíneas). A estas células troncales indiferenciadas de un tejido que pueden
desarrollarse a células especializadas de dicho tejido se las denomina multipotenciales. (Ej. Las de la
médula ósea que darán lugar a células sanguíneas).
REPRODUCCIÓN CELULAR MITOSIS
La mitosis es el proceso mediante el cual una célula eucariota separa los cromosomas en su núcleo,
dando como resultado dos juegos idénticos. Éstos se llaman “células hijas”.
Esencialmente, una célula (la célula madre)se divide en dos células(las células hijas), que son idénticas
a ella. Esto se hace dividiendo el núcleo de la célula original en dos partes. Las células hijas contienen
el mismo número de cromosomas que la célula madre.
La mitosis es una forma de reproducción asexual. Esta permite que un organismo pueda clonar copias
exactas de la célula original. Este método de reproducción es rápido y eficaz, sin embargo, no da lugar
para la diversidad; ya que todos los productos son idénticos a la célula de la cual se originan.
9
MEIOSIS
La meiosis, por otra parte, es un tipo de reproducción sexual. Es un tipo especial de división celular
necesaria para la reproducción sexual en las eucariotas.
Las células resultantes de la meiosis son gametos o esporas. Los gametos son el esperma y los óvulos
en la mayoría de los organismos(son las célulassexuales), comunestanto en animales como en plantas.
En el proceso de la meiosis, una célula que contiene dos copias de cada cromosoma, uno de la madre
y otro del padre (el cigoto –que es un óvulo femenino fecundado por el esperma masculino-), produce
cuatro células que contienen una copia de cada cromosoma. El resultado es una mezcla única de ADN
materno y paterno. Esto permite que la descendencia sea genéticamente diferente a cualquiera de los
padres. La meiosis introduce la diversidad genética dentro de la población.
DIFERENCIAS CLAVE ENTRE MEIOSIS Y MITOSIS
La mitosis es asexual, mientras que la meiosis es sexual.
En la mitosis, la célula madre se divide en dos; mientras que en la meiosis se divide en cuatro.
En lameiosis, las células hijassólo poseen la mitad de los cromosomas de las células originales;
mientras que en la mitosis la cantidad de cromosomas es igual tanto en las células madres como en
las hijas
La mitosis se lleva a cabo en todos los organismos con células eucariotas, mientras que la meiosis
sólo ocurre en organismos cuya reproducción es sexual (es decir, que necesitan de
TEJIDO
Son conjuntos de células especializadas en realizar una determinada actividad, muy parecida entre sí
y que tienen un mismo origen embriológico. Los principales tejidos son:
 Tejido epitelial (su función es recubrir superficies y segregar sustancias gracias a constituir
glándulas),
 Tejido conjuntivo (su función es unir órganos internos),
 Tejido cartilaginoso (su función es formar estructuras),
 Tejido adiposo (su función es constituir reservas energéticas),
 Tejido óseo (su función es formar estructuras esqueléticas),
 Tejido muscular (su función es hacer contracciones y extensiones),
 Tejido nervioso (su función es captar estímulos y emitir respuestas) y
 La sangre (su función es transportar alimentos, O2 y CO2).
10
Cada tejido está compuesto de células similares que se especializan para llevar a cabo funciones
particulares. En el cuerpo existen 4 tipos principales de tejidos: el tejido epitelial, el tejido conectivo, el
tejido muscular y el tejido nervioso. En general cada tejido del cuerpo tiene su función específica.
El tejido epitelial forma una cubierta protectora para el cuerpo y los órganos. Tiene funciones de
protección, excreción, secreción y absorción. El tejido conectivo lleva a cabo muchas funciones que
mencionaremos luego. El tejido muscular es el responsable de producir movimiento. El tejido nervioso
se especializa en conducir impulsos que ayudan a controlar y coordinar las actividades del cuerpo.
TEJIDO EPITELIAL
El tejido epitelial está distribuido a través de todo el cuerpo, cubriendo todas las superficies internas y
externas, incluyendo los órganos y las cavidades. Siempre tiene una superficie libre expuesta al exterior
o a un espacio interior abierto. El tejido epitelial está entretejido y se adhiere a otras células o
estructuras por una delgada capa llamada membrana basal, contiene poco material intercelular y se
reemplaza continuamente.
11
Las células epitelialesson clasificadastomando en cuenta diferentes criterios. Se clasifican porsu forma,
su función y por la disposición de las capas celulares. Por la forma de sus células se identifican 3 tipos:
escamosas, cuboideas, cilíndricas. Por su función o el revestimiento de órganos o estructuras están: la
capa de membranas mucosas, el epitelio glandular, el endotelio y el mesotelio. Con relación a la
disposición,se clasifican de acuerdo al acomodo o distribución en eltejido:simple (capa celular gruesa),
estratificada (capa gruesa de varias células), seudoestratificada (consta de varias capas pero partiendo
de la superficie de la membrana basal), de transición (varias capas de células aglomeradas, blandas,
flexibles y de fácil distinción).
TEJIDO CONECTIVO
Este tipo de tejido lleva a cabo muchasfunciones, algunas de ellasson:sostén, movimiento, inmunidad
del organismo, producción de sangre y anticuerpos, nutriciónde otrostejidos, etc. Existen distintostipos
de tejido conectivo: tejido conectivo propiamente dicho, tejido conectivo laxo, tejido conectivo denso,
tejido conectivo especializado. La diferenciación de los distintos tipos de tejidos es determinada por su
matriz (material intercelular) y su vascularidad. La vascularidad del tejido conectivo laxo es abundante
(gran cantidad de vasos sanguíneos), en el conectivo denso es poco, mientras el cartílago es avascular
(no contiene vasos sanguíneos). La matriz varía en tipo y cantidad dependiendo del tipo de tejido
conectivo. En la matriz existen 3 tipos de fibras glucoproteícas en proporciones variables: colágenas,
elásticas y reticulares.
a. Fibras colágenas - son de amplia distribución en el cuerpo, no son elásticas y tienen gran fuerza
tensil, como el caso de los tendones. Están formadas por moléculas de colágeno.
b. Fibras elásticas - proveen elasticidad y extensibilidad a los tejidos, permitiendo que estos se
expandan y se contraigan como ocurre con las paredes de las arterias grandes. Las fibras elásticas
están compuestas por una proteína llamada elastina.
c. Fibras reticulares - están compuestas de fibrillas de colágeno, con la diferencia que en las fibras
reticulareslasfibrillasforman una red laxa y delicada, que forman parte de la membrana basal en las
cuales se acomodan las células epiteliales.
Tejido conectivo laxo
Las fibras de este tejido llena espacios entre órganos, no están estrechamente entrelazadas y existen
3 tipos: areolar, adiposo, reticular.
a. Areolar: Es el tejido de mayor distribución en el cuerpo. Es flexible y está atravesado por múltiples
y delicados filamentos que lo hacen resistente a los desgarros, dándole cierta elasticidad. Sirve de
sostén, rodea los órganos, músculos, vasos sanguíneos y nervios. También rodea el cerebro y la
médula espinal con una delicada membrana, además de componer la aponeurosis superficial que
se encuentra en la parte profunda de la piel. El tejido areolar contiene fibroblastos, histocitos,
leucocitos y células cebadas.
b. Adiposo: Es un tejido areolar que posee células que contienen grasa o lípidos. El tejido adiposo actúa
como un empaque elástico y firme, alrededor y entre órganos, fibras musculares, nervios y vasos
sanguíneos de sostén. La función del tejido adiposo es proteger al cuerpo de la pérdida excesiva de
12
calor o de la elevación exagerada de la temperatura. Esto ocurre porque la grasa es mala
conductora de calor.
c. Reticular: Las fibras reticulares están diseminadas en el cuerpo. Forman el armazón del tejido
linfoide, hígado, médula ósea, mucosas respiratorias y el aparato digestivo.
Tejido conectivo denso
Está compuesto de fibras colágenas y elásticas adheridasfirmemente. Tienemenos células que eltejido
conectivo laxo. Se le clasifica en regular o irregular de acuerdo a la disposición de sus fibras y de la
proporción de colágeno y elastina que contenga. Una distribución regular se encuentra en tendones,
ligamentos y aponeurosis. Una disposición irregularse encuentra en la dermis(capa principal de la piel)
y en vainas musculares.
Tejido conectivo especializado
Los tejidos especializados son: cartílago, hueso, dentina, sangre y tejido hematopoyético, además del
tejido linfoide.
Cartílago
Está compuesto por células llamadas condrocitos con fibras colágenas y elásticas en su firme matriz,
que le proveen al cartílago elasticidad y resistencia. Existen 3 tipos de cartílago:
a.hialino - es translúcido por la abundante cantidad de fibras colágenas en su matriz. Es precursor del
sistema esqueletal.
b. fibroso - es denso y resistente al estiramiento. Se encuentra entre las vértebras de la columna
vertebral.
c.elástico - es más elástico que los anteriores porque en él predominan las fibras elásticas. Se
encuentra en la epíglotis, porciones de la laringe, en la trompa de Eustaquio.
Hueso
Es un tejido viviente y firme en constante renovación. Posee vasos sanguíneos y nervios. Hay dostipos:
compacto (forma la capa externa densa de los huesos largos), y esponjoso (forma el tejido más interno
y ligero del hueso).
Dentina
Está relacionada con el hueso, forma los dientes. Es más dura y densa que el hueso.
Sangre
Tejido líquido que transporta, a través del cuerpo, nutrientes a las células y recoge productos de
desecho para su eliminación.
13
Tejido hematopoyético
Es el tejido encargado de producir la sangre en la médula ósea.
Tejido linfoide
Este tejido es de vital importancia para la inmunidad del cuerpo. Se encuentra en los ganglios
linfáticos, timo, bazo y amígdalas.
TEJIDO MUSCULAR
Existen 3 tipos de tejido muscular: estriado, liso y cardiaco. El músculo estriado, también llamado
voluntario, tiene estriaciones transversales y puede ser controlado a voluntad. El músculo liso
(involuntario), no tiene estriaciones y es controlado por el sistema nervioso autónomo. El músculo
cardiaco está exclusivamente en el corazón, y aunque es estriado, no puede ser controlado
voluntariamente como el músculo estriado.
TEJIDO NERVIOSO
Es el tejido más altamente organizado. Su función es iniciar, controlar y coordinar la capacidad del
cuerpo para la adaptación con el medio ambiente. El tejido nervioso se divide en: tejido nervioso
propiamente dicho y neuroglia (tejido conectivo intersticial). La neuroglia es el tejido que enlaza a las
neuronas para formar vías nerviosas. Es el sostén del sistema nervioso. Las neuronas son las células
especializadas del sistema nervioso.
14
CUERPO HUMANO: NIVELES DE ORGANIZACIÓN ESTRUCTURAL. SISTEMAS DEL
CUERPO HUMANO
Un sistema es un conjunto de órganos que realizan una determinada función. Veremos brevemente
la función y los componentes de los distintos sistemas del cuerpo humano.
SISTEMA TEGUMENTARIO (la piel)
Las funciones de la piel son: proteger y aislar al cuerpo de los peligros del medio ambiente, regular la
temperatura corporal y regular la pérdida de agua, interviene en procesos de secreción y percibe
sensaciones que recibe de su entorno. Está formado por capas epidérmicas y dérmicas, glándulas
sebáceas y sudoríparas. Además, se incluye al pelo y las uñas como extensiones de la piel.
SISTEMA ESQUELÉTICO
Protege y da soporte a las partes blandas del
cuerpo. Provee para el movimiento corporal
mediante el tejido conectivo y las articulaciones.
Sus componentesson:loshuesos y las estructuras
cartilaginosas y membranosas que los
acompañan.
SISTEMA MUSCULAR
Interviene en el movimiento del cuerpo, así como en el funcionamiento de otros sistemas, mediante
contracción y relajaciónmuscular. Por ejemplo, los alimentossonmovidos a través delsistema digestivo
por el músculo liso. Al sistema muscular lo componen: músculos, aponeurosis, vainas y bolsas
tendinosas. Existen tres tipos de músculos: liso, estriado y cardíaco.
15
SISTEMA NERVIOSO
Es el sistema que controla al cuerpo en conexión
íntima con el ambiente exterior y con los otros
sistemas. Está compuesto por: el cerebro, la
médula espinal, los nervios craneales, los nervios
periféricos y las terminaciones sensitivas. El
entorno se percibe a través de los sentidos
especiales: vista, audición, olfato, gusto, además
de la piel. La información que reciben estos
sentidos es interpretada por el cerebro.
SISTEMA CIRCULATORIO
Bombea y distribuye la sangre, la cual se encarga del transporte de nutrientes, de gases y de desechos.
Está compuesto por el corazón, los vasos sanguíneos (arterias, venas, capilares) y los vasos linfáticos.
La función delsistema linfático es drenar espaciostisulares, y transportar grasa absorbida en la sangre.
SISTEMA RESPIRATORIO
En este sistema ocurre el intercambio de gases.
Lleva oxígeno a la sangre y elimina dióxido de
carbono de ella. Está compuesto por los senos
aéreos, faringe, laringe, tráquea, bronquios y
pulmones.
SISTEMA DIGESTIVO
Transforma los alimentos en sustancias más simples para ser absorbidas y utilizadas por el cuerpo. Sus
componentesson: eltubo digestivo con susrespectivas glándulas. Recorre el cuerpo desde la boca hasta
el ano.
SISTEMA URINARIO
Es un sistema excretor que forma y elimina la
orina, y mantiene la homeostasis (la
autorregulación que hace el cuerpo para
mantener equilibradas sus composiciones y
propiedades) del cuerpo. Este sistema se
compone de: los riñones, uréteres, vejiga
urinaria y uretra.
16
SISTEMA REPRODUCTOR
Interviene en la reproducción y la perpetuación de la especie. En la mujer consta de: vulva, vagina,
útero,trompasde Falopio yovarios. Enelhombre consta de:uretra,pene, próstata,testículos y vesículas
seminales.
SISTEMA ENDOCRINO
Participa en la regulación química de las funciones corporales. Sus componentes son: el hipotálamo, la
pituitaria (hipófisis), la tiroides, las paratiroides, las suprarrenales, islotes pancreáticos, cuerpo pineal,
ovarios, testículos, y en caso de embarazo, la placenta.
NOCIONES DE PLANIMETRÍA. TÉRMINOS ANATÓMICOS, ESPECIALES, DE POSICIÓN Y
DIRECCIÓN.
REFERENCIAS ANATÓMICAS PARA DESCRIBIR EL CUERPO HUMANO
Como modo de facilitar el trabajo de los
anatomistas, se ha desarrollado un sistema de
referencias que ofrece uniformidad en la
descripción del cuerpo humano. A partir de la
posición anatómica establecida, donde el cuerpo
está parado, erecto, mirada hacia el frente,
brazos extendidos a los lados y palmas de las
manos hacia delante. Este sistema está basado
en: la dirección, los planos, las cavidades y las
unidades estructurales del cuerpo.
SISTEMA DE REFERENCIAS DIRECCIÓN
Se han establecido las siguientes direcciones:
a.Superior - más alto o encima de. Ejemplo: el corazón es superior con respecto al estómago.
b.Inferior - más bajo o por debajo de. Ejemplo: el pie es inferior con respecto a la rodilla.
c.Anterior (ventral) - hacia delante. Ejemplo: el abdomen es anterior a la espalda.
d.Posterior (dorsal) - hacia detrás. Ejemplo: los talones están posterior con relación a los dedos de los pies.
e.Cefálico (craneal) - en dirección hacia la cabeza.
f. Caudal - en dirección opuesta a la cabeza.
g.Medial - más cerca de la línea media del cuerpo.
h.Lateral - hacia los lados, fuera de la línea media.
i. Proximal - cerca del punto de origen. Ejemplo: el pulgar está proximal a la muñeca.
j. Distal - lejos del punto de origen. Ejemplo: el pulgar está distal con respecto al codo.
17
REFERENCIA BASADA EN LA DIRECCIÓN
PLANOS
El cuerpo está dividido en planos que lo atraviesan:
a. Sagital - divide el cuerpo verticalmente en dos lados: derecho e izquierdo.
b. Transversal u horizontal - divide el cuerpo horizontalmente en dos mitades: superior e inferior.
c. Frontal o coronal - divide el cuerpo verticalmente en anterior (ventral) y posterior (dorsal).
d. Referencia basada en los planos
CAVIDADES
El cuerpo humano está dividido en dos cavidades principales, que a su vez están subdivididas. Cavidad
dorsal, compuesta por las cavidades craneal y raquídea, contiene las estructuras del sistema nervioso
que se encarga de coordinar las funciones corporales. Cavidad ventral, contiene las cavidades torácica
y abdominopélvica. Esta cavidad contiene los órganos que se encargan de mantener la homeostasis
del cuerpo.
18
Cavidad Dorsal:
Cavidad craneal: Contiene el cráneo, el cual encierra y protege al encéfalo y sus estructuras nerviosas.
Cavidad espinal o raquídea: Incluye la médula espinal Cavidad
Ventral:
Cavidad torácica o tórax: Se subdivide en:
Cavidades pleurales derecha e izquierda. La cavidad pleural (saco membranoso que cubre los
pulmones) derecha contiene al pulmón derecho, mientras que la izquierda al pulmón izquierdo.
Mediastino El mediastino representa la porción media de la cavidad torácica, el cual se encuentra
separado de las cavidades pleurales mediante una pared de tejido fibroso. El mediastino se encuentra
constituido por el corazón (en su saco pericárdico), la tráquea, los bronquios, el esófago, timo, y una
variedad de vasos sanguíneos, linfáticos y nervios.
Cavidad Abdominopélvica Se subdivide en:
Cavidad abdominal: Contiene el hígado, vesícula biliar, estómago, páncreas, intestinos, bazo, páncreas,
riñones y uréteres.
Cavidad pélvica: Incluye la vejiga urinaria, órganos de la reproducción (en varones: próstata, vesículas
seminales y parte del vaso deferens; en mujeres: útero, conductos uterinos y ovarios) y partes del
intestino grueso (colon sigmoideo y recto).
Referencia
basada en
las
cavidades
corporales
19
HOMEOSTASIS
El cuerpohumanoestá formadopor variossistemas yórganos, cadaunodeellos compuestopormillones
de células. Para mantener una función eficaz y contribuir a la supervivencia del organismo en su
conjunto, estas células necesitan unas condiciones relativamente estables. El mantenimiento de las
con- diciones estables para sus células es una función esencial de todo organismo pluricelular. Los
fisiólogos llaman homeostasis a esta estabilidad relativa.
La homeostasis (homeo = mismo; stasis = permanecer quieto) es una situación en la que el ambiente
interno del organismo se mantiene dentro de determinados límites fisiológicos.
Homeostasis: mantenimiento de los límites fisiológicos, sistemas de retroalimentación.
Para que las células del organismo sobrevivan, la composición de los líquidos que las rodean ha de
mantenerse de una forma precisa en todo momento. El líquido que se encuentra fuera de las células
recibe el nombre de líquido extracelular (extra = fuera) (LEC) y ocupa dos localizaciones principales. El
LEC que ocupa los estrechos espacios existentes entre las células es el líquido intersticial (inter = entre),
liquido intercelular o liquido hístico. El LEC existente en los vasos sanguíneos es el plasma.
El líquido del interior de las células es el líquido intracelular (intra = dentro) (LIC).
El plasma circula desde las arterias a las arteriolas y a vasos microscópicos llamados capilares
sanguíneos. Determinados componentes del plasma abandonan la sangre a través de los capilares y el
líquido circula por los espacios existentes entre las células del organismo. En estos lugares recibe el
nombre de líquido intersticial. La mayor parte de este líquido vuelve a los capilares en forma de plasma
y pasa a las vénulas y a las venas. Una parte del líquido intersticial pasa a microscópicos vasoslinfáticos
llamados capilares linfáticos. En ellos, el líquido recibe el nombre de linfa. En último término, la linfa
vuelve a la sangre. Como el líquido intersticial rodea a todaslas células del organismo,suele aplicársele
el nombre de medio interno. Entre las sustancias disueltas en el agua del LEC y del LIC hay gases,
elementos nutritivos y partículas químicas cargadas eléctricamente llamadas iones, como los de sodio
(Na+
) y cloruo (Cl-
), necesarios para mantener la vida.
Se dice que un organismo está en homeostasis cuando su medio interno:
1) tiene la concentración óptima de gases, elementos nutritivos, iones y agua
2) su temperatura es óptima
3) tiene un volumen óptimo para la salud de las células.
20
Cuando la homeostasis se altera puede producirse una enfermedad. Si los líquidos orgánicos no
recuperan la homeostasis, la consecuencia final puede ser la muerte.
La importancia de la homeostasia del medio interno es crucial para el perfecto funcionamiento del
organismo, yaqueesunapremisa imprescindiblepara queésteseadapte con eficiencia a las condiciones
cambiantes del medio y a sus exigencias representadas en forma de estímulos.
AUTOEVALUACIÓN UNIDAD 1
1) ¿Cuál esla organela u organelo celular en la que se realiza la respiración celular?
2) ¿Cuálesson las dos cavidades que están separadas por el diafragma?
3) ¿En qué cavidad se encuentra el mediastino?
4) ¿Cómo se denomina el espacio intracelular que se encuentra porfuera del núcleo de la célula?
5) ¿Cómo se denomina a las células que estructuralmente poseen dendritas y axón?
6) ¿Cuál esla organela u organelo celular en la que se realiza la síntesis de proteínas?
7) ¿Cómo divide el plano FRONTAL o CORONAL al cuerpo?
8) ¿Cómo se denomina la cavidad que se encuentra por encima del diafragma?
9) ¿A qué se denomina osteocito?
10) ¿Cuál es la característica fundamental de las células eucariotas?
11) Definirtejido y espacio intersticial
12) ¿Qué significa HOMEOSTASIS? Dar porlo menos DOS (2) ejemplos de procesos homeostáticos en el
organismo
13) ¿En qué cavidad se encuentran el encéfalo?
21
UNIDAD 2: SISTEMA LOCOMOTOR
INTRODUCCIÓN.
Todos nosotros nos podemos mover, pero no todos los organismos lo pueden hacer. Por ejemplo,
las plantas mueren en el mismo lugar dónde han nacido. Esto es muy importante, piensa como sería
nuestra vida sin la capacidad de movimiento. ¿Cómo podríamos conseguir el alimento? ¿Cómo
podríamos huir de los peligros? Nuestra capacidad de movimiento se fundamenta en unas
estructuras contráctiles, los músculos, que mueven unas palancas rígidas, los huesos, pero ¿los
huesos son estructuras vivas o son de materia mineral inerte? ¿Por qué muchas personas mayores
tienen dolores relacionados con sus huesos?
El sistema locomotor, es el sistema que nos permite mover y trasladarnos de un lugar a otro
(locomoción). Está constituido por el sistema esquelético y por el sistema muscular.
Elsistema esquelético. Es elresponsable de sostener el cuerpo, protegerlos órganos vitales,servir de
inserción a los músculos y fabricar las células sanguíneas. Está formado por unos elementos
semirrígidos (los cartílagos), unos elementos rígidos (los huesos), y unos elementos flexibles que
permiten la unión entre los huesos (los ligamentos) y entre los huesos y los músculos (los tendones).
Cartílagos. Son estructurassemirrígidas de tejido cartilaginoso, que es una forma de tejido conjuntivo
en cuya sustancia intercelular predomina la sustancia no fibrosa sobre lasfibras. Las célulasinmaduras
del tejido cartilaginoso se denominan condroblastos y las maduras, condrocitos. Un ejemplo de
cartílago es el pabellón de la oreja.
Huesos. Son estructuras rígidas de tejido óseo, que es un tejido derivado del tejido cartilaginoso que
se caracteriza por presentar en su sustancia intercelular un elevado porcentaje en peso de
precipitaciones de fosfato cálcico (60%) y carbonato cálcico (5%) sobre la sustancia orgánica
llamada osteína (30%), que está formada básicamente por fibras de la proteína colágeno. Sus células
inmaduras se denominan osteoblastos y sus células maduras se denominan osteocitos. Además,
presenta unas células denominadas osteoclastos que son las responsables de destruir el tejido óseo
cuando es necesario hacerlo para remodelar el hueso. Los osteocitos ocupan unas pequeñas
lagunas alargadas que hay en la materia extracelular de naturaleza calcárea antes mencionada. Los
huesos presentan unos canales denominados canales de Havers por dónde pasan las arterias, venas,
nervios y vasos linfáticos, que mantienen vivas las células óseas.
En los huesos largos se distingue la caña (diáfisis) que es de tejido óseo compacto y los dos extremos
(epífisis) que son de tejido óseo esponjoso. En el interior de la diáfisis está la denominada médula ósea
amarilla (el tuétano de los huesos) formada por célulasrepletas de grasas y en los espacios vacíos de las
22
epífisis se encuentra la médula ósea roja formada por las células madres de los glóbulos rojos y de los
glóbulos blancos de la sangre.
Los contactos entre huesos se denominan ARTICULACIONES. Estas pueden ser de tres tipos:
Inmóviles. Son las que no permiten movilidad entre los huesos. Un ejemplo son las articulaciones que
hay entre los huesos del cráneo, las denominadas suturas.
Semimóviles. Son las que permiten una cierta movilidad entre los huesos. Un ejemplo son las
articulaciones que hay entre las vértebras, que presentan un disco intervertebral cartilaginoso.
Móviles. Son las que permiten una gran movilidad entre los huesos, como pasa en la articulación de la
rodilla, que se encuentra toda ella dentro de una cápsula de tejido conjuntivo llena de un líquido
amortiguador denominado líquido sinovial.
Ligamentos. Son las estructuras de tejido conjuntivo que unen los huesos entre sí.
Tendones. Son las estructuras de tejido conjuntivo que unen músculos entre sí o músculos con huesos
El esqueleto humano. Está constituido por 206 huesos.Unosforman el esqueleto axial (cráneo, columna
vertebral, costillas y esternón) y el resto forman el esqueleto apendicular (extremidades superiores,
cintura escapular, extremidades inferiores y cintura pelviana).
23
24
1.a. ESQUELETO AXIAL: formado por las estructuras próximas al eje longitudinal del cuerpo: estará
formada por CABEZA, COLUMNA VERTEBRAL y TÓRAX.
1.b. ESQUELETO APENDICULAR: formado por la
CINTURA ESCAPULAR (articula el esqueleto axial con las EXTREMIDADES ……………………. CINTURA PÉLVICA
(articula el esqueleto axial con las EXTREMIDADES …………………….
CABEZA: Formada por el CRANEO y la CARA
CRANEO
CANTIDAD DE
HUESOS DENOMINACIÓN UBICACIÓN/FUNCIÓN/CARACTERÍSTICAS
NÚMERO LETRA
Forman la bóveda propiamente dicha
Articulan la mandíbula inferior y albergan el
oído medio e interno.
Anterior. Porción superior de los orbitales
oculares.
Sostén de las cavidades nasales
Cruza la base del cráneo y se articula con
todos los huesos. En él está la denominada
silla turca en donde se asienta la hipófisis
1. Tache dentro del paréntesis la opción que NO sea correcta)
a. Occipital, temporales, parietales y frontal son huesos (CORTOS – PLANOS* – LARGOS)
(* PLANOS Y ANCHOS ES LO MISMO)
b. La principal función de los huesos del cráneo es (PROTECCIÓN – MOVIMIENTO)
c. Las articulaciones de los huesos del cráneo se denominan (DIARTROSIS – ANFIARTROSIS –
SINARTROSIS) que son articulaciones (SEMIMÓVILES – INMÓVILES – MÓVILES)
Complete el cuadro
CARA
DENOMINACIÓN UBICACIÓN/FUNCIÓN/CARACTERÍSTICAS
Maxilar superior Son 2 (DOS). Insertan los dientes superiores.
Son 2 (DOS). Forman los pómulos.
Constituyen el esqueleto duro de la nariz
Se encuentran en la cara interna de las orbitas.
Cornetes inferiores
Contribuyen a formar el paladar óseo de la boca y lasfosas
nasales
Maxilar inferior o
………………….
Se insertan los ……………………………………
Forma el tabique nasal junto con el etmoides
2. En total, ¿cuántos son los huesos de la cara?
3. ¿Cuál es el único hueso con articulación móvil? ¿Cómo se denominan a las articulaciones móviles?
¿cuál es la función de esta articulación en este hueso?
25
4. ¿Cómo se articula la cabeza con la columna vertebral?
COLUMNA VERTEBRAL: “Es el pilar óseo articulado que recorre longitudinalmente el tronco”.
5. ¿Cuáles son las cavidades que conforman el tronco?
La función de la columna vertebral es de sostén, mantenimiento y protección. Está dividida en 5
(CINCO) regiones y posee 4 (CUATRO) curvaturas y entre 32 (TREINTA y DOS) a 33 (TREINTA y TRES)
vértebras.
COLUMNA
VERTEBRAL
CURVATURAS
2 (DOS) hacia adelante denominadas …………………………
2 (DOS) hacia atrás denominadas ………………………………
REGIONES
DENOMINACIÓN DE LA
REGIÓN
NUMERO DE
VERTEBRAS
CERVICAL
12
LUMBAR
SACROCOCCÍGEA
vértebras sacras
3 a 4
vértebras
coccígeas
6. Complete sobre las líneas punteadas.
a. Toda vértebra está constituida por CUERPO VERTEBRAL, un AGUJERO NEURONAL y diversas
…......................................................., una es posterior o espinosa y dos laterales o transversas.
b. La superposición de los agujeros neurales forman el................................................................. , que
es donde se aloja la médula espinal.
7. ¿Cómo se denomina según su movimiento las articulaciones de las vértebras?
8. ¿Cuál es la función del disco fibrocartilaginoso presente entre los cuerpos de las vértebras?
9. Tache dentro del paréntesis la opción que NO sea correcta. Las vértebras son huesos (LARGOS –
CORTOS – ANCHOS)
CINTURA ESCAPULAR
Está integrada a la cavidad torácica y permite la articulación con las extremidades superiores.
10. Enumere los huesos que forman la cintura escapular
26
HUESOS DEL TORAX: El tronco está formado por dos cavidades, la cavidad torácica y la cavidad
abdominal. Los huesos del tórax, forman la caja torácica que aloja a los órganos vitales como son el
corazón y los pulmones. Esta cavidad está separada del abdomen por el músculo denominado
……………………………….
11. Complete en el siguiente esquema con las siguientes referencias que se le dan a continuación:
cartílago dorsal, columna vertebral, esternón, costillas flotantes, clavícula, costillas verdaderas,
omoplato o escápula, apéndice xifoides, costillas falsas.
12. Complete sobre la línea de puntos. El tórax está formado por 7 (SIETE) pares de costillas
…................................................que se unen al esternón mediante un cartílago. También contiene 3
(TRES) pares de costillas........................................................ que se unen en forma indirecta al esternón,
mediante el cartílago del par anterior y dos pares de costillas.................................................. que no se
unen al esternón.
13. Tache dentro del paréntesis la opción que NO sea correcta. El esternón es un hueso (LARGO –
CORTO – PLANO). Las costillas son huesos (LARGOS –CORTOS – ANCHOS)
14. ¿Cuál es la principal función de los huesos anchos o planos como el esternón?
15. ¿Cuáles son las vértebras que forman la parte posterior de la caja torácica?
CINTURA PÉLVICA: Está formado por un único hueso, el coxal o ilíaco, formado a su vez por tres
huesos fusionados entre sí: el ilion, el isquion y el pubis
16. Ubique en el siguiente esquema los huesos de la cintura pélvica
27
17. Completar los siguientes cuadros
EXTREMIDADES SUPERIORES
CANTIDAD DE HUESOS NOMBRE DE LOS HUESOS
BRAZO
ANTEBRAZO
MANO
EXTREMIDADES INFERIORES
CANTIDAD DE HUESOS NOMBRE DE LOS HUESOS
MUSLO
PIERNA
PIE
18. ¿Qué es la rótula? Describa la articulación de la rodilla
19. Describa la articulación del codo y la articulación de la cadera
20. Tache dentro del paréntesisla opción que NO sea correcta. El fémur, la tibia y el peroné son
huesos (LARGOS –CORTOS – PLANOS).
21. Describa un hueso largo. Grafique colocando las siguientes referencias: diáfisis, epífisis, canal
medular, tejido óseo compacto, tejido óseo esponjosos, metáfisis. Indique donde se encuentra la
médula ósea roja y la médula ósea amarilla.
22. ¿Cuál es la función de la médula ósea amarilla y cuál es la función de la médula ósea roja?
EL SISTEMA MUSCULAR.
Es el sistema que realiza los movimientos gracias a la capacidad de contracción que tienen sus células,
las también denominadas fibras musculares. Estas son alargadas, presentan varios núcleos y
contienden muchas miofibrillas contráctiles formadas por las proteínas actina y miosina. Las fibras
musculares se unen y forman fascículos musculares y estos, a su vez, se unen y forman los músculos.
Estos están recubiertos por un tejido conjuntivo llamado perimisio cuya prolongación en los extremos
del músculo forma los tendones que sirven para unirlo a los huesos. Se distingue tres tipos de tejido
muscular:
28
Tejido muscular estriado. Se llama así porque visto al microscopio presenta un aspecto estriado debido
a la alternancia de las fibras de actina y las fibras de miosina. Es de contracción voluntaria. Forma los
músculos que actúan en la locomoción.
Tejido muscular lisnos. Es de contracción involuntaria. Constituye los músculos que mueven las
vísceras como son el estómago, el intestino, las vías respiratorias, etc.
Tejido muscular cardíaco. Presenta estructura estriada y contracción involuntaria. Sólo está en el
corazón.
Los músculos del cuerpo humano. Se pueden diferenciar los de la cabeza, los del cuello, los del tronco,
los de las extremidades superiores (brazo y antebrazo que es la parte que va del codo a la mano) y los
de las extremidades inferiores (muslo y pierna que es la parte que va de la rodilla al pie)
Ni los huesos ni las articulacionestienen la capacidad de ejercer la fuerza necesaria para el movimiento;
esta función queda a cargo de otro de los componentes del sistema locomotor que son los MUSCULOS
En general los músculos se unen a los huesos a través de los tendones, uno de sus extremos se inserta
al hueso fijo, que actúa como punto de apoyo, y el otro, en el hueso que se desplaza.
29
Ejemplo de movimientos realizados por los músculos:
1. Locomoción
2. Cardíacos (sístole y diástole) - músculo cardíaco -
3. Peristálticos (intestino, por ejemplo) - musculatura lisa de las vísceras -
1. ¿Qué tipo de tejido es el de los tendones?
De acuerdo con su organización, con los órganos de los cualesforman parte (ubicación) y con la función
que cumplen, se reconocen los siguientes tipos de músculos: esquelético, liso y cardíaco.
2. Complete el siguiente cuadro respecto a los tipos de músculos:
Músculos Ubicación Características
de la célula
Control nervioso (estimulación)
Involuntario - voluntario
Esquelético
Liso
Cardíaco
3. La contracción del bíceps produce el movimiento de FLEXION del antebrazo VERDADERO FALSO
4. FLEXION es sinónimo de ABDUCCIÓN VERDADERO FALSO
5. COMPLETE EL SIGUIENTE CUADRO
MÚSCULOS UBICACIÓN
Frontal y Temporales
Recto femoral
Escalenos
Sóleo
Sartorio
Deltoides
Esternocleidomastoideo
Gemelos
Tríceps
Trapecio
30
6. ¿Qué es el tendón de Aquiles?
7. ¿Cuáles son los músculos involucrados en la mecánica respiratoria?
8. Complete el siguiente cuadro según la forma de los músculos
MÚSCULOS UBICACIÓN
(en términos generales)
CANTIDAD DE MOVIMIENTO
(tache lo que no corresponda)
CANTIDAD DE FUERZA
(tache lo que no corresponda)
Cortos Mucho - Poco Mucha – Poca
Anchos Mucho – Poco Mucha – Poca
Largos Mucho - Poco Mucha - Poca
9. ¿Cómo se denominan las proteínas que actúan en la contracción muscular?
10. ¿Dónde se encuentra el músculo MASETERO y que función cumple?
AUTOEVALUACIÓN
1) ¿Qué tipo de huesos están conformados estructuralmente por una diáfisis, epífisis y metáfisis, los
huesos largos, los huesos cortos o los huesos planos?
2) Enumere los CUATRO (4) huesos que forman parte de la articulación de la rodilla
3) ¿Cómo se denomina al músculo compuesto por fibras largas, rodeadas de una membrana
celular llamada sarcolema?
4) ¿Qué es la escápula y con qué otro nombre se la conoce?
5) ¿Cuáles el hueso que constituye el principal sostén de las cavidades nasales?
6) ¿Qué tipo de músculo es el que forma la capa interna de las vísceras o de las paredes de los vasos?
7) ¿En qué parte de las extremidadesinferioresse encuentra el fémur?
8) Según su movimiento, ¿qué tipo de articulacionesse dan entre los huesos planos?
9) ¿Cuántos y cuáles son los huesos que conforman el cráneo?
10) ¿Qué es el deltoides? ¿Dónde se encuentra?
11) ¿Qué es el ATLAS? ¿Dónde se encuentra? (2 puntos)
31
12) Tache dentro de cada uno de los paréntesisla opción que no sea correcta (3 puntos)
La articulación de la cadera es una (ANFIARTROSIS – DIARTROSIS – SINARTROSIS) y tienen gran
movilidad. Las articulaciones entre los huesos del cráneo son (ANFIARTROSIS – DIARTROSIS –
SINARTROSIS). La sínfisis pubiana es una (ANFIARTROSIS – DIARTROSIS – SINARTROSIS),
tiene poca movilidad.
32
UNIDAD 3: SISTEMA CARDIOVASCULAR
INTRODUCCIÓN
El aparato circulatorio es el encargado de distribuir el oxígeno y los alimentos por todo el
cuerpo, y de recoger el dióxido de carbono y los productos de excreción procedentes de
las células. Está formato por:
 Un líquido circulatorio denominado sangre,
 Una bomba que impulsa la sangre denominada corazón, y
 Unos conductos denominados vasos sanguíneos (arterias, venas y capilares
sanguíneos) y vasos linfáticos.
Está formada por un líquido denominado plasma sanguíneo y por variostipos de elementos
celulares: los glóbulos rojos, los glóbulos blancos y las plaquetas.
Plasma. El plasma está formado básicamente por agua y por determinadas sustancias
disueltas (sales minerales, glucosa, lípidos y proteínas ). El plasma sin proteínas se
denomina suero sanguíneo.
 Glóbulos rojos,
hematíes o eritrocitos
son células sin núcleo y llenas de
hemoglobina, que es una proteína
capaz de captar y liberar oxígeno.
 Glóbulos blancos o leucocitos pueden
tenerfunción fagocítica (como hacen los
tipos neutrófilos, eosinófilos y monocito
s), función de producir anticuerpos (lo
hacen los linfocitos) o productora de
vaso dilatadores (lo hacen los basófilos).
 Plaquetas o trombocitos son
fragmentos de citoplasma que
contienen una sustancia que inicia la
coagulación de la sangre.
Los vasos sanguíneos. Se diferencian tres tipos denominados arterias, venas y capilares
sanguíneos.
Arterias. Son los vasos que llevan sangre desde el corazón a otras partes del cuerpo. Son
elásticas gracias a tener una gruesa capa muscularintermedia. Todas ellas,menosla arteria
pulmonar, llevan sangre rica en oxígeno.
Venas. Son los vasos que llevan sangre hacia el corazón. Son muy poco elásticas. Por ello
precisan tener unas válvulasinternas para evitar elregreso de la sangre. Todas ellas, menos
la vena pulmonar, conducen sangre pobre en oxígeno.
Capilares sanguíneos. Son unos vasos extremadamente delgados, originados por las
sucesivasramificaciones de arterias y venas, que unen elfinal de las arterias con el principio
de las venas. Sus paredes son tan delgadas que permiten el intercambio de gases en los
pulmones, la entrada de nutrientes en el intestino y la salida de los productos de excreción
en los riñones.
33
El conjunto de todos los vasos sanguíneos constituyen un aparato circulatorio doble y
completo. Se llama doble porque compran dos circuitos, que son el pulmonar y el general.
Se llama completo porqué en el corazón no hay mezcla de sangre oxigenada y no
oxigenada, concretamente la sangre oxigenada pasa por la parte izquierda del corazón y
la no oxigenada pasa por la parte derecha. . El aparato circulatorio. El conjunto de todos
los vasos sanguíneos constituyen un aparato circulatorio doble y completo . Se
llama doble porque compran dos circuitos, que son el pulmonar y el general. Se
llama completo porqué en el corazón no hay mezcla de sangre oxigenada y no oxigenada,
concretamente la sangre oxigenada pasa por la parte izquierda del corazón y la no
oxigenada pasa por la parte derecha.
Funcionamiento del aparato circulatorio sanguíneo.
Básicamente depende del funcionamiento del corazón. El corazón humano presenta
cuatro cámaras: dos que reciben sangre, las aurículas, y dos que expulsan sangre, los
ventrículos. Entre la aurícula izquierda y el ventrículo izquierdo está la válvula mitral que
regula el paso de la sangre. Entre la aurícula derecha y el ventrículo derecho está la válvula
tricúspide.
El corazón funciona como una bomba aspirante e impelente. Para lo cual realiza
movimientos de relajación (diástoles) seguidos de movimientos de contracción (sístoles).
El ciclo cardíaco (latido) dura 0,8 segundos y presenta 3 etapas:
Diástole. Las paredes de las aurículas y de los ventrículos se relajan y aspiran la sangre, la
cual llega por las venas. La sangre que llena las arterias no retrocede gracias a que
las válvulas semilunares (también denominadas sigmoideas) que hay en su inicio están
cerradas. Esta fase dura 0,35 segundos.
Sístole auricular. Las paredes de las aurículas se contraen, se abren las válvulas auriculoventriculares (mitral y tricúspide) y la sangre pasa a los ventrículos. Esta fase dura 0,15
segundos.
Sístole ventricular. Las paredes de los ventrículos se contraen y la sangre del ventrículo
izquierdo pasa a la arteria aorta, hacia el resto del cuerpo, y la del ventrículo derecho pasa
a la arteria pulmonar hacia los pulmones. Esta fase dura 0,3 segundos.
34
Principales arterias y venas del aparato circulatorio sanguíneo.
Las principales venas son las venas pulmonares que llevan sangre procedente de los
pulmones hasta la aurícula izquierda, y las venas cavas (la superior y la inferior) que llevan
sangre desde el resto del cuerpo hasta la aurícula derecha. Las principales arterias son
las arterias pulmonares que desde el ventrículo derecho envían sangre a los pulmones
y la arteria aorta que desde el ventrículo izquierdo envía sangre al resto del cuerpo.
Vasos sanguíneos que irrigan al corazón
35
El sistema cardiovascular es considerado sistema, porque está formado por corazón, vasos
sanguíneos (arterias, venas y capilares) y sangre
REVISIÓN GENERAL: PREGUNTAS Y SUS RESPUESTAS CORAZÓN
1. ¿Dónde está ubicado el corazón? Mediastino central
2. ¿Qué son el pericardio, miocardio y pericardio?, ¿Quién reviste las cavidades del
corazón?, y cuál es el músculo cardíaco?
Paredes musculares de gran resistencia que forman el corazón. El endocardio reviste las
cavidades cardíacas. El miocardio es el musculo cardiaco
36
3. ¿Por qué se afirma que el corazón es un órgano hueco? Especifique la estructura cardíaca
Es un órgano hueco porque está formado por cuatro cavidades. Dos aurículas (derecha e
izquierda) y dos ventrículos (derecho e izquierdo)
4. ¿Cómo se comunican entre sí, las aurículas con los ventrículos? Especifique. Las
aurículas se comunican con los ventrículos por medio de válvulas. La válvula tricúspide
comunica auricula derecha con ventrículo derecho y la auricula izquierda con el ventrículo
izquierdo se comunican por medio de la válvula bicúspide o mitral.
5. ¿Qué son las válvulas sigmoideas o semilunares? Son válvulas que comunican el
ventrículo derecho con arteria pulmonar y ventrículo izquierdo con la aorta
6. ¿Cómo se denominan los movimientos del corazón que se suceden rítmicamente y
determinan la frecuencia respiratoria? Sístole y diástole
7. ¿Cómo se denomina al movimiento cardíaco relacionado con la contracción de alguna de
las cavidades cardíacas? Sístole
8. ¿Qué sucede cuando se produce la sístole ventricular? Se vacía el ventrículo
9. ¿A qué se denomina automatismo cardíaco? El automatismo cardíaco es la capacidad
que tienen las células del miocardio de latir por sí mismas. Esta propiedad es única del
corazón, ya que ningún otro músculo del cuerpo puede desobedecer las órdenes dictadas
por el sistema nervioso central. Algunos autores consideran al cronotropismo y al
automatismo cardíaco como sinónimos fisiológicos.
10. ¿Dónde nace el impulso (nervioso) cardíaco? ¿Dónde se encuentra este centro
impulsor? Nace en el nódulo sinoauricular o sinusal (marcapasos) que se encuentra en la
auricula derecha
11. Luego de originado el impulso nervioso hacia donde se propaga la conducción eléctrica?
Se propaga a otrossistemas de conducción que son: nódulo aurículo-ventricular, haz de His
y fibras de purkinje
12. En el siguiente esquema usted verá, a la izquierda, las cavidades del corazón. Ubique
en el esquema de la derecha lassiguientesreferenciasrelacionadas con el impulso eléctrico
del corazón (AUTOMATISMO)
a) fibra de Purkinje, b) rama izquierda del Haz de His, c) nódulo sinoauricular (SA) o sinusal
d) Haz de His e) nódulo auriculo ventricular (AV), f) rama derecha del Haz de His
Rama derecha haz de His
Rama izquierda haz de His
Fibra de Purkinje
Nodulo auriculoventricular
Nodulo sinusal
37
13. El automatismo es de característica voluntario o involuntario? Involuntario
14. ¿Cómo se denominan los vasos sanguíneos que ingresan a cada una de las aurículas?
Venas cavas las que ingresan a la aurícula derecha y venas pulmonares las que ingresan a
la aurícula izquierda
15. ¿Cómo se denominan los vasos sanguíneos que salen de cada uno de los ventrículos?
Arteria pulmonarla que sale del ventrículo derecho y arteria aorta la que sale del ventrículo
izquierdo
16. ¿Cómo se denominan los vasossanguíneos que irrigan al corazón? ¿Para qué lo irrigan?
Son las arterias coronarias. Las irrigan para llevarles oxígeno y nutrientes
CIRCULACIÓN SANGUÍNEA
17. Explique por qué la circulación sanguínea es doble, cerrada y completa. Doble porque
recorre dos circuitos, el menor o pulmonar y el mayor o sistémico
Cerrada porque nunca sale de los vasos y completa porque la sangre carboxigenada
nunca se mezcla con la sangre oxigenada
18. ¿Con qué otro nombre se conoce a la circulación mayor? Descríbala comenzando desde
la aurícula izquierda. Circulación mayor o sistémica. Aurícula izquierda – ventrículo
izquierdo – arteria aorta-ramas de la aorta que llevan sangre oxigenada a todo el organismo
– venas cava superior vena cava inferior – aurícula derecha
19. ¿Con qué otro nombre se conoce a la circulaciónmenor?Descríbala comenzando desde
la aurícula derecha
Circulación menor o pulmonar. Aurícula derecha – ventrículo derecho – arteria pulmonar
– Pulmones (hematosis) – venas pulmonares (dos de cada pulmón) – aurícula izquierda
20. ¿cuál de las dos circulaciones está relacionado el proceso de hematosis? Circulación
menor
VASOS SANGUÍNEOS
21. ¿Cómo se clasifican los vasos sanguíneos? Arterias – Venas - capilares
22. ¿Cómo se denomina la única arteria que transporta sangre carboxigenada? pulmonar
23. ¿Cómo se denominan las únicas venas que transportan sangre oxigenada? pulmonares
24. Complete el cuadro referido a las propiedades de las arterias y venas
38
ARTERIAS VENAS
25. ¿Cómo se denominan los vasos sanguíneos que hacen de puente entre las venas y
arterias, formados únicamente por una única túnica íntima y en ellosse produce la difusión
de sustancias y gases? Capilares
26. Complete el cuadro colocando la función de los siguientes vasos
VASOS FUNCIÓN
ARTERIAS CARÓTIDAS Irrigan el cerebro
VENA YUGULAR Recoge la sangre carboxigenada de la cabeza y cuello
VENAS CAVA La superior lleva sangre carboxigenada al corazón,
proveniente de la cabeza y extremidades superiores. La
inferior lleva sangre carboxigenada del tronco y
extremidades inferiores
ARTERIA SUBCLAVIA Irriga extremidades superiores
ARTERIA PULMONAR Lleva sangre carboxigenada desde el corazón (VD)
pulmones
VENA PULMONAR Lleva sangre oxigenada desde los pulmones al corazón
(AI)
ARTERIA ILIACA Irriga extremidades inferiores
39
27. Mencione por lo menos 3 (TRES) arterias que sean ramificaciones de la arteria
aorta. Arteria iliaca, arteria femoral, arteria mesentérica, arteria hepática, arteria renal
28. Ubique donde se encuentran las siguientes arterias: radial, braquial, poplítea,
pedia dorsal, tibial posterior.
Radial: antebrazo
Braquial: antebrazo
Poplítea: a nivel deltercer anillo aductor como continuación de la arteria femoral. Atraviesa
el anillo del soleo y se divide en arteria tibial anterior y posterior. La podemos encontrar
(palpar) en el hueco poplíteo, detrás de la articulación de la rodilla
Pedia: Arteria pedia o dorsal del pie: Continuación de la tibial anterior Comienza en la
cara anterior de la articulación del tobillo 5 ramas: irriga músculos pie y dedos Irriga
superficie dorsal del pie
Tibial posterior: En la parte superior de la pierna la arteria poplitea se divide en arterias
tibial anterior y tibial posterior. La segunda irriga la parte posterior de la pierna, pasa por
detrás del maléolo medial y termina dividiéndose en arterias plantares medial y lateral
que irrigan la planta del pie.
SANGRE
29. ¿La sangre, es un tejido? Si su respuesta es afirmativa justifique por qué y qué tipo de
tejido es. Si su respuesta es negativa, justifique
La sangre es un tejido, es un conjunto de células. Es el único tejido liquido especializado.
Es tejido conectivo
30. La composición de la sangre es la siguiente: VERDADERO o FALSO SANGRE =
PLASMA + ELEMENTOS FORMES Rta: VERDADERO
31. ¿Qué es el plasma? ¿Quiénes forman parte de los elementos formes? Plasma es
la parte líquida de la sangre. Los elementos formes están formados por:
a. eritrocitos, hematíes o globulos rojos b. leucocitos o globulos blancos c. trombocitos
o plaquetas
32. Complete el siguiente cuadro:
OTRO NOMBRE FUNCION VALORES
NORMALES
GLOBULOS
ROJOS
Hematíes o
eritrocitos
Transportan gases
OXIGENO y dióxido de
carbono
4 a 5
millones/mm3
GLOBULOS
BLANCOS
Leucocitos Inmunitaria 5000 a
10000/mm3
PLAQUETAS Trombocitos coagulación 150000 a
450000/mm3
33. ¿Cuáles son las cinco variedades de glóbulos blancos que existen? Neutrófilos,
eosinófilos, basófilos, monocitos, linfocitos
40
34. Enumere por lo menos 5 (CINCO) funciones de la sangre. Transporte de nutrientes, de
gases, mantenimiento homogéneo de la temperatura corporal, transporte de hormonas,
transporte de desechos, función inmunitaria
35. ¿A que se denomina volemia? Volumen total de sangre
36. ¿A qué se denomina presión sanguínea? Fuerza que ejerce la sangre sobre las paredes
de los vasos
37. Explique cómo se relaciona la volemia con la presión sanguínea
Existe una relación de proporcionalidad directa. Cuando aumenta el volumen sanguíneo
mayosfuerza ejercerá la sangre contra las paredes de los vasos y por lo tanto mayor fuerza
ejercerá. Si la volemia disminuye, menor será la fuerza de la sangre contra las paredes de
los vasos y por lo tanto menor será la presión sanguínea.
41
42
AUTOEVALUACIÓN UNIDAD 3
1. ¿Cómo se denominan los vasossanguíneos que ingresan a la aurícula derecha?
2. ¿Cuálesson los vasossanguíneos que presentan válvulassemilunares?
3. ¿Cómo se denominan los movimientos del corazón que se suceden rítmicamente y determinan la
frecuencia cardíaca?
4. ¿En qué cavidad cardíaca encontramos al nódulo sinusal o más conocido como marcapasos fisiológico
del corazón?
5. ¿Cómo se denominan los vasossanguíneos que irrigan al corazón (que le llevan sangre y oxígeno)?
6. ¿Cómo se denomina la válvula que comunica a la aurícula derecha con el ventrículo derecho?
7. ¿Dónde se origina el impulso cardíaco, que es el responsable de las contracciones de las cavidades cardíacas?
8. ¿Cómo se denomina la arteria de mayor diámetro de nuestro organismo?
9. ¿Por qué causa se dice que la circulación sanguínea es doble y cerrada?
10. ¿Qué tipo de vasossanguíneosson las carótidas y qué función cumplen?
11. ¿Cómo se denomina el vaso sanguíneo que sale del ventrículo izquierdo?
12. ¿Cómo se denomina al tejido muscular cardíaco propiamente dicho y cuál es la membrana interior que
del corazón?
13. ¿Cuál esla función de las arterias coronarias?
14. ¿Cuáles son los vasos sanguíneos que tienen como características la de tener paredes gruesas y
resistentes y están formados por tres capas: la endotelial, la media (con fibras musculares y elásticas) y la
externa con fibra conjuntiva?
15. ¿Cómo se denominan las estructuras del corazón que separan las aurículas?
16. ¿Cuáles son las funciones del sistema linfático?
17. ¿Qué es la linfa?
18. ¿Qué son el bazo y el timo? ¿Cuáles son sus funciones?
19. ¿Qué es un ganglio?
20. Completar
La linfa que procede del intestino delgado es muy rica en grasa (por lo que se denomina quilo) y los vasos
linfáticos por los que circula son los vasos …………………………………….
La linfa recorre un largo camino a través de los conductos................................................... hasta llegar a dos
grandestroncos que la conducen a la circulación venosa, estos grandestroncosse denominan ………….
43
UNIDAD 4: SISTEMA RESPIRATORIO
INTRODUCCIÓN
Normalmente con el término respiración se define el intercambio de gases entre el medio ambiente
externo y el medio interno. Sin embargo, bajo esta definición tan simple se incluye no solamente el
movimiento de aire entre el interior y exterior de los pulmones,sino también el paso de los mismos del
interior pulmonar a la sangre; el transporte mediante la vía sanguínea hasta las células y su posterior
difusión a través de las membranas celulares. Todos estos pasos permiten a las células el consumo de
O2 y la liberación de CO2. Desde un punto de vista más limitado, como es el celular, la respiración (o
respiración celular)se refiere al metabolismo oxidativo (oxidación de nutrientes) para la generación de
energía metabólica; y en este proceso es dónde se consume el oxígeno y se forma anhídrido carbónico.
Para poder realizar todas las funciones descritas se requiere la participación de otros aparatos además
del respiratorio. Así el aparato cardiovascular o la sangre son piezas tan importantes e imprescindibles
como el propio aparato respiratorio.
Funciones no respiratorias del aparato respiratorio
Además del intercambio gaseoso, el aparato respiratorio desarrollas otras funciones. Así:
 El lecho capilar pulmonar actúa como un filtro para la sangre, ya que pequeños coágulos,
restos celulares o burbujas de aire son eliminados en este aparato.
 Las vías aéreas ejercen una gran acción de defensa del organismo, impidiendo la entrada de
agentes patógenos en el cuerpo.
 Participa en mecanismos homeostáticos como el control de la temperatura, control de líquidos
corporales, control ácido-básico, etc.
 El lecho capilar pulmonar es un importante reservorio de sangre.
 Tiene importantes acciones metabólicas.
ESTRUCTURA DEL APARATO RESPIRATORIO
El aparato respiratorio se divide en dos partes desde el punto de vista funcional
a) Sistema de conducción o vías aéreas.
b) Sistema de intercambio o superficie alveolar.
44
Vías respiratorias o sistema respiratorio conductor
 Vías aéreas altas: fosas nasales y faringe.
 Vías aéreas bajas: laringe, tráquea y bronquios.
La faringe es un conducto complejo que conecta la cavidad nasal y la cavidad oral con el esófago y con
la laringe. Es una zona de paso mixta para el alimento y el aire respirado.
Orificios nasales. Son dos orificios que comunican el exterior con las ventanas nasales, en el interior
de las cuales hay unos pelos que filtran el aire y unas glándulassecretoras democo que retienen el polvo
y humedecen el aire.
Fosas nasales. Son dos amplias cavidadessituadassobre la cavidad bucal. En su interior presentan unos
repliegues denominados cornetes, que frenan el paso del aire, favoreciendo así su humidificación y
calentamiento. En las cavidades nasales la presencia de los cornetes da lugar a un incremento de
superficie recubierta por un epitelio columnar ciliado y con gran cantidad de células mucosas. Además,
también hay pelos o vibrisas y una densa red de capilares a nivel de la submucosa. Estas características
estructurales, permite que el aire al penetrar en las fosas nasales, desarrolle, por lo tortuoso de su
recorrido, un flujo turbulento que golpea contra las paredes, permitiendo así las funciones siguientes:
 Filtrado del aire inspirado, eliminando las partículas en suspensión que tengan un diámetro superior
a las 4-6 micras.
 Calentamiento del aire, por contacto con el flujo sanguíneo, pudiendo elevarse la temperatura del
aire de 2 a 3ºC.
 Humidificación del aire, el recorrido por las vías aéreas altas produce una saturación de vapor de
agua (100%).
 Protección, ya que la presencia de terminaciones nerviosas sensoriales del nervio trigémino
detectan la presencia de irritantes y produce el reflejo del estornudo.
Faringe. Es un conducto de unos 14cm que permite la comunicación entre las fosas nasales, la cavidad
bucal. Se subdivide en nasofaringe, orofaringe y laringofaringe. También se comunica con el oído
medio (a través de las trompas de Eustaquio), la laringe y el esófago.
Regiones de la laringe.
La laringe tiene una región denominada la glotis, formada por dos pares de pliegues o cuerdas vocales,
siendo los pliegues superiores las cuerdas vocales falsas y los pliegues inferiores las cuerdas vocales
verdadera. Las cuerdas vocales verdaderasson lasresponsables de la emisión de lossonidos propios del
habla al vibrar cuando entre ellas pasa el aire espirado.
45
La tráquea es un conducto de unos 12 cm de longitud y 2,5-3,5 cm
de diámetro, que conecta la laringe con los bronquios. Su mucosa
tiene células pseudoestratificadas y ciliadas, que actúan de línea
defensiva frente a la entrada de partículas. Contiene unos 16-20
anillos de cartílago hialino en forma de C o de U localizados uno
encima de otro. La porción abierta de los anillos se orienta hacia
atrás, donde está el esófago, permitiendo su distensión durante la
deglución de los alimentos. La tráquea se divide en dos conductos
o bronquios primarios, uno dirigido hacia el pulmón izquierdo y
otro dirigido hacia el derecho. Dentro de cada pulmón, los
bronquios primarios van subdividiéndose en bronquios
secundarios, terciarios y así sucesivamente hasta llegar a las vías
aéreas de conducción de menor calibre o bronquiolos terminales.
Pulmones Los pulmones son dos masas
esponjosas situadas en la caja torácica,
formados por los bronquios,
bronquiolos y alvéolos, además de los
vasos sanguíneos para el intercambio.
El pulmón derecho es mayor que el
izquierdo y presenta tres lóbulos. El
izquierdo es más pequeño debido al
espacio ocupado por el corazón y sólo
tiene dos lóbulos.
El número total de alvéolos en los
pulmones oscila entre 300-600
millones; al final de la espiración, su
diámetromedio es de unas 100 μ, lo cual
hace que la superficie o área total
conjunta para el intercambio gaseoso
sea de 100 m2
, área de tamaño
suficientemente grande como para
garantizar los intercambios con toda
eficacia.
Los alvéolos son estructuras en forma esférica, llenas de aire, y de pared muy fina donde se realiza el
intercambio de gases.
El epitelio alveolar es muy plano y está rodeado de capilares. Formado por células epiteliales
denominadas neumocitos o células alveolares. Porfuera de estas células hay fibroblastos que sintetizan
fibras elásticas y conectivas que le proporcionan soporte al alvéolo y son responsables del
comportamiento elástico de este órgano.
46
Pleura Es una membrana serosa que tapiza los pulmones doblada sobre símisma. Dispone de dos hojas,
la externa o parietal, adherida a la cara interna de la pared costal; y la interna o visceral, que se encuentra
adherida firmemente a los pulmones. Entre ellas prácticamente no hay separación, tan sólo un poco
de líquido que las mantiene aún más adheridas entre sí.
El espacio pleural (también denominado intra o interpleural) separa ambas pleuras unas 5-10 μ y está
relleno de unos 20 ml de líquido pleural, obtenidos por ultrafiltración del plasma, que se están
renovando continuamente. Este espacio intrapleural es virtual, pero cuando entre las hojas aparece
aire o líquido, se separan y puede apreciarse la existencia individualizada de cada hoja. La pleura tiene
dos funciones:
a) mantener en contacto el pulmón con la pared torácica, de forma que sus movimientos vayan al
unísono, y actuar como lubricante permitiendo que las hojasresbalen entre sí y no haya mucha fricción
en un órgano en continuo movimiento. La presencia de esa pequeña cantidad de líquido favorece de
forma extraordinaria la adherencia. La presión en la cavidad pleural es negativa, y puede mantenerse
gracias a los capilareslinfáticos que drenan el líquido y generan con su aspiración una presión negativa.
La entrada de aire a la cavidad pleural elimina la presión negativa, provocando el colapso del pulmón y
limitando de forma importante la respiración.
Vascularización e inervación de los pulmones
El aporte de sangre a los pulmones es tan importante para la respiración como la entrada de aire al
espacio alveolar. La circulación pulmonar dispone de una extensa red de capilares (300 millones) que
rodean cada uno de los alvéolos. La superficie total de este lecho capilar es de unos 70m2
, lo que permite
una estrecha correlación entre las superficies alveolares y endoteliales. De esta forma se garantiza una
correcta difusión de los gases respiratorios.
Hasta las vías respiratorias llegan las fibras procedente del sistema nervioso autónomo que inervan las
fibras musculares lisas de esta zona.
47
Proceso de la Respiración
La respiración, de manera generalizada consiste en tomar oxigeno del aire y desprender el dióxido de
carbono que se produce en las células.
El transporte de oxígeno en la sangre esrealizado por los glóbulosrojos, quienesson los encargados de
llevarlo a cada célula, de nuestro organismo, que lo requiera. Al no respirar no llegaría oxigeno a
nuestras células y por lo tanto no podrían realizarse todos los procesos metabólicos que nuestro
organismo requiere para subsistir, esto traería como consecuencia una muerte súbita por asfixia (si no
llega oxígeno a los pulmones) o una muerte cerebral (si no llega oxígeno al cerebro.
Tiene tres fases:
1. Intercambio de gases.
2. El transporte de gases.
3. La respiración en las células y tejidos.
Respiramos unas 17 veces por minuto y cada vez introducimos en la respiración normal ½ litro de aire.
El número de inspiraciones depende del ejercicio, de la edad etc. la capacidad pulmonar de una persona
es de cinco litros. A la cantidad de aire que se pueda renovar en una inspiración forzada se llama
capacidad vital; suele ser de 3,5 litros.
Intercambio de gases: oxígeno para la sangre y dióxido de carbono para el ambiente
Inspiración o Inhalación
Cuando el diafragma se contrae y se mueve hacia abajo, los músculos pectorales menores y los
intercostales presionan las costillas hacia fuera. La cavidad torácica se expande y el aire entra con
rapidez en los pulmones a través de la tráquea para llenar el vacío resultante.
Espiración o Exhalación
Cuando el diafragma se relaja, adopta su posición normal, curvado hacia arriba; entonceslos pulmones
se contraen y el aire se expele.
Proceso de la Inhalación y la Exhalación: los dos movimientos respiratorios del organismo.
El primer paso en el proceso respiratorio consiste en la inhalación, es decir, introducir el aire al cuerpo
a través de lanariz, entrando en la faringe,siguiendo la epiglotis(ésta cubre a la tráqueamientras comes
para evitar que los alimentos entren a las vías respiratorias), pasando después a la laringe, el aire viaja
entonces por la tráquea, que es la vía que lo conduce a los pulmones.
HEMATOSIS
El intercambio de Oxígeno y dióxido de Carbono entre la sangre y el aire,se lleva a cabo en los Alvéolos.
Al llegar a los pulmones, la tráquea se divide en dos tubos más angostos llamados bronquios, cada uno
de ellos se divide a su vez en numerosas ramificaciones en los que al finalse encuentran miles de sacos
de pared delgada llamados alveólos, los cuales son considerados como la Unidad Funcional del Pulmón,
porque es en estossacos donde el oxígeno y el dióxido de carbono se intercambian por difusión entre el
aire y la sangre, este es el proceso de la respiración externa.
48
De esta manera, cuando el aire llega a los alvéolos, parte del oxigeno del aire se difunde en los vasos
sanguíneos que los rodean atravesando las finísimas paredes (membrana alveolo capilar o barrera
hemato gaseosa) y pasa a los glóbulos rojos de la sangre.
Y el dióxido de carbono que traía la sangre pasa al aire, así la sangre venenosa se convierte en sangre
arterial esta operación se denomina hematosis.
Barrera hemato-gaseosa
La barrera entre el gassituado en el interior del alvéolo y la sangre en la densa red capilar que tapiza los
alvéolos, barrera hemato-gaseosa o membrana alvéolo-capilar, es de aproximadamente 0,5 μ.
Los elementos que conforman esta barrera de separación son:
 La capa de agua que tapiza el alvéolo en su interior.
 El epitelio alveolar con su membrana basal.
 El líquido intersticial.
 El endotelio capilar con su membrana basal
El epitelio alveolar está formado por células de dos tipos:
1. Células alveolares o neumocitos Tipo I.
2. Células alveolares o neumocitos Tipo II.
Las células alveolares Tipo Ison las más abundantes (95%) y son células epiteliales planas o escamosas;
las de Tipo II son células cúbicas más grandes, con microvellosidades en su superficie apical, su
metabolismo es mucho más activo, sintetizan surfactante que acumulan en cuerpos lamelares y
secretan a la capa líquida que baña los alvéolos. El surfactante es una sustancia tensoactiva, mezcla de
fosfolípidos, principalmente dipalmitoilfosfatidilcolina (lecitina), proteínas e iones, que reduce la
tensión superficial entre aire respirado y sangre, disminuye el trabajo respiratorio y proporciona
estabilidad a los alvéolos impidiendo su colapso. También se encuentran macrófagos alveolares que
recorren la superficie alveolar y fagocitan las partículas extrañas que alcanzan el epitelio alveolar,
constituyendo la última barrera defensiva.
49
Transporte de Gases:
Una vez que el oxígeno del aire se difunde en los vasos sanguíneos que rodean a los alveólos, es
transportado por los glóbulos rojos de la sangre hasta el corazón y después distribuido por las arterias
a todaslas células del cuerpo, donde se usa en la respiración celular. En este proceso se utiliza el oxígeno
por el cual se descompone la glucosa, lo cual da como resultado la liberación de energía y la formación
de ATP, originando Dióxido de Carbono y agua como productos de desecho, difundiéndose en la sangre
y posteriormente es transportado hacia los pulmones.
En el transporte de gases, la sangre oxigenada llega al corazón por medio de la arteria pulmonar
El dióxido de carbono es recogido en parte por los glóbulos rojos y parte por el plasma y transportado
por las venas cavas hasta el corazón y de allí es llevado a los pulmones para ser arrojado al exterior.
La sangre que llega a los pulmones, previene de las células del cuerpo, y tiene un alto
contenido de dióxido de carbono y baja de oxígeno. Así, el dióxido de carbono del cuerpo difunde desde
la sangre hacia el aire de los alvéolos, para ser eliminado del organismo.
Mientras que el oxígeno difunde desde el aire de los alvéolos hacia la sangre, con lo cual, esta se vuelve
rica en oxígeno. Esta sangre ya oxigenada, deja los pulmones y es transportada hacia el corazón quien
la bombea a todas las células del cuerpo. Repitiéndose entonces el ciclo
AUTOEVALUACIÓN UNIDAD 4
1. ¿Cuántoslóbulos posee el pulmón derecho?
2. ¿Cómo se denominan las membranasseparadas por un espacio virtual que recubren a los pulmones?
3. Además del tejido epitelial ciliado que se encuentra en la pared interna de la tráquea, ¿cuál es el otro tejido
característico de la tráquea?
4. ¿Dónde se encuentra la membrana o mucosa pituitaria?
5. ¿Cómo actúa elsistema nervioso autónomo simpático a nivel de los bronquios?
6. ¿Cómo se denomina a cada uno de los divertículos o sacosterminales del árbol bronquial en los que tiene
lugar el intercambio gaseoso?
7. ¿Cuál esla función de la epiglotis?
8. ¿En qué estructura delsistema respiratorio se encuentran las cuerdas vocales?
9. ¿Cuálesson los músculos que participan en la mecánica respiratoria (respiración)?
10. ¿Cómo se denomina a cada uno de los divertículos o sacosterminales del árbol bronquial en los que tiene
lugar el intercambio gaseoso?
11. ¿Cómo se denominan las estructuras delsistema respiratorio que continúan a la tráquea?
12. ¿Qué son las pleuras? ¿Cuántasson? ¿Cómo se llama cada una?
13. ¿La tráquea se encuentra por detrás o por delante del esófago?
14. ¿Cuál esla función de las vellosidades nasales?
15. Enumere cómo se denomina cada uno de los dos mecanismos que forman parte de la mecánica respiratoria
16. Describa el proceso de hematosis
50
UNIDAD 5: SISTEMA URINARIO
INTRODUCCIÓN
Al sistema urinario se lo conoce con el nombre de sistema excretor. Está formado por una serie
de estructuras cuya función principal es recoger y eliminar todas las sustancias de desecho
resultantes de las reacciones bioquímicas (del metabolismo) que tienen lugar en el organismo.
Los órganos principales de este sistema son los riñones que forman la orina a partir de un proceso de
filtración de la sangre.
Por tanto, las funciones del aparato urinario se pueden resumir como:
a. Formación de la orina.
b. La formación y eliminación de la orina contribuye a la regulación del medio interno: (volemia,
electrolitos, equilibrio hídrico, pH)
c. El riñón también se comporta como una glándula endocrina secretando una hormona, la
eritropoyetina, que es necesaria en la hematopoyesis, producción de glóbulos rojos, también llamados
hematíes o eritrocitos.
d. También produce renina que participa en la regulación de la presión arterial.
e. Transporte de la orina desde los riñones hasta la vejiga urinaria a través de los ureteres.
f. Almacenamiento de la orina en la vejiga.
g. Eliminación de la orina a través de la uretra, proceso conocido como micción.
Anatomía del aparato urinario
Constituido por dos riñones, dos uréteres, la vejiga y la uretra.
RIÑONES
Son dos órganos macizos, uno derecho y otro izquierdo, situados en la región lumbar, uno a cada lado
de la columna vertebral y algo por delante de ésta. Son órganos retroperitoneales. Su tamaño es de 11
x 3 x 5 cm, aproximadamente y su peso oscila entre 110 y 180 gramos. En forma de poroto, el riñón
presenta dos bordes, uno externo y otro interno en el que se localiza una hendidura central
denominada hilio renal.
51
El riñón (DERECHO) está ligeramente más bajo que el (IZQUIERDO), ya que el hígado lo desplaza hacia
abajo.
Si realizamos un corte en un riñón en sentido vertical, se observarán las siguientes partes:
a) Corteza renal: Es la porción más externa del mismo. De aspecto uniforme. Tiene aproximadamente
1 cm de espesor y rodea la médula.
b) Médula renal: Eslaporciónmásinternadelriñón.Tiene aspecto estriado yestá formadaporpirámides
cónicas denominadas pirámides de malphigi. El número de pirámides oscila entre 8 y 18 en cada riñón.
La base de cada pirámide está orientada hacia el exterior y el vértice hacia el hilio renal. Las pirámides
renalesse unen porsu extremo convexo en losllamados cálicesmenores,que son de 8 a 10 por pirámide,
y que a su vez se unen para formar de 2 a 3 cálices mayores. los cálices mayores se unen entre sí para
formar la (pelvis renal). la pelvis renal desemboca en el (uréter). en el vértice de la misma se localiza la
papila renal.
c) el hilio renal es una hendidura situada en el borde interno del riñón. a través del hilio renal penetran
en el rinón la (arteria) renal y nervios y salen la vena renal y (uréter). la zona de la corteza renal situada
entre cada dos pirámides se denomina columna de bertin.
d) un lóbulo renal está formado por la pirámide renal y la correspondiente zona de corteza que la rodea.
vascularización del riñón
la arteria renal, que es una rama de la arteria (aorta abdominal), penetra en el riñón a través del hilio,
ramificándose internamente de manera que el riñón sea uno de los órganos mejor vascularizados.
la arteria renal se ramifica formando pequeñas arterias interlobulares que llegan a la zona cortical para
formar las arterias arqueadas que se sitúan alrededor de la base de las pirámides. de las arterias
arqueadas nacen las arteriolas aferentes que llegan a la cápsula de (bowman) para dividirse en su
interior en una tupida red de capilares, denominados, los capilares (glomerulares).
Estos capilares vuelven a fusionarse entre sí para dar lugar a la arteriola eferente que abandona la
cápsula de Bowman y, a su vez, desaguan en las venas intertabulares y éstas a su vez en la vena renal
que abandona el riñón por el hilio renal. La vena renal desemboca en la vena cava inferior.
52
El flujo de sangre que llega al riñón es muy elevado, 1.200 ml/minuto, lo que representa la quinta parte
de sangre que bombea el corazón en un minuto.
De esta manera la sangre es sometida en el riñón a un proceso de depuración donde son eliminados
todos aquellos metabolitos de desecho y sustancias que se encuentran en exceso, para mantener así
el equilibrio homeostático.
La nefona
La nefrona o nefron es la unidad estructural y funcional del riñón. En cada riñón hay entre uno y tres
millones de nefronas. Cada nefrona está formada por:
a. CORPUSCULO RENAL: Constituido por el Glomérulo y la Cápsula de Bowman. El glomérulo está
formado a su vez por una tupida red de capilares sanguíneos envueltos por una membrana
denominada cápsula de bowman. En el interior de esa cápsula entra una arteriola, denominada
arteriola aferente y sale otra llamada arteriola eferente. La Cápsula de Bowman es una membrana de
doble hoja, que se invagina sobre sí misma para alojar al glomerulo, creando en su interior un espacio,
el espacio de bowman, donde se recoge la orina filtrada del glomérulo.
53
b. TÚBULO CONTORNEADO PROXIMAL
(TCP): Es la continuación del corpúsculo renal.
presenta dos zonas, una situada en la corteza
renal, que presenta muchas sinuosidades
alrededor del corpúsculo renal, y otra situada en
la zona medular del riñón, mucho más recta que
la primera. La pared del TCP está formada por
una capa de células epiteliales apoyadas sobre
una membrana basal.
c. ASA DE HENLE: En forma de U. Está formada
por una porción descendente y delgada y una
porción ascendente que en la primera parte del
trayecto es delgada mientras que en la segunda
es gruesa.
d. TÚBULO CONTORNEADO DISTAL (TCD):
Es la continuación del Asa de Henle.
e. TÚBULO COLECTOR (TC): Es un tubo recto. Se
reúnen entre sí para desaguar en los cálices de la
pelvis renal.
54
La cápsula de Bowman, TCP y TCD están situados
en la CORTEZA renal mientras que el Asa de
Henle y TC se sitúan en la MÉDULA renal.
Hay nefronas que ocupan en el riñón una posición cortical mientras otras se sitúan en posición
yuxtamedular.
URÉTERES
Son dos largos tubos, uno izquierdo y otro derecho, que comunican por su extremo superior con la
PELVIS RENAL y por su extremo inferior con la VEJIGA URINARIA. Tienen una longitud aproximada de
30 cm.
La pared ureteral está formada por las siguientes capas: una capa mucosa, que tapiza internamente la
luz del tubo, una capa de músculo liso y una capa externa o adventicia.
VEJIGA
Es una especie de saco membranoso que actúa como reservorio de orina entre cada dos micciones.
Situada detrás de la SÍNFISIS DEL PUBIS tiene forma de pera. Presenta una base ancha de forma
triangular, el trígono de lietaud, en cuyos vértices superiores desembocan los uréteres. Tiene la
capacidad de almacenar hasta 500 ml de orina. En el vértice inferior tiene su comienzo la uretra.
URETRA
Representa laparte final de las vías urinarias. En lamujerlauretra esmuy corta (4 cmaproximadamente)
y más gruesa. En el varón mide unos 20 cm aproximadamente y es más estrecha.
En el varón hay que diferenciar tres segmentos, a saber: uretra prostática, uretra membranosa y uretra
cavernosa.
La uretra prostática mide unos 3 cm de longitud atraviesa el espesor de la próstata y en ella desemboca
la próstata y los dos conductos deferentes.
La uretra membranosa es muy corta (2,5 cm), y presenta un engrosamiento de fibras musculares
esqueléticas que corresponde al esfínter externo. Dicho esfínter está controlado voluntariamente.
La uretra cavernosa discurre en el espesor del músculo del mismo nombre, mide unos 15 cm y termina
en el meato urinario.
La unión de la uretra con la vejiga presenta un engrosamiento muscular denominado esfínter uretral
interno, formado por fíbras musculares dispuestas en haces espirales, circulares y longitudinales que
constituyen el músculo detrusor de la vejiga.
55
4
La formación de la orina pasa por tres etapas fundamentales:
1. La filtración glomerular
2. La reabsorción tubular
3. La secreción tubular
La mayor parte de sustancias excretadas, es decir las que se encuentran en la orina definitiva, pasan
por las dos primeras.
1. La filtración glomerular
La filtración glomerular es la etapa inicial en la formación de la orina. Consiste en el paso, a través de la
membrana de filtración, de parte del plasma sanguíneo que circula. Se obtiene orina primitiva u orina inicial,
similar al plasma, excepto en lo que concierne a las proteínas. Para que haya filtración glomerular, debe
haber suficiente presión sanguínea glomerular, esto se consigue si la presión arterial sistémica es igual o
superior a 60 mmHg.
La tasa de filtración glomerular (TFG) es uno de los parámetros a saber de la fisiología renal. Es el volumen
de filtrado que se produce por unidad de tiempo. Es de unos 120 ml/min, aproximadamente, lo que en 24
horas supone la elevada cifra de 180 l. Es evidente la necesidad de la reabsorción tubular para alcanzar el
volumen definitivo de orina, que, en general, en el adulto es de unos (1500 a 1800 ml) /día. Se puede
estudiar la TFG midiendo, en orina, la concentración de sustancias que, como la inulina o la creatinina, se
filtran en forma de molécula libre, no se reabsorben ni se secretan a nivel tubular, no se producen ni
destruyen por el riñón, ni modifican el funcionamiento del mismo.
2. La reabsorción tubular
La reabsorción tubular es el retorno de gran parte del filtrado al torrente sanguíneo de las sustancias
imprescindibles para el cuerpo, como el agua, la glucosa, los aminoácidos, las vitaminas, parte de la urea y
los iones de sodio (Na+
), potasio (K+
), calcio (Ca2+), cloruro (Cl-
), bicarbonato (HCO3
-
) y fosfato (HPO4
2-
).
Elmotor de la reabsorción tubular de gran parte del filtrado es el continuo funcionamiento de las bombas de
sodio/potasio (ATPasa de Na+
/K+
). La reabsorción del 99 % del filtrado sucede a todo lo largo del túbulo
renal. La reabsorción del 99 % del filtrado se produce a lo largo del túbulo renal, especialmente en el
segmento contorneado proximal (un 80 % aproximadamente), y el ajuste preciso del volumen y de la
composición de orina definitiva se efectúa en el túbulo contorneado distal y en el túbulo colector.
3. Secreción tubular
La secreción tubular es la transferencia de materiales con el objetivo de regular la tasa de sustancias
en el torrente sanguíneo y de eliminar desechos del cuerpo. Las principales sustancias secretadas son
hidrógeno (H+
), potasio (K+
), iones amonio (NH +
), creatinina y ciertos fármacos, como la penicilina.
Agua y cloruro sódico a través de la nefrona
En el glomérulo renal se filtra toda la sal y el agua del plasma a razón de 120 ml/min. En los 180 litros
de filtrado producidos diariamente, hay 1,5 kg de sal (cloruro de sodio), del que sólo será eliminado el
1%, principalmente por la hormona antidiurética o ADH y la hormona aldosterona, que regulan
la excreción de agua y sal en función de las necesidades del organismo.
En ausencia de ADH, se producirá orina hipotónica u orina diluida. El déficit de agua en el organismo o
el descenso de la presión arterial estimulan la secreción de la ADH y el resultado es poco volumen de
orina concentrada.
Potasio, calcio, urea e hidrogeniones a través de la nefrona
El potasio juega un papel crucial en la excitabilidad neuromuscular, y los cambios de sus valores
sanguíneos por exceso o por defecto pueden originar trastornos graves de conductibilidad y
contractibilidad cardiacas, de modo que, tras ser filtrado, el potasio es totalmente reabsorbido.
56
Los descensos del calcio sanguíneo aumentan la excitabilidad neuromuscular y precisan de la
paratohormona (hormona hipercalcemiante) para su regulación. (glándulas paratiroides)
La urea es un producto residual del metabolismo de los aminoácidos y de otros compuestos
nitrogenados.
La secreción de hidrogeniones (también llamados protones o H+) permite mantener el equilibrio
ácido base del organismo
La micción
La micción es el vaciado vesical que permite la evacuación de la orina. Un volumen de orina superior a
350 ml, aproximadamente, desencadena el llamado reflejo de la micción, la distensión de las paredes
vesicales, la contracción del músculo detrusor y la relajación del esfínter. El control voluntario de la
micción se efectúa gracias a la contracción y la relajación voluntarias del esfínter uretral externo.
Equilibrio osmótico o hidroelectrolitico
La correcta hidratación del cuerpo depende tanto del volumen preciso de agua corporal como de la
proporción adecuada de sustancias iónicas (electrolitos) disueltas en ella. Diversos mecanismos
nerviosos y hormonales actúan continuamente para mantener constante la proporción de estas
sustancias, a base de regular ganancias y pérdidas de las mismas.
Volúmen y composición de los compartimientos fluidos del organismo
De forma abstracta, se puede considerar el cuerpo humano como la suma de dos grandes
compartimentos o espacios rellenos de fluidos: el celular, que comprende el líquido o fluido
intracelular (LIC) de todas las células de todos los tejidos, y el extracelular, que contiene el líquido o
fluido extracelular (LEC), subdividido en el líquido intersticial del espacio intersticial (75 % del LEC) y el
plasma sanguíneo del espacio vascular (25 % del LEC). El 55-60 % de la masa corporal total de una
persona adulta corresponde al agua. Dos terceras partes de este gran volumen acuoso constituyen el
LIC, mientras que el tercio restante corresponde al LEC.
Ganancias y pérdidas diarias de agua y electrolitos
Generalizando, se puede considerar que el adulto sano obtiene unos 2500 ml de agua al día a partir de
los alimentos (30 %), de las bebidas (60 %) y del agua metabólica, que resulta de la oxidación
intracelular de los compuestos nutritivos durante la respiración celular (10 %).
Para mantener la constancia hídrica del medio interno, las pérdidas hídricas son proporcionales a las
ganancias, de modo que se pierden unos 2500 ml/día de agua por 4 vías: la renal, que excreta un 60 %
aproximadamente de este volumen en forma de orina; la dérmica, que a través del sudor elimina un 8
%; la pulmonar, que a través del aliento elimina aproximadamente un 28 %, y la gastrointestinal, que
elimina un 4% en el agua que contienen las heces.
Tanto las ganancias como las pérdidas de agua van acompañadas de las ganancias y pérdidas
correspondientes de electrolitos, principalmente de sodio (Na+
), cloro (Cl-
) y potasio (K+
).
Control de la ganancia de agua
Cuando las pérdidas de agua del cuerpo superan a las ganancias, el centro hipotalámico de la sed genera
la necesidad de beber, o conducta de la sed, para evitar la disminución del volumen de líquido y el
aumento de la concentración de los electrolitos disueltos, situación que se conoce como
deshidratación. Los estímulos y las señales que desencadena la conducta de la sed son los siguientes:
1. el aumento de la osmolaridad del plasma
2. la sensación de boca seca
3. la disminución de la presión arterial
4. el aumento de la angiotensina II ante la disminución de la presión arterial y el filtrado
57
Control de las pérdidas de agua y solutos
Los riñones regulan los líquidos y la concentración de sustancias disueltas, como el cloruro sódico
(NaCl). Mediante el control hormonal, modifican las características de la orina y contribuyen al
mantenimiento de la homeostasis hidroelectrolítica del organismo.
Las hormonas que más influyen sobre el riñón son:
1. La angiotensina II y la aldosterona. Ambas promueven la reabsorción de Na+ y Cl-, lo que reduce las
pérdidas urinarias de ambos iones, con lo que aumenta el volumen de líquidos corporales. Forman el
sistema renina-angiotensina-aldosterona. (glándulas suprarrenales)
2. péptido natriurético auricular (PNA). Promueve la excreción urinaria de Na+ y Cl-, que se acompaña
de pérdida de agua, de manera que disminuye el volumen de los líquidos corporales.
3. La hormona antidiurética (HAD). Es el principal factor regulador del volumen de orina, gracias a ella
se produce una orina concentrada.
AUTOEVALUACIÓN UNIDAD 5
1. ¿En qué estructura del riñón se realiza el proceso de formación de orina?
2. ¿Qué órgano delsistema urinario se ubica en la cavidad de la pelvis y que por detráslimita con el
recto, por delante con el pubis y, en el caso de los hombres, con la parte superior de la próstata?
3. ¿Qué forma tienen losriñones?
4. ¿Con que otro sistema el hombre comparte la uretra?
5. ¿Dónde se encuentra el meato urinario?
6. ¿En qué estructura del riñón se realiza el proceso de formación de orina?
7. ¿Por qué al sistema urinario se lo considera como un sistema excretor?
8. ¿Cómo se denominan a cada una de las unidades estructurales y fisiológicas del riñón en la que se
lleva a cabo el proceso de formación de orina?
9. ¿Cuál esla función de la vejiga?
10. ¿Cómo se denomina el conducto delsistema urinario por donde se expele la orina?
11. En el proceso de formación de orina, ¿cuál esla función específica del glomérulo?
12. Enumere cuáles son las estructuras (capas o zonas) bien diferenciadas en un corte esquemático
del riñón
13. Enumere lostres procesos principales que se realizan en la nefrona para la formación de orina
14. ¿Qué consiste la micción?
15. ¿Existe una diferencia anatómica entre la uretramasculina y femenina? Sisu respuesta es afirmativa
enumere una diferencia
58
UNIDAD 6: APARATO DIGESTIVO
INTRODUCCIÓN
Es el aparato encargado de ingerir los alimentos, degradarlos hasta moléculas pequeñas capaces de
entrar en las células, los denominados nutrientes, y de expulsar los restos no digeribles (hecesfecales).
Partes del aparato digestivo.
El aparato digestivo humano es un tubo con un orificio de entrada (boca) y un de salida (ano), en el cual
se puede distinguir diferentes regiones (cavidad bucal, faringe, esófago, estómago, intestino
delgado e intestino grueso) y varias glándulas anejas (glándulas salivales, hígado y páncreas ).
Cavidad bucal.
Es la cavidad por dónde se ingiere el alimento. Está delimitada por los labios, las mejillas, el paladar
duro, el paladar blando (el denominado "velo del paladar") y por la base de la boca. Interiormente está
recubierta por un epitelio húmedo denominado mucosa bucal. En el interior se encuentra la lengua y
los dientes, y en ella desembocan las glándulas salivales. En los adultos se distinguen 32 dientes. En
cada mandíbula hay 4 incisivos, 2 caninos, 4 premolares y 6 molares (para masticar). Entre la cavidad
bucal y la faringe se encuentran las amígdalas con función de barrera defensiva inmunológica. Al final
de este apartado hay una descripción de la estructura interna de los dientes.
59
Glándulas salivales. Hay tres pares de glándulas que segregan saliva. Ésta está constituida por
agua, enzimas digestivas (ptialina y amilasa) y mucina (una sustancia mucosa). Gracias a la saliva el
alimento se humedece, resulta más fácil su deglución, se eliminan algunas de las bacterias
acompañantes y se inicia la digestión de los glúcidos.
Dientes
Los dientes presentan una parte externa
(corona), una parte interna (raíz) y una parte
intermedia (cuello). Los dientes están
constituidos por una sustancia
denominada dentina o marfil (básicamente de
fosfato cálcico). La parte externa presenta
además una cubierta de un material muy duro
denominado esmalte. La raíz se une al hueso
mandibular mediante una sustancia llamada
cemento.
En los adultos se distinguen 32 dientes. En cada
mandíbula hay:
 4 incisivos (para cortar),
 2 caninos (para rasgar o desgarrar),
 4 premolares (para triturar) y
 6 molares (para masticar).
Los últimos molaresson las denominadas muelas
del juicio y aparecen entre los 18 y 20 años. La
primera dentición, la denominada dentición de
leche, sólo presenta 20 dientes y empieza a caer
a partir de los 5 o 6 años.
Faringe.
Es un conducto muy corto (12cm) que va desde el final de la cavidad bucal hasta el principio del
esófago. Se comunica también con la laringe a través de la glotis, con las fosas nasales a través de las
coanas (ver dibujo) y con el oído medio, a través de las trompas de Eustaquio.
Esófago.
Es el conducto comprendido entre la faringe y el
estómago. Tiene una longitud de unos 25cm. Al
introducirse en él el alimento se originan
contracciones y relajaciones musculares anulares
(olas peristálticas) que provocan el avance
del bolo alimentario.
60
Estómago.
Es un órgano en forma de saco de unos 2,5 litros de
capacidad y de paredes muy gruesas debido a que posee
tres capas de células musculares. En él se puede
distinguir tres regiones: Es un órgano en forma de saco
de unos 2,5 litros de capacidad y de paredesmuy gruesas
debido a que posee tres capas de células musculares. En
él se puede distinguir tres regiones:
Región del cardias. Es la que comunica con el esófago a
través del esfínter "cardias"
Región del fundus. Es la más grande y es la que
corresponde a la gran curvatura.
Región pilórica. Es la que comunica con el duodeno a
través del esfínter "píloro".
Hígado.
Es un órgano voluminoso,situado bajo el pulmón derecho que realiza variasfunciones. Una de ellas es
segregar la bilis que se almacena en la vesícula biliar. La presencia de alimento en el duodeno estimula
la secreción de la bilis por el conducto cístico y después por el conducto colédoco, que desemboca en
la ampolla de Váter, por dónde sale al duodeno. La bilis es la responsable de la emulsión de las grasas.
Páncreas.
Es una glándula doble puesto que tiene una función exocrina (secreción al exterior, concretamente
secreción del jugo digestivo pancreático al duodeno) y una función endocrina (secreción al interior del
cuerpo, es decir a la sangre, concretamente secreción de las hormonas insulina y glucagón. El jugo
pancreático pasa por los canales
secretores a un conducto
central, el canal de Wirsung, que
desemboca en la ampolla de
Váter y de aquí pasa al duodeno. Puede
haber también otro conducto
que desemboca en el duodeno
denominado conducto
d
e Santorini.
61
Intestino delgado.
Es un tubo de unos 7metros de longitud y unos 2,5 centímetros de diámetro. En élse puede diferenciar
tres sectores denominados:
Duodeno. Es la primera parte del intestino delgado. Se comunica con el estómago a través de una
válvula denominada píloro. Tiene una longitud de unos 30cm. En él se abocan la bilis , el jugo
pancreático y el jugo intestinal procedente de las glándulas que están englobadas en sus paredes.
Yeyuno. Es la parte intermedia del intestino delgado y también la de mayor tamaño. Presenta muchas
curvaturas sobre sí mismo, las denominadas asas intestinales.
Íleon. Es la última parte del intestino delgado. Se comunica con el intestino grueso a través de la
válvula ileocecal.
Intestino grueso.
Esla parte final deltubo digestivo. Es un conducto de unos 1,7 metros de longitud y unos 8 centímetros
de diámetro. En su interior abundan las bacterias, la denominada flora bacteriana. En el intestino
grueso se puede diferenciar tres tramos, que son:
Ciego. Es la primera parte del intestino grueso. Su nombre hace referencia a que es un conducto sin
salida (ciego). Al final presenta un apéndice vermiforme (con forma de gusano), que si no se vacía
continuamente puede infectarse e inflamarse (apendicitis) y que sise perfora se produce una infección
generalizada (septicemia) que puede provocar la muerte.
Colon. Es la segunda parte del intestino grueso. Este va desde el final del intestino delgado, el ileon,
con el cual comunica a través de la válvula ileocecal, hasta el recto. En el intestino grueso se pueden
diferenciar tres sectores denominados: colon ascendente, colon transverso y colon descendente.
Recto. Es la última parte del intestino grueso. Finaliza en el ano (esfínter anal).
62
Complete en la columna vacía con las referencias del 1 al 11
LA DIGESTIÓN.
Es el proceso que permite aprovechar las sustancias nutritivas de los alimentos. Comprende las
siguientes etapas:
Ingestión. Es la entrada del alimento.
Digestión de los alimentos. Es la degradación de los alimentos en moléculas muy pequeñas capaces de
entrar en las células. Puede ser mecánica, como la trituración que realizan los dientes, o química , como
la acción de las enzimas digestivas.
Absorción. Es el paso de los nutrientes desde el intestino a la sangre y a la linfa.
Defecación. Es la expulsión al exterior de las sustancias que no se han podido digerir.
LA DIGESTIÓN EN LA BOCA.
En la boca se producen dos tipos de digestión:
Una digestión mecánica denominada "masticación", que es realizada por los dientes, y
Una digestión química que es realizada por la saliva al ponerse en contacto con el alimento, proceso
que se denomina "insalivación".
GLÁNDULAS SALIVALES.
Hay tres pares de glándulas denominadas: parótidas, submaxilares y sublinguales.
La saliva contiene: Agua (un 98%), Mucina (una sustancia mucosa que facilita el paso de los alimentos).
La enzima digestiva ptialina (enzima que degrada el glúcido almidón hasta llegar a moléculas de
maltosa)
La enzima digestiva maltasa (enzima que degrada la maltosa en dos moléculas de glucosa)
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
63
LA DEGLUCIÓN.
La deglución es el paso del alimento de la boca al esófago. Se realiza en tres etapas: Impulso
del bolo alimentario hacia el fondo de la boca gracias al movimiento de la lengua. Entrada del
bolo en la faringe.
Paso del bolo alimentario de la faringe al esófago.
LAS ONDAS PERISTÀLTICAS EN EL ESÓFAGO.
Son contracciones y relajaciones musculares anulares que facilitan el avance del bolo alimentario.
LA DIGESTIÓN QUÍMICA ESTOMACAL.
El estómago presenta una capa interior denominada mucosa gástrica que contiene varios tipos de
glándulas especializadas en segregar las distintas sustancias del jugo gástrico. Estas son:
Ácido clorhídrico (HCl). Degrada lostejidos duros de los alimentos,mata muchas bacterias y transforma el
pepsinógeno en pepsina
Pepsinogeno. Sustancia que se transforma en la enzima pepsina que degrada las proteínas en
aminoácidos.
Factor de Castle. Sustancia que permite que la vitamina B12 pueda ser absorbida en el intestino. Mucina.
Sustancia que favorece el paso del alimento.
Bicarbonato sódico. Sustancia que neutraliza el ácido clorhídrico antes de pasar al duodeno.
En el estómago se producen olas peristálticas para mover los alimentos. La digestión. Es el proceso que permite
aprovechar las sustancias nutritivas de los alimentos.
La ACCIÓN DE LA BILIS EN LA DIGESTIÓN.
La bilis está producida por las células del hígado. Si la persona está en ayunas la bilis se acumula en la
vesícula biliar, pero si en el duodeno hay alimento, la bilis es liberada sobre él. Cada día se segregan unos
600ml. La bilis además de agua contiene ácidos biliares, colesterol y lecitina, que son sustancias
emulsionantes de las grasas. Es decir que realizan la misma función que los detergentes, que dispersan las
grasas en el agua. Así facilitan su posterior digestión química y su absorción. La bilis también
contiene bilirrubina (una sustancia amarillenta) y biliverdina (una sustancia verdosa) procedentes de la
degradación de la hemoglobina. Son las responsables de la coloración de las defecaciones.
LA DIGESTIÓN DEBIDA AL JUGO PANCREÁTICO
Las proteasas pancreáticas (tripsina y quimiotripsina) degradan las proteínas. La
lipasa pancreática degrada los lípidos
La amilasa pancreática degrada el glúcido almidón.
FORMACIÓN DEL QUILO.
La masa pastosa que sale del estómago se denomina quimo. Posteriormente, tras experimentar la digestión
intestinal en el duodeno, se transforma en una masa más fina denominada quilo.
LA DIGESTIÓN DEBIDA AL JUGO INTESTINAL
Las peptidasas intestinales degradan las proteínas a aminoácidos. La
lipasa intestinal degrada los lípidos.
Las disacaridasas intestinales degradan los disacáridos en glucosas y otros glúcidos pequeños.
LA ABSORCIÓN INTESTINAL.
En el yeyuno las pequeñas moléculas obtenidas son absorbidas a través de las vellosidades intestinales. Las
pequeñas moléculas absorbidas de naturaleza glucídica o proteica, como la glucosa y los
aminoácidos respectivamente, pasan a los capilares venosos.
Las pequeñas moléculas absorbidas de naturaleza lipídica como los ácidos grasos pasan a los vasos
linfáticos.
64
LA FORMACIÓN DE LAS HECES.
El quilo que pasa al intestino grueso contiene un 80% de agua, las sustancias que no se han podido
digerir y los restos de los jugos digestivos. En el intestino grueso se reabsorbe gran parte de esta agua
y, debido a la flora bacteriana, se consigue digerir muchas de las sustancias resistentes. El resto forma
la denominada materia fecal que sale por el ano.
AUTOEVALUACIÓN UNIDAD 6
1. ¿Cuántostipos de digestión conoce usted?, ¿En cuál de estas digestiones participan las enzimas?
2. Enumere porlo menos DOS (2) glándulas que formen parte delsistema digestivo
3. ¿Por qué causa el contenido gástrico (en condiciones normales) no retorna al esófago
(reflujo gastroesofágico?
4. ¿En qué estructura del sistema digestivo se encuentra el ciego?
5. ¿Cómo se denomina al proceso que se realiza en el intestino delgado por el cual los nutrientes
presentes en el quilo pasan a la sangre?
6. ¿Qué estructura delsistema digestivo se encuentra entre el píloro y la válvula ileocecal?
7. ¿Cómo se denomina cada una de las porciones en la que podemos dividir al colon?
8. En el proceso de la masticación, ¿cuál esla función de los dientes denominados caninos?
9. ¿Qué es el colédoco?
10. ¿A qué estructura delsistema digestivo pertenecen el CARDIAS, FUNDUS o FONDO, CUERPO y
ANTRO?
11. ¿Cuál es el número total de dientes en un individuo adulto normal? y de éstos, ¿cuántos y
quiénes tienen la función de cortar el alimento?
12. Enumere por lo menos CUATRO (4) órganos o estructuras del aparato digestivo que se encuentren
en la cavidad abdominal
13. ¿Cómo se denominan los movimientos de contracciones rítmicas musculares de ciertos órganos
del aparato digestivo que tienen como objeto hacer transitar los alimentos y que estos no
retrocedan?
14. ¿Hacia qué órgano del sistema digestivo, el páncreas libera jugo pancreático para la realización
del proceso de digestión?
15. ¿En qué estructura delsistema digestivo se encuentran las vellosidades y microvellosidades y cuál
es la función de ellas?
65
UNIDAD 7: SISTEMA NERVIOSO
INTRODUCCIÓN.
La función de relación. Es la función basada en la captación de las variaciones del medio (los
denominados estímulos), su evaluación y en la emisión de las respuestas adecuadas.
El sistema nervioso. Es el sistema constituido básicamente por el tejido nervioso, que es el tejido
formado por las células nerviosas o neuronas.
Las neuronas y la transmisión del impulso nervioso.
Las neuronasson células especializadas en la transmisión de información gracias a que su membrana es
capaz de generar débiles corrientes eléctricas que avanzan de un extremo al otro, el llamado impulso
nervioso. Las neuronas que conducen el impulso nervioso hacia el sistema nervioso central se
llaman sensitivas, y las que lo conducen el impulso nervioso desde el sistema nervioso central hacia los
músculos y las glándulas se denominan motoras.
Las neuronas motoras presentan un cuerpo celular (cuerpo neuronal) en el que hay el núcleo y los
orgánulos, una larga prolongación denominada axón y numerosas pequeñas prolongaciones
denominadas dendritas. Las neuronas sensitivas presentan un cuerpo neuronal y dos axones.
El axón también se denomina fibra nerviosa. Puede estar recubierto por una serie de células que forman la
denominada vaina de mielina, que es de color blanco. Los haces de estos axones forman la denominada
sustancia blanca del sistema nervioso. Los cuerpos neuronales y los axones sin vaina de mielina forman la
denominada sustancia gris.
Las neuronasse conectan entre si sin llegar a tocarse (esto recibe el nombre de sinapsis). Losreceptores estimulan
en la neurona el impulso nervioso que avanza por el axón hasta el botón sináptico, allí provoca la generación de
unas pequeñas vesículas sinápticas que contienen unas sustancias denominadas neurotransmisores, que
atraviesan la fisura sináptica y son captadas por las dendritas de la siguiente neurona, generando en ella una
nueva corriente eléctrica, y así sucesivamente, hasta llegar a los órganos efectores. Todo ello es la denominada
66
transmisión del impulso nervioso.
El sistema nervioso: humano. Presenta dos partes, el sistema nervioso central (SNC) y el sistema
nervioso periférico (SNP).
El Sistema Nervioso Central (SNC). Está constituido por el encéfalo y por la médula espinal. Ambos
órganos están protegidos por huesos (cráneo y columna vertebral respectivamente) y recubiertos por
tres membranas protectoras denominadas meninges, (duramadre, piamadre y aracnoides) existiendo
un líquido amortiguador, el líquido cefalorraquídeo, entre la más interna y la siguiente. El SNC es el
encargado de recibir e interpretar los impulsos sensitivos y generar los impulsos motores.
El Sistema Nervioso Periférico (SNP). Es el conjunto de nervios que conectan el sistema nervioso
central (el encéfalo y la médula espinal) con las diversas partes del cuerpo. Los nervios son estructuras
con forma de cable constituidas por haces de axones de numerosas neuronas. Los más gruesos
presentan unamembrana externa protectora. Es pues una estructura similar a la de los cables eléctricos
domésticos.
Los nervios se pueden clasificar:
1) Según el sentido en qué transmiten el impulso nervioso. Se diferencian tres tipos de nervios:
los sensitivos (conducen el impulso nervioso hacia el sistema nervioso central), los motores (conducen
el impulso nervioso hacia los músculos y las glándulas) y los mixtos (conducen el impulso nervioso en
los dos sentidos).
2) Según el lugar de dónde salen. Se diferencian dos tipos de nervios: los nervios craneales que salen
del cráneo y los nervios espinales o raquídeos que salen de la médula espinal.
a) Nervios craneales. Sólo son 12 parejas (12 hacia la izquierda y 12 hacia la derecha). Unos son
sensitivos, otros motores y otros mixtos. Básicamente controlan los músculos de la cabeza y el cuello,
exceptuando uno, el llamado nervio vago que controla muchas vísceras.
¿Qué son los pares craneales?
De manera general, se puede decir que el encéfalo humano se comunica con casi todos los nervios
del cerebro a través de la médula espinal.
Así, por ejemplo, la información que nos llega sobre lo que tocamos con las manos es recogida por
nervios que recorren elbrazo hasta llegar a lamédula espinal, y de ahí al cerebro, desde donde se emitirá
la orden de seguir examinando el objeto. Esta orden eferente saldrá del cerebro también a través de
la médula espinal, y llegará al brazo correspondiente a través de las fibras nerviosas que salen de esta.
Sin embargo, esto no es una regla que se cumpla siempre, ya que también hay algunos nervios que salen
directamente del encéfalo, sin nacer en la médula espinal. Se trata de los pares craneales, o nervios
craneales, que surgen de la parte inferior del encéfalo y llegan a sus zonas de destino atravesando
unos
67
pequeños agujeros repartidos por la base del cráneo. Desde estos orificios, los pares craneales se
comunican con áreas periféricas.
Además, aunque pueda parecer extraño, no todos estos nervios craneales tienen la función de alcanzar
áreas y órganos que se encuentran en la cabeza. Algunos se extienden hacia el cuello e incluso la zona
del abdomen.
¿Cómo se clasifican y distribuyen los pares craneales?
Los pares cranealesse llaman así porque se cuentan a pares, al existir uno tanto en el lado derecho como
en el izquierdo del cerebro. Así, hay doce nervios craneales apuntando hacia el hemisferio derecho y
otros doce apuntando hacia el izquierdo, de manera simétrica.
Cada par está numerado con un número romano según si la posición desde la que salen del encéfalo
más o menos cerca de la zona frontal. De hecho, los nervios craneales pueden ser agrupados y
clasificados en categorías según dos criterios: el lugar del que parten y su función.
Pares craneales clasificados según su posición
 Partiendo desde áreas que están
por encima del tronco del encéfalo
están los pares I y II.
 Partiendo del mesencéfalo (la parte
superior del tronco encefálico),
están los pares craneales III y IV.
 Partiendo del puente de
Varolio (o puente
troncoencefálico), están los
nervios craneales V, VI, VII y
VIII.
 Partiendo del bulbo raquídeo
(en la parte más baja del
tronco encefálico) están los
nervios IX, X, XI y XII.
Pares craneales clasificados según su
función
 Sensitivos: los pares I, II y VIII.
 Relacionados con los
movimientos de los ojos (y sus
partes) y los párpados: los
pares craneales III, IV y VI.
 Relacionados con la activación de
músculos del cuello y la lengua: los
pares craneales XI y XII.
 Nervios craneales mixtos: los pares
V, VII, IX y X.
 Fibras parasimpáticas: nervios III,
VII, IX y X.
¿Cuáles son los pares craneales?
Vamos a conocer a continuación cuálesson los pares craneales uno por uno, y sus principalesfunciones.
1. Nervio olfatorio (par craneal I)
68
Tal y como su nombre indica, este nervio craneal se dedica a transmitir específicamente información
nerviosa sobre lo que se detecta a través del sentido del olfato, y por lo tanto es una fibra aferente. Es
el más corto de los pares craneales, ya que su lugar de destino está muy cerca de la zona del encéfalo
2. Nervio óptico (par craneal II)
También forma parte de las fibras aferentes, y se encarga de transmitir al cerebro la información visual
que se recoge desde el ojo. Surge desde el diencéfalo.
3. Nervio oculomotor u motor ocular (par craneal III)
También conocido como nervio motor ocular común, este nervio craneal manda órdenes a la mayoría
de músculos que intervienen en el movimiento de los ojos, y hace que la pupila se dilate o se contraiga.
4. Nervio troclear, o patético (par craneal IV)
Como el nervio oculomotor, este par cranealse ocupa delmovimiento de los ojos. En concreto, lemanda
señales al músculo oblicuo superior del ojo. El lugar del que surge este par de nervios es el mesencéfalo.
5. Nervio trigémino (par craneal V)
Se trata de uno de los pares craneales mixtos, porque tiene funciones tanto motoras como sensoriales.
En su faceta de nervio motor, manda órdenes a músculos encargados de realizar los movimientos de
la masticación, mientras que como nervio craneal sensorial recoge información táctil, propioceptiva y
del dolor de varias zonas de la cara y la boca.
6. Nervio abductor o motor ocular externo (par craneal VI)
Este es otro de los pares craneales encargados de hacer que el ojo se mueva. En concreto, se encarga
de producir la abducción, es decir, que el ojo se mueva hacia el lado opuesto a donde está la nariz.
7. Nervio facial (par craneal VII)
Es uno de los pares craneales mixtos. Se encarga tanto de mandar órdenes a músculos de la cara
dedicados a crear expresiones faciales (permitiendo así socializar y comunicar correctamente) como a
las glándulas lagrimales y salivales. También recoge datos gustativos de la lengua.
8. Nervio vestibulococlear (par craneal VIII)
Es uno de los pares cranealessensoriales, y recoge información de la zona auditiva. En concreto, recibe
datosrelativos a lo que se oye y a la posición en la que nos encontramosrespecto al centro de gravedad,
lo que permite mantener el equilibrio.
9. Nervio glosofaríngeo (par craneal IV)
Es un nervio tanto sensitivo como motor y, tal y como su nombre indica, tiene influencia tanto en la
lengua como en la faringe (el conducto que comunica la boca con el estómago). Recibe información de
las papilas gustativas de la lengua, pero también manda órdenes tanto a la glándula parótida (salival)
como a músculos del cuello que facilitan la acción de tragar.
10. Nervio vago o neumogástrico (par craneal X)
Este par craneal lleva órdenes a lamayoría de losmúsculosfaríngeos y laríngeos,manda fibras nerviosas
delsistema simpático a vísceras que se encuentran en la zona de nuestro abdomen y recibe información
gustativa que llega desde la epiglotis. Al igual que el nervio glosofaríngeo, interviene en la acción de
tragar, de modo que tiene mucha relevancia dado lo importante de esta función vital.
69
11. Nervio espinal (par craneal XI)
A este par craneal también se lo conoce como nervio espinal.
Se trata de uno de los pares craneales puros, y activa los músculos trapecio y
esternocleidomastoideo, que intervienen en el movimiento de la cabeza y los hombros, de modo que
sus señales se hacen notar en parte de la zona superior del tórax. En concreto, permite que la cabeza
quede decantada hacia un lado y que pueda inclinarse hacia atrás.
12. Nervio hipogloso mayor (par craneal XII)
Al igual que el nervio vago y el glosofaríngeo, activa músculos de la lengua y participa en la acción de
tragar. Así pues, trabaja junto a los pares craneales IX y X para permitir que la deglución sea realizada
correctamente, algo fundamental para el buen estado del organismo.
Nervios raquídeos. Son 31 parejas. Todos son de tipo mixto. Los de la región sacra, debido a su forma,
reciben el nombre de "cola de caballo". Todoslos nerviosraquídeos presentan una raíz dorsal y una raíz
ventral. La raíz dorsal es sensitiva y presenta un ganglio, denominado ganglio raquídeo espinal,
constituido por los cuerpos de las neuronas que reciben información de la piel y de los órganos. La raíz
ventral es motora, es decir lleva información hacia la piel y los órganos.
Y la tercera forma de clasificación de los nervios es
3) Según si coordinan actos involuntarios o actos voluntarios.
Se diferencian dos tipos de nervios: los nervios del Sistema Nervioso Autónomo y los nervios
del Sistema Nervioso Voluntario.
a) Sistema Nervioso Autónomo o Vegetativo. Es el que controla de forma involuntaria, total o
parcialmente, lasfunciones de las vísceras(corazón, pulmones, estómago, intestino y vejiga de la orina),
la presión arterial, la producción de sudor, la producción de orina y la temperatura corporal. Está
controlado por el hipotálamo y la médula espinal. Los nervios están formados casitotalmente porfibras
amielínicas. Se diferencian dos tipos:
El Sistema Nervioso Autónomo Parasimpático. Es el que predomina en los momentos de relajación.
Está constituido por el nervio craneal vago y comparte los nervios raquídeos de la región sacra.
El Sistema Nervioso Autónomo Simpático. Es el que predomina en los momentos de tensión. Sus
nervios comparten el resto de los nervios raquídeos. Las fibras nerviosas de este sistema están
parcialmente separadas del resto de los nervios raquídeos y forman dos cadenas de ganglios situadas
a ambos lados de la columna vertebral.
SistemaNervioso Voluntario. Es el que controla total o parcialmente las acciones voluntarias de nuestro
cuerpo. Estas pueden ser acciones conscientes, como por ejemplo coger un objeto que queremos, o
inconsciente, como por ejemplo adelantar la pierna derecha al andar. Está controlado por el cerebro.
Sus nervios están formados totalmente por fibras mielínicas.
70
Partes del Sistema Nervioso Central (SNC). Son
dos: el encéfalo y la médula espinal.
SNC = ENCEFALO + MÉDULA ESPINAL
a) ENCÉFALO. Es una masa de neuronas de aproximadamente 1,5Kg de peso que está constituida, en
su parte externa, por sustancia gris, formada básicamente por cuerpos neuronales, y, en su parte
interna, por sustancia blanca formada por axones. El encéfalo presenta profundos entrantes (cisuras)
que delimitan zonas lobuladas (circunvoluciones). De diferentes zonas del encéfalo salen unos nervios
denominados nervios craneales. En el encéfalo se pueden distinguir las siguientes seis partes:
Cerebro. Esla partemás grande y en élreside la memoria, la capacidad de pensar y, porlo tanto, de tener
un lenguaje significativo y una capacidad creadora. Presenta una profunda cisura que lo divide en
dos hemisferios cerebrales.
Sistema límbico. Está en el centro profundo del cerebro (cuerpo calloso). Recibe las emociones(hambre,
sed, miedo, agresividad y deseo sexual) e interviene en las acciones de respuesta.
Tálamo. Actúa seleccionando las informaciones que van hacia el cerebro.
Hipotálamo. Regula el sistema nervioso autónomo. Además, influye en la glándula hipófisis a través de
dos vías: mediante neuronas y segregando hormonas.
Cerebelo. Interviene controlando los músculos responsables del mantenimiento de la postura y del
equilibrio corporal.
71
Bulbo raquídeo. Está bajo el cerebelo. En él se produce el control autónomo reflejo del ritmo
respiratorio y del cardíaco, la deglución, el vómito y la presión sanguínea.
b) MÉDULA ESPINAL. Presenta sustancia gris por dentro y sustancia blanca por fuera (al revés que el encéfalo).
De ella salen los nervios espinales que inervan losmúsculos, glándulas y órganos de la zona próxima. Realiza dos
funciones: en su sustancia gris se producen los reflejos espinales (ver el capítulo siguiente) y en su sustancia
blanca se realiza la transmisión de los impulsos nerviosos entre el encéfalo y el resto del cuerpo.
Órganos efectores.
Son los órganos que ejecutan las respuestas del Sistema Nervioso. Hay dos tipos de efectores, que son
los músculos (también denominados "efectores motores") y las glándulas exocrinas (también llamados
"efectores secretores"). Todos los efectores están estimulados por nervios es decir están "inervados".
Los nerviosse denominan nervios craneales sisalen del cráneo o nerviosraquídeos sisalen de la médula espinal.
El conjunto de todoslos nerviosforma eldenominado SistemaNervioso Periférico. Los efectoresmotores pueden
ser músculos de fibra estriada y contracción voluntaria o músculos de fibra lisa y contracción involuntaria. El
sistema nervioso que inerva los músculos de contracción voluntaria se denomina Sistema Nervioso Voluntario y
el sistema nervioso que inerva los músculos de contracción involuntaria y también las glándulas exocrinas se
denomina Sistema Nervioso Autónomo o Neurovegetativo.
La respuesta del Sistema Nervioso Voluntario.
La respuesta puede ser un acto reflejo o un acto voluntario.
Acto reflejo. Es el que se da cuando la respuesta se elabora en la médula espinal. Su coordinación nerviosa
consiste en una neurona sensitiva que conduce un impulso nervioso hasta la sustancia gris de la médula y allí lo
transmite a una neurona intercalar o de asociación, la cual lo pasa a una neurona motora que estimula el
movimiento de una fibra muscular.
72
También se puede producir sin intervención de la neurona intercalar, es decir con sólo dos neuronas. Se trata de
una respuesta muy rápida e inconsciente ante situaciones de peligro que necesitan una respuesta inmediata,
como por ejemplo cuando sentimos un pinchazo en una pierna. La sensación de dolor llega al cerebro después
de producirse el movimiento. Se trata pues de una especie de corto circuito en el recorrido normal de un acto
voluntario, con el fin de conseguir una respuesta muy rápida. También se puede producir sin intervención de la
neurona intercalar, es decir con sólo dos neuronas. Se trata de una respuesta muy rápida e inconsciente ante
situaciones de peligro que necesitan una respuesta inmediata, como por ejemplo cuando sentimos un pinchazo
en una pierna. La sensación de dolor llega al cerebro después de producirse el movimiento. Se trata pues de una
especie de corto circuito en el recorrido normal de un acto voluntario, con el fin de conseguir una respuesta muy
rápida. También se puede producir sin intervención de la neurona intercalar, es decir con sólo dos neuronas. Se
trata de una respuesta muy rápida e inconsciente ante situaciones de peligro que necesitan una respuesta
inmediata, como por ejemplo cuando sentimos un pinchazo en una pierna. La sensación de dolor llega al cerebro
después de producirse el movimiento. Se trata pues de una especie de corto circuito en el recorrido normal de
un acto voluntario, con el fin de conseguir una respuesta muy rápida. También se puede producir sin
intervención de la neurona intercalar, es decir con sólo dos neuronas. Se trata de una respuesta muy rápida e
inconsciente ante situaciones de peligro que necesitan una respuesta inmediata, como por ejemplo cuando
sentimos un pinchazo en una pierna. La sensación de dolor llega al cerebro después de producirse el
movimiento. Se trata pues de una especie de corto circuito en el recorrido normal de un acto voluntario, con el
fin de conseguir una respuesta muy rápida.
Acto voluntario. Es el que se da cuando la respuesta se elabora en el cerebro. Su coordinación nerviosa consiste
en una neurona sensitiva que comunica con una neurona de la médula, la cual comunica con una neurona que
va hasta el cerebro, allí intervienen varias neuronas (neuronas de asociación) y se emite un impulso nervioso de
respuesta que desciende por la médula y, a través de una neurona motora, llega hasta el músculo. En este caso
sí hay conciencia de la respuesta decidida antes de ejecutarla.
73
La respuesta del Sistema Nervioso Autónomo.
Este sistema controla las funciones que realizan nuestras vísceras independientemente de nuestra voluntad. Por
ejemplo, el latido cardíaco, los movimientos respiratorios, la digestión, la excreción, etc. Está constituido por
algunos nervios craneales (salen del cráneo) y por algunos nervios raquídeos (salen de la médula). Se distinguen
dos tipos de sistema nervioso autónomo:
El sistema nervioso simpático (SNS). Es el predominante en las situaciones de peligro. Provoca las acciones
adecuadas para la respuesta rápida como son: aumento del ritmo cardíaco, dilatación de los bronquios para
favorecer la entrada y salida de gases, aumento de la sudoración, disminución del peristaltismo intestinal para
disminuir la energía invertida en la digestión, vasoconstricción de las arterias, dilatación de las pupilas para que
entre más luz, etc.
El sistema nervioso parasimpático (SNP). Es el que predomina en las situaciones de reposo. Provoca acciones
adecuadas para la relajación y la inversión de mucha energía en la función digestiva. Estas acciones son:
disminución del ritmo cardíaco, disminución del ritmo respiratorio, disminución de la sudoración, aumento del
peristaltismo intestinal, vasodilatación de las arterias, contracción de las pupilas, etc.
La respuesta del sistema nervioso autónomo está controlada por el hipotálamo pero también presenta actos
reflejos, los denominados reflejos viscerales, como por ejemplo cambios de sudoración y de tensión muscular en
respuesta al calor localizado o de movilidad intestinal en respuesta a un estímulo.
AUTOEVALUACIÓN UNIDAD 7
1. ¿Cómo se denomina al sistema nervioso formado por el encéfalo y la médula espinal?
2. ¿Cómo se denominan cada uno de los cuatro lóbulos cerebrales?
3. ¿Qué estructura del sistema nervioso forman las membranas llamadas duramadre, piamadre
y aracnoides?
74
4. ¿El sistema nervioso autónomo es voluntario o involuntario?
5. ¿En qué estructura del encéfalo se encuentra el Tálamo y el hipotálamo?
6. ¿Cómo se denominan a cada una de las células propias del tejido nervioso, que son
responsables de la producción y la conducción del impulso nervioso?
7. ¿Cómo se denomina al sistema nervioso constituido por nervios y ganglios en el que se
puede distinguir dos sistemas, el simpático y parasimpático?
8. ¿Cuál de los nervios craneales tiene como función la de transmitir información desde la
retina a los centros visuales y que es de tipo sensorial?
9. ¿En qué estructura del sistema nervioso central (SNC) se encuentra el sistema límbico?
10. ¿Cómo actúa sobre los vasos sanguíneos la estimulación del sistema nervioso parasimpático?
11. ¿Cómo se denomina al trayecto que realizan uno o más impulsos nerviosos como respuesta
a un estímulo (golpe o dolor por ejemplo)?
12. ¿Qué estructura del encéfalo tiene como función la coordinación de la movilidad fina
por ejemplo el equilibrio?
13. ¿Qué lóbulos del cerebro están separados por la cisura de Rolando?
14. ¿Cómo se denominan los nervios encefálicos simétricos que comunican el encéfalo con
distintas zonas periféricas como ser la cabeza, el cuello, el tórax y el abdomen?
15. ¿Cómo se denomina al líquido que circula por el espacio subaracnoideo, los
ventrículos cerebrales y el canal medular (médula espinal)?
75
UNIDAD 8: SISTEMA REPRODUCTOR
INTRODUCCIÓN
La reproducción humana es la generación de nuevos individuos. La reproducción humana es de
tipo sexual puesto que se realiza a partir de dos gametos de diferente tipo, denominados
espermatozoides y óvulos, que se unen en el interior del cuerpo femenino (fecundación interna), tras
realizarse la cópula (coito), que es la introducción del pene masculino en la vagina de la mujer. La célula
que se forma, que se denomina zigoto, se multiplica constantemente (desarrollo embrionario)
originando un embrión que se alimenta a partir del cuerpo materno mediante un órgano denominado
placenta. Gracias a esto, el nuevo individuo ya sale completamente formado (viviparismo). En los
humanos la reproducción sexual no es un mero acto fisiológico, sino que precisa de un contexto de
afectividad y compromiso entre las dos personas para que psíquicamente sea satisfactorio para ambos.
Esto es una de las características de la sexualidad humana.
EL APARATO REPRODUCTOR MASCULINO.
Está constituido por dos testículos y dos epidídimos contenidos en una bolsa (escroto), dos conductos
deferentes acabados en una dilatación denominada "ampolla del conducto deferente", cinco glándulas
anejas (dos vesículas seminales, dos glándulas de Cowper y la próstata) que aportan sustancias
nutritivas, y dos conductos eyaculadores que desembocan en la uretra que recorre el interior del
órgano copulador o pene. El escroto permite que lostestículos estén a una temperatura inferior a la del
resto del cuerpo, lo cual es necesario para la formación de los espermatozoides (espermatogénesis)
Los testículos son unos órganos de unos 4 cm de diámetro mayor. En el interior de estos órgano hay
unos largos conductos muy replegados denominados conductos seminales, en el interior de los cuales
es dónde se generan los espermatozoides. También contiene las denominadas células de Leydig que
producen la hormona testosterona, que es la responsable de los caracteres sexuales masculinos (voz
grave, barba, espaldas anchas, etc.). Los epidídimos son los lugares donde se almacenan los
espermatozoides. Las vesículas seminales segregan un líquido nutritivo para los espermatozoides. La
próstata segrega el líquido prostático, que estimula los espermatozoides. Constituye la mayor parte
del líquido que contiene los espermatozoides, el denominado semen o esperma. Las glándulas de
Cowper segregan un líquido que lubrifica la uretra antes de la salida del semen (eyaculación).
El pene es el órgano copulador masculino. A su interior presenta tres cilindros de tejido esponjoso (2
cuerpos cavernosos arriba y 1 cuerpo esponjoso debajo), que en el momento de la excitación se llenan
de sangre. Esto provoca su erección y su aumento de tamaño. El extremo anterior recibe el nombre
de glande. Es una zona muy vascularizada y muy sensible que presenta un orificio denominado orificio
urinario o meato urinario. El glande está recubierto de una piel denominada prepucio, que al retirarse
permite que aflore el glande. Su excesiva estrechez se denomina fimosis. La operación de recortarlo
quirúrgicamente se denomina circuncisión
76
Fisiología del aparato reproductor masculino.
Los espermatozoides se generan en los conductos seminales de los testículos. Posteriormente se
almacenan en una estructura denominada epidídimo. En el momento de la eyaculación los
espermatozoides recorren el conducto deferente, el eyaculador (que sólo tiene unos 2 cm de longitud)
y la uretra. Durante el recorrido las glándulas anejas segregan las sustancias que constituyen la parte
líquida del semen. Aproximadamente se eyaculan unos 3cm3 de semen con una concentración de
espermatozoides de (100 millones/cm3
) Fisiología del aparato reproductor masculino. Los
espermatozoides se generan en los conductos seminales de los testículos. Posteriormente se
almacenan en una estructura denominada epidídimo. En el momento de la eyaculación los
espermatozoides recorren el conducto deferente, el eyaculador (que sólo tiene unos 2 cm de longitud)
y la uretra. Durante el recorrido las glándulas anexas segregan las sustancias que constituyen la parte
líquida del semen. Aproximadamente se eyaculan unos 3cm3 de semen con una concentración de
espermatozoides de (100 millones/cm3
)
EL APARATO REPRODUCTOR FEMENINO.
Está formato por dos ovarios, dos trompas de Falopio u oviductos, que son dos conductos con el
extremo libre dilatado y capaz de recoger los óvulos que producen los ovarios, un órgano de paredes
musculosas y muy dilatables denominado útero o matriz, un conducto elástico denominado vagina y
dosrepliegues cutáneos gruesos que cierran su entrada y que forman los genitales externos femeninos
o vulva
Los ovarios tienen una longitud de unos 3 cm y están sustentados por ligamentos. Las trompas de
Falopio tienen unos 15 cm de longitud y presentan unas prolongaciones denominadasfímbrias.
El útero es una bolsa con forma de pera invertida de unos 6 a 9 cm de largo y 3 a 4 cm de ancho. En él
se puede diferenciar una entrada o cuello y el resto o cuerpo uterino. Éste presenta unas paredes muy
musculosas y una capa mucosa muy vascularizada, el endometrio, que cada mes se desprende en parte
(menstruación) y que, después,se vuelve a regenerar. La vagina es un conducto musculoso y elástico de
unos 8 a 12cm, capaz de alojar el pene durante el coito. En la vulva o genitales externos femeninos se
puede diferenciar los siguientes elementos: los dos labios mayores (dos gruesos repliegues cutáneos
cubiertos de pelos), los dos labios menores (dos fines repliegues cutáneos internos), el clítoris (un
pequeño órgano eréctil muy sensible), el orificio uretral o meato urinario (el orificio de salida de la
orina) y el orificio vaginal (el orificio del aparato reproductor), que está parcialmente cerrado por una
membrana denominada himen, que se rasga al realizarse el primero coito.
77
Fisiología del aparato reproductor femenino.
Aproximadamente cada mes, en un u otro de los dos ovarios, un folículo ovárico madura y libera
un óvulo. El resto del folículo se transforma en el cuerpo blanco o cuerpo álbicans y posteriormente se
cicatriza. El óvulo entra en la trompa de Falopio dónde puede unirse a un espermatozoide si ha habido
una cópula. Si el óvulo no es fecundado, tras recorrer la trompa de Falopio, atraviesa el útero y
la vagina y sale al exterior. Al cabo de dos semanas, como no hay ningún embrión que acoger,
el endometrio uterino se desprende (menstruación). Posteriormente se regenera en tan sólo 5 días.
La formación de las células sexuales.
Las células sexuales o gametos son células especiales que presentan la mitad de cromosomas que las
células del resto del cuerpo, las denominadas células somáticas. Gracias a ello cuando se juntan dos
células sexuales de diferente tipo para formar la primera célula somática del nuevo ser, se recupera
el número de cromosomas propio de estas células. Si no fuera así los hijos tendrían el doble de
cromosomas que suspadres.Hace falta recordar que un cromosoma es unamolécula deADNenrollada
sobre sí misma y que un gen es un segmento de ADN que contiene una información sobre una
determinada característica del organismo. En los humanoslas célulassomáticastienen 46 cromosomas
y los gametos tienen 23 cromosomas.
El paso de células somáticas a células sexuales se denomina meiosis y consiste en dos divisiones
celularessucesivas. Hay dostipos de meiosis: la espermatogénesis o generación de las célulassexuales
de los hombres, que son los espermatozoides, y la ovogénesis o generación de las células sexuales de
las mujeres, que son los óvulos. En la espermatogénesis por cada célula madre se originan 4
espermatozoides,mientras que en la ovogénesis por cada célulamadre sólo se origina un óvulo, puesto
que en cada división se degrada una de las dos células hijas.
Se diferencian dos tipos de cromosomas, los que determinan el sexo del individuo, los
denominados cromosomassexuales, que son el cromosoma X y el cromosoma Y, y los 44 cromosomas
restantes, los denominados cromosomas no sexuales que son comunes a mujeres y hombres. Si en
las células hay dos cromosomas X el individuo es mujer y si hay un X y un Y el individuo es un hombre.
En el dibujo siguiente se expone como esla gametogénesis en la rata. En los humanos el proceso es un
pocomás complicado, puesto que el espermatozoide no se une a un óvulo sino a un ovocito de segundo
orden.
El ciclo menstrual.
Se denomina menstruación al desprendimiento del endometrio, que es la capa que tapiza el interior
del útero. Este proceso va acompañado de pérdida de sangre y de molestias que pueden ser
importantes, dura entre 3 y 5 días y se repite cada 28 a 32 días, por lo cual recibe el nombre de ciclo
menstrual. La menstruación está controlada por dos hormonas hipofisárias, la FSH y la LH.
1) La FSH estimula que madure un folículo ovárico y que los ovarios produzcan las denominadas
hormonas estrógenas, las cuales estimulan el engrosamiento del endometrio del útero.
2) La LH provoca que el folículo ya maduro libere su óvulo (ovulación) y que se transforme en cuerpo
lúteo, el cual produce la hormona progesterona que actúa estimulando la continuación del
engrosamiento del endometrio. La ovulación se produce cuando la concentración de LH en la sangre
alcanza su máxima superioridad respecto a la concentración de la FSH.
3) Cuando la hormona progesterona empieza a disminuir se produce el desprendimiento del
endometrio o menstruación, que dura de 3 a 5 días. El óvulo se libera unas dos semanas después del
inicio de la menstruación y tiene una vida de unas 24 horas, durante las cuales puede ser fecundado.
78
Glándula mamaria
La mama está formada principalmente por tejido adiposo (grasa) y la glándula mamaria. Con los ciclos
hormonales y el embarazo, el tejido predominante es el glandular, mientras que, tras la menopausia,
la glándula se atrofia y el volumen de la mama depende básicamente del tejido adiposo. El tejido
adiposo mamario es uno de los que más se afecta con las oscilaciones del peso, siendo de los primeros
tejidos que disminuyen de tamaño al adelgazar, y de los primeros que aumentan al incrementar el
peso. La glándula está formada por diferentes lobulillos glandulares (entre 15 y 20), de los
cuales salen
los conductos galactóforos que confluyen en el seno galactóforo. Esta última estructura comunicará
el interior de la mama con el exterior a través del pezón, y es por donde se expulsa la leche en la
lactancia. La mama se extiende desde la 2ª hasta la 6ª costillas, medialmente hasta el esternón (a unos
2 cm de la línea media) y lateralmente hasta la línea media axilar. Está anclada a la fascia del músculo
pectoral mayor mediante los ligamentos de Cooper. La cola de la mama o cola de Spence, extiende la
mama oblicuamente hacia la axila.
El complejo areola-pezón (CAP)se encuentra entre la 4ª y 5ª costilla en mamas no ptósicas(no caídas),
lateral a la línea medioclavicular. La distancia ideal entre el pezón y la horquilla esternal se sitúa entre
19 y 21 cm, aunque puede variar en función de la constitución de la mujer. Esta medida es similar al
segmento que une la línea medio clavicular con el pezón. Cifras incrementadas en estas medidas
pueden indicar que el pecho está ptósico (caído). Otras medidas importantes se encuentran entre el
surco submamario y el pezón (situado en 5-6 cm) y del pezón a la línea media (entre 9 y 11 cm).
El diámetro areolar suele situarse en torno a los 4-5 cm, y en el centro se sitúa el pezón, con una
proyección de 1 cm y un diámetro de unos 5 mm. La horquilla esternal y los pezones deben formar
un triángulo equilátero.
Todo el tejido mamario está vascularizado principalmente por vasos perforantes de la arteria y venas
mamarias internas, situados a los lados del esternón. También recibe vascularización de los vasos
torácicos laterales, rama de la arteria axilar. Otras arterias que aportan vascularización a la mama son
los intercostales y toracoacromiales. Conocer la vascularización de la mama es esencial para poder
realizar determinadas cirugías como reducciones mamarias, mamas tuberosas e incluso mamoplastias
79
de aumento. Una planificación sin tener en cuenta los patrones vasculares puede llevar al fracaso de
la cirugía e incluso a la pérdida del complejo areola-pezón.
El líquido intersticial de la glándula mamaria es drenado mediante los vasos linfáticos de la mama a
través de los linfáticos interlobulillares que confluyen formando el plexo linfático subareolar. Todos
ellos drenan a los ganglios linfáticos, situados principalmente en la axila, aunque también puede estar
en las proximidades de los vasos mamarios internos e incluso supraclaviculares. Este drenaje linfático
tiene especial relevancia sobre todo en los tumores malignos, que usan los vasos linfáticos para
propagar la enfermedad a distancia.
En el embarazo y por acción de las hormonas segregadas se produce un aumento de los conductos y
acinos desde la 5-8 semana de gestación. Además, se produce un aumento de la vascularización y una
dilatación venosa superficial y una hiperpigmentación de la areola y el pezón. En la primera mitad de
la gestación aumenta el sistema de conductos y se forman nuevos acinos. En la segunda mitad de
gestación se inicia la actividad secretora y esla responsable del aumento de volumen mamario a partir
de las 20 semanas de embarazo.
A los 2-4 días postparto se ingurgitan las mamas por el aumento de secreción en ellas. Se inicia la
lactogénesis después del parto, es decir la secreción de leche, estimulada por la producción de
prolactina en la hipófisis. La velocidad de producción en los diferentes alveolos hace que la leche se
produzca de forma continua. Elreflejo liberador de prolactina se produce por el estímulo areola-pezón
que por vía de un reflejo neurohormonal permite la liberación de prolactina que estimulará la
producción de leche a nivel de las células alveolares mamarias. Se necesita un estímulo adecuado de
succión para mantener la producción de prolactina.
La leche de los alveolos no fluye espontáneamente a los conductos, sino que precisa del reflejo
eyectolácteo. Las fibras mioepiteliales de los alveolos se contraen en respuesta a la oxitocina
liberada por la hipófisis y evacuan la leche hacia los conductos. El estímulo a la liberación de oxitocina
es básicamente los estímulos mecánicos del complejo areola-pezón pero también se libera por
estímulos visuales, auditivos u olfatorios. La oxitocina es la hormona de la galactopoyesis, es decir del
mantenimiento de la lactancia.
AUTOEVALUACIÓN UNIDAD 8
1. ¿Cómo se denominan las gametas masculinas?
2. ¿Cómo se denomina el pliegue de la piel que recubre y protege al glande?
3. ¿Cómo se denominan las glándulas accesorias de los órganos genitales femenino que se hallan a
ambos lados del orificio vaginal y sus secreciones actúan como lubricante de los órganos genitales
externos?
4. ¿A qué se denomina fecundación propiamente dicha?
5. ¿Cuálesson las dos hormonas del ciclo menstrual que interactúan entre el útero, ovario y la hipófisis?
6. ¿Cuáles son las gónadas femeninas?
7. ¿Cuál es la función de la uretra en el hombre como parte de su sistema reproductor?
8. ¿Cómo se denomina el conducto en el que los espermatozoides se almacenan y maduran hasta
cuatro semanas?
80
9. ¿Dónde se encuentra el endometrio?
10. ¿En qué estructura del aparato reproductorfemenino se produce la unión entre el espermatozoide
y el óvulo (fecundación)? ¿Cuáles son las gónadas femeninas?
11. ¿Con qué nombre se conoce a la primera menstruación?
12. Describa qué tipo de tejido forma la glándula mamaria y enumere por lo menos TRES (3)
estructuras que formen parte de esta glándula?
13. ¿En qué estructura del aparato reproductor masculino encontramos a los denominados cuerpos
cavernosos?
14. Explique por qué los testículos son glándulas de secreción mixta (endócrina y exócrina)?
LICENCIATURA EN ENFERMERÍA
GUÍA DE ESTUDIO EXAMEN INGRESO

ASIGNATURA: ELEMENTOS BÁSICOS de las CIENCIAS EXACTAS

INTRODUCCIÓN

Las ciencias exactas son aquellas ciencias que producen conocimiento científico a partir de modelos teóricos apli-
cados, empíricos, cuantificables, por lo general experimentales, que se basan en los pasos del método científico y

en la objetividad como los mecanismos para comprender sus diferentes áreas de estudio.
Se las distingue de las llamadas ciencias blandas o ciencias humanas, cuyos ejes de estudio se sostienen en la
conjetura, el análisis cualitativo y experimentos que arrojan resultados inciertos, no predictivos.
No se trata de una clasificación universal ni determinante de las ciencias, sino que usualmente estos términos,
duras, puras, exactas se emplean un poco coloquialmente para discernir ciertos campos delsaber. De hecho,
ninguna ciencia contemporánea abraza o pretende paradigmas de exactitud o de verdad inmutable, sin
importar los métodos y aproximaciones en que se sustente.
Nuestra guía de estudio estará integrada por nociones básicas de matemática, de física y de química.

Matemática: Dado que opera en base a un conjunto de relaciones, signos y proporciones de índole lógica y abs-
tracta, la matemática en tanto ciencia formal echa mano a métodos exactos y determinados, repetibles y deduci-
bles, más o menos experimentales. Se la considera el epítome de las ciencias formales, ya que muchas otras,

como la física, se sirven de ella para establecer su lectura del mundo.
Física: A menudo entendida como matemática aplicada a la descripción de los fenómenos y fuerzas que ocurren

en la realidad circundante, se fundamenta en la aspiración de una medición formal y descripción teórica del uni-
verso. Para ello emplea la experimentación, la observación y numerosos instrumentos. Muchos aspectos de los

seres vivos guardan relación con leyes de la Física, por ejemplo, los conocimientos de la mecánica son usados para

explicar el sostén, equilibrio y movimiento del organismo (mecánica corporal), el potencial eléctrico y la conducti-
bilidad intervienen en la formación y transmisión del impulso nervioso. Una de las principales áreas frontera en

este nivel es la biofísica, que trata la influencia de los fenómenos físicos en los seres vivos, en nuestro caso al ser
humano.

Química: Estudia el funcionamiento de la materia y las relaciones atómicas en ella, la química emprende la expe-
rimentación como un modo de demostrar con más o menos exactitud un conjunto de sus principios teóricos fun-
damentales, replicables en laboratorio y con numerosas aplicaciones cotidianas demostrables. Las principales

áreas fronteras de este nivel son la biología molecular, la bioquímica y la química biológica, que estudian el papel
de las biomoléculas en los seres vivos, en nuestro caso el ser humano, y el metabolismo celular.
Las ciencias exactas forman parte de la vida de todos los individuos. A medida que se incrementa el uso de la
tecnología (la aplicación de la ciencia) y nuestra dependencia a ella, los conceptos científicos y sus consecuencias
intervendrán cada vez más en la vida de individuos, comunidades y naciones. Como ciudadanos es nuestro deber
tomar decisiones respecto a la problemática en la que intervienen factores químicos y físicos, para lo que es
necesario dominar dichos conceptos.
Todos los días entramos en contacto con el cambio químico, físico o con materiales útiles que se obtuvieron
gracias al conocimiento de esta ciencia.
El aprendizaje de las Ciencias Exactas, además de aportar conocimientos indispensables para comprender los

asombrosos cambios que se producen a nuestro alrededor, permite el desarrollo de destrezas, hábitos y habili-
dades intelectuales necesarias para la formación integral de los futuros cadetes del Colegio Militar de la Nación

y futuros profesionales de la salud.
Hay una fuerza motriz más poderosa que el vapor, la electricidad y la energía atómica: la voluntad”
Albert Einstein

2 - 51

OBJETIVO DE LA GUIA DE ESTUDIO
Esta guía de estudio no nos vamos a limitar a la simple memorización de símbolos, reacciones, nombres
y fórmulas,sino que vamos a aprendermás que eso. Es verdad que ciertamemorización es necesaria, pero
lo importante es adquirir conceptos y estrategias para comenzar a razonar y así a comprender.
Por ello lo invitamos a recorrer esta guía de estudio, que incluye los temas del programa de la materia y
el desarrollo de los mismos a modo de orientación o guía de lo que se les pedirá en el examen de ingreso
para que demuestre e integre los conocimientos de la física de la química y de la matemática a la biología
humana y demuestre habilidades al resolver los problemas y ejercicios de autoevaluación, problemas
modelos de los que se tomarán en el examen de ingreso.

ORGANIZADOR DE CONTENIDOS

BIBLIOGRAFÍA: ver programa de estudios
NOTA: al final de la presente guía usted encontrará un glosario
Elementos Básicos de
las Ciencias Exactas

Eje Estructural I
“Matemática”

Eje Estructural II
“Física”

Eje estructural III
“Química”

UD.1: Operacio-
nes básicas

UD. 2: Elemen-
tos básicos de la

física

UD.3: Elementos
básicos de la
química

UD.4: Soluciones

UD. 5: Ácidos y
Bases

UD. 6:Química
Orgánica

3 - 51
UNIDAD 1

1- Razón
Una razón es una comparación entre dos o más cantidades. Es el cociente entre dos términos. Puede expresarse
mediante una fracción. Si las cantidades a comparar son a y b, la razón entre ellas se escribe como:

a
b

Ejemplo: En una sala de clases hay 10 mujeres y 18 hombres. ¿Qué relación numérica existe entre el número de
mujeres y el número de hombres?
La relación entre el número de mujeres y el número de hombres es de "10 a 18"
En una razón el término a (numerador) es el antecedente de la razón y el b (denominador), el consecuente.

El resultado de la división o cociente entre el antecedente y el consecuente se denomina valor de la razón o co-
ciente.

Dos o más razones son equivalentes cuando tienen igual valor.
2- Proporciones
Una proporción es la igualdad de dos razones.

https://www.youtube.com/watch?v=jboHWe4_6D8

Propiedad fundamental En toda proporción, el producto de los términos medios es igual al producto de los térmi-
nos extremos (Teorema fundamental de las proporciones). Es decir:

Entonces se lee o interpreta “a multiplicado por d es igual a b multiplicado por c”

4 - 51

Ejemplo: Si tenemos la proporción:

Y le aplicamos la propiedad fundamental señalada queda:
3 • 20 = 4 • 15, es decir, 60 = 60
3 x 20 = 4 x 15, es decir, 60 = 60

Esta es la propiedad que nos permite detectar si dos cantidades presentadas como proporción lo
son verdaderamente. Otros ejemplos:
a) x
10
=
5
30
x . 30 = 10 . 5 x = 10 .5
30
=
50
30
= 1,67

b) 20
8
=
x
24
x . 8 = 20 . 24 x = 20 .24
8
=
480
8
= 60

c) 3
x
=
48
25
x . 48 = 3 . 25 x = 3 . 25
48
=
75
48
= 1,5625

3- Regla de tres simple

Seguimos trabajando con la proporcionalidad. Esta vez, veremos una forma de resolver los proble-
mas de proporcionalidad, directa e inversa: la regla de 3 simple.

Si la relación entre las magnitudes es directa (cuando aumenta una magnitud también lo hace la otra) hay que apli-
car la regla de tres simple directa.

Por el contrario, si la relación entre las magnitudes es inversa (cuando aumenta una magnitud disminuye la otra)
se aplica la regla de tres simple inversa.
¿Qué es la regla de 3 simple?

La regla de 3 simple es una operación que nos ayuda a resolver rápidamente problemas de proporcionali-
dad, tanto directa como inversa.

Para hacer una regla de tres simple necesitamos 3 datos: dos magnitudes proporcionales entre sí, y una
tercera magnitud. A partir de estos, averiguaremos el cuarto término de la proporcionalidad.
Regla de 3 simple directa
Empezaremos viendo cómo aplicarla en casos de proporcionalidad directa (cuando aumenta una
magnitud también lo hace la otra). Colocaremos en una tabla los 3 datos (a los que llamamos «a», «b» y
«c») y la incógnita, es decir, el dato que queremos averiguar (que llamaremos “x”). Después, aplicaremos la
siguiente fórmula:

5 - 51

Ejemplo:
Al llegar al hotel nos han dado un mapa con los lugares de interés de la ciudad, y nos han dicho que
5 centímetros del mapa representan 600 metros de la realidad. Hoy queremos ir a un parque que
se encuentra a 8 centímetros del hotel en el mapa. ¿A qué distancia del hotel se encuentra este
parque?
Resolución: Vamos a hacer la tabla con los 3 datos y la incógnita (“x”), y hallaremos “x” con la fórmula
que acabamos de aprender:

Solución: El parque se encuentra a 960 metros del ho-
tel

https://www.youtube.com/watch?v=_JeR bXzG0
4- Promedio
El valor medio (también se llama la media) es simplemente el promedio de los números.

Es fácil de calcular: sólo se suma los números, después divide por cuántos números hay. (En otras pala-
bras es la suma dividida por el número de cifras).

Ejemplo 1: ¿Cuál es el promedio de estos números? 3, 10, 5
Suma de los números: 3 + 10 + 5 = 18
Dividir por cuántas cifras hay (tenemos 3 cifras): 18 ÷ 3 = 6 El promedio es 6
Ejemplo 2: Calcular el promedio de estos valores: 3, 7, 5, 13, 20, 23, 39, 23, 40, 23, 14, 12, 56, 23, 29
La suma de estos números (3 + 7 + 5 + 13 + 20 + 23 + 39 + 23 + 40 + 23 +14 + 12 + 56 +23 + 29) = 330
Hay quince cifras.
El promedio es igual a 330 ÷ 15 = 22
https://www.youtube.com/watch?v=_B50eYV44-k

6 - 51

5- Porcentaje
Si hablamos de porcentajes a todos nos resulta un tema familiar, pero: ¿sabríamos decir qué es un
porcentaje? ¿cómo se calcula? y ¿qué significa exactamente?
El porcentaje es, realmente, un símbolo.
Un símbolo que representa una fracción de denominador 100. Así, en el lenguaje escrito, es mucho
más sencillo escribir el porcentaje que la fracción:

Este símbolo (%) se lee como “por ciento” e indica, como hemos dicho, el número de partes en
que la unidad, o cantidad de referencia, ha sido dividida. Es decir, el porcentaje (%) siempre
aparece en una expresión que relaciona dos cantidades. Por ejemplo: “El 13% de los niños que hacen
Smartick eligen el juego de Enredados para jugar después de su sesión”. En este caso, las cantidades que
se están relacionando son la cantidad de niños que hacen Smartick con la cantidad de esos niños
que, además eligen jugar a Enredados después de su sesión.
Pero, ¿cómo podríamos calcular el número exacto de niños que eligen jugar a Enredados? Bien, es
muy sencillo, pero debemos saber algunas cosas:
Multiplicar fracciones y Cuántos niños hacen Smartick: imaginemos que fueran solo 300 niños.

Como sabemos la cantidad de referencia (el número de niños que hacen Smartick) solo tenemos
que multiplicar la fracción que nos indica el porcentaje 13%, es decir, “13 partido de 100” por
300. Donde lo que hacemos es dividir la cantidad de referencia en 100 partes iguales y tomar 13.
Así, 300 entre 100 es 3. Que multiplicado por 13 es 39. Por tanto 39 de los 300 alumnos de
Smartick eligen el juego de Enredados después de sus sesiones.
Para más información
https://www.youtube.com/watch?v=gM9BAOBeTKg
https://www.youtube.com/watch?v=LKwYjUV5Exo
https://www.youtube.com/watch?v=bVOzZbmytcI
https://www.ematematicas.net/porcentajes.php?a=&tp=5
https://www.profesorenlinea.cl/matematica/Porcentaje_calcular.html

7 - 51

AUTOEVALUACIÓN UNIDAD 1

1. Según últimos datos, en nuestro país el 61,6% de la población posee exceso de peso, pudiéndose
clasificar dentro de este 61,6% a individuos con sobrepeso e individuos con obesidad. Si la población de
nuestro país alcanza a un total de 44.270.000 habitantes
a) Calcular el número de habitantes de nuestro país con exceso de peso
b) Si aproximadamente la cuarta parte de los individuos con exceso de peso son considerados obesos,
calcular el número de individuos obesos en nuestro país
2. En la Argentina, cuatro de cada diez individuos es hipertenso. Exprese una razón matemática a partir
de los datos del texto leído.
3. La relación nutricional calcio/hierro adecuada en un neonato es una relación dos a uno (2:1). ¿Cuántos

gramos de calcio serán necesarios por cada 50 miligramos de hierro para conservar la proporción expre-
sada anteriormente?

4. A un individuo hay que administrarle, en 8 horas, un litro de solución fisiológica. Calcular cuántas gotas
por minuto se deberá administrar ese litro de solución fisiológica.
DATOS: 1 mililitro = 20 gotas. 1 hora = 60 minutos

5. Cada cien mililitros de leche materna hay 0,9 de proteínas y de éstas el 40% corresponde a la ca-
seína. Calcularlos gramos de proteínas y los miligramos de caseína que habrá en un cuarto litro de leche

materna.
6. En promedio el esqueleto humano pesa aproximadamente el 15% de nuestro peso corporal. Calcule
el peso de su propio esqueleto.

7.El fémur en promedio mide aproximadamente el 25% de la altura de un individuo. Calcular la longi-
tud del fémur de una persona de 1,72 metros.

8 - 51
UNIDAD 2

1- Magnitudes

Las magnitudes son propiedades físicas que pueden ser medidas, como por ejemplo temperatura, longi-
tud, fuerza, corriente eléctrica, etc. Encontramos dos tipos de magnitudes, las escalares y las vectoriales.

Magnitudes escalares

Las magnitudes escalares tienen únicamente como variable a un número que representa una determi-
nada cantidad seguida de una unidad. La masa de un cuerpo, se mide en kilogramos (5 kg), el volumen,

que se mide en mililitros (500 ml) o litros (2 l), la temperatura, en grados centígrados o la longitud en
metros (5 m), son algunos ejemplos de magnitudes escalares.

Magnitudes vectoriales
En muchos casos las magnitudes escalares no nos dan información completa sobre una propiedad física.

Por ejemplo, una fuerza de determinado valor puede estar aplicada sobre un cuerpo en diferentes sen-
tidos y direcciones. Tenemos entonces las magnitudes vectoriales que, como su nombre lo indica, se re-
presentan mediante vectores, es decir que además de un módulo (o valor absoluto) tienen una dirección

y un sentido.
Ejemplos de magnitudes vectoriales son la velocidad, la fuerza, la aceleración y el campo eléctrico.

VOLUMEN Y CAPACIDAD
Volumen y capacidad son dos conceptos que hacen referencia al espacio que un cuerpo cualquiera puede
ocupar. Ambos se interrelacionan en atención a que, son propiedades que poseen los cuerpos en sus
diferentes estados.
Volumen
El volumen se puede definir como el espacio que ocupa un cuerpo en un lugar determinado, es decir, la
cantidad de espacio que ocupa su materia y que no podrá ser ocupada por otro cuerpo a la vez. Asimismo,
el espacio o volumen ocupado por la materia, puede medirse cuantitativamente en cualquiera de las
diversas unidades de medida.

9 - 51

El Sistema Internacional de Unidades establece como unidad principal de volumen al metro cúbico. Tam-
bién se encuentran el decímetro cúbico y centímetro cúbico. En los cuerpos sólidos de forma regular, el

volumen está determinado por sus dimensiones y se obtiene aplicando una fórmula matemática para
obtener el resultado de sus tres dimensiones (largo, ancho y alto).
Finalmente, el volumen indica cuánto espacio ocupa un objeto, es decir, es la masa y el tamaño de un
cuerpo. Por lo tanto, el volumen es una cualidad susceptible de ser medida, cualquier objeto del mundo
tiene volumen independientemente de su tamaño y de su forma o de su estado.
Capacidad

La capacidad es la propiedad de poder contener cierta cantidad de alguna cosa hasta un límite determi-
nado. La unidad principal para medir la capacidad de un objeto es el litro (L) pero ésta es una unidad

divisible. Adicionalmente, están los múltiplos, que son las unidades para expresar capacidades más gran-
des que el litro y los submúltiplos, que son las unidades para expresar capacidades más pequeñas.

En este sentido, las unidades derivadas son el kilolitro, el decalitro, el hectolitro, el decilitro, el centilitro
y el mililitro.
En atención a lo anteriormente señalado, se puede decir que, la capacidad y el volumen son términos
que se encuentran estrechamente relacionados, debido a que, ambasse refieren al espacio que ocupa un
cuerpo. Por lo tanto, las principales diferencias entre volumen y capacidad son:

 El volumen hace referencia al espacio que ocupa un objeto mientras que la capacidad hace referen-
cia al espacio que contiene.

 Calcular el volumen de un cuerpo es medir cuánto ocupa mientras que calcularsu capacidad es me-
dir cuánto cabe en él.

 La unidad de medida del volumen es el metro cúbico mientras que la unidad de medida de la capaci-
dad es el litro.

 El volumen es la masa y el tamaño de un cuerpo mientras que la capacidad de un recipiente u ob-
jeto es la cantidad de volumen que cabe dentro del mismo.

Equivalencia de unidades
1 l = 1000 cm3
1 l = 1000 ml

Como los primeros miembros son iguales los segundos también lo son, por lo tanto

1 cm3 = 1 ml

Aplicando las propiedades de las proporciones se puede calcular el valor de una incógnita, conociendo la
relación de equivalencia
1 l
1000cc
=
x
300 cc
x . 1000 cm3 = 1l . 300 cm3
x =
1l .300cc
1000 cc
= 0, 3 l

10 - 51

¿Cuántoslitrosrepresentan 174,2 mililitros?
1000 ml 1 litro
174,2 ml X = 0,1742 litros
¿Cuántos mililitrosrepresentan 0,25 litros?
1 l 1000 ml
0,25 l X = 250 ml
RECORDAR:
La unidad ml (mililitro) es equivalente a cm3

(centímetro cúbico) es decir que 10 ml = 10 cm3

; 150 ml = 150 cm3

PESO Y MASA
La masa es la cantidad de materia que posee un cuerpo y el peso es la medida de esa masa. Si bien
conceptualmente masa y peso no es lo mismo, si podemos utilizar sus unidades de medición en forma
común.
La unidad patrón es el gramo (g) y tendremos varios múltiplos y submúltiplos de los cualessólo usaremos:

Múltiplo: Kilogramo (Kg) Submúltiplo: miligramo (mg)

Unidades de equivalencia
1 kg = 1000 g
1 g = 1000 mg

Aplicando las propiedades de las proporciones se puede calcular el valor de una incógnita, conociendo la
relación de equivalencia
1 kg
1000mg
=
x
300 mg
x . 1000 mg = 1kg . 300 mg x = 1kg .300mg
1000 mg
= 0, 3 kg

1 kg
1000 mg
=
0, 75 kg
x

x . 1 g = 1000 mg . 0,75 g x =

1000 mg . 0,75 kg =

750 = 750 mg
1 kg 1

¿Cuántos gramos representan 400 miligramos?
1000 mg 1 g
400 mg X = 0,4 g
¿Cuántos miligramos representan 0,9 gramos?
1 g 1000 mg
0,9 g X = 900 mg
¿Cuantos kilos representan 750 gramos?
1000 g 1 kg
750 g X = 0,75 g
Generalmente cuando alguien nos pregunta cuanto pesamos,solemos dar un valor en kilogramos(Kg). Si
usted se fija en clases anteriores, la unidad con que estás expresando su peso es de masa. Esto es un
error general y es que habitualmente suelen confundirse los conceptos de masa y peso.

11 - 51

El peso es la fuerza de atracción que la Tierra ejerce sobre cualquier objeto. Su dirección y sentido se
orienta hacia el centro de esta y como fuerza que es, se mide en newtons (N).

P = m⋅g

donde:
 P: es el peso de un cuerpo.
 m: es su masa.

 g: es la gravedad o aceleración con la que caen los cuerpos sobre la Tierra. Su valor es aproxima-
damente 9.8 m/s2 a nivel del mar. Su valor disminuye cuanto más nos alejamos del centro de la

Tierra.
Aunque en la vida cotidiana se confundan, la masa y el peso son bastante diferentes:
 La masa se mide en kilogramos y el peso en newtons.
 La masa es independiente del lugar donde la midamos, es intrínseco del cuerpo, sin embargo, el
peso no. Cuanto más alejados del centro de la Tierra nos encontremos, menor será nuestro peso,
ya que la gravedad disminuye a medida que nos alejamos de dicho centro, pero la masa siempre
será la misma, en cualquier lugar del universo
Así que, si tienes una masa de 50Kg, tu peso en la superficie terrestre será: P = 50 Kg· 9.8 m/s2 = 490 N.
Cuando alguien tepregunte lapróxima vez portu peso,puedesdecirle sintemor a equivocarte: "¿Mipeso?
490 Newtons"

12 - 51

2. Fuerza
Denominamos fuerza a toda acción capaz de producir cambios en el movimiento o en la estructura de
un cuerpo.

Si empujamos una bola con el dedo le estaremos aplicando una fuerza. Tras aplicarla caben varias posi-
bilidades. Una de ellas es que empiece a moverse. Otra es que se deforme. Dependiendo de donde la

apliquemos, en qué dirección, sentido o cantidad, la bola se moverá o deformará hacia un lado o a otro.

Por tanto, es lógico pensar que las fuerzas tienen un carácter vectorial, de hecho, son magnitudes vec-
toriales.

Como vector que es, las fuerzas se representan como una flecha, que se caracterizan por su longitud
(módulo), donde se aplica (punto de aplicación), su dirección y sentido.

La fuerza es una magnitud vectorial que representa toda causa capaz de modificar el estado de movi-
miento o de reposo de un cuerpo o de producir una deformación en él.

Su unidad en el Sistema Internacional es el Newton (N). Un Newton es la fuerza que al aplicarse sobre
una masa de 1 Kg le provoca una aceleración de 1 m/s2
.

Unidad de Fuerza
Adicionalmente alNewton (N)suelen utilizarse otras unidades para medirlasfuerzas. Entre ellas podemos
encontrar: dina (d). 1 d = 10-5 N
Efectos de las fuerzas
Tal y como hemos visto anteriormente, las fuerzas son las responsables de producir:
 cambios de velocidad, o lo que es lo mismo, aceleración
 deformaciones en un cuerpo.
En el primer caso, si la dirección de la fuerza que se aplica a un cuerpo libre no pasa por su centro de
gravedad, le producirá un movimiento de rotación (giro) y un movimiento de traslación (desplazamiento).
https://www.youtube.com/watch?v=NBY8cnL4Tdshttps://www.youtube.com/watch?v=NBY8cnL4Tds

Sabemos que la materia es todo aquello que ocupa un
lugar en el espacio y tiene masa.
También sabemos que los estados de la materia son los
estados sólidos, líquido y gaseoso.
Pero sabemos ¿A qué estado o estados de la materia
llamamos FLUIDOS?

13 - 51

3. FLUIDOS

Un fluido es todo cuerpo que tiene la propiedad de fluir, y carece de rigidez y elasticidad, y en conse-
cuencia cede inmediatamente a cualquier fuerza tendente a alterarsu forma y adoptando así la forma del

recipiente que lo contiene. Los fluidos pueden ser líquidos o gases según la diferente intensidad de las
fuerzas de cohesión existentes entre sus moléculas.
En los líquidos, las fuerzas intermoleculares permiten que las partículas se muevan libremente, aunque
mantienen enlaceslatentes que hacen que lassustancias en este estado presenten volumen constante o
fijo. Cuando se vierte un líquido a un recipiente, el líquido ocupará el volumen parcial o igual al volumen
del recipiente sin importar la forma de este último.
Loslíquidosson incompresibles debido a que su volumen no disminuye al ejercerle fuerzas muy grandes.

Otra de sus propiedades es que ejercen presión sobre los cuerpos sumergidos en ellos o sobre las pare-
des del recipiente que los contiene. Esta presión se llama presión hidrostática.

Los gases,por el contrario, constan de partículas enmovimiento bien separadas que chocanunas con otras
y tratan de dispersarse, de tal modo que los gases no tienen forma ni volumen definidos. Y así adquieren

la forma el recipiente que los contenga y tienden a ocupar el mayor volumen posible (son muy expandi-
bles). La presión que los gases ejercen sobre la superficie del recipiente que los contiene es directamente

proporcional a la concentración de los mismos.
Los gases son compresibles; es decir, su volumen disminuye cuando sobre ellos se aplican fuerzas. Por
ejemplo, cuando se ejerce fuerza sobre el émbolo de una jeringa.
La mecánica de fluidos esla parte de la Física que estudia losfluidostanto en reposo como enmovimiento,
así como de las aplicaciones y mecanismos de ingeniería que utilizan fluidos. La mecánica se divide en la
estática de fluidos o hidrostática, que se ocupa de los fluidos en reposo o en equilibrio; y en la dinámica
de fluidos o hidrodinámica, que trata de los fluidos en movimiento.
Presión

En física, la presión (símbolo P) es una magnitud física vectorial que mide la fuerza en dirección perpen-
dicular por unidad de superficie o área, y sirve para caracterizar como se aplica una determinada fuerza

resultante sobre una superficie. Presión: Magnitud que se define como el cociente entre la fuerza que el
fluido ejerce respecto al área o superficie.

A partir de la definición de presión dar la defini-
ción de presión atmosférica: será la fuerza que

ejerce el aire atmosférico sobre la superficie de
la tierra.

Mecánica de los fluidos: GASES
La atmósfera es la capa de aire que rodea la tierra. El aire es una mezcla de gases. La composición de la
atmósfera es 78% - 79% nitrógeno y 20% - 21% de oxígeno, el resto son distintos tipos de gases, dióxido
de carbono, monóxido de carbono, ozono, metano y gases raros: argón, xenón, etc.

14 - 51

Unidades de presión

Variasson las unidades de medición de la presión, pero en salud, utilizaremos dos denominadas milíme-
tros de mercurio (mm Hg) y atmósferas (atm).

Unidades de equivalencia: 1 atm (se lee atmósfera) = 760 mm Hg (se lee milímetros de mercurio)
La presión atmosférica normal (a nivel del mar) es de 1 (una) atmósfera o de 760 mm Hg
Se denomina presión positiva a aquella presión que es mayor a la presión atmosférica.
La presión negativa es aquella presión que es menor a la presión atmosférica.
Difusión de los gases
Los gases difunden (se desplazan) desde un lugar de mayor presión a un lugar de menor presión.
Ley de las presiones parciales
La presión total de una mezcla de gases es la sumatoria de cada una de las presiones que cada gas ejerce
en esa mezcla. La presión parcial de un gas es la presión que cada gas ejerce dentro de una mezcla de
gases.

Ptotal = Pgas1 + Pgas2 + Pgas3 + .... Pgasn

Ley de Boyle Mariotte
Esta ley enuncia que, a TEMPERATURA CONSTANTE, la PRESIÓN que ejerce un gas dentro del recipiente

en el que está contenido es inversamente proporcional al VOLUMEN que este gas ocupa en ese reci-
piente.

http://www.quimicabasica.cl/tema_04.pdf
https://www.profesorenlinea.cl/fisica/Fuerza_concepto.html
https://www.profesorenlinea.cl/fisica/PresionAtmosferica.htm
https://www.profesorenlinea.cl/fisica/GasesPropiedades.htmhttps://www.profesorenlinea.cl/fisica/Gases
Propiedades.htm
https://www.profesorenlinea.cl/fisica/GasesLeyes.htm

15 - 51

AUTOEVALUACIÓN UNIDAD 2
1.Explique por qué causa los gases no tienen ni forma ni volumen fijo.
2. Sabiendo que la presión de un gases el cociente entre la fuerza que ejerce ese gassobre la superficie
del recipiente donde el fluido está contenido
a. Exprese matemáticamente la definición de presión enunciada anteriormente
b. ¿Qué tipo de magnitud es la presión?
c. A partir de la definición de presión defina: presión sanguínea, presión del aire alveolar, y presión
arterial
d. ¿Cuál es la relación de proporcionalidad entre la fuerza que el gas ejerce sobre una superficie y la
presión que ese gas ejerce?
3.¿Cuáles son las variables involucradas en la ley de Boyle Mariotte?
4. ¿Cuál esla relación de proporcionalidad entre la concentración de un gas y la presión que ese gas ejerce?

5.Los gases se movilizan desde un sitio donde ejercen mayor .................... a un sitio donde ejercen menor
................................
6. Los gases se movilizan desde un sitio donde tienen ..................... concentración a un sitio donde
tienen ................................................................................ concentración.
7. Mencione los valores de la presión atmosférica normal en dos unidades distintas y escriba cuál es su
relación de equivalencia.
8.Considerando el valor de la presión atmosférica normal, tache dentro del paréntesis la opción que NO
sea correcta
a. Una presión de 775 mm de Hg es una presión (NEGATIVA – POSITIVA)
b. Una presión de 0,95 atmósferas es una presión (NEGATIVA – POSITIVA)
c. Un gas difunde desde un lugar donde tiene una presión (NEGATIVA – POSITIVA) hacia un sitio
donde ejerce una presión (NEGATIVA – POSITIVA)
9. Un gas difunde desde un sitio donde la presión es la atmosférica a un sitio donde la presión es positiva.
¿Esta afirmación es VERDADERA o FALSA? JUSTIFIQUE
10. Se tiene una mezcla de 79% de nitrógeno y 21 % de oxígeno. Calcular la presión del gas oxígeno en
milímetros de mercurio si la presión de la mezcla es de 1,12 atmosferas.
11. Se tiene una mezcla de gas oxígeno a 90 mm de Hg y de dióxido de carbono a 0,05 atmósferas.
a. Calcular la presión total de la mezcla (en cualquier unidad),
b. ¿Qué ley se aplicó para calcular la presión total?
c. Calcular en que porcentaje se encuentra cada uno de los gases en la mezcla

16 - 51
12. Circule o marque la única opción correcta
a) los gases difunden de un lugar de mayor presión a un lugar de menor presión
b) los gases difunden de un lugar de menor presión a un lugar de mayor presión
c) los gases no difunden
13. El peso de un cuerpo es una magnitud escalar VERDADERO o FALSO
14. Se tiene tres cuartos litros de aire medicinal que es una mezcla formada por 79% de nitrógeno y
21% de oxígeno. Si la mezcla se encuentra a 1,04 atmósferas de presión total. Calcular:
a) la presión del oxígeno en milímetros de mercurio.
b) el volumen, en mililitros, que ocupará el nitrógeno en dicha mezcla.
15. La Ley de Dalton hace referencia a la propiedad que tienen los gases de difundir desde un sitio de
mayor presión a un lugar de menor presión. VERDADERO O FALSO

17 - 51
UNIDAD 3
1. LA MATERIA y SUS NIVELES DE ORGANIZACIÓN

La materia viva e inerte se puede encontrar en diversos estados de agrupación diferentes a los que se deno-
minan niveles de organización. Nosotros estudiaremos los niveles de organización de los seres vivos.

Esta agrupación u organización puede definirse en una escala de organización que sigue como se describe
más adelante el criterio de menor a mayor complejidad, de menor a mayor organización.

Es necesario tener en cuenta que cada uno de los niveles de organización de la materia agrupa a los anterio-
res, así, por ejemplo, el nivel de organización de la molécula engloba al nivel atómico, y al nivel subatómico.

Niveles de organización biológica
Cada uno de los niveles de organización de la materia se puede estudiar desde diferentes ámbitos, así que
mientras que el nivel de organización atómico y subátomico se afrontan desde la física, la célula se afronta
desde la citología, y el nivel molecular se estudia desde la química o desde la bioquímica.
Nivel Subatómico: este nivel es el mássimple de todo y está formado por electrones, protones y neutrones, que
son las distintas partículas que configuran el átomo.

Nivel Atómico: es el siguiente nivel de organización. Se conoce como átomo a la unidad más pequeña e indi-
visible que constituye lamateria, dotada de propiedades químicas y físicas propias y clasificable según su peso,

valencia y otras característicasfísicas, en una serie de elementos básicos del universo, contenidos en la Tabla
periódica de los elementos. Los átomos están formados por constituyentes subatómicos como
los protones (con carga positiva), los neutrones (sin carga) y los electrones. (con carga

negativa). Por ejemplo, imaginemos que tenemos un trozo de hierro. Lo partimos. Seguimos te-
niendo dos trozos de hierro, pero más pequeños. Los volvemos a partir, otra vez... Cada vez ten-
dremos más trozos cada vez más pequeños hasta que llegará un momento, en que si lo volviése-
mos a partir lo que nos quedaría ya no sería hierro, sería otro elemento de la tabla periódica.

En este momento, podemos decir que lo que nos ha quedado es un átomo, un átomo de hierro.
Definición de átomo
De un modo más formal, definimos átomo como la partícula más pequeña en que un elemento
puede ser dividido sin perder sus propiedades químicas.
El origen de la palabra átomo proviene del griego, que significa indivisible. En el momento que se
bautizaron estas partículas se creía que efectivamente no se podían dividir, aunque hoy en día
sabemos que los átomos están formados por partículas aún más pequeñas, repartidas en las dos
partes del átomo, las llamadas partículas subatómicas.
¿Cuáles son las partes de un átomo?
El átomo se divide en dos partes: el núcleo y la corteza. El núcleo, a su vez, está formado por
neutrones (partículas sin carga eléctrica) y protones (partículas con carga positiva). La corteza,
sin embargo, está formada únicamente por electrones (partículas con carga negativa).

18 - 51
Los protones, neutrones y electrones son
las partículas subatómicas que forman la
estructura del átomo. Lo que diferencia a un
átomo de otro es la relación que se establecen
entre ellas.

Los electrones, de carga negativa, son las par-
tículas subatómicas más ligeras. Los proto-
nes, de carga positiva, pesan unas 1.836 veces

más que los electrones.

Los neutrones, los únicos que no tienen carga eléctrica, pesan aproximadamente lo mismo que
los protones.
Los protones y neutrones se encuentran agrupados en la parte central del átomo formado

el núcleo atómico. Por este motivo también se les llama nucleones. La energía que mantiene uni-
dos los neutrones y los neutrones es la energía nuclear;.

De este modo, la parte central del átomo, el núcleo atómico, tiene una carga positiva en la
que se concentra casi toda su masa, mientras que en el escorzo alrededor del núcleo atómico
hay un cierto número de electrones, cargados negativamente. La carga total del núcleo
atómico (positiva) es igual a la carga negativa de los electrones, de modo que la carga eléctrica
total del átomo sea neutra.
Partículas subatómicas fundamentales:
 P
+ = protón: partícula con carga positiva.
 No = neutrón: partícula sin carga eléctrica.
 e
- = electrón: partícula con carga eléctrica negativa.
Conceptos clave:
 Los P
+ y los No se encuentran en la zona nuclear, y los e

- en la zona extranuclear (orbitas)

 El núcleo posee carga positiva, y la zona extranuclear carga negativa.
 El átomo en su conjunto es neutro.
 El átomo posee igual cantidad de protones que de electrones.
Elemento químico

La forma en la que un elemento puede encontrarse en la naturaleza se denomina variedad alotrópica. Por
ejemplo, el carbono se puede presentar en forma de grafito, diamante y hulla.
A nivel biológico podemos llamar a los átomos como bioelementos (biomoléculas inorgánicas) y clasificarlos
según su función:
a. Si cumplen una función estructural son bioelementos primarios: son el carbono, el fósforo, nitrógeno,
hidrógeno, oxígeno y azufre que forman, por ejemplo, las membranas de las células, las proteínas, los
ácidos grasos, los lípidos...

b. Si cumplen una función estructural y catalítica son bioelementos secundarios: calcio, sodio, potasio, mag-
nesio, cloro, iodo... son fundamentales para el funcionamiento de la célula, pero no forman parte estruc-
tural de las mismas.

Se llama elemento químico al componente común de una sustancia. Los átomos de un mismo elemento
son iguales entre sí.

19 - 51

c. Si cumplen sólo función catalítica son oligoelementos porque sus cantidades en el organismo son muy
escasas, pero de suma importancia, como por ejemplo pueden ser el cobre, el zinc, que intervienen en el
funcionamiento de ciertas enzimas.
Nivel Molecular: las moléculas consisten en la unión de átomos diferentes, por ejemplo, oxígeno en
estado gaseoso (O2), dióxido de carbono (CO2), agua (H2O) o simplemente hidratos de carbono, proteínas,

lípidos... Las moléculas pueden ser orgánicas (glucosa, lípidos, grasas) o inorgánicas (agua, sales minera-
les como el cloruro de sodio, cloruro de potasio, bicarbonato de sodio, gases como por ejemplo los ya

mencionados oxígeno y dióxido de carbono. La bioquímica se encarga del estudio de este nivel de orga-
nización. Dentro del nivel molecular se encuentran los virus ya que son complejos moleculares que no

tienen las mismas estructuras que los niveles superiores como son las células o sus organelas. Los virus
son estructuras formadas por una porción de ADN o ARN envueltas en una proteína.
Los átomos se asocian entre sí formando moléculas. En algunos casos los átomos asociados son iguales,
como en el caso del gas oxígeno constituido por 2 átomos de oxígeno (O2), o del ozono constituido por 3
átomos de oxígeno (O3).

En otros casos se asocian átomos diferentes, como en el caso del agua, cuya molécula está formada por
2 átomos de hidrógeno y 1 de oxígeno.

20 - 51

También puede ocurrir que un átomo no se asocie con otros para formar una molécula. Ellos mismos
constituyen en estos casos la molécula. Hablamos entonces, de moléculas monoatómicas (constituidas
por un solo átomo). Los metales y los gases nobles son monoatómicos. Por ejemplo, el Hierro (metal), y
el Helio (gas noble).
2. MATERIA

ION: átomo o grupo de átomos que presentan cargas eléctricas. Si estas cargas son negativas, se deno-
minan ANIONES (por ejemplo, anión cloruro, anión bicarbonato, anión fosfato). Si la carga es positiva se

denominan CATIONES (por ejemplo, catión sodio, catión potasio, catión calcio, catión ferroso)

Los iones se forman por la pérdida o ganancia de electrones (partículas con cargas negativas). Sabemos
que el átomo es eléctricamente neutro porque la cantidad de cargas positivas y negativas son iguales.
Cuando un átomo pierde un electrón queda eléctricamente desbalanceado y queda con un excedente
de una carga positiva, por eso se transforma en un catión. Si un átomo gana un electrón, entonces queda
con un excedente de cargas negativas, por lo tanto, se transforma en anión.
Materia es todo aquello que tiene masa, ocupa un lugar en el espacio e impresiona nuestros sentidos.

21 - 51

¿Podría explicar entonces qué le sucede a un átomo cuando pierde dos electrones? ¿Podría explicar
entonces que le sucede a un átomo que gana tres electrones?
CUERPO: porción limitada de materia
3. SUSTANCIA: es la calidad de la materia que constituye un cuerpo.

También podemos observar que hay distintas clases de materia, diferentes entre sí porsu color, olor, es-
tado físico, textura, aspecto, etc. A cada una de estas clases de materia se la denomina sustancia.

Sustancias inorgánicas Sus moléculas pueden contener átomos diversos.

Ejemplos: H2O, O2, O3, FeS, etc.

Sustancias orgánicas

Sus moléculas contienen siempre átomos de car-
bono e hidrógeno, pudiendo contener además oxí-
geno y nitrógeno. Ejemplos: sacarosa, alcohol, hi-
drocarburos, etc.

PROPIEDADES DE LAS SUSTANCIAS

Distinguiremos fundamentalmente 2 tipos de propiedades: intensivas y extensivas.

Son ejemplos de este tipo de propiedades el volumen, el peso, la superficie, etc. Las propiedades exten-
sivas no permiten identificar a la sustancia en estudio, pues se puede tener el mismo volumen de agua

que de alcohol, o igual peso de sal que de cal, a pesar de ser sustancias diferentes.
Propiedades extensivas son aquellas que dependen de la cantidad de materia considerada.

22 - 51

Entre las propiedades intensivas de las sustancias hay algunas que se pueden apreciar por medio de los

sentidos, como el olor, el sabor, el color, la sensación al tacto, el sonido, etc. y que se denominan pro-
piedades organolépticas.

Existen otro tipo de propiedades intensivas que deben ser determinadas a través de mediciones experi-
mentales, tales como el punto de fusión, el punto de ebullición, la densidad, el índice de refracción, el

calor específico etc. que, al ser determinadas en las mismas condiciones, tienen valores definidos y cons-
tantes para cada sustancia y se denominan constantes físicas.

Se le propone entonces que investigue: valores de punto de fusión, el punto de ebullición, la densidad,
el calor específico, pH del agua pura
4. SISTEMAS MATERIALES
Se llama sistema material a un cuerpo o conjunto de cuerpos que se aíslan en forma real o imaginaria
para ser estudiados. los sistemas materiales se clasifican en:

A este tipo de sistemas pertenecen las sustancias puras y las soluciones. Ej. Agua y alcohol en un vaso.

Las sustancias puras son sistemas homogéneos formados por una sola sustancia, cuyas propiedades in-
tensivas son particulares y constantes. Una sustancia pura no puede separarse en otras utilizando pro-
cedimientos mecánicos o físicos. Ej. Agua, oxígeno, hierro.

Por ej. Agua y aceite en un vaso. En un sistema heterogéneo se llama fase a cada uno de los sistemas
homogéneos perfectamente diferenciables que lo componen.
5. REACCIONES QUÍMICAS

Se llaman reacciones químicas a las combinaciones y descomposiciones. Una reacción química se repre-
senta mediante una ecuación, en la cual en el primer miembro se indican las sustancias que reaccionan

y en el segundo los productos que resultan.

A B C D

Esto indica que las sustancias A y B (REACTIVOS) reaccionan dando como (PRODUCTOS) las sustan-
cias C y D.

Propiedades intensivas son aquellas que NO dependen de la cantidad de materia sino de la calidad de
la misma.

Sistema homogéneo: aquel sistema que en todos los puntos de su masa presenta las mismas
propiedades intensivas.

Sistema heterogéneo: aquel sistema que presenta propiedades intensivas diferentes en algunas de sus
porciones o FASES.

23 - 51
https://www.profesorenlinea.cl/fisica/atomoEstructura.htm
https://www.profesorenlinea.cl/Quimica/Molecula.htm
https://www.profesorenlinea.cl/Quimica/ElementoQumicoNocion.htm
https://www.profesorenlinea.cl/fisica/Materia1.htm

AUTOEVALUACIÓN UNIDAD 3

1. Explique por qué un átomo es eléctricamente neutro
2. Enumere TRES (3) propiedades intensivas del agua pura y sus valores normales.

3. Los electrolitos son átomos o grupos de átomos con capacidad de conducir la corriente eléc-
trica. VERDADERO o FALSO. JUSTIFIQUE. EL NO JUSTIFICAR INVALIDA SU RESPUESTA

4. ¿Cuáles son las partículas subatómicas nucleares?
5. ¿En qué se diferencian las propiedades intensivas de las extensivas?
6. ¿Cómo se denominan los sistemas materiales formados por dos o más fases?
7. Dada siguiente fórmula Na+

, explique qué tipo de ión es el sodio (Na) y por qué.

8. En el caso de que el carbono reaccione con el oxígeno para formar dióxido de carbono, ¿Quiénes son
los reactivos? Escriba la reacción química.
9. ¿A cuáles de los niveles de organización de la materia pertenecen:
a) los virus
b) el anión cloruro
c) la albúmina
d) el colesterol
e) el agua pura

24 - 51
UNIDAD 4

1. SOLUCIONES
a. Soluciones verdaderas o propiamente dichas

Sistema homogéneo que admite fraccionamiento. Homogéneo significa que en cada punto de la solu-
ción se conservan las mismas propiedades (color, sabor, densidad, punto de ebullición...)

Fraccionamiento significa que se puede separar en cada uno de los componentes que la forma. Recuerde
que una solución es un sistema por eso está formado por lo menos por dos componentes.

En nuestra guía de estudio sólo estudiaremos las soluciones liquidas. De masa en volumen o de volu-
men en volumen.

Una SOLUCIÓN está formada por una parte que se disuelve denominada SOLUTO y una parte que
disuelve al soluto denominada SOLVENTE

25 - 51

¿Se puede seguir agregando soluto indefinidamente y siempre obtener una solución?

No, no es posible. Existe un límite –que en cada caso depende del tipo de soluto y solvente y de la tem-
peratura a la cual se realice el experimento– a partir del cual el sistema deja de ser una solución para

transformarse en un sistema heterogéneo.
Si en una taza con té agrega un exceso importante de azúcar aun cuando agite continuamente, llega un
momento en el que el sistema no admite más azúcar y ésta se empieza a acumular en el fondo de la taza.
Se dice entonces que la solución se saturó.

La única manera de estar completamente seguro de que una solución está saturada es que se encuentre
presente, también, un exceso de soluto sin disolver.
 La solubilidad es la concentración de la solución saturada para una solución que se disuelve en
un determinado solvente a una cierta temperatura.
 En general la solubilidad de los sólidos en el agua aumenta al aumentar la temperatura.

 Cuando la que se disuelve en agua es una sustancia gaseosa, por ejemplo, el oxígeno que se encuen-
tra en el aire, la solubilidad disminuye al aumentar la temperatura.

SOLUCIÓN

DILUÍDA

Cuando posee una mínima cantidad
de soluto disuelto.

CONCENTRADA

Cuando posee gran cantidad
de soluto, pero sin llegar a
la saturación.

Una solución está saturada cuando contiene disuelta la máxima cantidad delsoluto que puede disolverse
a una cierta temperatura.

26 - 51

SOLUCIÓN

SATURADA

Cuando posee la máxima cantidad de
soluto que se puede disolver en esa

cantidad de solvente, a una determi-
nada temperatura.

SOBRESATURADA

Cuando ésta contiene más soluto que
la cantidad soportada en condiciones
de equilibrio por el solvente, a una
temperatura dada. Es por lo tanto
una solución inestable, en la cual el
exceso disuelto se depositará.

CONCENTRACIÓN DE UNA SOLUCIÓN
La concentración de una solución esla forma de “medir” una solución. Nosindica cómo está formada esa
solución. Representa la cantidad de soluto que hay en una determinada cantidad de solvente. Al disolver
una determinada cantidad de soluto en una determinada cantidad de solvente la cantidad de solución es
el mismo volumen que el del solvente. Por ejemplo, si disuelvo 2 gramos de sal (soluto) en 300 mililitros
de agua (solvente) obtendremos 300 ml de agua salada (solución).

Por eso podemos definir a la concentración de una solución como la cantidad de soluto que hay en una
determinada cantidad de solución. Es la relación existente entre la cantidad de soluto en la solución.
C = cantidad de soluto = cantidad de soluto

cantidad de solvente cantidad de solu-
ción

Una solución es más concentrada que otra cuando tiene mayor concentración
Una solución es más diluida que otra cuando tiene menor concentración

27 - 51

DISOLVER: agregar una determinada cantidad de solvente a una determinada cantidad de soluto para
formar una solución. Por ejemplo, si tengo 2 gramos de cloruro de sodio (NaCl) y le agrego 100 ml de
agua pura, quiere decir que disolví, 2 gramos de (NaCl) en 100 ml de agua y se obtuvo una solución de 2
gramos de (NaCl) en 100 ml (2%)

DILUIR: agregar solvente a una solución ya preparada para bajar su concentración. En este caso la solu-
ción ya está preparada, pero le agregamos solvente. Si a la solución anterior le agregamos 100 ml más de

solvente, ¿que tendremos? Una solución diluida, porque ahora vamos a tener esos mismos 2 gramos de
(NaCl) (NaCl) pero en 200 ml. Si queremos calcular la concentración tendremos
C = cantidad de soluto = cantidad de soluto = 2 gramos de (NaCl) = 1 gramo (NaCl) = 1%
cantidad de solvente cantidad de solución 200 ml 100 ml
como se podrá observar ahora la concentración esmenor, en el primer caso era 2g en 100 ml y ahora pasó
a ser 1 g en 100 ml
FORMAS DE EXPRESAR LA CONCENTRACIÓN DE UNA SOLUCIÓN
1) % (m/V) – porcentaje masa en volumen- o %(P/V) – porcentaje peso en volumen o simplemente %,

Ejemplos:
a) NaCl (cloruro de sodio) al 0,9%: representan 0,9 gramos de cloruro de sodio en 100 ml de solución
b) Dextrosa 5%: 5 gramos de dextrosa (glucosa) en 100 ml de solución
% m/V: indica cuántos gramos de soluto están disueltos en 100 cm3 o ml de solución.
Ejemplo para resolver:
Si 100 cm3 de una solución contienen 2g de soluto, entonces la concentración de dicha solución será

2%m/V. ¿Qué masa de soluto estará disuelta en 30cm3 de la solución anterior? Referencias: Sn: solu-
ción y St: soluto

2) mg/ml (miligramos/mililitros)
% = % m/V: representa los GRAMOS de SOLUTO que hay en 100 ml o 100 cm3 de

SOLUCIÓN

mg/ml: representa los MILIGRAMOS de SOLUTO que hay en 1 ml de SOLUCIÓN

28 - 51

Ejemplos:
a) Morfina 10 mg/ml: hay 10 miligramos de morfina en 1 mililitro de solución
b) Lidocaína 20 mg/ml: hay 20 miligramos de lidocaína en 1 mililitro de solución
EQUIVALENCIA de UNIDADES
Para pasar de % a mg/ml sólo se necesita multiplicar por 10 a la concentración expresada en %
1 % x 10 = 10 mg/ml es decir que una solución al 1% es lo mismo que una solución de 10 mg/ml.
0,9% x 10 = 9 mg/ml es decir que una solución al 0,9% es lo mismo que una solución de 9 mg/ml
5% x 10 = 50 mg/ml
Para pasar de mg/ml a % sólo se necesita dividir por 10 a la concentración expresada en mg/ml
20 mg/ml ÷ 10 = 2% es decir que una solución de 20 mg/ml es lo mismo que una solución al 2%
100 mg/ml ÷ 10 = 10% es decir que una solución de 100 mg/ml e lo mismo que una solución al 10%
50 mg/ml ÷ 10 = 5%
EJEMPLO 1: Se tiene una solución al 10% de concentración. Calcular los miligramos de soluto que habrá
en 5 mililitros de la solución. ACLARACIÓN: 10% es lo mismo que 10%(m/V) o 10%(P/V)
10% 0 10 % (m/V) significa 10 gramos de soluto que hay en 100 ml de solución.
Entonces 10% = 100 mg/ml
1 ml 100 mg
5 ml X = 500 mg (Rta: 500 mg es la respuesta)
EJEMPLO 2: Se tiene una solución de cloruro de sodio 0,9% de concentración. Calcular los miligramos de
cloruro de sodio que habrá en un cuarto litro de la solución. ACLARACIÓN: 0,9% es lo mismo que
0,9%(m/V) o 0,9%(P/V), por lo tanto 0,9% = 9 mg/ml o sea que en 1 ml hay 9 mg
Además sabemos que un cuarto litro = 250 ml
1 ml 9 mg
250 ml X = 2250 mg
EJEMPLO 3: Se disuelven 2500 miligramos de ácido ascórbico en 500 centímetros cúbicos de solvente
a) Expresar la concentración de la solución en % (m/V) y en mg/ml

b) Si a la solución anteriormente preparada, se le agrega más solvente, ¿Qué sucederá con la concentra-
ción de la solución?

a) 500 cm3 = 500 ml
500 ml 2500 mg
1 ml X = 5 mg/ml
1000 mg 1 g 500 ml 2,5 g
2500 mg X = 2,5 g 100 ml X = 0,5g es decir 0,5%(m/V)
b) Al agregar solvente a la solución ya preparada la concentración de la solución baja.

29 - 51

EJEMPLO 4: Se tiene una solución de sulfato de magnesio al 5%. ¿Cuántos mg de sulfato de magnesio habrá en 5
centímetros cúbicos?
5% es lo mismo que 5% (m/V) y significa 5 gramos de soluto que hay en 100 ml de solución es decir 50 mg/ml es decir
que en 1 ml hay 50 mg.
Además, sabemos que, cm3 = ml.
Entonces
1 ml 50 mg
5ml x = 250 mg
3) g/l (gramos/litro)

Ejemplos:
9 g/l: significa 9 gramos de soluto en un litro de solución
0,5 g/l: significa 0,5 gramos de soluto en un litro de solución
ATENCIÓN: La expresión gramos/litro es equivalente a miligramos/ mililitro
Esto quiere decir que 5g/l = 5 mg/ml 10 g/l = 10 mg/ml 0,5g/l = 0,5 mg/ ml
MOLARIDAD: M indica los moles de soluto que hay en 1 dm3 o litro de solución. Ejemplo: se
prepara una solución que contiene 6g de soluto cuyo M=60g en 500ml de solución. Expresar
su concentración en molaridad (M).
Referencias: st: soluto, sn: solución

MOLALIDAD (m): se define como el número de moles de soluto disueltos en 1kg de solvente.
Ejemplo: Si en 1Kg de agua disolvemos 0,5 moles de azúcar, diremos que se preparó una solución 0,5m.
NORMALIDAD (N): corresponde al número de equivalentes de soluto por litro de solución.
Se define como equivalente gramo de un ácido a la masa de dicho ácido (expresada en gramos) que
proporciona, en solución acuosa, un mol de iones H+
.

De igual forma, se define como equivalente gramo de una base a la masa de dicha base (expresada en
gramos) que proporciona, en solución acuosa, un mol de iones OH-
.

g/l: representa los GRAMOS de SOLUTO que hay en 1 l de SOLUCIÓN

30 - 51

Por último, se define como equivalente gramo de una sal a la masa de dicha sal (expresada en gra-
mos) que proporciona, en solución acuosa, un mol de iones con cargas + ó -.

Se define como equivalente gramo de un ácido a la masa de dicho ácido (expresada en gramos) que
proporciona, en solución acuosa, un mol de iones H+
.

De igual forma, se define como equivalente gramo de una base a la masa de dicha base (expresada en
gramos) que proporciona, en solución acuosa, un mol de iones OH-
.

Por último, se define como equivalente gramo de una sal a la masa de dicha sal (expresada en gra-
mos) que proporciona, en solución acuosa, un mol de iones con cargas positivas o negativas.

Si consideramos que el H2SO4 interviene en una reacción ácido-base liberando 2 moles de iones H+ por
cada mol de ácido tendremos:

Como la masa molar del ácido es 98g, 0,5 moles corresponden a 49g, que es el equivalente gramo de
ácido en esta reacción.
Ejemplo:
Calcular la normalidad de una solución de Fe(OH)2 que contiene 1,796g de base en 100cm3 de solución.
1o Se debe calcular el equivalente gramo de la base: se define como equivalente gramo de una base a
la masa de dicha base (expresada en gramos) que proporciona, en solución acuosa, un mol de iones
OH-
.

2o Hallar los gramos de base por litro de solución:

3o Hallar la N:

2. SUSPENSIONES
Suspensiones son aquellas soluciones en la que las partículas de soluto no están totalmente disueltas en
la solución. Hay partículas insolubles o parcialmente disueltas. La propiedad de estas soluciones es que
cuando están en reposo sedimentan, es decir que las partículas de soluto que no se disolvieron se van al
fondo delreciente “sedimentan” por acción de la gravedad. Ejemplo:sangre, orina y solución de contraste
de sulfato de bario. Se tratan de sistemas heterogéneos, puesto que en reposo hay más de una fase.

31 - 51

3. SOLUCIONES ELECTROLÍTICAS
Son aquellas soluciones que contienen electrolitos en solución. Se denominan electrolitos a los iones en
solución. Recuerde que un ion es un átomo o grupo de átomos con cargas eléctricas.
CATIONES: átomo o grupo de átomos con
cargas eléctricas positiva.

ANIONES: átomo o grupo de átomos con cargas
eléctricas negativa.

Sodio Na+ Cloruro Cl-
Potasio K

+ Bicarbonato HCO3
-
Catión ferroso Fe 2+ Fosfato PO4
3-

Calcio Ca2+
Soluciones electrolíticas: ejemplos
a. solución salina normal, solución salina o solución fisiológica que es una solución de cloruro de sodio
al 0,9%
b. Solución de cloruro de calcio al 10%
c. Solución ringer: solución de tres cloruros: cloruro de sodio, cloruro de potasio y cloruro de calcio

https://www.profesorenlinea.cl/Quimica/Disoluciones_quimicas.htmlhttps://www.profesorenlinea.cl/Qui
mica/Disoluciones_quimicas.html

32 - 51

AUTOEVALUACIÓN UNIDAD 4

En la práctica de enfermería usted trabajará fundamentalmente con las unidades de concentración expresadas en %
(m/V) o simplemente “%” y en mg/ ml por eso se le sugiere que para preparar muy bien su examen de ingreso centre
su estudio y atención en la realización de problemas con las concentraciones anteriormente mencionadas.
1. Calcular la concentración (en la unidad que usted prefiera) de una solución al disolver 3 g de cloruro de
sodio en medio litro de agua pura. ¿Cuántos centímetros cúbicos de solución se formaron?
2. Se disolvieron 250 miligramos de una sal de iodo en 500 mililitros de agua destilada
a. Calcular la concentración de la solución en mg/ml
b. ¿Cuántos mililitros de solución se prepararon?

c. Si a la solución preparada anteriormente le agregan 250 ml más de agua destilada. ¿Cuántos miligra-
mos de soluto habrá en la nueva solución? Calcular la concentración en %(m/V) o % de la nueva solu-
ción formada.

3. Se disuelven 250 mg en tres cuartos litros de solvente puro, calcular la concentración de la solución en
mg/ml y en %
4. Se tiene una solución de sulfato de bario al 66%,
a. ¿Cuántos gramos de sulfato de bario hay en 250 ml de solución?
b. ¿Cuántos miligramos de sulfato de bario hay en 300 ml?
c. ¿Cuántos gramos de sulfato de bario hay en 1 litro de solución?
5. Se disuelven 400 miligramos de un soluto soluble en 200 centímetros cúbicos de solvente. Expresar la
concentración de la solución formada en % (m/V)
6. Los sistemas homogéneos presentan las mismas propiedades intensivas en toda la masa del sistema
VERDADERO O FALSO
7. Se tiene un fármaco cuya concentración es 10 mg/ml. ¿Cuántos gramos de fármaco contendrán medio
litro de solución?
8. ¿Qué significa que una solución sea un sistema homogéneo?
9. Se tiene una solución de cloruro de sodio 0,9% de concentración. Calcular los miligramos de cloruro de
sodio que habrá en un cuarto litro de la solución. ACLARACIÓN: 0,9% es lo mismo que 0,9%(m/V) o
0,9%(P/V)
10. Se disuelven 2500 miligramos de ácido ascórbico en 500 centímetros cúbicos de solvente
a) Expresar la concentración de la solución en % (m/V) y en mg/ml

b) Si a la solución anteriormente preparada,se le agrega mássolvente, ¿Qué sucederá con la concentra-
ción de la solución?

11. Se tiene una ampolla de 1 ml de capacidad de una solución farmacológica al 2%.
a) ¿Cuántos miligramos de fármaco habrá en ese mililitro de solución?
b) ¿Cuántos mililitros de solución contendrán 10 mg de fármaco?
c) ¿Cuántos miligramos de fármaco habrá en dos ampollas?

33 - 51

3

2

UNIDAD 5

1. ÁCIDOS - BASES

La primera aproximación a los conceptos de ácido y de base está asociada a la experiencia. Todos cono-
cemos el sabor agrio del limón o del vinagre, o hemos probado, de manera accidental, una solución

jabonosa. Estos sabores característicos son debidos a la presencia de determinadas sustancias que,
desde hace tiempo,se conocen como ácidos o bases. Además del sabor, estas sustancias son capaces de
cambiar el color de los indicadores y, en soluciones concentradas, resultan corrosivas.
En 1887, el químico sueco Arrhenius, publicó su teoría de la disociación iónica, en la que la conductividad
eléctrica de soluciones acuosas de ácidos, bases y sales (electrolitos) se justifica por la existencia de iones

positivos y negativos en las soluciones. Arrhenius asoció el carácter ácido a la presencia de iones hidró-
geno (H+

), y el carácter básico, a la existencia de iones hidróxido (OH-

), en solución acuosa.

Definiciones de ácido y base
Según la teoría de Arrhenius, los ácidos son sustancias que en solución acuosa se disocian para liberar
iones hidrógeno (H+

). Las bases son sustancias que en solución acuosa se disocian y dan iones hidróxido

(OH-
).
Según la teoría de Brönsted y Lowry, un ácido es toda sustancia capaz de ceder un protón (H+
) y una

base, aquélla capaz de aceptar un protón.
Lewis, considera ácido a todo átomo, molécula o ion capaz de aceptar un par de electrones para formar
una unión covalente y base a toda especie química capaz de ceder un par de electrones para formar una
unión covalente.
Es importante recordar que la neutralización es la reacción que ocurre entre los iones hidrógeno de un
ácido y los iones hidróxido de una base para dar agua, con la consiguiente formación de una sal.
2. CONCEPTO DE pH
Por lo general,se considera que el agua pura no conduce la corriente eléctrica. Sin embargo,si el registro
se efectúa con un aparato de medición muy sensible, se advierte que existe un valor muy pequeño de
conductividad eléctrica.
Esta propiedad se debe a la existencia de iones que sólo pueden provenir del equilibrio derivado de su
propia disociación. Las moléculas de agua, en una proporción muy pequeña, reaccionan entre sí para dar

iones oxonio e hidróxido como consecuencia de que una molécula de agua, que actúa como ácido, trans-
fiere un protón a otra molécula que se comporta como base y establece el equilibrio:

H2O (l) H2O (l) OH-

(ac) H O (ac)
La expresión de la constante de equilibrio para ese proceso es:

H O OH-
K

H O
2

Donde los corchetes expresan la concentración molar de las especies indicadas (en moles por litro).
Como la cantidad de moléculas de agua disociadas es muy pequeña, la concentración de H2O es
casi constante y eltérmino [H2O]2

se puede englobar en el primertérmino de la expresión anterior. El

producto K x [H2O]2

se representa como Kw y entonces la expresión es:

3

34 - 51
3

3

3

3
3

Kw H O OH-
El producto de las concentraciones de iones oxonio e hidróxido es una constante, Kw, que se deno-
mina producto iónico del agua. El valor de Kw varía en función de la temperatura, y a 25 oC es igual

a 1,00 x 10 –14
En el agua pura se cumple que la concentración de iones oxonio es igual a la concentración de iones
hidróxido

H O OH-
por lo tanto:

Por lo que:

Kw H O
2
1,00 10 14

H O OH- 1,00 10-7 mol
3

l

Una solución acuosa en la que se cumple que la concentración de oxonios esigual a la concentración
de hidróxidos, se considera una solución neutra, es decir que:

H O OH-
Cuando se adiciona una sustancia que aumenta la concentración de oxonios, la concentración de

hidróxidos tiene que disminuir para que se mantenga constante el producto iónico del agua.
Se obtiene así una solución ácida ([H3O
+
] > 1,00 x 10-7
y [HO-
] < 1,00 x 10 –7
).

Si, por el contrario,se adiciona una sustancia que aumente la concentración de hidróxidos, disminuye
y se obtiene una solución básica ([H3O
+
] < 1,00 x 10-7
y

[HO-
] > 1,00 x 10 –7
).

El valor de las concentraciones de iones oxonio o hidróxido indica, en forma cuantitativa, el carácter
ácido o el carácter básico de una solución. Como el valor de estas concentraciones suele ser muy
pequeño, conviene expresarlo en términos de pH.

El pH de una solución se define como el logaritmo decimal de la concentración molar de iones oxo-
nio cambiado de signo.

pH -log H O

El pH de una solución se define como el logaritmo decimal de la concentración molar de iones hidronio (H+
) o

hidrógeno cambiado de signo.
Por lo tanto, el valor del pH disminuye al aumentar la concentración de iones oxonio y viceversa.
También puede definirse el pOH como:

pOH -log OH-

35 - 51
3

3

La relación que existe entre el pH y el pOH se deduce a partir del producto iónico del agua. Se conoce
que a 25 oC se cumple:

H O OH- 10-14
Al aplicar logaritmos a esta expresión y cambiarlos de signo, resulta:
log H O - log OH- 14

ESCALA DE pH El pH tiene una influencia decisiva en el

curso de las reacciones químicas. Mu-
chos procesos industriales, reacciones

de análisis y procesos biológicos se pro-
ducen en solución acuosa y requieren de

una cierta estabilidad en el pH.
Es el caso del agua de mar, que mantiene
un pHcomprendido entre 7,8 y 8,3 lo que

posibilita la vida subacuática, o de la san-
gre humana, que es una solución acuosa

de composición compleja que mantiene
un pH de 7,4.

El pH es un valor numérico absoluto (que no tiene unidades) que nos permite identificar si una solución
es ácida, alcalina (básica) o neutra. La escala numérica de pH toma valores que van desde el CERO (0) a

CATORCE (14) y según los rangos de valores de esta escala podremos clasificar a las soluciones, sustan-
cias o medios biológicos en ÁCIDAS, ALCALINAS o NEUTRAS

Valores de pH Característica o propiedad Ejemplo
De 0 hasta 7 (menor que 7) ÁCIDO

pH estomacal: 1 a 4
pH duodeno: 4 a 5
pH piel: 5 a 6
pH orina: 5 a 6,5
7 NEUTRO pH agua pura

De 7 (mayor que 7) hasta 14 ALCALINO o BÁSICO pH sangre: 7,35 a 7,45 pH
intestinal: 8 promedio

El ácido clorhídrico es elresponsable de la acidez del jugo gástrico. El anión bicarbonato, es elresponsable
de que la sangre sea ligeramente alcalina. Por eso al bicarbonato se lo considera como nuestra reserva
alcalina.

36 - 51

VALORES DE pH y ACIDEZ VALORES DE pH y ALCALINIDAD

A medida que el pH disminuye la acidez au-
menta, o a medida que el pH aumenta la acidez

disminuye.

A medida que el pH disminuye la alcalinidad dis-
minuye, o a medida que el pH aumenta la alcali-
nidad aumenta

Existen soluciones, llamadassoluciones amortiguadoras, que son capaces demantener constante el valor

de pH, después de la adición de pequeñas cantidades tanto de ácido como de base. También se las de-
nomina buffer o tampón. Las proteínas plasmáticas al tener en su estructura un grupo ácido y un grupo

alcalino (amino) actúan como amortiguadoras del pH sanguíneo.
3. NEUTRALIZACIÓN – SALES
Se denominan reacciones de neutralización a aquellas reacciones químicas entre un ácido y una base en
cantidades estequiométricas que dan como productos de esta reacción una sal (neutra) y agua.

https://www.profesorenlinea.cl/Quimica/PH2.htm https://www.profesorenlinea.cl/Qui-
mica/Acido_base.htm

http://ciencianet.com/acidobase.htmlhttp://ciencianet.com/acidobase.htmlhttp://ciencianet.com/acido-
bas e.html

37 - 51

AUTOEVALUACIÓN UNIDAD 5

1. ¿Qué valor de pH tendrán todas aquellas sustancias o soluciones que sean de naturaleza ácida?
2. ¿Qué rango de valores de pH tendrán las soluciones de ácido ascórbico? Justifique
3. Tache dentro de cada uno de los paréntesis la opción que NO sea correcta

La reacción química entre ácidos y bases se denomina reacción de (NEUTRALIZACIÓN – COM-
BUSTIÓN) siendo el producto de esta reacción (EL OXÍGENO – UNA SAL) y agua.

4. Indique si las siguientes afirmaciones son verdaderas o falsas. Justifique sus respuestas.
a. El pH de una solución es 5, por lo tanto, es básica.
b. Un ácido fuerte es aquel que en solución acuosa se encuentra totalmente disociado.
c. El grado de disociación iónica indica si una sustancia en solución es ácida, básica o neutra.
d. Según Arrhenius, un ácido es toda sustancia que en solución acuosa libera protones.
5. ¿Cuál es el electrolito responsable de la ligera alcalinidad de la sangre?
6. ¿Cómo se podrá determinar si una solución es ácida o alcalina?
7. ¿Con que tipo de sustancia se puede neutralizar a una sustancia de naturaleza ácida?
8. ¿Para qué sirve el pH?

38 - 51
UNIDAD 6

1. LA QUÍMICA ORGÁNICA
La QUÍMICA ORGÁNICA es la química del carbono y de sus compuestos. Los seres vivos estamos formados

pormoléculas orgánicas, proteínas, ácidos nucleicos, azúcares y grasas. Todos ellosson compuestos cuya base prin-
cipal es el carbono. Los productos orgánicos están presentes en todos los aspectos de nuestra vida: la ropa que

vestimos, los jabones, desodorantes, medicinas, perfumes, utensilios de cocina, la comida, etc.
Los productos orgánicos han mejorado nuestra calidad y esperanza de vida. Podemos citar una familia de
compuestos que a casi todos nos ha salvado la vida, los antibióticos.

2. GRUPOS FUNCIONALES

Adicionalmente al carbono y al hidrógeno, los hidrocarbonos también pueden contener otros elemen-
tos. En realidad, hay muchos grupos comunes de átomos que pueden producirse dentro de las molé-
culas orgánicas, estos grupos de átomos son llamados grupos funcionales. Un buen ejemplo es el grupo

funcional oxhidrilo.
El grupo oxhidrilo consiste en un átomo de oxígeno solo enlazado a un átomo de hidrógeno (-OH). El
grupo de hidrocarbonos que contiene un grupo funcional oxhidrilo hace parte de losllamados alcoholes.
Los alcoholes son llamados de manera similar a los hidrocarbonos simples, se pone un prefijo a la raíz
(en este caso “ol”) que designa el alcohol. La existencia de un grupo funcional cambia completamente
las propiedades químicas de la molécula. El etano, el alcano con 2 carbones, es un gas a temperatura
ambiente; el etanol, el alcohol de 2 carbones, es un líquido.

ÁCIDOS CAR-
BOXÍLICOS

ALDEHÍDOS Y
CETONAS
AMINAS
ALCOHOLES
HIDROCARBUROS CARBOHIDRATOS LÍPIDOS PROTEÍNAS ÁCIDOS NUCLEICOS

BIOMOLÉCULAS GRUPOS FUN-
CIONALES

QUÍMICA DEL
CARBONO

39 - 51

Etanol: es el alcohol usado como antiséptico

ALDEHIDOS Y CETONAS
Aldehídos y cetonas se caracterizan por tener el grupo carbonilo
La fórmula general de los aldehídos es
La fórmula general de las cetonas es
Aldehídos

Elsistema de nomenclatura corriente consiste en emplear el nombre del alcano correspondiente termi-
nado en -al. Cuando el grupo CHO es sustituyente se utiliza el prefijo formil-.

También se utiliza el prefijo formil- cuando hay tres o más funciones aldehídos sobre el mismo com-
puesto. En esos casos se puede utilizar otro sistema de nomenclatura que consiste en dar el nombre de

carbaldehído a los grupos CHO (los carbonos de esos CHO no se numeran, se considera que no forman

parte de la cadena). Este último sistema es el idóneo para compuestos con grupos CHO unidos directa-
mente a ciclos.

Cetonas
Para nombrar las cetonas tenemos dos alternativas:
1. El nombre del hidrocarburo del que procede terminado en -ona. Como sustituyente debe emplearse
el prefijo oxo-.
2. Citar los dos radicales que están unidos al grupo carbonilo por orden alfabético y a continuación la
palabra cetona.

Los compuestos carbonílicos presentan puntos de ebullición más bajos que los alcoholes de su mismo
peso molecular. No hay grandes diferencias entre los puntos de ebullición de aldehídos y cetonas de igual
peso molecular.
Los compuestos carbonílicos de cadena corta son solubles en agua y a medida que aumenta la longitud
de la cadena disminuye la solubilidad.

40 - 51

ÁCIDOS CARBOXÍLICOS
Los ácidos carboxílicos presentan el grupo:
Ácidos carboxílicos.
Cuando el grupo carboxilo es la función principal se antepone la palabra ácido al nombre del
hidrocarburo correspondiente acabado en -oico.

Cuando en un compuesto hay tres o más grupos COOH y en caso de ácidos cíclicos se utiliza el sufijo -
carboxílico.

Cuando el grupo -COOH se considera como sustituyente se utiliza el prefijo carboxi
AMINAS
Las aminas pueden considerarse como derivados del Amoníaco.

El cloruro de amonio es un excelente antiséptico.
El método más extendido para nombrar las aminas es el radicofuncional que consiste en tomar como

base el radical más complejo y añadirle el sufijo -amina. Los otros radicales se nombran como sustitu-
yentes sobre el nitrógeno.

Cuando la función amina no es principal se utiliza el prefijo -amino.

Las aminas primarias y secundarias (pueden formar puentes de Hidrógeno) tienen puntos de ebullición
más altos que las terciarias de igual peso molecular.
Las aminas son compuestos eminentemente básicos y forman parte estructural de los aminoácidos y
proteínas

41 - 51

BIOMOLÉCULAS
1. GLÚCIDOS o CARBOHIDRATOS
El término hidrato de carbono es poco apropiado, ya que estas moléculas no son átomos de carbono
hidratados, es decir, enlazados a moléculas de agua, sino de átomos de carbono unidos a otros grupos

funcionales químicos. Este nombre proviene de la nomenclatura química del siglo XIX, ya que las prime-
rassustancias aisladasrespondían a la fórmula elementalCn (H2O)n (donde"n" esunentero=1,2,3... según

el número de átomos). De aquí el término "carbono-hidratado" se haya mantenido, si bien posterior-
mente se vio que otras moléculas con las mismas características químicas no se corresponden con esta

fórmula.
Nombres genéricos que se les han asignado a estos compuestos:
 Carbohidrato: aunque ha habido intentos para sustituir el término de hidratos de carbono, (debido a
que se descubrió que realmente también están compuestos de oxígeno, aparte de carbono e hidrógeno)
desde 1996 el Comité Conjunto de la Unión Internacional de Química Pura y Aplicada (International

Union of Pure and Applied Chemistry o IUPAC) y de la Unión Internacional de Bioquímica y Biología Mo-
lecular (International Union of Biochemistry and Molecular Biology) recomienda el término carbohidrato

y desaconseja el de hidratos de carbono.
 Glúcido: este nombre proviene de que pueden considerarse derivados de la glucosa por polimerización
y pérdida de agua. El vocablo procede del griego "glycýs", que significa dulce.

 Azúcares: este término sólo puede usarse para los monosacáridos (aldosas y cetosas) y los oligosacá-
ridosinferiores(disacáridos). En singular (azúcar)se utiliza para referirse a la sacarosa o azúcar de mesa.

Estructura química

Los glúcidos son moléculas compuestas en su mayor parte por átomos de carbono, hidrógeno y oxí-
geno, su función es producir energía.

En la naturaleza se encuentran en los seres vivos, formando parte de biomoléculas aisladas o asociadas a
otras como las proteínas y los lípidos.

Molécula de glucosa (representación lineal)

42 - 51

Tipos de Carbohidratos
 Monosacáridos. son los que están formados por una molécula de azúcar.
 Disacáridos. Al hidrolizarse producen dos monosacáridos (2 moléculas de azúcar).
 Oligosacáridos. Al hidrolizarse producen de tres a veinte moléculas de monosacáridos.

 Polisacáridos. Al hidrolizarse producen más de veinte moléculas de monosacáridos (miles de molécu-
las de azúcar)

Función de los glúcidos

Los carbohidratos desempeñan diversas funciones, siendo la de reserva energética y formación de es-
tructuraslas dos másimportantes. Por otro lado, esla de mantener la actividad muscular, la temperatura

corporal, la tensión arterial, el correcto funcionamiento del intestino y la actividad neuronal. Actúan
también como elementos de protección.
2. LÍPIDOS
Loslípidos, compuestos químicos que ayudan al buen funcionamiento de losseres vivos,son un conjunto
de moléculas orgánicas, la mayoría biomoléculas, compuestas principalmente por carbono e hidrógeno
y en menor medida oxígeno, aunque también pueden contener fósforo, azufre y nitrógeno, que tienen
como característica principal el ser hidrofóbicas o insolubles en agua y sí en disolventes orgánicos como
la bencina. En el uso coloquial, a los lípidos se les llama incorrectamente grasas, aunque las grasas son
sólo un tipo de lípidos procedentes de animales.
 Lípidos simples: Son aquellos lípidos que sólo contienen carbono, hidrógeno y oxígeno. Estos lípidos
simples se subdividen a su vez en:
1. Glicéridos o grasas: Cuando los acilglicéridos son sólidos se les llama grasas y cuando son líquidos a
temperatura ambiente se llaman aceites.
2. Céridos o ceras.

 Lípidos complejos: Son los lípidos que además de contener en su molécula carbono, hidrógeno y oxí-
geno, también contienen otros elementos como nitrógeno, fósforo, azufre u otra biomolécula como un

glúcido. A los lípidos complejos también se les llama lípidos de membrana pues son las principales mo-
léculas que forman las membranas celulares.

1. Fosfolípidos
2. Glucolípidos
Funciones de los lípidos
Los lípidos desempeñan diferentes tipos de funciones biológicas:
 Función energética: Los lípidos son la principal reserva de energía de los animales y ser humano y una
muy poderosa fuente de energía ya que un gramo de grasa produce 9,4 kilocalorías en las reacciones
metabólicas de oxidación, mientras que las proteínas y los glúcidos sólo producen 4,1 kilocalorías por
gramo.

 Función estructural: Los lípidos forman las bicapas lipídicas de las membranas celulares. Además recu-
bren y proporcionan consistencia a los órganos y protegen mecánicamente estructuras En este grupo

hay tres tipos generales: Glicerofosfolípidos Esfingolípidos Esteroles
 Función aislante térmico: son aislantes térmicos como el tejido adiposo.
 Función catalizadora, hormonal o de mensajeros químicos: Los lípidos facilitan determinadas
reacciones químicas y los esteroides cumplen funciones hormonales.

43 - 51

 Función transportadora: Los lípidos se absorben en el intestino gracias a la emulsión de las sales
biliares y el transporte de lípidos por la sangre y la linfa se realiza a través de las lipoproteínas.
3. ÁCIDOS NUCLEICOS

Los ácidos nucleicosson macromoléculas, polímerosformados por la repetición de monómerosllama-
dos nucleótidos, unidos mediante enlacesfosfodiéster. Se forman así largas cadenas o polinucleótidos.

Pueden alcanzar tamaños gigantes (millones de nucleótidos), siendo las moléculas más grandes que se
conocen. El descubrimiento de los ácidos nucleicosse debe a Miescher que en la década de 1860 aisló de
los núcleos de las células una sustancia ácida a la que llamó nucleína, nombre que posteriormente se
cambió a ácido nucleico.
Existen dostipos de ácidos nucleicos, ADN (ácido desoxirribonucleico) y ARN (ácido ribonucleico), que
se diferencian en:
 El azúcar (pentosa) que contienen: la desoxirribosa en el ADN y la ribosa en el ARN.
 Las bases nitrogenadas que contienen: adenina, guanina, citosina y timina en el ADN; y adenina,
guanina, citosina y uracilo en el ARN.
 La masa molecular del ADN es generalmente mayor que la del ARN.

Las unidades que forman los ácidos nucleicos son los nucleótidos. Cada nucleótido es una molécula com-
puesta por la unión de tres unidades: un monosacárido (una pentosa), una base nitrogenada purínica

(adenina, guanina) o pirimidínica (citosina, timina o uracilo) y uno o varios grupos fosfato (ácido fosfó-
rico). Tanto la base nitrogenada como los grupos fosfato están unidos a la pentosa.

La unión formada por la pentosa y la base nitrogenada se denomina nucleósido.
El ADNes bicatenario, está constituido por 2 cadenas polinucleotídicas unidas entre sí en toda su longitud.
Esta doble cadena puede disponerse en forma lineal (ADN del núcleo de las células eucarióticas) o en

forma circular (ADN de las células procarióticas, así como de las mitocondrias y cloroplastos eucarióti-
cos). La molécula de ADNporta la información necesaria para el desarrollo de las características biológicas

de un individuo y contiene los mensajes e instrucciones para que las células realicen sus funciones.
El ARN difiere del ADN en que la pentosa de los nucleótidos constituyentes, en lugar de desoxirribosa es
ribosa, y en que en lugar de las cuatro bases A, G, C, T aparece A, G, C, U (es decir, uracilo en lugar de
timina). Las cadenas de ARN son más cortas que las de ADN. El ARN está constituido casi siempre por
una única cadena (es monocatenario).
Mientras que el ADN contiene la información, el ARN actúa de mensajero de dicha información para dar
lugar a la síntesis de proteínas.
4. AMINOÁCIDOS y PROTEÍNAS
Los aminoácidos son las unidades químicas estructurales de las proteínas y péptidos. Esto quiere decir

que las uniones de dos o más aminoácidos forman un péptido y si las uniones químicas entre los ami-
noácidos son muy largas, ramificadas y /o extensas forman las proteínas. Como su nombre lo indica los

aminoácidos están formados por un grupo carboxilo (ácido) y el grupo funcional amina, por lo tanto en

su estructura tienen un grupo ácido y un grupo alcalino, por eso las proteínas pueden actuar como solu-
ciones amortiguadoras del pH sanguíneo. Los aminoácidos de importancia biológica para nuestro

organismo son VEINTE y se clasifican en esenciales y no esenciales. Esenciales significa que nuestro or-
ganismo no los puede sintetizar y deben ser incorporados si o si con las dietas. Ejemplos de aminoácidos:

tryptofano, leucina, isoleucina, argidina, lisina, fenilalanina, cisteína, valina, etc.
Las proteínas(del griego poton, primero)son macromoléculas de masa molecular elevada, formadas por

cadenaslineales de aminoácidos unidos mediante enlaces peptídicos. Las proteínas pueden estar forma-
das por una o varias cadenas peptídicas.

44 - 51

Las proteínas son biomoléculas formadas básicamente por carbono, hidrógeno, oxígeno y nitrógeno.
Suelen además contener azufre y algunas proteínas contienen además fósforo, hierro, magnesio o cobre,
entre otros elementos.
La unión de un número pequeño de aminoácidos da lugar a un péptido:
 Péptido: número de aminoácidos MENOR a 10
 polipéptido o proteína:100 o más aminoácidos
Representan las biomoléculasmás abundantes, pues constituyenmás del 50% del peso seco de las células.

La síntesis proteica es un proceso complejo cumplido por las células según las directrices de la informa-
ción suministrada por los genes.

Funciones
 Transporte de: Dióxido de Carbono y Oxígeno (Hemoglobina); Hierro (Ferritina y Transferrina); Cobre
(Ceruloplasmina).
 Protección inmunológica a través de los anticuerpos o inmunoglobulinas: IgA, IgD, IgG, IgM, IgE (Ig:
inmunoglobulinas)
 Intervienen en la coagulación sanguínea: Fibrina, Fibrinógeno, Protrombina y Trombina.
 Intervienen en los procesos contracción muscular: Miosina, Tropomiosina, Actina.
 Transmisión del impulso nervioso a través de los neuropéptidos y neurotransmisores: Acetilcolina, Gaba.
 Función hormonal: la insulina y el glucagón son péptidos
 Función estructural: el colágeno, las histonas, quitina, fibrina, queratina
 Función catalítica: las enzimas son todas proteínas (con la única excepción de la ribozima)
 Función amortiguadora o buffer: Hemoglobina
 Mantenimiento de la presión osmótica. (por ejemplo, la albúmina)
 Energética.
Clasificación
Se suelen clasificar de acuerdo con los siguientes criterios: color, olor y aspecto.
Según su forma:
Fibrosas: presentan cadenas polipéptidicas largas y una atípica estructura secundaria. Son insolubles en
agua y en soluciones acuosas. Ejemplo: la queratina.
Globulares: se caracterizan por doblar apretadamente sus cadenas en una forma esférica apretada o

compacta. La mayoría de las enzimas, anticuerpos, algunas hormonas, proteínas de transporte, son ejem-
plo de proteínas globulares.

Según su composición química
Simples u holoproteínas: su hidrólisis sólo produce aminoácidos. Ejemplos de estas son la insulina y el
colágeno (fibrosas y globulares).

45 - 51

Conjugadas o heteroproteínas: su hidrólisis produce aminoácidos y otras sustancias no proteicas llamado
grupo prostético (sólo globulares).
Estructura

Presentan una disposición característica en condiciones ambientales, si se cambia la presión, tempera-
tura, pH, etc. pierde la conformación y su función, proceso denominado desnaturalización. La función de-
pende de la conformación y ésta viene determinada por la secuencia de aminoácidos.

Las estructuras son: primarias a cuaternaria
COMBUSTIÓN

La combustión es una reacción química en la que un elemento combustible se combina con otro com-
burente (generalmente oxígeno en forma de O2 gaseoso), desprendiendo energía en forma de calor; la

combustión es una reacción exotérmica debido a su descomposición en los elementos liberados: calor
al quemar y luz al arder.
Es la combinación rápida de un material con el oxígeno, acompañada de un gran desprendimiento de
energía térmica y energía luminosa.

Los tipos más frecuentes de combustible son los materiales orgánicos que contienen carbono e hidró-
geno. El producto de esasreacciones puede incluir monóxido de carbono (CO), dióxido de carbono (CO2),

agua (H2O) y cenizas.
El proceso de destruir materiales por combustión se conoce como incineración.
Para iniciar la combustión de cualquier combustible, es necesario alcanzar una temperatura mínima,
llamada ignición o de inflamación.
Cuando una sustancia orgánica al reaccionar con el oxígeno el producto resultante es sólo CO2 (g) y H2O
(l); esto es, la combustión completa se produce cuando el total del combustible reacciona con el oxígeno.
Si la combustión es incompleta se produce monóxido de carbono.
La combustión se denomina completa o perfecta, cuando toda la parte combustible se ha oxidado al
máximo, es decir, no quedan residuos de combustible sin quemar.
La fórmula de la combustión completa es:

La ecuación de combustión de la glucosa es la siguiente:

Una de las reacciones más importantes del metabolismo que vamos a estudiar es la respiración celular.

Se define a la RESPIRACIÓN CELULAR como la degradación de una fuente de energía para obtener ener-
gía

Como es una reacción de degradación es una reacción CATABÓLICA
Si se trata de respiración celular se da en la célula y comienza en el citoplasma y sigue en la mitocondria

46 - 51
RESPIRACIÓN CELULAR

REACTIVOS PRODUCTOS DE LA REACCIÓN
C6H12O6 + 6 O2 6 CO2 + 6 H2O + ATP
GLUCOSA
(Fuente de
Energía)

OXIGENO 1. Glucolisis (se

produce en el cito-
plasma)

2. Ciclo de Krebs

3. Cadena respi-
ratoria y fosfori- la-
ción oxidativa

(2 y 3 se producen
en la mitocondria)

DIÓXIDO

de CAR-
BONO

AGUA ENERGÍA

El oxígeno degrada, por oxidación, a la glucosa. ¿En qué la degrada? En dióxido de carbono, agua y ener-
gía.

Las reacciones de oxidación también son conocidas como reacciones de combustión, porque el oxígeno
(comburente) degrada a la glucosa (combustible). Siempre en una reacción de oxidación o combustión
se libera dióxido de carbono agua y se libera energía (por eso es exotérmica).
La respiración celular en presencia de oxígeno se denomina AERÓBICA y la combustión es completa.
Cuando la concentración de oxígeno es baja se denomina ANAEROBICA y la combustión esincompleta La
principal fuente de energía en la respiración celular es la glucosa, porque de ella se obtiene energía en
forma rápida pero no quiere decir que ésta sea la única fuente de energía,también lo son los ácidos grasos
(lípidos) y las proteínas, pero en estos casosla obtención de energía esmáslenta. De loslípidosse obtiene
el doble de energía que de la glucosa, pero lo hace en forma lenta.
El ATP (Adenosin TriFosfato) es la forma de energía química que luego, por el principio de conservación
de la energía se transforma en CALOR
https://www.profesorenlinea.cl/Quimica/Quimica_organica.htmlhttps://www.profesorenlinea.cl/Quimica
/Quimica_organica.htmlhttps://www.profesorenlinea.cl/Quimica/Quimica_organica.html
https://www.profesorenlinea.cl/Ciencias/ProteinasEstruct.htm
https://www.profesorenlinea.cl/Ciencias/ProteinasAminoacidos.htm
https://www.profesorenlinea.cl/Ciencias/Biomoleculas.html

47 - 51

AUTOEVALUACIÓN UNIDAD 6

1. ¿Cómo se denomina a las moléculas relativamente pequeñas que constituyen la base estructural de
los glúcidos o hidratos de carbono más complejos? Dar TRES (3) ejemplos de los mismos
2. ¿Cómo se denomina al grupo de biomoléculas orgánicas formadas por cadenas muy ramificadas de
aminoácidos?
3. Tache dentro de cada uno de los paréntesis la opción que no sea correcta.

Los lípidos son biomoléculas (ORGÁNICAS – INORGÁNICAS) de naturaleza (ALCALINA – ÁCIDA) que si es-
tán en estado líquido se los conoce con el nombre de (ACEITES - GRASAS)

4. En cada ítem, complete con la respuesta correcta sobre la línea punteada.
a) Las unidades químicas estructurales de las proteínas se denominan ..........................................
b) Las principales biomóleculas orgánicas encargadas de proveer energía al organismo son ...............
c) Tres ejemplos de proteína son .......................................................................................
d) El alcohol etílico también es conocido con el nombre de ........................................................
5. ¿En qué tipo de solventes son insolubles los lípidos?
6. Dar por lo menos TRES (3) ejemplos de:
a. Proteínas
b. Glúcidos
c. lípidos
7. ¿Cuál es el grupo funcional de los compuestos de amonio cuaternario?
8. ¿Cuál es la función de la hemoglobina?
9. Las proteínas tienen funciones estructurales VERDADERO FALSO
10. ¿Cuál es la función de los lípidos en cuánto a la temperatura corporal?
11. ¿Por qué las reacciones de combustión son reacciones de oxidación?
12. ¿Las reacciones de combustión, gastan (consumen) o producen (liberan) energía? Dar un ejemplo.

48 - 51
GLOSARIO

Ácidos Nucleicos
Son macromoléculas, polímeros formados por la repetición de monómeros llamados nucleótidos, unidos
mediante enlaces fosfodiéster. Se forman así largas cadenas o polinucleótidos. Pueden alcanzar tamaños
gigantes (millones de nucleótidos), siendo las moléculas más grandes que se conocen.
Anabolismo
Conjunto de reacciones químicas intracelulares que forman parte del metabolismo que son reacciones
de síntesis o de producción, y por lo tanto implica un gasto de energía.
Átomo
Menor porción de materia que participa en una reacción química.
Agente oxidante
Especie que tiende a captar electrones, quedando con carga positiva menor a la que tenía.
Agente reductor
Especie química que tiende a ceder electrones de su estructura química al medio, quedando con una carga
positiva mayor a la que tenía.
Catabolismo
Conjunto de reacciones químicas de degradación que forman parte del metabolismo.
Combinación química
Fenómeno químico en el cual dos o mássustanciasse unen dando lugar a otra sustancia, cuyas propiedades
son diferentes de las que tenían las sustancias combinadas.
Combustión
Reacción química en la que un elemento combustible se combina con otro comburente (oxígeno en forma
de O2 gaseoso), desprendiendo calor y produciendo un óxido; la combustión es una reacción exotérmica
debido a su descomposición en los elementos liberado.
Concentración
Relación entre la cantidad de soluto y de solvente o entre la cantidad de soluto y la solución.
Constantes físicas
Propiedades intensivas que deben ser determinadas a través de mediciones experimentales.
Cuerpo
Toda porción limitada de material.
Densidad ( )
Es una magnitud referida a la cantidad de masa contenida en un determinado volumen.
Descomposición
Es un fenómeno químico en el cual partiendo de una sustancia se obtienen dos o más sustancias con
distintas propiedades a la primera.

49 - 51

Electrolitos
Las sustancias que, disueltas en agua, conducen la corriente eléctrica. Átomos o grupos de átomos con

cargas eléctricas en solución. Cationes, quienes presenten cargas positivas y aniones quienestengan car-
gas negativas

Electrón
Partícula atómica con carga eléctrica negativa.
Elemento químico
Componente común de una sustancia.
Enzima (Catalizador)

Toda sustancia que aumenta la velocidad de una reacción química, sin modificar el resultado ni ser con-
sumida en la misma.

Fase

En un sistema heterogéneo se llama fase a cada uno de los sistemas homogéneos perfecta-
mente diferenciables que lo componen.

Función química
Es un conjunto de propiedades que permiten agrupar a ciertas sustancias.
Gas
Estado de agregación de la materia que no tiene forma ni volumen propio.
Glúcidos
Son moléculas compuestas en su mayor parte por átomos de carbono, hidrógeno y oxígeno, su función es
producir energía. También llamados hidratos de carbono.
Hidrocarburos
Son los químicos orgánicos más simples, contienen sólo carbono y átomos de hidrógeno.
Indicador de pH
Sustancia que permite medir el pH de un medio.
Ión
Átomos con carga eléctrica. Surgen de la ganancia o pérdida de electrones por parte de un átomo. El
electrón es más fácil de desprender cuanto más alejado del núcleo esté. Se clasifican en aniones (con
cargas negativas) y en cationes (con cargas positivas)
Isómeros
Son moléculas que tienen la misma fórmula química, pero diferentes fórmulas estructurales.
Isótopo
Átomo de un elemento que tiene igual Z (número atómica) y diferente A (número másico).
Leyes gravimétricas
Leyes fundamentales de la química que establecen las relaciones entre las masas.

50 - 51

Leyes volumétricas
Leyes fundamentales de la química que establecen las relaciones entre los volúmenes.
Lípidos
Conjunto de moléculas orgánicas, la mayoría biomoléculas, compuestas principalmente por carbono e
hidrógeno y en menor medida oxígeno, aunque también pueden contener fósforo, azufre y nitrógeno,

que tienen como característica principal el ser hidrofóbicas o insolubles en agua y sí en disolventes orgá-
nicos como la bencina. En el uso coloquial, a los lípidos se les llama incorrectamente grasas, aunque las

grasas son sólo un tipo de lípidos procedentes de animales.
Materia
Todo aquello que tiene masa, ocupa un lugar en el espacio e impresiona nuestros sentidos.
Materiales
Son los diferentes tipos de componentes que constituyen los cuerpos.
Metabolismo
Conjunto de reacciones químicas intracelulares que pueden ser de síntesis (anabolismo) o de degradación
(catabolismo)
Mol
Es la unidad de cantidad de sustancia.
Molécula
Es la porción más pequeña de una sustancia que puede existir libre y conservar las propiedades de dicha
sustancia. La molécula está formada por 1 o más átomos.
Moléculas monoatómicas
Moléculas constituidas por un solo átomo.
Neutrón
Partícula del núcleo atómico sin carga eléctrica.
Propiedades extensivas
Son aquellas que dependen de la cantidad de materia considerada.
Propiedades intensivas
Son aquellas que NO dependen de la cantidad de materia sino de la calidad de las mismas.
Propiedades organolépticas
Propiedades intensivas de las sustancias que se pueden apreciar por medio de los sentidos, como el olor,
el sabor, el color, la sensación al tacto, el sonido, etc.
Proteínas
Son macromoléculas de masa molecular elevada, formadas por cadenas lineales de aminoácidos unidos
mediante enlaces peptídicos. Las proteínas pueden estar formadas por una o varias cadenas peptídicas.

51 - 51

Protón
Partícula del núcleo del átomo con carga positiva.
Química Orgánica
Rama de la Química que estudia principalmente los compuestos que contienen carbono.
Sistema material
Cuerpo o conjunto de cuerpos que se aíslan en forma real o imaginaria para ser estudiados.
Sistema heterogéneo
Sistema que presenta propiedades intensivas diferentes en algunas de sus fases.
Sistema homogéneo
Sistema que en todos los puntos de su masa presenta las mismas propiedades intensivas.
Solubilidad
Propiedad que tiene un soluto de disolverse en un determinado solvente a una cierta temperatura.
Soluciones
Son sistemas homogéneos que admiten fraccionamiento formados por dos o más solutos.
Soluciones amortiguadoras

Soluciones que son capaces de mantener constante el valor de pH, después de la adición de peque-
ñas cantidades tanto de ácido como de base. También se las denomina buffer o tampón.

Soluto
Componente/s que se halla/n en menor proporción en la masa de la solución. La parte de la solución
que se disuelve en el solvente
Solvente
Componente/s que se halla/n en mayor proporción en la masa de la solución. La parte que disuelve al
soluto.
Sustancia
Es la calidad de la materia que constituye un cuerpo.
Sustancias puras

Son sistemas homogéneos formados por una sola sustancia, cuyas propiedades intensivasson particula-
res y constantes.

Zona extranuclear
Espacio, zona alrededor del núcleo. Orbita
    """
def extract_keywords_from_message(message):
    words = re.findall(r'\b\w+\b', message.lower())
    return set(words)

# Guardar el historial de conversaciones en un archivo JSON
def load_conversations():
    if os.path.exists("conversation_history.json"):
        with open("conversation_history.json", "r") as f:
            return json.load(f)
    return []

def save_conversation_to_json(conversation):
    conversations = load_conversations()
    conversations.append(conversation)
    with open("conversation_history.json", "w") as f:
        json.dump(conversations, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    conversation_history = data.get('conversationHistory', [])

    if not user_message:
        return jsonify({"message": "Falta el mensaje"}), 400

    print(f"Mensaje del usuario: {user_message}")

    # Ahora usamos directamente pdf_text en el system prompt
    messages = conversation_history + [
        {"role": "system", "content": f"Información relevante de los manuales:\n{pdf_text}"},
        {"role": "user", "content": user_message}
    ]

    try:
        # Solicitar la respuesta a OpenAI usando el historial de la conversación
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.9
        )
        ai_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error en la API de OpenAI: {str(e)}")
        ai_response = "Hubo un error al procesar tu solicitud."

    # Guardar la conversación en un archivo JSON
    conversation = {
        "message": user_message,
        "response": ai_response
    }
    save_conversation_to_json(conversation)

    return jsonify({"response": ai_response, "conversationHistory": messages})

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)



