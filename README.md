# rongzi
Supply two Chinese characters, and the application will find optimized character-paths connecting them.  

## input: ```蓉 榮```
## output: ```蓉 容 榕 木 榮```

---

### Demonstration webapp:

(link to Streamlit webapp)

### Challenge specification:
- Query a database of Chinese character radical breakdowns.
    - modeled as a directed graph.
- Develop an process that can:
    - when given a Chinese poem as an input,
    - find an optimized path stringing the characters together,
    - by moving from character to character via shared components and intermediate characters,
    - while:
        - using the fewest possible steps,
        - avoiding using the basic and compound strokes as components to link characters
        - with minimal duplication of characters.
- Present it as a hosted interactive web-app.

### the name rongzi

>熔字，róngzì  
[蓉子，Róngzì](https://yungtze.e-lib.nctu.edu.tw/index.htm)  
榕子，róngzi  
榮。róng  

>Molten words,  
[Yungtze](https://yungtze.e-lib.nctu.edu.tw/index.htm),  
a banyan seed,  
and honor.
