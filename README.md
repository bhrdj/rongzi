# rongzi
Input Chinese characters, and the application will find optimized component-paths connecting them. It's like melting a word. Or traversing a banyan grove by following branches between prop-trunks.  
With appreciation and respect for the late poet Yungtze (1922-2021).

## input: ่ ๆฆฎ
## output: ่๐กๅฎน๐กๆฆ๐กๆจ๐กๆฆฎ

---

### Link to streamlit demonstration webapp:
<font size="6"><a href="http://rongzi.bhrdwj.net">http://rongzi.bhrdwj.net</a></font>

 

### Usage:

##### Simply connect the characters of a poem:

```Python
    import rongzi
    rz = rongzi.RongZi()
    df = rz.analyze_sequence('ๆฐธ้ ็้้ณฅ')
    print(df.to_markdown())
```

|    | ๆฐธ้            | ้ ็           | ็้         | ้้ณฅ       |
|---:|:---------------|:---------------|:-------------|:-----------|
|  0 | ๆฐธๆ ๆจๆฆฌ่ข้    | ้ ่ณ่น่็     | ็็ฝ็้     | ้้ถ้ณฅ     |
|  1 | ๆฐธๆฐด้้้ง้    | ้ ่พถ่ฟซ็ฝ็     | ็็ฝ่ๆ้   | ้่่ณ้ต้ณฅ |
|  2 | ๆฐธ่ฉ ่จ่ชพ้้ง้  | ้ ่ข้ฑ้้็ฝ็ | ็็ฝๆฅๆด้   | ้้้้ตญ้ณฅ |
|  3 | ๆฐธ่ฉ ่จ้่พถ้    | ้ ่ข่คค่กค่ข็ฝ็ | ็็ฝ้ฒ้ฑผ้ฒญ้ | ้้็ซ้ด้ณฅ |
|  4 | ๆฐธๆณณๆฐตๆบ่ข้    | ้ ่ข๐ ฎทๅฃๅฒ็   | ็็ฝ้้้้ | ้้ฏ้ญ้ท ้ณฅ |


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

>็ๅญ๏ผrรณngzรฌ  
[่ๅญ๏ผRรณngzi](https://yungtze.e-lib.nctu.edu.tw/index.htm)  
ๆฆๅญ๏ผrรณngzi  
ๆฆฎใrรณng  

>Molten words,  
[Yungtze](https://yungtze.e-lib.nctu.edu.tw/index.htm),  
a banyan seed,  
and honor.

### TODO:
- Refactor (ccd, pdb, kdb) as class property methods:
    - https://stackoverflow.com/questions/128573/using-property-on-classmethods
- Allow to choose between CJK languages/scripts (CH, JA, TW)
- Create CICD pipeline using github actions.
- Dockerize application
