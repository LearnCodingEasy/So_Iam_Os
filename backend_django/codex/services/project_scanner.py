from pathlib import Path
import hashlib
from django.conf import settings
from django.urls import get_resolver
from ..models import ProjectRegistry,Feature,FileRegistry,APIEndpoint,ProtectedFeature

EXCLUDED={".git","node_modules","__pycache__",".venv","venv","dist","coverage"}

class ProjectScanner:
    def __init__(self, project=None):
        self.project=project or ProjectRegistry.objects.get_or_create(key="so_iam_os",defaults={"name":"SO_IAM_OS"})[0]
        self.root=Path(settings.BASE_DIR).parent
    def scan_files(self):
        seen=set(); count=0
        for p in self.root.rglob("*"):
            if not p.is_file() or any(part in EXCLUDED for part in p.parts): continue
            rel=str(p.relative_to(self.root)).replace("\\","/")
            if rel.startswith(".env") or rel.endswith(".pyc"): continue
            try: data=p.read_bytes(); size=len(data); digest=hashlib.sha256(data).hexdigest()
            except OSError: continue
            ext=p.suffix.lower(); kind={".py":"python",".js":"javascript",".vue":"vue",".json":"json",".md":"markdown",".css":"css",".scss":"scss"}.get(ext,"other")
            app=rel.split("/")[1] if rel.startswith("backend_django/") and len(rel.split("/"))>1 else ""
            FileRegistry.objects.update_or_create(project=self.project,path=rel,defaults={"kind":kind,"app_label":app,"sha256":digest,"size":size})
            seen.add(rel); count+=1
        FileRegistry.objects.filter(project=self.project).exclude(path__in=seen).delete()
        return count
    def scan_features(self):
        backend=Path(settings.BASE_DIR)
        apps=[]
        for p in backend.iterdir():
            if p.is_dir() and (p/"apps.py").exists() and p.name not in {"backend_django","media"}: apps.append(p.name)
        for app in apps:
            key=f"app:{app}"; obj,_=Feature.objects.update_or_create(project=self.project,key=key,defaults={"name":app.replace("_"," ").title(),"app_label":app,"status":"active"})
            protected=ProtectedFeature.objects.filter(project=self.project,key=key).exists()
            obj.protected=protected; obj.save(update_fields=["protected"])
        return len(apps)
    def scan_apis(self):
        # Central registry guarantees a frontend place even when a domain page is not yet specialized.
        resolver=get_resolver(); rows=[]
        def walk(patterns,prefix=""):
            for pat in patterns:
                route=str(getattr(pat,"pattern",pat.pattern)).lstrip("^")
                full=(prefix+route).replace("$","")
                if hasattr(pat,"url_patterns"):
                    walk(pat.url_patterns,full)
                    continue
                callback=getattr(pat,"callback",None); name=getattr(pat,"name","") or ""
                if not full.startswith("api/"): continue
                method="ANY"
                view_class=getattr(callback,"view_class",None)
                if view_class and hasattr(view_class,"http_method_names"):
                    method=",".join(m.upper() for m in view_class.http_method_names if m not in {"options","head"})
                source=getattr(callback,"__module__","")
                app=source.split(".")[0] if source else ""
                rows.append((method,"/"+full,name,source,app))
        walk(resolver.url_patterns)
        for method,path,name,source,app in rows:
            APIEndpoint.objects.update_or_create(project=self.project,method=method,path=path,name=name,defaults={"source":source,"app_label":app,"frontend_route":"/codex","frontend_section":"API Registry","frontend_service":app,"coverage_status":"registry-covered"})
        self.project.scanned_at=__import__("django.utils.timezone",fromlist=["now"]).now(); self.project.save(update_fields=["scanned_at"])
        return len(rows)
    def run(self):
        return {"files":self.scan_files(),"features":self.scan_features(),"apis":self.scan_apis()}
