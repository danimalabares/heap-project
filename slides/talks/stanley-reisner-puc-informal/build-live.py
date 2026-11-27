#!/usr/bin/env python3
"""Build live.html: the beamer PDF as a slideshow, with live models on the
vertex-figure slides. Usage: python3 build-live.py [deck.pdf]

Run it again after every change to the slides. Slides are found by the first
line of their text, not by page number, so reordering is safe (see SLOTS).
Needs: gs (Ghostscript), python3. Optional: node + npx esbuild (lowers the
model scripts for old browsers).
"""
import base64, json, os, re, subprocess, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/github/heap-slides-sr/build/stanley-reisner-puc-informal-v2.pdf")
OUT = os.path.join(HERE, "live.html")
DPI = 200            # about 1300 px wide for a 16:9 beamer page

# Live models. title: start of the slide's first text line. rect: left, top,
# width, height as fractions of the page. model: "2d" or "4d".
# hash: for 4d, the sphere (#Mb = M seen from b). click: text of a button to press.
# spin: turn slowly at start (4d only).
# auto: the model plays by itself (window.AUTO in the model): seq is played in a loop, extra can only be chosen;
# all the controls are hidden except one small row of names.
SLOTS = [
    {"title": "The link of a vertex", "rect": [0.01, 0.193, 0.98, 0.747], "model": "2d", "auto": {
        "end": "Turned so that <i>v</i> points at us: this is the picture on the left.",
        "seq": [
            {"key": "octa", "label": "octahedron", "cap": "The octahedron. In green: a vertex <i>v</i>. Thick: the link of <i>v</i>, a square."},
            {"key": "bip5", "vi": 2, "label": "double pyramid", "cap": "A double pyramid over a pentagon: not regular. Thick: the link of <i>v</i>, a square."},
        ],
        # not played by themselves: the two links drawn on the next slide, each seen from the vertex that sits in the dent there
        "extra": [
            {"key": "linkb", "vi": 0, "label": "link of <i>b</i> in <i>M</i>",
             "cap": "The link of <i>b</i> in <i>M</i>, seen from its vertex <i>a</i>. Thick: the link of <i>a</i> in it, a triangle."},
            {"key": "barn1", "vi": 4, "label": "link of 1 in Barnette",
             "cap": "The link of 1 in Barnette's sphere, seen from its vertex 6. Thick: the link of 6 in it, a triangle."},
        ]}},
    {"title": "The same for a 3-sphere", "rect": [0.03, 0.17, 0.32, 0.41], "model": "tets"},
    {"title": "M seen from a vertex", "rect": [0.01, 0.10, 0.98, 0.855], "model": "4d", "auto": {
        "seq": [
            {"key": "5", "label": "5-cell", "cap": "The 5-cell, seen from a vertex <i>v</i>. Thick: the link of <i>v</i>, a tetrahedron."},
            {"key": "16", "label": "16-cell", "cap": "The 16-cell, seen from a vertex <i>v</i>. Thick: the link of <i>v</i>, an octahedron."},
            {"key": "M", "label": "<i>M</i>", "cap": "<i>M</i>, seen from the vertex <i>b</i>. Thick: the link of <i>b</i>, a 2-sphere with 7 vertices."},
        ],
        "extra": [
            {"key": "B", "vi": 0, "label": "Barnette",      # vi 0 is the vertex 1 (vi 6 is the vertex 7, whose link is an octahedron)
             "cap": "Barnette's sphere, seen from the vertex 1. Thick: the link of 1, a 2-sphere with 7 vertices."},
        ]}},
    # only the symmetry of order three, a true rotation of the picture from d; the three of order two have no such picture
    {"title": "Figure for",
     "rect": [0.47, 0.095, 0.52, 0.76], "model": "sym", "hash": "rot", "auto": {
        "seq": [{"key": "rot", "label": "&sigma;&tau; from <i>d</i>", "cap": "<i>M</i> seen from <i>d</i>. Thick: the link of <i>d</i>. Dotted: the axis.", "capm": "&sigma;&tau; = (a g c)(b e h): a third of a turn about the axis.", "cap2": "Again <i>M</i> seen from <i>d</i>: &sigma;&tau; keeps <i>d</i> and its link."}],
        "extra": []}},
]
MODELS = {"2d": "from-a-vertex.html", "4d": "from-a-vertex-4d.html", "tets": "two-tetrahedra.html", "sym": "symmetries-of-m.html"}

EMBED_CSS = """<style id="embed">
h1,#info,.hint,aside,.fs,.tb,.dk,nav.models,.steer,details{display:none!important}
html,body{height:100%;overflow:hidden;background:#fff}
.wrap{height:100%}
#stage{min-height:0!important}
canvas{top:0;left:0;right:0;bottom:0}
</style>"""
EMBED_CSS_FULL = """<style id="embed">
h1,.fs,.tb,nav.models{display:none!important}
html,body{height:100%;overflow:hidden;background:#fff}
.wrap{height:100%}
#stage{min-height:110px}
aside{max-height:52%}
#grip{flex:0 0 16px;position:relative;background:var(--panel);border-top:1px solid var(--line);cursor:ns-resize;touch-action:none;-webkit-user-select:none;user-select:none}
#grip:before{content:"";position:absolute;left:50%;top:6px;width:44px;margin-left:-22px;border-top:3px double var(--mute)}
#grip button{position:absolute;right:8px;top:0;margin:0;padding:0 7px;font-size:11px;line-height:13px;cursor:pointer}
#grip + aside{border-top:0}
canvas{top:0;left:0;right:0;bottom:0}
#info{top:6px!important;right:200px!important}
.hint{display:none}
</style>"""
EMBED_JS = """<script>
(function(){
  var cfg = %s;
  function go(){
    try{
      if(cfg.solo){window.SOLO=true;}
      if(cfg.click){var b=document.querySelectorAll("button,a.btn");
        for(var i=0;i<b.length;i++){if((b[i].textContent||"").replace(/\\s+/g," ").indexOf(cfg.click)>=0){b[i].click();break;}}}
      if(cfg.spin){var s=document.getElementById("spin"); if(s){s.checked=true;}}
      if(cfg.zoom){var z=document.getElementById("zoom"); if(z){z.value=cfg.zoom; z.dispatchEvent(new Event("input"));}}
      var cv=document.getElementById("cv"), box=document.getElementById("spin"), on=false;
      function loop(){ if(on){ try{ if(!drag){ R3=mul(rotY(0.006),R3); draw(); } }catch(e){} requestAnimationFrame(loop);} }
      if(cv){ cv.addEventListener("dblclick",function(){
        if(box){ box.checked=!box.checked; }
        else { on=!on; if(on){ loop(); } } }); }
      if(cfg.full){ (function(){
        // A bar between the picture and the controls: drag it to resize the controls, button to hide them.
        var as=document.querySelector("aside"); if(!as){return;}
        var g=document.createElement("div"), hb=document.createElement("button"), y0=null, h0=0, key="live-controls-"+cfg.id;
        g.id="grip"; g.title="Drag up or down to resize the controls"; hb.textContent="hide controls"; g.appendChild(hb);
        as.parentNode.insertBefore(g,as);
        function relayout(){ window.dispatchEvent(new Event("resize")); }
        function save(){ try{ localStorage.setItem(key, JSON.stringify({h:as.style.height||"", off:as.style.display==="none"})); }catch(e){} }
        function setH(h){ var max=(window.innerHeight||400)-56; if(h<24){h=24;} if(h>max){h=max;}
          as.style.maxHeight="none"; as.style.height=h+"px"; relayout(); }
        function setOff(off){ as.style.display=off?"none":""; hb.textContent=off?"show controls":"hide controls"; relayout(); }
        function down(y){ if(as.style.display==="none"){return;} y0=y; h0=as.getBoundingClientRect().height; }
        function move(y){ if(y0!==null){ setH(h0+(y0-y)); } }
        function up(){ if(y0!==null){ y0=null; save(); } }
        g.addEventListener("mousedown",function(e){ if(e.target===hb){return;} down(e.clientY); e.preventDefault(); });
        window.addEventListener("mousemove",function(e){ move(e.clientY); });
        window.addEventListener("mouseup",up);
        document.addEventListener("mouseleave",up);
        g.addEventListener("touchstart",function(e){ if(e.target===hb){return;} down(e.touches[0].clientY); e.preventDefault(); });
        window.addEventListener("touchmove",function(e){ move(e.touches[0].clientY); });
        window.addEventListener("touchend",up);
        hb.addEventListener("click",function(e){ e.stopPropagation(); setOff(as.style.display!=="none"); save(); });
        try{ var st=JSON.parse(localStorage.getItem(key)||"null");
          if(st){ if(st.h){ as.style.maxHeight="none"; as.style.height=st.h; } if(st.off){ setOff(true); } } }catch(e){}
      })(); }
      window.dispatchEvent(new Event("resize"));
    }catch(e){}
    setTimeout(function(){try{parent.postMessage("live-ready:"+cfg.id,"*");}catch(e){}},250);
  }
  if(document.readyState==="complete"){go();}else{window.addEventListener("load",go);}
})();
</script>"""


def squash(x):
    return re.sub(r"\s", "", x)


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def pages_text(tmp):
    txt = os.path.join(tmp, "t%03d.txt")
    subprocess.run(["gs", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=txtwrite",
                    "-sOutputFile=" + txt, PDF], check=True, capture_output=True)
    out, i = [], 1
    while os.path.exists(txt % i):
        raw = open(txt % i, encoding="utf-8", errors="replace").read()
        lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines() if l.strip()]
        out.append(lines[:2])
        i += 1
    return out


def detex(t):
    """A frame title as plain text."""
    t = re.sub(r"\\cite\{([^}]*)\}", r"[\1]", t)
    t = t.replace("\\mathcal M", "M").replace("\\Pj", "P").replace("\\C", "C").replace("\\ne", "≠").replace("\\sigma", "σ").replace("\\tau", "τ")
    t = re.sub(r"\\operatorname\{([^}]*)\}", r"\1 ", t)
    sup = {"2": "²", "3": "³", "7": "⁷"}
    t = re.sub(r"\^(\d)", lambda m: sup.get(m.group(1), "^" + m.group(1)), t)
    t = re.sub(r"_(\d)", lambda m: chr(0x2080 + int(m.group(1))), t)
    t = t.replace("\\(", "").replace("\\)", "").replace("\\ ", " ").replace("\\,", "").replace("--", "–")
    t = re.sub(r"\\[a-zA-Z]+", "", t).replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", t).strip()


def toc(titles):
    """One entry per page: [text, is_part]. Titles are read from the TeX source (the text drawn from the
    PDF loses spaces and ligatures) and matched to the pages in order; a page without a match keeps the PDF's text."""
    import difflib
    src = []
    tex = os.path.join(HERE, os.path.splitext(os.path.basename(PDF))[0] + ".tex")
    if os.path.exists(tex):
        body = open(tex, encoding="utf-8").read().split("\\begin{document}", 1)[-1].split("\\end{document}")[0]
        body = re.sub(r"\\iffalse.*?\\fi\b", "", body, flags=re.S)
        body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))
        for m in re.finditer(r"\\partslide\{(\d+)\}\{((?:[^{}]|\{[^{}]*\})*)\}|\\begin\{frame\}(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            if m.group(1):
                src.append(("Part %s. %s" % (m.group(1), detex(m.group(2))), True, "Part" + m.group(1)))
            else:
                src.append((detex(m.group(3)), False, detex(m.group(3))))
    out, j = [], 0
    fix = lambda x: x.replace("昀椀", "fi").replace("昀氀", "fl")
    for t in titles:
        got = fix(t[0]) if t else ""
        hit = None
        for line in t[:2]:      # a superscript in the title can come out as a line of its own, before the title
            for k in range(j, min(j + 4, len(src))):
                a, b = squash(fix(line)).lower(), squash(src[k][2]).lower()
                if a and b and (a.startswith(b) or difflib.SequenceMatcher(None, a, b).ratio() > 0.6):
                    hit = k; break
            if hit is not None:
                break
        if hit is None:
            out.append([got, False])
        else:
            out.append([src[hit][0], src[hit][1]]); j = hit + 1
    if out and os.path.exists(tex):
        m = re.search(r"\\title\{((?:[^{}]|\{[^{}]*\})*)\}", open(tex, encoding="utf-8").read())
        if m:
            out[0][0] = detex(m.group(1))
    return out


def lower(js):
    """Lower modern syntax (??, ?., ...) for old browsers with esbuild, if present."""
    exe = os.environ.get("ESBUILD") or shutil.which("esbuild")
    if not exe:
        print("note: esbuild not found; model scripts not lowered for old browsers")
        return js
    try:
        r = subprocess.run([exe, "--target=chrome49,firefox52,safari10,edge14"],
                           input=js, capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    except Exception:
        pass
    return js


def prepare(model, cfg):
    full = cfg.get("full")
    html = open(os.path.join(HERE, MODELS[model]), encoding="utf-8").read()
    html = html.replace("inset:0", "top:0;left:0;right:0;bottom:0")
    def low(m):
        return m.group(1) + lower(m.group(2)) + m.group(3)
    html = re.sub(r"(<script>)(.*?)(</script>)", low, html, flags=re.S)
    if not full:
        html = html.replace("box = Math.min(W/2, H-70), cy = (H+30)/2", "box = Math.min(window.SOLO ? W : W/2, H-4), cy = H/2")
        html = html.replace("H/2+18 -", "H/2 -")
    html = html.replace("ctx.rect(0,0,W/2,H); ctx.clip();", "ctx.rect(0,0,window.SOLO ? 0 : W/2,H); ctx.clip();")
    html = html.replace("3*W/4 + (R3", "(window.SOLO ? W/2 : 3*W/4) + (R3")
    html = html.replace("</head>", (EMBED_CSS_FULL if full else EMBED_CSS) + "</head>", 1)
    html = html.replace("</body>", (EMBED_JS % json.dumps(cfg)) + "</body>", 1)
    if cfg.get("auto"):
        html = html.replace("<script>", "<script>window.AUTO=%s;</script><script>" % json.dumps(cfg["auto"]).replace("</", "<\\/"), 1)
    if cfg.get("hash"):
        html = html.replace("location.hash", '"#%s"' % cfg["hash"])
    return html


def main():
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, "p%03d.png")
    subprocess.run(["gs", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png256", "-r%d" % DPI,
                    "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sOutputFile=" + png, PDF],
                   check=True, capture_output=True)
    titles = pages_text(tmp)
    n = len(titles)
    imgs = []
    for i in range(1, n + 1):
        imgs.append("data:image/png;base64," + base64.b64encode(open(png % i, "rb").read()).decode())
    w, h = 16, 9
    with open(png % 1, "rb") as f:
        head = f.read(24)
    pw, ph = int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")

    slots, models, missing = {}, {}, []
    for k, s in enumerate(SLOTS):
        page = next((i for i, t in enumerate(titles) if t and (squash(t[0]).endswith(squash(s["title"])) if s.get("tail") else squash(t[0]).startswith(squash(s["title"])))), None)
        if page is None:
            missing.append(s["title"]); continue
        cfg = {"id": k, "auto": s.get("auto"), "click": s.get("click"), "spin": s.get("spin", False), "solo": s.get("solo", False), "full": s.get("full", False), "zoom": s.get("zoom"), "hash": s.get("hash")}
        models[k] = prepare(s["model"], cfg)
        slots.setdefault(page, []).append({"id": k, "rect": s["rect"], "full": bool(s.get("full")), "auto": bool(s.get("auto"))})

    page = open(os.path.join(HERE, "live-template.html"), encoding="utf-8").read()
    rd = lambda f: open(os.path.join(HERE, "vendor", f), encoding="utf-8").read()
    pdfb64 = base64.b64encode(open(PDF, "rb").read()).decode()
    page = page.replace("/*PDFJS*/", rd("pdf.min.js").replace("</script", "<\\/script"))
    wk = "var WORKER=%s;\nvar PDFB64=\"%s\";\n" % (json.dumps(rd("pdf.worker.min.js")).replace("</", "<\\/"), pdfb64)
    data = (wk + "var TOC=%s;\n" % json.dumps(toc(titles)) + "var IMGS=%s;\nvar ASPECT=%f;\nvar SLOTS=%s;\nvar MODELS=%s;\n" % (
        json.dumps(imgs), pw / float(ph), json.dumps(slots),
        json.dumps(models).replace("</", "<\\/")))
    open(OUT, "w", encoding="utf-8").write(page.replace("/*DATA*/", data))
    shutil.rmtree(tmp)
    print("%d pages, %d live slots, %.1f MB -> %s" % (n, sum(len(v) for v in slots.values()),
                                                   os.path.getsize(OUT) / 1e6, OUT))
    for m in missing:
        print("WARNING: no slide titled %r; its model is not placed" % m)


main()
