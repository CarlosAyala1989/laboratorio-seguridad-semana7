rule Cadena_Controlada_Muestra
{
    meta:
        descripcion = "Marca de prueba insertada intencionalmente en un archivo benigno"
        interpretacion = "Coincidencia didáctica; no indica malware"
    strings:
        $marca = "MARCA_PRUEBA_YARA_CONTROLADA" ascii
    condition:
        $marca
}

rule Marcador_JSON_Benigno
{
    meta:
        descripcion = "Campo de control presente en el JSON creado para el laboratorio"
        interpretacion = "Coincidencia didáctica; no indica malware"
    strings:
        $campo = "\"indicador_json_benigno\"" ascii
        $valor = "registro_controlado" ascii
    condition:
        $campo and $valor
}
