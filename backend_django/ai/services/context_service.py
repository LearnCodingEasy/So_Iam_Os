from .core import AIContextBuilder

class ContextService:
    def __init__(self,user): self.user=user
    def build(self,max_items=20): return AIContextBuilder(self.user,max_items=max_items).build()
