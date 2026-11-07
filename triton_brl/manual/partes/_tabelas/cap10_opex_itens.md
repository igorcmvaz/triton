<!-- tabela: Itens que entram sozinhos no custeio anual de um projeto novo, com valor padrão, periodicidade, origem e modo de alterar -->
| Item | Valor padrão | Periodicidade | Origem | Como alterar ou desligar |
| :--- | :--- | :--- | :--- | :--- |
| Inspeção e limpeza de calhas/pré-filtro | R$ 240,00 por evento | a cada 12 meses | padrão do projeto novo; os mesmos três valores estão em `default_maintenance_items` | botão «3. Outros Custos Operacionais»: editar, excluir ou acrescentar |
| Limpeza e inspeção do reservatório | R$ 320,00 por evento | a cada 12 meses | padrão do projeto novo; os mesmos três valores estão em `default_maintenance_items` | botão «3. Outros Custos Operacionais»: editar, excluir ou acrescentar |
| Manutenção preventiva da motobomba | R$ 180,00 por evento | a cada 12 meses | padrão do projeto novo; os mesmos três valores estão em `default_maintenance_items` | botão «3. Outros Custos Operacionais»: editar, excluir ou acrescentar |
| cloração | 1,5 mg/L de cloro ativo, pastilha a 65%, R$ 25,00 por kg de produto: 0,00231 kg e R$ 0,0577 por m³ | contínua, proporcional ao volume pluvial aproveitado | `Cloracao` (`chlorination.py`) e `chlorine_cost_per_kg` | dose e desinfetante na etapa «3. Qualidade & ETAP»; o preço do quilograma só pelo arquivo do projeto |
| descarte inicial | R$ 40,00 por ano (reservatório de descarte e separador de folhas) | anual | `size_first_flush_system` | caixa do descarte físico na etapa «3. Qualidade & ETAP» |
| energia da motobomba | R$ 0,6957 por kWh, bandeira verde, impostos de 0% | contínua, proporcional à energia anual da motobomba | tarifa B1 residencial do município na base ANEEL, ou o padrão do projeto | botão «2. Motobomba e Custo de Energia»: cidade, tarifa, impostos; bandeira na etapa econômica |
| IPTU Verde | desligado | anual | opção do município na base de tarifas | caixa na etapa econômica |
