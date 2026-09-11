# 21. Importar um projeto do Netuno 4

> **Pergunta que este guia responde:** meus estudos antigos abrem no Netuno 5?

Abrem. Mas nem tudo atravessa, e o que não atravessa não avisa.

---

## 21.1. Como importar

Abra o arquivo `.netuno` antigo pelo menu de abertura. O programa reconhece o
formato legado — texto separado por ponto e vírgula — e converte para a estrutura
nova.

Salve em seguida. O arquivo passa a ser gravado no formato JSON do Netuno 5, com os
103 campos, e o original permanece intacto.

---

## 21.2. O que vem

| Dado | Vem? |
| :--- | :---: |
| arquivo e data inicial da chuva | sim |
| área de captação, coeficiente de escoamento | sim |
| descarte de primeiras águas e modo | sim |
| demanda total e número de moradores | sim |
| percentual atendível por água pluvial | sim |
| reservatório superior, limiar de recalque | sim |
| reservatório inferior, faixa e passo | sim |
| diferença entre potenciais | sim |
| tarifas de água e esgoto, impostos | sim |
| custos iniciais: mão de obra, tubulação, acessórios | sim |
| motobomba: potência, rendimento, vazão, tempo de partida, custo | sim |
| tarifa de energia e impostos | sim |
| inflação, reajuste, período de análise, TMA | sim |
| custos operacionais | sim |

---

## 21.3. O que **não** vem

> **Atenção, e confira sempre.** O leitor de arquivos antigos **não reconhece
> nenhuma chave de demanda variável**. Um projeto do Netuno 4 com demanda mensal ou
> diária é importado como demanda **constante**, em silêncio.

Se o seu estudo antigo usava demanda variável, a importação o degrada. Confira na
aba Edificação depois de importar: se o modo estiver em «constante» e você sabe que
não era, relance o perfil à mão.

Também não vêm, por não existirem no Netuno 4:

- irrigação e supressão por chuva;
- classe de qualidade da água e linha de tratamento;
- materiais dos reservatórios e comprimentos por diâmetro de tubo;
- parâmetros de ciclo de vida;
- IPTU verde e incentivos;
- tipologia da edificação;
- número de economias.

Todos assumem o padrão da versão 5, e vale revisá-los.

---

## 21.4. Por que o resultado muda

Mesmo com a importação perfeita, o número **não** será idêntico. A diferença é
deliberada e está quantificada.

**O descarte de primeiras águas.** O Netuno 4 trata a lâmina como **limiar do
evento**: abaixo dela nada é captado, acima dela capta-se a chuva inteira. O Netuno 5
**subtrai** a lâmina. A mudança é fisicamente mais fiel — a água desviada para o
dispositivo de autolimpeza não chega à cisterna.

Sobre 4.050 casos de referência, o Netuno 5 estima, em média, de **2,3 a 2,7 pontos
percentuais menos** economia de água potável que o Netuno 4. Cerca de 46% dessa
diferença vem daqui.

**As demais causas** estão decompostas no capítulo 35.

---

## 21.5. Comparar as duas versões corretamente

Se o seu estudo compara as versões, há um procedimento que isola o balanço hídrico
da divergência deliberada:

**Rode com descarte igual a zero.** Sem descarte, as duas regras coincidem, e a
comparação fica direta. É a forma mais simples e não exige nada do programa.

Feita a comparação com descarte zero, repita com o descarte real para medir a
diferença total. Os dois números juntos separam o que é mudança de método do que é
mudança de implementação.

> O protocolo de verificação do repositório menciona uma opção de linha de comando
> para emular a regra antiga. **Essa opção não está implementada.** Use o caminho do
> descarte zero.

---

## 21.6. Depois de importar

Uma lista de conferência:

1. **modo de demanda** — foi degradado para constante?
2. **tipologia** — está na correta?
3. **materiais** dos reservatórios — o padrão é polietileno;
4. **classe de qualidade** e desinfecção;
5. **regime tarifário** do município — o Netuno 4 não o distinguia;
6. **rendimento do motor** da bomba, campo novo da versão 5.0.8;
7. rode `validate` pela linha de comando antes de confiar.

E guarde o arquivo original. Ele é a evidência do estudo antigo.
