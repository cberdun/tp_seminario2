#ANÁLISIS DE DEPARTAMENTOS DEL PAÍS Y SUCURSALES DE BANCOS

El trabajo final integrador de la especialización consiste en el desarrollo de un modelo que describa y mida las correlaciones existentes entre datos demográficos y geográficos del negocio bancario y determine las reglas de localización de entidades financieras físicas. Se propone realizar un análisis de clúster con datos demográficos a fin de agrupar y caracterizar departamentos, para luego relevar con herramientas de sistemas de información geográfica (GIS) las correlaciones existentes. La comparación a nivel geográfico de las agrupaciones de departamentos y la presencia bancaria actual permitirá describir las reglas de correlación y sus variaciones geográficas.

Para el trabajo práctico presente, se realizará un análisis de los datos del dataset y se ensayará un modelo de regresión para estudiar si es posible estimar las localizaciones con los datos relevados.

##CARGA DE DATOS
Se ingresa un dataset compilado a partir de datos del Censo de hogares del INDEC y la nómina de filiales de bancos del BCRA.

BANCO CENTRAL DE LA REPÚBLICA ARGENTINA (s.f. -b), Sucursales Plenas (a junio de 2023). Recuperado el 30/9/2023 de: https://www.bcra.gob.ar/SistemasFinancierosYdePagos/Entidades_financieras_filiales_y_cajeros.asp?bco=AAA00&tipo=1&Tit=1
** Instituto Nacional de Estadística y Censos de la República Argentina (s.f. -c), INDEC: Censo 2022 - Indicadores de condiciones habitacionales de las viviendas particulares ocupadas. Recuperado el 30/9/2023 de: https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos-3
