<div id="doc" class="markdown-body container-fluid comment-inner comment-enabled" data-hard-breaks="true">

# [<span class="octicon octicon-link"></span>](#Week-5---Distributed-Hash-Tables "Week-5---Distributed-Hash-Tables")<span>Week 5 - Distributed Hash Tables</span>

> <span>Distributed Systems and Network Programming - Spring 2023</span>

## [<span class="octicon octicon-link"></span>](#Overview "Overview")<span>Overview</span>

<span>Your task for this lab is to implement a simplified version of the</span> [<span>Chord</span>](https://en.wikipedia.org/wiki/Chord_(peer-to-peer)) <span>algorithm used to maintain a Distributed Hash Table (DHT) in peer-to-peer systems</span>

*   <span>DHT is a regular dictionary (HashMap) in which entries (i.e., keys and their corresponding values) are distributed over multiple nodes (peers) based on the consistent hash of the key</span>
*   <span>Nodes only support the two basic hash table operations:</span> `get(key)` <span>and</span> `put(key, value)`

## [<span class="octicon octicon-link"></span>](#System-Architecture "System-Architecture")<span>System Architecture</span>

<span>Chord operates over a structured P2P overlay network in which nodes (peers) are organized in a ring</span>

*   <span>Each node has an integer identifier:</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-1-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-1" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-2" class="mjx-mrow"><span id="MJXc-Node-3" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">n</span></span><span id="MJXc-Node-4" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.265em; padding-bottom: 0.37em;">∈</span></span><span id="MJXc-Node-5" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">[</span></span><span id="MJXc-Node-6" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.37em;">0</span></span><span id="MJXc-Node-7" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="margin-top: -0.155em; padding-bottom: 0.528em;">,</span></span><span id="MJXc-Node-8" class="mjx-msubsup MJXc-space1"><span class="mjx-base"><span id="MJXc-Node-9" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.318em;">2</span></span></span><span class="mjx-sup" style="font-size: 70.7%; vertical-align: 0.591em; padding-left: 0px; padding-right: 0.071em;"><span id="MJXc-Node-10" class="mjx-texatom" style=""><span id="MJXc-Node-11" class="mjx-mrow"><span id="MJXc-Node-12" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span></span></span></span></span><span id="MJXc-Node-13" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">)</span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>n</mi><mo>∈</mo><mo stretchy="false">[</mo><mn>0</mn><mo>,</mo><msup><mn>2</mn><mrow class="MJX-TeXAtom-ORD"><mi>M</mi></mrow></msup><mo stretchy="false">)</mo></math></span><mi>n</mi><mo>&amp;#x2208;</mo><mo stretchy=&quot;false&quot;>[</mo><mn>0</mn><mo>,</mo><msup><mn>2</mn><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>M</mi></mrow></msup><mo stretchy=&quot;false&quot;>)</mo></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-1">n \in [0, 2^{M})</script></span><span>, where</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-2-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-14" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-15" class="mjx-mrow"><span id="MJXc-Node-16" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>M</mi></math></span><mi>M</mi></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-2">M</script></span> <span>is the key-length in bits</span>
*   <span>Total number of nodes:</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-3-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-17" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-18" class="mjx-mrow"><span id="MJXc-Node-19" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.085em;">N</span></span><span id="MJXc-Node-20" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.475em;">≤</span></span><span id="MJXc-Node-21" class="mjx-msubsup MJXc-space3"><span class="mjx-base"><span id="MJXc-Node-22" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.318em;">2</span></span></span><span class="mjx-sup" style="font-size: 70.7%; vertical-align: 0.591em; padding-left: 0px; padding-right: 0.071em;"><span id="MJXc-Node-23" class="mjx-mi" style=""><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span></span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>N</mi><mo>≤</mo><msup><mn>2</mn><mi>M</mi></msup></math></span><mi>N</mi><mo>&amp;#x2264;</mo><msup><mn>2</mn><mi>M</mi></msup></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-3">N \leq 2^M</script></span>
*   <span>Each node should stay up-to-date about the current topology of the ring</span>
*   <span>Nodes communicate over the network using RPC</span>

### [<span class="octicon octicon-link"></span>](#Node "Node")<span>Node</span>

*   <span>Each node is responsible for storing values for keys in the range</span> `(predecessor_id, node_id]` <span>except the first node which stores values for keys in the range</span> `(predecessor_id, 2**M) U [0, node_id]`

*   <span>Each node maintains a</span> **<span>finger table</span>** <span>(i.e., a list of identifiers for some other nodes)</span>

    *   <span>A finger table contains</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-28-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-402" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-403" class="mjx-mrow"><span id="MJXc-Node-404" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>M</mi></math></span><mi>M</mi></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-28">M</script></span> <span>entries (repetitions are allowed)</span>

    *   <span>The value of the</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-29-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-405" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-406" class="mjx-mrow"><span id="MJXc-Node-407" class="mjx-msubsup"><span class="mjx-base"><span id="MJXc-Node-408" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.423em; padding-bottom: 0.265em;">i</span></span></span><span class="mjx-sup" style="font-size: 70.7%; vertical-align: 0.513em; padding-left: 0px; padding-right: 0.071em;"><span id="MJXc-Node-409" class="mjx-texatom" style=""><span id="MJXc-Node-410" class="mjx-mrow"><span id="MJXc-Node-411" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.423em; padding-bottom: 0.265em;">t</span></span><span id="MJXc-Node-412" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em;">h</span></span></span></span></span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>i</mi><mrow class="MJX-TeXAtom-ORD"><mi>t</mi><mi>h</mi></mrow></msup></math></span><msup><mi>i</mi><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>t</mi><mi>h</mi></mrow></msup></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-29">i^{th}</script></span> <span>element in the finger table for node</span> <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span id="MathJax-Element-30-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><span id="MJXc-Node-413" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-414" class="mjx-mrow"><span id="MJXc-Node-415" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">n</span></span></span></span><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>n</mi></math></span><mi>n</mi></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-30">n</script></span> <span>is defined as follows:</span>

        <span class="mathjax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="mjx-chtml MJXc-display" style="text-align: center;"><span id="MathJax-Element-31-Frame" class="mjx-chtml MathJax_CHTML" tabindex="0" style="font-size: 119%; text-align: center; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><span id="MJXc-Node-416" class="mjx-math" aria-hidden="true"><span id="MJXc-Node-417" class="mjx-mrow"><span id="MJXc-Node-418" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.106em;">F</span></span><span id="MJXc-Node-419" class="mjx-msubsup"><span class="mjx-base" style="margin-right: -0.12em;"><span id="MJXc-Node-420" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.12em;">T</span></span></span><span class="mjx-sub" style="font-size: 70.7%; vertical-align: -0.212em; padding-right: 0.071em;"><span id="MJXc-Node-421" class="mjx-texatom" style=""><span id="MJXc-Node-422" class="mjx-mrow"><span id="MJXc-Node-423" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">n</span></span></span></span></span></span><span id="MJXc-Node-424" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">[</span></span><span id="MJXc-Node-425" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.423em; padding-bottom: 0.265em;">i</span></span><span id="MJXc-Node-426" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">]</span></span><span id="MJXc-Node-427" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.055em; padding-bottom: 0.318em;">=</span></span><span id="MJXc-Node-428" class="mjx-mi MJXc-space3"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">s</span></span><span id="MJXc-Node-429" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">u</span></span><span id="MJXc-Node-430" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">c</span></span><span id="MJXc-Node-431" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">c</span></span><span id="MJXc-Node-432" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">e</span></span><span id="MJXc-Node-433" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">s</span></span><span id="MJXc-Node-434" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">s</span></span><span id="MJXc-Node-435" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">o</span></span><span id="MJXc-Node-436" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">r</span></span><span id="MJXc-Node-437" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">(</span></span><span id="MJXc-Node-438" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">(</span></span><span id="MJXc-Node-439" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.213em; padding-bottom: 0.265em;">n</span></span><span id="MJXc-Node-440" class="mjx-mo MJXc-space2"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.318em; padding-bottom: 0.423em;">+</span></span><span id="MJXc-Node-441" class="mjx-msubsup MJXc-space2"><span class="mjx-base"><span id="MJXc-Node-442" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.318em;">2</span></span></span><span class="mjx-sup" style="font-size: 70.7%; vertical-align: 0.591em; padding-left: 0px; padding-right: 0.071em;"><span id="MJXc-Node-443" class="mjx-texatom" style=""><span id="MJXc-Node-444" class="mjx-mrow"><span id="MJXc-Node-445" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.423em; padding-bottom: 0.265em;">i</span></span></span></span></span></span><span id="MJXc-Node-446" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">)</span></span><span id="MJXc-Node-447" class="mjx-TeXmathchoice"><span id="MJXc-Node-448" class="mjx-mspace" style="width: 1em; height: 0px;"></span></span><span id="MJXc-Node-449" class="mjx-mi MJXc-space1"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.423em; padding-bottom: 0.37em;">mod</span></span><span id="MJXc-Node-450" class="mjx-mspace" style="width: 0.167em; height: 0px;"></span><span id="MJXc-Node-451" class="mjx-mspace" style="width: 0.167em; height: 0px;"></span><span id="MJXc-Node-452" class="mjx-msubsup MJXc-space1"><span class="mjx-base"><span id="MJXc-Node-453" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.318em;">2</span></span></span><span class="mjx-sup" style="font-size: 70.7%; vertical-align: 0.591em; padding-left: 0px; padding-right: 0.071em;"><span id="MJXc-Node-454" class="mjx-mi" style=""><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span></span></span><span id="MJXc-Node-455" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">)</span></span><span id="MJXc-Node-456" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="margin-top: -0.155em; padding-bottom: 0.528em;">,</span></span><span id="MJXc-Node-457" class="mjx-mi MJXc-space1"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.423em; padding-bottom: 0.265em;">i</span></span><span id="MJXc-Node-458" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.265em; padding-bottom: 0.37em;">∈</span></span><span id="MJXc-Node-459" class="mjx-mo MJXc-space3"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">{</span></span><span id="MJXc-Node-460" class="mjx-mn"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.37em;">0..</span></span><span id="MJXc-Node-461" class="mjx-mi"><span class="mjx-char MJXc-TeX-math-I" style="padding-top: 0.475em; padding-bottom: 0.265em; padding-right: 0.081em;">M</span></span><span id="MJXc-Node-462" class="mjx-mo MJXc-space2"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.318em; padding-bottom: 0.423em;">−</span></span><span id="MJXc-Node-463" class="mjx-mn MJXc-space2"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.37em; padding-bottom: 0.318em;">1</span></span><span id="MJXc-Node-464" class="mjx-mo"><span class="mjx-char MJXc-TeX-main-R" style="padding-top: 0.475em; padding-bottom: 0.58em;">}</span></span></span></span><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>F</mi><msub><mi>T</mi><mrow class="MJX-TeXAtom-ORD"><mi>n</mi></mrow></msub><mo stretchy="false">[</mo><mi>i</mi><mo stretchy="false">]</mo><mo>=</mo><mi>s</mi><mi>u</mi><mi>c</mi><mi>c</mi><mi>e</mi><mi>s</mi><mi>s</mi><mi>o</mi><mi>r</mi><mo stretchy="false">(</mo><mo stretchy="false">(</mo><mi>n</mi><mo>+</mo><msup><mn>2</mn><mrow class="MJX-TeXAtom-ORD"><mi>i</mi></mrow></msup><mo stretchy="false">)</mo><mi>mod</mi><msup><mn>2</mn><mi>M</mi></msup><mo stretchy="false">)</mo><mo>,</mo><mi>i</mi><mo>∈</mo><mo fence="false" stretchy="false">{</mo><mn>0..</mn><mi>M</mi><mo>−</mo><mn>1</mn><mo fence="false" stretchy="false">}</mo></math></span><mi>F</mi><msub><mi>T</mi><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>n</mi></mrow></msub><mo stretchy=&quot;false&quot;>[</mo><mi>i</mi><mo stretchy=&quot;false&quot;>]</mo><mo>=</mo><mi>s</mi><mi>u</mi><mi>c</mi><mi>c</mi><mi>e</mi><mi>s</mi><mi>s</mi><mi>o</mi><mi>r</mi><mo stretchy=&quot;false&quot;>(</mo><mo stretchy=&quot;false&quot;>(</mo><mi>n</mi><mo>+</mo><msup><mn>2</mn><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>i</mi></mrow></msup><mo stretchy=&quot;false&quot;>)</mo><mspace width=&quot;1em&quot; /><mi>mod</mi><mspace width=&quot;thinmathspace&quot; /><mspace width=&quot;thinmathspace&quot; /><msup><mn>2</mn><mi>M</mi></msup><mo stretchy=&quot;false&quot;>)</mo><mo>,</mo><mi>i</mi><mo>&amp;#x2208;</mo><mo fence=&quot;false&quot; stretchy=&quot;false&quot;>{</mo><mn>0..</mn><mi>M</mi><mo>&amp;#x2212;</mo><mn>1</mn><mo fence=&quot;false&quot; stretchy=&quot;false&quot;>}</mo></math>" role="presentation"></span></span> <script type="math/tex; mode=display" id="MathJax-Element-31">FT_{n}[i] = successor((n + 2^{i}) \mod 2^M), i \in \{0..M-1\}</script></span>

    *   <span>Successor function returns the identifier of the next online node in the ring (clockwise direction).</span>

    *   <span>Finger tables are used by the Chord algorithm to achieve a logarithmic search time. They are the reason behind Chord scalability.</span>

*   <span>Chord algorithm relies on two functions (</span>`find_successor` <span>and</span> `closest_preceding_node`<span>) to determine in which node should an entry (key-value pair) reside. The pseudo-code for these functions is given below:</span>

        # Recursive function returning the identifier of the node responsible for a given id
        n.find_successor(id):
          if id == n.id:
              return id

          # Note the half-open interval and that L <= R does not necessarily hold
          if id ∈ (n.id, n.successor_id] then
              return n.successor_id

          # Forward the query to the closest preceding node in the finger table for n
          n0 := closest_preceding_node(id)
          return n0.find_successor(id)

        # Returns the closest preceeding node (from n.finger_table) for a given id
        n.closest_preceding_node(id):
          # Note the full-open interval and that L <= R does not necessarily hold
          for i = m downto 1 do
              if finger[i].id ∈ (n.id, id) then
                  return finger[i]
          return n

### [<span class="octicon octicon-link"></span>](#Client "Client")<span>Client</span>

*   <span>The client provided uses</span> [<span>xmlrpc</span>](https://docs.python.org/3/library/xmlrpc.html) <span>to:</span>

    *   <span>Call a random node over RPC, the node should be ready and listening</span>
    *   <span>Ask the node to insert an entry into the chord</span>
    *   <span>Then execute some lookup operations</span>
        *   <span>Lookup operation asks a certain node about the value for a certain key</span>
*   <span>For the node to answer a request, it may contact other nodes as explained above</span>

    *   **<span>For</span> `put` <span>queries:</span>** <span>return</span> `True` <span>on successful insertion and</span> `False` <span>otherwise</span>
    *   **<span>For</span> `get` <span>queries:</span>**
        *   <span>If the value for the given key is found, return that value</span>
        *   <span>If the value is not found, return</span> `-1`

## [<span class="octicon octicon-link"></span>](#Task "Task")<span>Task</span>

*   <span>Implement the Node class as explained above. The boilerplate is given in</span> `node.py`
    *   <span>Parse one integer argument (</span>`node_id`<span>)</span>
    *   <span>Create a Node instance and register its methods for calling over XML-RPC</span>
    *   <span>Run XML-RPC server on</span> [<span>http://0.0.0.0:1234</span>](http://0.0.0.0:1234)
    *   <span>Write implementation for</span> `find_successor` <span>and</span> `closest_preceding_node` <span>according to the provided pseudo-code</span>
    *   <span>Write the logic for</span> `n.get(key)` <span>and</span> `n.put(key, value)` <span>to insert and retrieve data from the Chord</span>
*   <span>Test your code using docker as explained below.</span> **<span>Code which does not work will receive 0 grade</span>**
*   <span>Submit a single file</span> `node_NameSurname.py`

## [<span class="octicon octicon-link"></span>](#Example-Run "Example-Run")<span>Example Run</span>

### [<span class="octicon octicon-link"></span>](#Input "Input")<span>Input</span>

*   <span>We have prepared an example ring of 6 nodes and the required docker files to run all such nodes in one network, nodes are reachable from each other by their hostname (e.g.,</span> `http://node_22:1234`<span>)</span>

*   <span>An example client is also provided (</span>`client.py`<span>). The client runs in the same network with nodes and contacts random nodes from the ring, asking them to insert data into the Chord</span>

    *   <span>Overall, the client inserts 32 key-value pairs (i.e.,</span> `(0, "value_0")` <span>up to</span> `(31, "value_31")`<span>)</span>
*   <span>To run the example, execute the following command in the project directory</span>

        docker-compose build --no-cache && docker-compose up

*   <span>Note that your code will be tested on different rings, a correct implementation should always work</span>

### [<span class="octicon octicon-link"></span>](#Output "Output")<span>Output</span>

*   <span>The output shows how lookup queries are routed through the ring, the routing order is deterministic.</span>

*   <span>For simplicity, the Chord does not have any data stored in this run (that is why</span> `-1` <span>is returned)</span>

*   <span>The</span> `client.py` <span>provided should result in more output as</span> `put` <span>requests are routed between nodes.</span> `get` <span>requests should then return the expected values (i.e.,</span> `lookup(N, X) = "value_X"`<span>)</span>

    ![output](https://i.imgur.com/oQwlFla.png)

### [<span class="octicon octicon-link"></span>](#Visualization "Visualization")<span>Visualization</span>

*   <span>You can use</span> [<span>Chordgen</span>](https://msindwan.github.io/chordgen/) <span>to visualize test cases and verify finger tables and lookup order</span>
*   <span>The following diagram shows the given example ring and data allocation</span>  
    ![example](https://i.imgur.com/0vQxm0W.png)

## [<span class="octicon octicon-link"></span>](#Checklist "Checklist")<span>Checklist</span>

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>A single submitted file (</span>`node_NameSurname.py`<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code is formatted and does not use any external dependencies</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Logging shows the finger table for each node</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Logging shows which node functions were called over RPC and how the request was routed (see example output above)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The system provides the correct output for</span> **<span>the given example</span>** <span>ring and lookup queries</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The system provides the correct output for</span> **<span>a different</span>** <span>ring and lookup queries</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code is the author’s original work. Both parties will be penalized for detected plagiarism</span>

## [<span class="octicon octicon-link"></span>](#Additional-Notes "Additional-Notes")<span>Additional Notes</span>

*   <span>Chord is quite a complex protocol, you can find the original implementation</span> [<span>here</span>](https://github.com/sit/dht)
*   <span>The following simplifications were made to adjust the complexity of the task:</span>
    *   <span>Each node is initialized with knowledge about other nodes in the ring, removing the need to implement notification procedures</span>
    *   <span>The system topology is fixed, removing the need to implement procedures for stabilization, node joining/exiting and finger table updates</span>
    *   <span>A client is provided to test the system. In real-world scenarios, that client is typically a node as well</span>
*   <span>In real-world implementations, the Chord and its finger tables should update dynamically as nodes enter and exit the system. Periodical stabilization procedures are also used to ensure that nodes stay up-to-date with the current topology of the ring</span>

</div>

<div class="ui-toc dropup unselectable hidden-print" style="display:none;">

<div class="pull-right dropdown">[](# "Table of content")

<div class="toc">

- [Week 5 - Distributed Hash Tables](#week-5---distributed-hash-tables)
  - [Overview](#overview)
  - [System Architecture](#system-architecture)
    - [Node](#node)
    - [Client](#client)
  - [Task](#task)
  - [Example Run](#example-run)
    - [Input](#input)
    - [Output](#output)
    - [Visualization](#visualization)
  - [Checklist](#checklist)
  - [Additional Notes](#additional-notes)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

</div>

<div id="ui-toc-affix" class="ui-affix-toc ui-toc-dropdown unselectable hidden-print" data-spy="affix" style="top:17px;display:none;" null="">

<div class="toc">

- [Week 5 - Distributed Hash Tables](#week-5---distributed-hash-tables)
  - [Overview](#overview)
  - [System Architecture](#system-architecture)
    - [Node](#node)
    - [Client](#client)
  - [Task](#task)
  - [Example Run](#example-run)
    - [Input](#input)
    - [Output](#output)
    - [Visualization](#visualization)
  - [Checklist](#checklist)
  - [Additional Notes](#additional-notes)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

<script>var markdown = $(".markdown-body"); //smooth all hash trigger scrolling function smoothHashScroll() { var hashElements = $("a[href^='#']").toArray(); for (var i = 0; i < hashElements.length; i++) { var element = hashElements[i]; var $element = $(element); var hash = element.hash; if (hash) { $element.on('click', function (e) { // store hash var hash = this.hash; if ($(hash).length <= 0) return; // prevent default anchor click behavior e.preventDefault(); // animate $('body, html').stop(true, true).animate({ scrollTop: $(hash).offset().top }, 100, "linear", function () { // when done, add hash to url // (default click behaviour) window.location.hash = hash; }); }); } } } smoothHashScroll(); var toc = $('.ui-toc'); var tocAffix = $('.ui-affix-toc'); var tocDropdown = $('.ui-toc-dropdown'); //toc tocDropdown.click(function (e) { e.stopPropagation(); }); var enoughForAffixToc = true; function generateScrollspy() { $(document.body).scrollspy({ target: '' }); $(document.body).scrollspy('refresh'); if (enoughForAffixToc) { toc.hide(); tocAffix.show(); } else { tocAffix.hide(); toc.show(); } $(document.body).scroll(); } function windowResize() { //toc right var paddingRight = parseFloat(markdown.css('padding-right')); var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight)); toc.css('right', right + 'px'); //affix toc left var newbool; var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth()) / 2; //for ipad or wider device if (rightMargin >= 133) { newbool = true; var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2; var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin; tocAffix.css('left', left + 'px'); } else { newbool = false; } if (newbool != enoughForAffixToc) { enoughForAffixToc = newbool; generateScrollspy(); } } $(window).resize(function () { windowResize(); }); $(document).ready(function () { windowResize(); generateScrollspy(); }); //remove hash function removeHash() { window.location.hash = ''; } var backtotop = $('.back-to-top'); var gotobottom = $('.go-to-bottom'); backtotop.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToTop) scrollToTop(); removeHash(); }); gotobottom.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToBottom) scrollToBottom(); removeHash(); }); var toggle = $('.expand-toggle'); var tocExpand = false; checkExpandToggle(); toggle.click(function (e) { e.preventDefault(); e.stopPropagation(); tocExpand = !tocExpand; checkExpandToggle(); }) function checkExpandToggle () { var toc = $('.ui-toc-dropdown .toc'); var toggle = $('.expand-toggle'); if (!tocExpand) { toc.removeClass('expand'); toggle.text('Expand all'); } else { toc.addClass('expand'); toggle.text('Collapse all'); } } function scrollToTop() { $('body, html').stop(true, true).animate({ scrollTop: 0 }, 100, "linear"); } function scrollToBottom() { $('body, html').stop(true, true).animate({ scrollTop: $(document.body)[0].scrollHeight }, 100, "linear"); }</script>