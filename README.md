# human-mobility-covid19
# Human Mobility and COVID-19 epidemic correlation. 

## Project for Life Data Epidemiology course at University of Padova.

**Author**: Lucia Depaoli

**Project Summary**: the COVID-19 epidemic had an unprecedent effect on human mobility.
Governments and the scientific community needed to find a way to reduce the spreading of the disease.
The aim of this project is to answers questions such as: How was COVID-19 epidemic influenced by reducing-spreading factors such as masks, mobility restrictions, and were lockdowns useful for the reduction of the spreading?

For more information, see the [report](https://github.com/luciadepaoli/human-mobility-covid19/blob/main/human_mobility_covid.pdf).

### Introduction
In this work I've evaluated the correlation between different mobility indicators, namely:
- Google COVID 19 Community Mobility Reports
- Median of users' radius of gyration
- Average degree of the proximity network
- $𝑅_𝑡$ computed with CovidStat algorithm
With the daily infected number, provided by Dipartimento della Protezione Civile.

The project involves only italian data. The correlation was evaluated considering a shift in days between the variables. Such shift was selected evaluate the difference in number of days that maximizes the absolute value of the correlation.

### Results achieved:
- Mobility variables and $𝑅_𝑡$ number are correlated
- - Lockdowns were useful for the reduction of the spreading
- - By monitoring the occupation of the places, we can monitor the spreading of the disease
- - A reduction in mobility led to a reduction in $𝑅_𝑡$ number, the spreading of the disease was reduced
- - By impose specific restrictions , we can control the spreading of the disease
