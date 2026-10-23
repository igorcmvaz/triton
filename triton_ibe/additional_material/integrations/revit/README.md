# Integração Triton → Revit

O Triton exporta a biblioteca CAD em escala 1:1 mm e, ao lado dela, um arquivo
`*_triton-bim.json`. O JSON é o contrato auditável entre o cálculo e o modelo.

## Fluxo recomendado

1. No Triton Desktop, escolha **Biblioteca de Blocos para Plantas + BIM JSON**.
2. Insira os blocos DXF na planta CAD ou preencha `bim_components` no projeto
   com coordenadas locais em milímetros, nível, rotação e parâmetros.
3. No Revit, carregue e revise as famílias hidrossanitárias do escritório.
4. Ajuste `family_mapping.json` para os nomes reais de família e tipo.
5. Execute `triton_import.py` no motor CPython 3 do pyRevit, com um documento
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

## Trechos de tubulação e planta 3D (manifesto 1.1)

Na Central de Exportação, **Organizar Trechos de Tubulação (Planta 3D)** abre
uma tabela em que o projetista posiciona os componentes e lista os trechos na
ordem de montagem. Cada trecho parte de um componente (`CI-01`), do fim de um
trecho anterior (`T-01`), de coordenadas (`0 0 -1500`) ou, com a origem em
branco, do fim do trecho imediatamente acima. O percurso é descrito por
direções e comprimentos em mm:

```text
+x 3000; +y 2000; sobe 6500        eixos: ±x, ±y, ±z, sobe, desce, norte, sul, leste, oeste
d 3000 0 -30                       deslocamento livre (aqui, 1 % de declividade)
```

Origem e destino num componente aceitam um **ponto de conexão** após `:`,
calculado pela mesma envoltória desenhada na volumetria:

| Ponto | Posição |
|---|---|
| `RS-01` ou `RS-01:fundo` | centro da base |
| `RS-01:topo` | centro do topo |
| `RS-01:sup+x`, `sup-x`, `sup+y`, `sup-y` | lateral, a 85 % da altura, do lado indicado (eixos do componente) |
| `RS-01:inf+x` … `inf-y` | lateral, a 12 % da altura |

Use pontos distintos para quem chega e quem sai: o recalque entra pelo topo ou
pela lateral superior do reservatório superior e a distribuição sai pelo fundo
ou pela lateral inferior. Dois tubos nunca ocupam o mesmo espaço: sobreposição,
cruzamento ou saída quase paralela do mesmo ponto (menos de ~24°) é erro de
interferência, com o local e a extensão; curvas, continuações e tês são
aceitos. Os pontos laterais e o topo de reservatórios sem Ø e altura informados
dependem da capacidade; informe as medidas para fixá-los.

O destino, quando informado, é conferido e não completado: se o percurso não
chega ao componente, o Triton informa o deslocamento que falta. Em sistemas por
gravidade (captação, descarte, extravasor), segmentos que sobem ou com
declividade abaixo de 0,5 % geram aviso. A organização é salva no `.triton`.

Com o modo **Planta 3D dos Trechos Organizados + BIM JSON**, o DXF traz, por
sistema, o eixo em POLYLINE 3D e o tubo em malha no diâmetro nominal, além dos
blocos na cota de cada componente; o SVG é um esquema 3D fora de escala, numerado na ordem
dos trechos. O manifesto passa a registrar `pipe_runs` com os vértices já
resolvidos:

```json
{
  "run_id": "T-02", "sequence": 2, "system": "recalque", "dn_mm": 25,
  "material": "PVC", "level": "Nível 0", "start_ref": "T-01", "end_ref": "RS-01",
  "route": "+x 3000; +y 2000; +z 6500",
  "vertices_mm": [{"x": 1500, "y": 0, "z": 0}, "..."],
  "segments": [{"start_mm": {"...": 0}, "end_mm": {"...": 0}, "length_mm": 3000}],
  "length_mm": 11500
}
```

No Revit, `triton_import.py` cria cada segmento como `Pipe` nativo, na ordem do
manifesto, e une segmentos consecutivos por curva ou luva. A seção
`_tubulacoes` de `family_mapping.json` associa cada sistema Triton a um
*Piping System Type* e cada material a um *Pipe Type* do template do escritório;
ajuste os nomes antes de importar. Trechos sem sistema, tipo ou nível
correspondente ficam pendentes, e juntas que o Revit recusar (por falta de
preferência de roteamento) são listadas ao final.

## Volumetria 3D girável

Na mesma janela de organização, a aba **Volumetria 3D** mostra a maquete de
estudo em escala, que pode ser girada, aproximada e clicada (a peça clicada
mostra a sua ficha):

| Elemento | Sólido | Dimensões |
|---|---|---|
| Cisterna e reservatório superior | prisma circular | `DIAMETRO_MM` e `ALTURA_MM`; na falta, estimadas pela capacidade (a do componente ou a calculada pelo Triton), com H = D na cisterna e H = 0,55·D no superior. A ficha avisa quando a medida é estimada. |
| Edificação | prisma retangular translúcido, com as lajes | canto, largura, profundidade, altura e pavimentos informados na janela |
| Motobomba | prisma de base losango | proporcional à potência, quando informada |
| Filtro, descarte, registros, válvulas | cilindros e cubos pequenos | ilustrativas |
| Tubulação | prisma octogonal por segmento, no DN | tubos muito finos para a escala da cena ganham espessura mínima de visualização (declarada) |

A posição de cada componente é o **centro da base**. Controles: arrastar gira;
Shift, botão direito ou do meio deslocam; a roda aproxima; 1–4 escolhem
perspectiva, planta, frente e lateral; F enquadra; Esc limpa a seleção.

A volumetria é exportada em dois formatos, pelos botões da janela ou junto do
DXF da Planta 3D (`*_volumetria.glb` e `*_volumetria.html`):

* `.glb` (glTF 2.0): abre no Visualizador 3D do Windows, no Blender e em
  visualizadores web; cada sólido é um nó nomeado com a ficha em `extras`.
  O arquivo passa sem erros nem avisos no validador oficial da Khronos.
* `.html`: página autocontida (sem internet nem bibliotecas externas) com o
  mesmo visualizador, para enviar a quem não tem o Triton.
