# Ficheiros de projeto do manual (Edição Portugal)

Cada ficheiro reproduz um estudo de caso descrito no manual do utilizador da Edição Portugal. Abra através do menu **Ficheiro > Abrir projeto**, e clique em **Simular**.

A série de precipitação está integrada **dentro** de cada ficheiro: abre sem necessidade do ficheiro CSV original, em qualquer computador. Lisboa e Porto utilizam a base E-OBS por concelho (normal 1991–2020), enquanto o Funchal utiliza a série horária ERA5 agregada diariamente.

| Ficheiro | Secção | O que demonstra | Concelho / Contexto |
| :--- | :--- | :--- | :--- |
| `01_tutorial_lisboa.triton` | Capítulos 4 e 5 | Moradia do tutorial com 150 m² de cobertura, 4 residentes, cisterna de 4.000 L, tarifário EPAL/Câmara | Lisboa (E-OBS 1991–2020) |
| `02_porto.triton` | Secção 3.1 | Moradia do tutorial simulada no clima atlântico do norte e tarifário da Águas e Energia do Porto | Porto (E-OBS 1991–2020) |
| `03_funchal.triton` | Secção 3.1 | Moradia do tutorial simulada no arquipélago da Madeira, tarifário do Funchal e eletricidade EEM | Funchal (ERA5 1991–2020) |
| `04_tutorial_varredura.triton` | Secção 4.4 | Varredura e otimização do volume do reservatório de 0 a 20.000 L com passo de 1.000 L | Lisboa (E-OBS 1991–2020) |
| `05_dez_dias.triton` | Secção 2.1 | Caso didático de dez dias para verificação manual do balanço hídrico diário | Verificação e controlo |
