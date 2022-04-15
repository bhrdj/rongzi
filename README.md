# rongzi
Supply Chinese characters, and the application will find optimized component-paths connecting them.  
Like melting a word. Or traversing a banyan grove by following branches between prop-trunks.  
With appreciation and respect for the late poet Yungtze (1922-2021).

## input: ```蓉 榮```
## output: ```蓉 容 榕 木 榮```

---

### Demonstration webapp:
(Link to Streamlit webapp forthcoming.)

### Usage:

##### Simply connect the characters of a poem:

```Python
    import rongzi
    rz = rongzi.RongZi()
    df = rz.analyze_sequence('永遠的青鳥')
    print(df.to_markdown())
```

|    | 永遠           | 遠的           | 的青         | 青鳥       |
|---:|:---------------|:---------------|:-------------|:-----------|
|  0 | 永栐木榬袁遠   | 遠薳艹菂的     | 的白皘青     | 青鶄鳥     |
|  1 | 永水閖門闧遠   | 遠辶迫白的     | 的白胉月青   | 青聙耳鵈鳥 |
|  2 | 永詠言誾門闧遠 | 遠袁鎱金鉑白的 | 的白日晴青   | 青錆金鵭鳥 |
|  3 | 永詠言這辶遠   | 遠袁褤衤袙白的 | 的白鲌鱼鲭青 | 青靖立鴗鳥 |
|  4 | 永泳氵溒袁遠   | 遠袁𠮷口啲的   | 的白鉑金錆青 | 青鯖魚鷠鳥 |


### Installation and dependencies:
- For basic usage rongzi requires:
    - ```python``` version 3.9 or newer.
    - Third-party libraries ```pandas``` (1.3.4 or newer), and ```numpy```.
- For graph visualization rongzi additionally needs:
    - ```graphviz```
    - (Sometimes graphviz may be a trickier install, so I split this functionality out into a separate library, starting with the streamlit app app.py.)

### Challenge specification:
- Query the [CCD](https://commons.wikimedia.org/wiki/Commons:Chinese_characters_decomposition) database of Chinese character radical breakdowns,
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

### The name "rongzi"

>熔字，róngzì  
[蓉子，Róngzi](https://yungtze.e-lib.nctu.edu.tw/index.htm)  
榕子，róngzi  
榮。róng  

>Molten words,  
[Yungtze](https://yungtze.e-lib.nctu.edu.tw/index.htm),  
a banyan seed,  
and honor.

### TODO:
- Refactor (ccd, pdb, kdb) as class property methods:
    - https://stackoverflow.com/questions/128573/using-property-on-classmethods
- Allow to choose between CJK languages/scripts (CH, JA, TW)