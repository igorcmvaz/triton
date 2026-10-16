<!-- tabela: The variables that probabilistic modulation can draw, with the screening distribution the screen proposes -->
| Group | Variable | Unit | Screening distribution | Ticked on opening |
| :--- | :--- | :--- | :--- | :--- |
| Demand | Per capita consumption | L/person/day | lognormal, project mean, CV of 20% | yes |
| Demand | Number of occupants | occupants | normal, project mean, deviation of 1 occupant; integer from 1 to double | yes |
| Demand | Indoor non-potable fraction | % | normal, project mean, deviation of 5 points; 0 to 100% | yes |
| Demand | Outdoor demand | L/day | normal, project mean, CV of 30% | no |
| Catchment | Catchment area | m² | normal, project mean, CV of 5% | no |
| Catchment | Runoff coefficient | — | triangular, from project −0.10 to project +0.05; 0 to 1 | no |
| Catchment | First-flush depth | mm | uniform, from project −1 mm to project +1 mm | no |
| Rain | Rainfall factor | × | normal, mean 1, deviation of 0.10 | no |
| Tariffs | Water and sewerage tariff factor | × | normal, mean 1, deviation of 0.10 | no |
| Tariffs | Sewerage factor | × | normal, mean 1, deviation of 0.10 | no |
| Tariffs | Tariff escalation | % per period | normal, project mean, deviation of 2 points | no |
| Tariffs | Energy tariff | currency units/kWh | normal, project mean, CV of 10% | no |
| Tariffs | Electricity escalation | % per period | normal, project mean, deviation of 2 points | no |
| Costs | Investment factor | × | lognormal, mean 1, deviation of 0.15 | no |
| Costs | Cistern price factor | × | lognormal, mean 1, deviation of 0.15 | no |
| Costs | Running cost factor (O&M) | × | lognormal, mean 1, deviation of 0.25 | no |
| Costs | Running cost inflation | % per month | normal, project mean, deviation of 0.10 point | no |
| Cash flow | Minimum attractive rate of return | % per month | normal, project mean, deviation of 0.25 point | no |
| Cash flow | Analysis period | years | triangular, from project −5 to project +5 years; integer, at least 1 | no |
| Environment | Potable water emission factor | × | normal, mean 1, deviation of 0.20 | no |
| Environment | Grid electricity emission factor | × | normal, mean 1, deviation of 0.20 | no |
