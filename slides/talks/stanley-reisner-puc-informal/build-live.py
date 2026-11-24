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
SLOTS = [
    {"title": "The link of a vertex", "rect": [0.01, 0.21, 0.98, 0.73], "model": "2d", "full": True},
    {"title": "M seen from a vertex", "rect": [0.01, 0.10, 0.98, 0.84], "model": "4d", "hash": "Mb", "full": True},
]
MODELS = {"2d": "from-a-vertex.html", "4d": "from-a-vertex-4d.html"}

EMBED_CSS = """<style id="embed">
h1,#info,.hint,aside,.fs,button.dk,nav.models,.steer,details{display:none!important}
html,body{height:100%;overflow:hidden;background:#fff}
.wrap{height:100%}
canvas{top:0;left:0;right:0;bottom:0}
</style>"""
EMBED_CSS_FULL = """<style id="embed">
h1,.fs,nav.models{display:none!important}
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
        page = next((i for i, t in enumerate(titles) if t and squash(t[0]).startswith(squash(s["title"]))), None)
        if page is None:
            missing.append(s["title"]); continue
        cfg = {"id": k, "click": s.get("click"), "spin": s.get("spin", False), "solo": s.get("solo", False), "full": s.get("full", False), "zoom": s.get("zoom"), "hash": s.get("hash")}
        models[k] = prepare(s["model"], cfg)
        slots.setdefault(page, []).append({"id": k, "rect": s["rect"], "full": bool(s.get("full"))})

    page = open(os.path.join(HERE, "live-template.html"), encoding="utf-8").read()
    rd = lambda f: open(os.path.join(HERE, "vendor", f), encoding="utf-8").read()
    pdfb64 = base64.b64encode(open(PDF, "rb").read()).decode()
    page = page.replace("/*PDFJS*/", rd("pdf.min.js").replace("</script", "<\\/script"))
    wk = "var WORKER=%s;\nvar PDFB64=\"%s\";\n" % (json.dumps(rd("pdf.worker.min.js")).replace("</", "<\\/"), pdfb64)
    data = (wk + "var IMGS=%s;\nvar ASPECT=%f;\nvar SLOTS=%s;\nvar MODELS=%s;\n" % (
        json.dumps(imgs), pw / float(ph), json.dumps(slots),
        json.dumps(models).replace("</", "<\\/")))
    open(OUT, "w", encoding="utf-8").write(page.replace("/*DATA*/", data))
    shutil.rmtree(tmp)
    print("%d pages, %d live slots, %.1f MB -> %s" % (n, sum(len(v) for v in slots.values()),
                                                   os.path.getsize(OUT) / 1e6, OUT))
    for m in missing:
        print("WARNING: no slide titled %r; its model is not placed" % m)


main()
