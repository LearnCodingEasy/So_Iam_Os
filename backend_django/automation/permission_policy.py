DEFAULT_POLICY = {'read':'allowed','write':'allowed','execute':'ask','network':'ask','filesystem':'ask','shell':'denied','database':'ask'}
SENSITIVE_MAP = {'shell':'shell','command':'shell','powershell':'shell','filesystem':'filesystem','file':'filesystem','http':'network','request':'network','network':'network','database':'database','sql':'database'}

def effective_policy(workflow):
    return {**DEFAULT_POLICY, **(workflow.permissions or {})}

def required_permissions(workflow):
    required=set()
    for node in workflow.nodes.prefetch_related('actions'):
        for action in node.actions.all():
            key=str(action.action_type or '').lower()
            if key in SENSITIVE_MAP: required.add(SENSITIVE_MAP[key])
            else: required.add('execute')
    return required

def validate_permissions(workflow, approved=False):
    policy=effective_policy(workflow); required=required_permissions(workflow)
    denied=[x for x in required if policy.get(x)=='denied']
    asking=[x for x in required if policy.get(x)=='ask']
    if denied: return {'allowed':False,'status':'denied','denied':denied,'ask':asking}
    if asking and not approved: return {'allowed':False,'status':'approval_required','denied':[],'ask':asking}
    return {'allowed':True,'status':'allowed','denied':[],'ask':[]}
