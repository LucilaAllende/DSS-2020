 /* CREATE TABLE */
CREATE TABLE IF NOT EXISTS datos_covid(
code VARCHAR( 100 ),
name VARCHAR( 100 ),
pop_dens VARCHAR( 100 ),
total_pop INT,
country_percentage VARCHAR( 100 ),
fecha VARCHAR( 100 ),
dia_inicio INT,
dia_cuarentena INT,
provincia VARCHAR( 100 ),
ciudad VARCHAR( 100 ),
tot_casosconf INT,
nue_casosconf INT,
tot_fallecidos INT,
transmision_tipo VARCHAR( 100 ),
informe_tipo VARCHAR( 100 ),
fuente VARCHAR( 200 )
);