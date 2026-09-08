# Integração Netuno 5 → Revit

O Netuno exporta a biblioteca CAD em escala 1:1 mm e, ao lado dela, um arquivo
`*_netuno-bim.json`. O JSON é o contrato auditável entre o cálculo e o modelo.

## Fluxo recomendado

1. No Netuno Desktop, escolha **Biblioteca de Blocos para Plantas + BIM JSON**.
2. Insira os blocos DXF na planta CAD ou preencha `bim_components` no projeto
   com coordenadas locais em milímetros, nível, rotação e parâmetros.
3. No Revit, carregue e revise as famílias hidrossanitárias do escritório.
4. Ajuste `family_mapping.json` para os nomes reais de família e tipo.
5. Execute `netuno_import.py` no motor CPython 3 do pyRevit, com um documento
   RVT aberto (Revit 2022 ou mais recente).

O script não cria famílias `.rfa` nem um arquivo `.rvt` fora do Revit. Isso
exigiria a API da versão instalada, templates e famílias aprovadas pelo
projetista. Instâncias sem família ou nível correspondente são apenas listadas
como pendentes; não são substituídas silenciosamente.

## Estrutura mínima de uma instância

```json
{
  "instance_id": "CI-01",
  "type_id": "cisterna_inferior",
  "level": "Térreo",
  "position_mm": {"x": 12500, "y": 8200, "z": 0},
  "rotation_deg": 90,
  "parameters": {"CAPACIDADE_L": 10000, "DIAMETRO_MM": 2400}
}
```

As coordenadas são locais e não georreferenciadas até que o projetista defina
o ponto-base, norte e sistema compartilhado no Revit.
